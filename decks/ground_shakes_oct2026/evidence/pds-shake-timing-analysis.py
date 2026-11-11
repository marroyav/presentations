#!/usr/bin/env python3
"""Histogram recorded PDS pulse times without imposing the old -300:-100 us cut."""
from pathlib import Path
import csv
import datetime as dt
import hashlib
import json
import platform
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
ANALYSIS = HERE.parent
WORK = ANALYSIS.parents[1]
TOKENS = WORK / 'presentations/templates/dune-professional/design-tokens.json'


def sha(p):
    with Path(p).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def write(p, obj):
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False, allow_nan=False) + '\n')


def describe(values):
    a = np.asarray(values, float)
    if not len(a):
        return {'records': 0}
    q = np.quantile(a, [0, .05, .25, .5, .75, .95, 1])
    return {'records': len(a), 'quantiles_us': dict(zip(['min', 'p05', 'p25', 'median', 'p75', 'p95', 'max'], q.tolist())),
            'outside_old_minus300_to_minus100_window': int(np.sum((a < -300) | (a >= -100))),
            'standard_deviation_us': float(np.std(a))}


def main():
    sources = {}

    def source(p):
        sources[str(p)] = sha(p)
        return p

    def read(name):
        return json.loads(source(ANALYSIS / name).read_text())

    screen = read('all-runs/sharp-pds.json')
    metrics = read('electrical-pattern-20261023/sequence-event-metrics.json')
    coverage = read('all-runs/event-coverage.json')
    for name in ['all-runs/screen_sharp_pds.py', 'all-runs/screen_charge.py',
                 'electrical-pattern-20261023/sequence.py', 'all-runs/charge-screen.json']:
        source(ANALYSIS / name)
    source(Path(__file__).resolve()); source(TOKENS)
    metric = {(r['run'], r['event']): r for r in metrics}
    cover = {(r['run'], r['trigger_number']): r for r in coverage['events']}
    time = (np.arange(8192) - 4096 + .5) * .256
    edge_time = (time[1:] + time[:-1]) / 2
    rows = []
    groups = []
    for event in screen['events']:
        run, number = event['run'], event['trigger_number']
        for group in event['groups']:
            groups.append({'run': run, 'event': number, 'endpoint': group['endpoint_group'],
                           'times_us': group['pulse_candidate_times_us']})
        if run not in (32731, 32739):
            continue
        group = next((g for g in event['groups'] if g['endpoint_group'] == '109'), None)
        pulses = group['pulse_candidate_times_us'] if group else []
        old = [p for p in pulses if -300 <= p < -100]
        m = metric.get((run, number))
        marker = m['TPC']['1']['sustained_threshold_crossings_us']['2'] if m else None
        before = [p for p in pulses if marker is not None and p < marker]
        c = cover[(run, number)]
        starts = [ch['first_sample_us'] - event['onset_proxy_trigger_relative_us']
                  for packet in c['PDS'] if packet['endpoint_from_frame_header'] == 109
                  for ch in packet['channels']]
        row = {'run': run, 'event': number, 'file': event['file'],
               'precursor_marker_us': marker, 'old_window_first_us': min(old) if old else None,
               'before_marker_times_us': before, 'all_screen_times_us': pulses,
               'before_marker_first_us': min(before) if before else None,
               'before_marker_largest_edge_us': None, 'candidate_edge_scores': [],
               'first_recorded_PDS_sample_us': min(starts) if starts else None}
        if before:
            path = source(ANALYSIS / f'electrical-pattern-20261023/cache/r{run}_e{number}.npz')
            with np.load(path) as z:
                a = z['adc'].astype(float)
                # Recorded edge strength, not photon yield. Exclude reported disconnected inputs.
                connected = ~np.isin(z['channels'], [11, 13, 14, 16])
                d = np.diff(a[connected], axis=1)
                rail = z['rail'][connected]
                d[rail[:, :-1] | rail[:, 1:]] = np.nan
                scores = []
                for p in before:
                    part = d[:, np.abs(edge_time - p) <= 4.096]
                    per_channel = [max(0., -float(np.min(v[np.isfinite(v)])))
                                   for v in part if np.any(np.isfinite(v))]
                    score = float(np.median(per_channel)) if len(per_channel) >= 21 else None
                    scores.append({'time_us': p, 'median_peak_negative_edge_ADC_per_256ns': score,
                                   'channels_with_recorded_edge': len(per_channel)})
                row['candidate_edge_scores'] = scores
                eligible = [p for p in scores if p['median_peak_negative_edge_ADC_per_256ns'] is not None]
                # Tie rule: first in time. All candidate times already precede the marker.
                if eligible:
                    chosen = max(eligible, key=lambda p: (p['median_peak_negative_edge_ADC_per_256ns'], -p['time_us']))
                    row['before_marker_largest_edge_us'] = chosen['time_us']
        rows.append(row)

    summary = []
    fields = ['old_window_first_us', 'before_marker_first_us', 'before_marker_largest_edge_us']
    for run in (32731, 32739):
        rr = [r for r in rows if r['run'] == run]
        result = {'run': run, 'charge_selected_records': len(rr),
                  'records_with_precursor_marker': sum(r['precursor_marker_us'] is not None for r in rr),
                  'records_with_candidate_before_marker': sum(bool(r['before_marker_times_us']) for r in rr),
                  'records_missing_existing_sequence_metrics': sum((r['run'], r['event']) not in metric for r in rr)}
        for field in fields:
            result[field] = describe([r[field] for r in rr if r[field] is not None])
        result['first_recorded_sample_us'] = describe([r['first_recorded_PDS_sample_us'] for r in rr if r['first_recorded_PDS_sample_us'] is not None])
        summary.append(result)
    all_groups = []
    for run, ep in sorted({(g['run'], g['endpoint']) for g in groups}):
        gg = [g for g in groups if (g['run'], g['endpoint']) == (run, ep)]
        first = [min(g['times_us']) for g in gg if g['times_us']]
        all_groups.append({'run': run, 'endpoint': ep, 'records_with_this_group': len(gg),
                           'records_with_candidate': len(first), 'first_candidate': describe(first)})
    limits = [
        't = PDS time minus the main-shake onset proxy; negative means before the main shake. This is not a measured electron drift time.',
        'Main shake: start of strongest connected component with >=50% of sampled channels above 1000 ADC on both APAs, 2.048 us bins.',
        'Pulses: existing >=21-channel fast-negative-edge candidates, searched in [-4000,-20) us wherever samples exist. Not confirmed light flashes or sparks.',
        'Precursor: existing APA1 signed-median 2 ADC crossing, sustained five bins, with amplitude/noise eligibility and left-censor rejection. Diagnostic marker, not a physical charge arrival.',
        'Largest means greatest median peak negative edge among recorded connected-input samples within +/-4.096 us of each candidate; >=21 channels with a valid edge required. Cached ADC uses 256 ns bins. It is not calibrated photon yield or integrated pulse size.',
        'Reported disconnected DAPHNE109 channels 11,13,14,16 excluded only from amplitude ranking; original candidate membership unchanged.',
        'One pulse per record: largest recorded edge before the marker. First before marker shown as a sensitivity comparison. Missing scores are not set to zero.',
        'Individual PDS channels sometimes have samples earlier than -320 us. Those samples do not establish continuous >=21-channel coverage. Packet gaps, self-triggering and readout limits can hide earlier qualifying pulses. No live-time or efficiency correction.',
        'Requiring a pulse before the precursor truncates timing in a record-dependent way. The old -300 to -100 us cut is shown separately, not reused for the wider histogram.',
        'November is the supported precursor subset: 1378 charge candidates, 1376 with existing sequence metrics. Other run/endpoint first-candidate summaries use no precursor requirement and must not be pooled as the same population.',
        'No fixed-location exclusion, causal claim, Gaussian width fit or independent-sample significance is inferred from these histograms.'
    ]
    data = {'created_utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'question': 'Do large early PDS pulses occur at the same time relative to the ground shake?',
            'summary': summary, 'all_run_endpoint_first_candidates': all_groups, 'limits': limits}
    write(HERE / 'results.json', data)
    write(HERE / 'event-metrics.json', rows)
    with (HERE / 'event-times.csv').open('w') as stream:
        columns = ['run', 'event', 'precursor_marker_us', *fields, 'first_recorded_PDS_sample_us']
        writer = csv.DictWriter(stream, fieldnames=columns, extrasaction='ignore'); writer.writeheader(); writer.writerows(rows)

    colors = json.loads(TOKENS.read_text())['colors']
    blue, orange, ink, rule = [colors[n]['hex'] for n in ['editorial-muted', 'editorial-accent-deep', 'editorial-text', 'editorial-rule']]
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 14, 'axes.labelsize': 15,
                         'axes.titlesize': 17, 'text.color': ink, 'axes.labelcolor': ink,
                         'axes.spines.top': False, 'axes.spines.right': False, 'pdf.fonttype': 42})
    bins = np.arange(-340, 1, 20)
    for name, field, subtitle in [
        ('pds-to-shake-histogram', 'before_marker_largest_edge_us', 'Largest early PDS pulse in each event'),
        ('first-pds-to-shake-histogram', 'before_marker_first_us', 'First early PDS pulse in each event'),
        ('old-window-histogram', 'old_window_first_us', 'First candidate in the old selected window: -300 to -100 microseconds')]:
        fig, axes = plt.subplots(1, 2, figsize=(13, 3.8), sharex=True, sharey=True)
        for ax, run, color in zip(axes, (32731, 32739), (blue, orange)):
            vals = [r[field] for r in rows if r['run'] == run and r[field] is not None]
            ax.hist(vals, bins=bins, color=color, edgecolor='white', linewidth=.6)
            ax.axvline(0, color=ink, lw=1)
            ax.set_title(f'Run {run}: {len(vals)} events', loc='left')
            ax.set_xlim(-340, 8); ax.set_xticks([-300, -200, -100, 0]); ax.grid(axis='y', color=rule, alpha=.6); ax.set_axisbelow(True)
            ax.set_xlabel('PDS time - main-shake time (microseconds)')
            if field == 'old_window_first_us':
                for x in (-300, -100): ax.axvline(x, color=ink, ls='--', lw=1)
        axes[0].set_ylabel('Number of events')
        fig.suptitle(subtitle, fontsize=16, x=.065, ha='left')
        fig.tight_layout(pad=.9, rect=[0, 0, 1, .96])
        fig.savefig(HERE / f'{name}.pdf'); fig.savefig(HERE / f'{name}.png', dpi=170); plt.close(fig)

    # Validate selection, signs, histogram totals and consistency with the saved sequence subset.
    checked = 0
    for r in rows:
        p = r['before_marker_largest_edge_us']
        if p is not None:
            assert -4000 <= p < -20 and p < r['precursor_marker_us']
            assert p in r['all_screen_times_us']
        m = metric.get((r['run'], r['event']))
        if m:
            assert r['old_window_first_us'] == m['first_recorded_candidate_time_us']
            checked += 1
    for run in (32731, 32739):
        for field in fields:
            vals = [r[field] for r in rows if r['run'] == run and r[field] is not None]
            assert np.histogram(vals, bins=bins)[0].sum() == len(vals)
    evidence = {'created_utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'host': platform.node(),
                'command': 'python3 analysis/pds-shake-timing-20261028/analyze.py',
                'cwd': str(ANALYSIS.parent), 'python': sys.version, 'numpy': np.__version__, 'matplotlib': matplotlib.__version__,
                'git_state': 'Analysis store outside Git; exact scripts and inputs hashed.',
                'source_sha256': sources, 'output_sha256': {str(p): sha(p) for p in HERE.iterdir() if p.suffix in ('.json', '.csv', '.pdf', '.png') and not p.name.startswith('validation-')},
                'checks': {'all_old_first_times_match_existing_metrics': checked, 'histogram_counts_match_selected_records': True,
                           'selected_times_precede_precursor_and_shake': True}, 'reviewer': None, 'limits': limits}
    stamp = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    write(HERE / f'validation-{stamp}.json', evidence)
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Make plain-language figures from existing, pinned results. No detector refit."""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

HERE = Path(__file__).resolve().parent
WORK = HERE.parents[2]
ANALYSIS = WORK / 'ground-shake-data/analysis'
EDMS = WORK / 'ground-shake-recovery-20261015/edms'
EVIDENCE = HERE / 'evidence'
FIGURES = HERE / 'figures'
TOKENS = HERE.parents[1] / 'templates/dune-professional/design-tokens.json'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def write(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False, allow_nan=False) + '\n')


def freeze():
    sources = {}

    def source(path):
        sources[str(path)] = sha(path)
        return path

    def read(name):
        return json.loads(source(ANALYSIS / name).read_text())

    pair = read('double-pulse-display/results.json')
    metrics = read('electrical-pattern-20261023/sequence-event-metrics.json')
    sequence = read('electrical-pattern-20261023/sequence-results.json')
    tracks = read('charge-light-matching/track-onset-results.json')
    fits = read('electrical-pattern-20261023/results.json')
    for name in ['double-pulse-display/README.txt', 'double-pulse-display/make.py',
                 'electrical-pattern-20261023/sequence.py', 'charge-light-matching/track_onsets.py',
                 'charge-light-matching/README.txt', 'charge-light-matching/report-data.json',
                 'charge-light-matching/event-mixing-results.json', 'sc-correlation-20261027/report-data.json']:
        source(ANALYSIS / name)
    for name in ['ground_shake_200726.pdf', 'ground_shake_200726.txt', '3493627.json', '3493642.json',
                 'snapshots/20261028/3493642-evolving-material.pdf', 'snapshots/20261028/retrieval.json']:
        source(EDMS / name)

    arrays = {}
    pds_time = (np.arange(8192) - 4096 + .5) * .256
    keep_pds = (pds_time >= -280) & (pds_time <= 30)
    arrays['pds_time_us'] = pds_time[keep_pds]
    examples = []
    for event in [33, 52]:
        with np.load(source(ANALYSIS / f'electrical-pattern-20261023/cache/r32731_e{event}.npz')) as z:
            for channel in [12, 14, 15, 16, 47]:
                row = int(np.flatnonzero(z['channels'] == channel)[0])
                raw = z['adc'][row].copy()
                raw[z['rail'][row]] = np.nan
                arrays[f'e{event}_PDS_ch{channel}'] = raw[keep_pds]
        with np.load(source(ANALYSIS / f'charge-light-matching/cache/r32731_e{event}.npz')) as z:
            t = z['time_us']
            keep = (t >= -280) & (t <= 30)
            arrays[f'e{event}_tpc_time_us'] = t[keep]
            for apa in [1, 2]:
                baseline = np.median(z[f'APA{apa}_median'][(t >= -300) & (t < -260)])
                arrays[f'e{event}_TPC_APA{apa}'] = z[f'APA{apa}_median'][keep] - baseline
        r = next(r for r in metrics if r['run'] == 32731 and r['event'] == event)
        pp = next(r for r in pair['pairs'] if r['event'] == event)
        examples.append({'run': 32731, 'event': event, **pp,
                         'APA1_2ADC_crossing_us': r['TPC']['1']['sustained_threshold_crossings_us']['2']})

    clock = next(r for r in sequence['fixed_delay_clock_tests'] if r['split'] == 'other_run'
                 and r['TPC_APA'] == 1 and r['threshold_ADC'] == 2 and r['PDS_pulse'] == 'first')
    arrays['clock_errors_us'] = np.array([clock['fixed_PDS_delay_MAE_us'], clock['shake_clock_only_MAE_us']])
    test = [r for r in metrics if r['split'] == 'other_run'
            and r['first_recorded_candidate_time_us'] is not None
            and r['TPC']['1']['sustained_threshold_crossings_us']['2'] is not None]
    assert len(test) == clock['events'] == 225
    train = [r for r in metrics if r['split'] == 'train'
             and r['first_recorded_candidate_time_us'] is not None
             and r['TPC']['1']['sustained_threshold_crossings_us']['2'] is not None]
    delay = np.median([r['TPC']['1']['sustained_threshold_crossings_us']['2']
                      - r['first_recorded_candidate_time_us'] for r in train])
    phase = np.median([r['TPC']['1']['sustained_threshold_crossings_us']['2'] for r in train])
    y = np.array([r['TPC']['1']['sustained_threshold_crossings_us']['2'] for r in test])
    x = np.array([r['first_recorded_candidate_time_us'] for r in test])
    np.testing.assert_allclose(arrays['clock_errors_us'], [np.mean(np.abs(y - (x + delay))), np.mean(np.abs(y - phase))])
    timing_examples = []
    for run, event in [(32731, 33), (32731, 52), (32739, 5)]:
        r = next(r for r in metrics if (r['run'], r['event']) == (run, event))
        timing_examples.append({'run': run, 'event': event, 'first_PDS_us': r['first_recorded_candidate_time_us'],
                                'charge_marker_us': r['TPC']['1']['sustained_threshold_crossings_us']['2']})

    with np.load(source(ANALYSIS / 'charge-light-matching/cache/r32731_e33.npz')) as z:
        t = z['time_us']; ids = np.flatnonzero(z['APA2_planes'] == 2)
        ids = ids[np.argsort(z['APA2_offline_channels'][ids])]
        wires = np.arange(480, 680); columns = ids[wires]
        keep = (t >= -340) & (t <= 30)
        data = z['APA2_residual'][:, columns].copy()
        valid = z['APA2_drift_search_usable'][:, None] & ~z['APA2_rails'][:, columns]
        data[~valid] = np.nan
        arrays['track_time_us'] = t[keep]; arrays['track_wire_index'] = wires
        arrays['track_ADC'] = data[keep].T
    segment = next(r for r in tracks['segments'] if r['run'] == 32731 and r['event'] == 33 and r['APA'] == 2)['segments'][0]
    comparisons = [r for r in tracks['PDS_segment_comparisons'] if r['run'] == 32731
                   and r['event'] == 33 and r['APA'] == 2 and r['segment'] == 1]
    assert len(comparisons) == 2 and all(r['charge_already_arriving_before_PDS'] for r in comparisons)
    early = next(r for r in fits['summary'] if r['split'] == 'other_run' and r['trained_region'] == 'early'
                 and r['tested_region'] == 'early' and r['model'] == 'FIR3')
    arrays['electrical_relative_error'] = np.sqrt(1 - np.array([early['paired_actual_skill'], early['paired_shuffled_skill']]))
    assert len(pair['events']) == 101 and len(pair['pairs']) == 125
    assert sum(len(r['times_us']) == 2 for r in pair['events']) == 80
    for row in pair['pairs']:
        np.testing.assert_allclose(row['separation_us'], row['second_us'] - row['first_us'])
    stats = {'prepared_UTC': dt.datetime.now(dt.timezone.utc).isoformat(),
             'pair_scope': {k: v for k, v in pair.items() if k not in ['events', 'pairs']},
             'double_pulse_examples': examples, 'timing_examples': timing_examples,
             'clock_test': clock, 'clock_arithmetic_independently_recomputed': True,
             'track_segment': segment, 'track_comparisons': comparisons,
             'electrical_paired_scores': [early['paired_actual_skill'], early['paired_shuffled_skill']],
             'electrical_median_event_score': early.get('median_event_skill'),
             'limits': ['Existing exploratory tests, not a newly established cause.',
                        'First pulse means first retained candidate in the selected window, not necessarily the first physical pulse.',
                        'Missing PDS samples and ADC rail bins remain gaps. Raw ADC is not calibrated light.',
                        'A threshold crossing is a timing marker, not a physical start time.',
                        'Charge segments are 2D raw-signal features, not fitted 3D tracks.']}
    np.savez_compressed(EVIDENCE / 'public-plot-data.npz', **arrays)
    write(EVIDENCE / 'public-review-data.json', stats)
    write(EVIDENCE / 'public-source-manifest.json', {'source_sha256': sources,
          'frozen_sha256': {n: sha(EVIDENCE / n) for n in ['public-plot-data.npz', 'public-review-data.json']},
          'scope': 'Presentation of existing tests; separate known EDMS observations from added quantitative checks.'})


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--refresh', action='store_true'); args = parser.parse_args()
    if args.refresh:
        freeze()
    manifest = json.loads((EVIDENCE / 'public-source-manifest.json').read_text())
    for name, h in manifest['frozen_sha256'].items():
        assert sha(EVIDENCE / name) == h, name
    z = np.load(EVIDENCE / 'public-plot-data.npz')
    stats = json.loads((EVIDENCE / 'public-review-data.json').read_text())
    colors = json.loads(TOKENS.read_text())['colors']; c = lambda name: colors[name]['hex']
    blue, orange, ink, gray = c('editorial-muted'), c('editorial-accent-deep'), c('editorial-text'), c('border')
    rule, white = c('editorial-rule'), c('editorial-canvas')
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 17, 'axes.labelsize': 17,
                        'axes.titlesize': 19, 'xtick.labelsize': 16, 'ytick.labelsize': 15,
                        'text.color': ink, 'axes.labelcolor': ink, 'axes.edgecolor': gray,
                        'axes.spines.top': False, 'axes.spines.right': False, 'pdf.fonttype': 42,
                        'figure.facecolor': white, 'axes.facecolor': white, 'lines.linewidth': 1.6})
    outputs = {}

    def save(fig, name):
        for ext in ['pdf', 'png']:
            path = FIGURES / f'{name}.{ext}'; fig.savefig(path, dpi=180)
            outputs[str(path.relative_to(HERE))] = sha(path)
        plt.close(fig)

    # A measured example: show the sharp pulses, the magnified slow change and
    # the much larger main shake separately, without mixing vertical scales.
    fig, axs = plt.subplots(3, 1, figsize=(13, 4.2), sharex=True, layout='constrained',
                            gridspec_kw={'height_ratios': [1, 1, 1]})
    t = z['pds_time_us']; use = t < -20
    axs[0].plot(t[use], z['e33_PDS_ch47'][use], color=blue)
    axs[0].set(ylim=(7500, 8800), yticks=[7800, 8400])
    axs[0].set_ylabel('Light readout\n(raw units)', rotation=0, ha='right', va='center')
    for p, label in [(-183.296, 'Pulse 1'), (-160.768, 'Pulse 2')]:
        axs[0].axvline(p, color=orange, ls=':', lw=1.2)
        axs[0].annotate(label, (p, 8350), xytext=(p + (-30 if label.endswith('1') else 18), 8650),
                        ha='center', fontsize=15, arrowprops={'arrowstyle': '-', 'color': ink})
    t = z['e33_tpc_time_us']; use = t < -20
    for apa, color, style in [(1, blue, '-'), (2, orange, '--')]:
        axs[1].plot(t[use], z[f'e33_TPC_APA{apa}'][use], color=color, ls=style, label=f'APA{apa}')
    axs[1].set(ylim=(-15, 15), yticks=[-10, 0, 10])
    axs[1].set_ylabel('Slow charge\nchange (units)', rotation=0, ha='right', va='center')
    axs[1].text(-100, 9, 'Slow precursor', fontsize=16, ha='center')
    axs[1].legend(loc='upper left', ncol=2, frameon=False, fontsize=12)
    axs[2].plot(t, z['e33_TPC_APA1'], color=blue)
    axs[2].set(ylim=(-9000, 10500), yticks=[-8000, 0, 8000],
               xlabel='Time from the main shake (microseconds)', xlim=(-280, 30))
    axs[2].set_ylabel('Full charge\nchange (units)', rotation=0, ha='right', va='center')
    axs[2].text(-58, 6500, 'Main shake at 0', ha='center', fontsize=16)
    for ax in axs:
        ax.axvline(0, color=ink, lw=1.2); ax.grid(axis='x', color=rule, lw=.6)
        ax.set_xticks([-250, -200, -150, -100, -50, 0])
    for ax in axs[:2]:
        ax.axvspan(-20, 30, color=rule, alpha=.7)
        ax.text(5, .5, 'Shown\nbelow', transform=ax.get_xaxis_transform(), ha='center', va='center', fontsize=12)
    save(fig, '10-event-sequence')

    fig, axs = plt.subplots(1, 2, figsize=(13, 3.6), layout='constrained')
    for ax, row in zip(axs, stats['double_pulse_examples']):
        event = row['event']; t = z['pds_time_us']; use = (t > row['first_us'] - 14) & (t < row['second_us'] + 13)
        ax.plot(t[use], z[f'e{event}_PDS_ch47'][use], color=blue)
        ax.set(xlabel='Time from main shake (microseconds)', ylabel='Light-readout units',
               ylim=(7500, 8800), title=f"Event {event}: {row['separation_us']:.0f} microseconds apart")
        for n, pulse in enumerate([row['first_us'], row['second_us']], 1):
            ax.axvline(pulse, color=orange, ls=':', lw=1)
            ax.text(pulse, 8670, str(n), ha='center', fontsize=20)
        ax.annotate('', (row['first_us'], 8550), (row['second_us'], 8550),
                    arrowprops={'arrowstyle': '<->', 'color': ink})
        ax.grid(axis='y', color=rule, lw=.7)
    save(fig, '11-double-pulses')

    fig, axs = plt.subplots(1, 2, figsize=(13, 3.6), layout='constrained', gridspec_kw={'width_ratios': [1.1, 1]})
    for y, row in zip([2, 1, 0], stats['timing_examples']):
        p, q = row['first_PDS_us'], row['charge_marker_us']
        axs[0].plot([p, q], [y, y], color=gray, lw=2)
        axs[0].scatter(p, y, color=orange, marker='v', s=95, zorder=3)
        axs[0].scatter(q, y, color=blue, marker='o', s=70, zorder=3)
    axs[0].set(yticks=[2, 1, 0], yticklabels=['32731 / 33', '32731 / 52', '32739 / 5'], ylim=(-.55, 2.8),
               xlabel='Time from main shake (microseconds)', ylabel='Run / event', title='The order can differ')
    axs[0].scatter([], [], color=orange, marker='v', s=65, label='First selected PDS pulse')
    axs[0].scatter([], [], color=blue, marker='o', s=55, label='Slow-charge marker')
    axs[0].legend(loc='upper left', frameon=False, fontsize=12); axs[0].grid(axis='x', color=rule, lw=.7)
    bars = axs[1].bar([0, 1], z['clock_errors_us'], .55, color=[orange, blue])
    axs[1].bar_label(bars, fmt='%.0f', fontsize=22, padding=4)
    axs[1].set(xticks=[0, 1], xticklabels=['Use first\nPDS pulse', 'Use known\nmain shake'],
               ylabel='Average timing error\n(microseconds)', ylim=(0, 88), title='225 unused records: lower is better')
    save(fig, '12-first-pulse-clock')

    fig, ax = plt.subplots(figsize=(13, 3.7), layout='constrained')
    cmap = LinearSegmentedColormap.from_list('signed', [blue, white, orange]); cmap.set_bad(rule)
    t, w = z['track_time_us'], z['track_wire_index']
    im = ax.imshow(z['track_ADC'], origin='lower', aspect='auto', interpolation='nearest',
                   extent=[t[0]-1.024, t[-1]+1.024, w[0]-.5, w[-1]+.5], cmap=cmap, vmin=-100, vmax=100, rasterized=True)
    for p, name in [(-183.296, 'Pulse 1'), (-160.768, 'Pulse 2')]:
        ax.axvline(p, color=ink, ls='--', lw=1)
        ax.text(p + (-7 if name.endswith('1') else 7), 687, name, fontsize=17,
                ha='right' if name.endswith('1') else 'left')
    ax.annotate('Charge feature already present', xy=(-310, 509), xytext=(-319, 660),
                ha='left', fontsize=17, arrowprops={'arrowstyle': '->', 'color': ink})
    ax.axvline(0, color=ink, lw=1.4); ax.text(0, 687, 'Main shake', ha='center', fontsize=17)
    ax.set(xlim=(-334, 25), ylim=(480, 710), xlabel='Time from main shake (microseconds)',
           ylabel='Charge-wire index', yticks=[500, 550, 600, 650])
    fig.colorbar(im, ax=ax, pad=.015, fraction=.025, label='Charge change (readout units)', ticks=[-100, 0, 100])
    save(fig, '13-charge-before-pulses')

    fig, ax = plt.subplots(figsize=(13, 3.4), layout='constrained')
    bars = ax.barh([1, 0], 100*z['electrical_relative_error'], .5, color=[blue, orange])
    ax.bar_label(bars, labels=[f'{v*100:.1f}%' for v in z['electrical_relative_error']], fontsize=22, padding=7)
    ax.axvline(100, color=gray, ls=':', lw=1.2)
    ax.set(yticks=[1, 0], yticklabels=['Use inputs from\nthe same event', 'Use inputs from\nother events'], xlim=(0, 118), ylim=(-.5, 1.65),
           xlabel='Prediction error relative to a zero-change estimate (%)', title='Model built on run 32731; tested on run 32739')
    ax.text(100, 1.42, '100% = predict no signal change', ha='right', color=ink, fontsize=14)
    save(fig, '14-electrical-test')
    write(EVIDENCE / 'public-figure-manifest.json', {'script_sha256': sha(Path(__file__)), 'figure_sha256': outputs,
          'frozen_sha256': manifest['frozen_sha256'], 'method': 'Existing recorded samples; no interpolation, refit or new physics classification.'})
    print('Made five figures for the public review; existing timing arithmetic checked.')


if __name__ == '__main__':
    main()

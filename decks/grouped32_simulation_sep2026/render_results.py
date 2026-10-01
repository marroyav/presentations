#!/usr/bin/env python3
"""Generate the deck's vector figure and tables from a verified XC report.

Use --report and --replay-dir to import a fresh run, or no arguments to rebuild
from the compact evidence copied into this deck. Raw packet traces stay in XC.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent
LABELS = ['Simultaneous', 'Short stalls', 'Long stall', 'Dense overlap', 'Control/reset']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    parser.add_argument('--replay-dir', type=Path)
    args = parser.parse_args()
    if bool(args.report) != bool(args.replay_dir):
        parser.error('Supply both --report and --replay-dir, or neither')
    evidence = ROOT / 'evidence'
    evidence.mkdir(exist_ok=True)
    if args.report:
        report = json.loads(args.report.read_text())
        if report['status'] != 'PASS':
            raise ValueError('Report did not pass')
        summaries = []
        for case in report['cases']:
            candidates = json.loads((args.replay_dir / f"summary-phase{case['phase_ps']}.json").read_text())
            summary = next(row for row in candidates if row['mode'] == case['mode'])
            trace = args.replay_dir / f"mode{case['mode']}-phase{case['phase_ps']}.csv"
            digest = hashlib.sha256(trace.read_bytes()).hexdigest()
            if not digest == summary['csv_sha256'] == case['trace_sha256']:
                raise ValueError(f'Trace checksum mismatch: {trace}')
            summaries.append(dict(summary, phase_ps=case['phase_ps']))
        (evidence / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
        (evidence / 'packet-summaries.json').write_text(json.dumps(summaries, indent=2) + '\n')
    report = json.loads((evidence / 'report.json').read_text())
    summaries = json.loads((evidence / 'packet-summaries.json').read_text())
    cases = sorted(report['cases'], key=lambda row: row['mode'])
    if report['status'] != 'PASS' or [row['mode'] for row in cases] != list(range(5)):
        raise ValueError('This deck requires exactly the five standard verified modes')
    for case in cases:
        summary = next(s for s in summaries if s['mode'] == case['mode'] and s['phase_ps'] == case['phase_ps'])
        for key, field in [('grouped', 'grouped_packets'), ('native_reference', 'reference_packets')]:
            if summary[field] != case[key]['packets']:
                raise ValueError('Packet count differs between oracle and coverage analysis')

    with (ROOT / 'results.csv').open('w') as stream:
        writer = csv.writer(stream)
        writer.writerow(['mode', 'scenario', 'implementation', 'packets', 'active_sample_loss_percent', 'charge_loss_percent', 'comparison_qualified'])
        for row in cases:
            for implementation in ['grouped', 'native_reference']:
                metrics = row[implementation]
                writer.writerow([row['mode'], row['scenario'], implementation, metrics['packets'],
                                 100 * metrics['active_sample_loss_fraction'], 100 * metrics['charge_loss_fraction'],
                                 row.get('comparison_qualified', row['mode'] != 4)])

    from palette import colors
    color = colors()
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 15,
                         'text.color': color['text'], 'axes.labelcolor': color['text'],
                         'xtick.color': color['text'], 'ytick.color': color['text'],
                         'axes.edgecolor': color['border'], 'pdf.fonttype': 42})
    fig, axis = plt.subplots(figsize=(12.0, 4.6), facecolor=color['background'])
    selected = cases[:4]
    y = np.arange(len(selected))
    for ax, field, title in [(axis, 'active_sample_loss_fraction', 'Active sample loss [%]')]:
        ax.set_facecolor(color['background'])
        for implementation, offset, role, marker, label in [
                ('native_reference', -0.12, 'paper', 's', 'Native reference'),
                ('grouped', 0.12, 'sky', 'o', 'Grouped')]:
            values = [100 * row[implementation][field] for row in selected]
            ax.scatter(values, y + offset, color=color[role], marker=marker, s=75, label=label, zorder=3)
            for value, ypos in zip(values, y + offset):
                ax.annotate(f'{value:.2f}', (value, ypos), xytext=(8, 0), textcoords='offset points',
                            va='center', fontsize=12, color=color[role])
        ax.set_yticks(y, LABELS[:4])
        ax.invert_yaxis()
        ax.set_xlim(-1.5, max(12, max(100 * row[impl][field] for row in selected
                                    for impl in ['grouped', 'native_reference']) + 9))
        ax.set_xlabel(title)
        ax.grid(axis='x', color=color['border'], alpha=0.5)
        ax.spines[['top', 'right']].set_visible(False)
    axis.legend(loc='lower right', facecolor=color['background'], edgecolor=color['border'], fontsize=14)
    fig.tight_layout(pad=1.3, w_pad=2.2)
    (ROOT / 'figures').mkdir(exist_ok=True)
    fig.savefig(ROOT / 'figures/retention.pdf', facecolor=fig.get_facecolor())
    fig.savefig(ROOT / 'figures/retention.png', dpi=140, facecolor=fig.get_facecolor())
    plt.close(fig)

    table = []
    for case in cases:
        summary = next(s for s in summaries if s['mode'] == case['mode'] and s['phase_ps'] == case['phase_ps'])
        latency = summary['max_grouped_packet_latency_adc_ticks'] / 62.5
        table.append(f"    {case['mode']} & {case['grouped']['packets']:,} & {case['native_reference']['packets']:,} & "
                     f"{summary['byte_identical_common_packets']:,} & {latency:.3f} " + r'\\')
    common = sum(s['byte_identical_common_packets'] for s in summaries)
    samples = sum(s['samples_checked'] for s in summaries)
    source = report['firmware_commit'][:8]
    tex = r'''% Generated by render_results.py; edit the generator, not this file.
\begin{frame}{Every common packet matches}
  \framesubtitle{Fresh five-mode RTL replay; firmware SOURCE}
  \small
  \renewcommand{\arraystretch}{1.3}
  \begin{tabular}{@{}lrrrr@{}}
    \toprule
    Mode & Grouped packets & Native packets & Common / identical & Max latency [$\mu$s] \\
    \midrule
TABLE
    \bottomrule
  \end{tabular}\par
  \medskip
  COMMON common packets are byte-identical; SAMPLES ADC samples checked across both implementations.\par\medskip
  Mode 4 includes deliberate reset and disable losses. Latency runs from the first sample to the final output word.
\end{frame}
SPLIT
\begin{frame}{Saving samples is not the same as finding pulses}
  \centering
  \renewcommand{\arraystretch}{1.6}
  \begin{tabular}{@{}lll@{}}
    \toprule
    Readout & Sample retention & Pulse finding \\
    \midrule
    Self-trigger 1024 & Limited by busy windows & FPGA descriptors \\
    Self-trigger 512 + ring & Buffers reduce losses & FPGA descriptors \\
    Full stream & Every sample$^{*}$ & DAQ must find the peaks \\
    \bottomrule
  \end{tabular}\par\medskip
  Full stream is the sample reference.\par\smallskip
  Self-trigger moves pulse finding into the FPGA.\par\medskip
  \DuneDiagramCaption{$^{*}$Assuming lossless transport and storage. Saving all samples does not guarantee finding every pulse online.}
\end{frame}
'''
    tex = tex.replace('SOURCE', source).replace('TABLE', '\n'.join(table)).replace('COMMON', f'{common:,}').replace('SAMPLES', f'{samples:,}')
    packet_tex, result_tex = tex.split('SPLIT')
    (ROOT / 'packet-evidence.tex').write_text(packet_tex)
    (ROOT / 'results-slides.tex').write_text(result_tex)
    print(f'Generated results from {source}: {common:,} common records, {samples:,} samples checked')


if __name__ == '__main__':
    main()

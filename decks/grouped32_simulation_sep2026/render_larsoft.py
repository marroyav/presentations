#!/usr/bin/env python3
"""Plot the existing September 9 LArSoft snapshot and a normalized traffic estimate.

No detector jobs run here. HD and VD traffic are both calculated for an
illustrative homogeneous 32-channel board, never copied from the older 40-channel
HD board traffic column. Full-stream comparisons are arithmetic payload estimates.
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--snapshot', type=Path, help='Existing activity deck with results.csv and gamma_pilot_results.csv')
    parser.add_argument('--summary', type=Path, help='Original combined_deadtime_summary.json to cross-check the displayed rates')
    args = parser.parse_args()
    evidence = ROOT / 'evidence'
    evidence.mkdir(exist_ok=True)
    if args.snapshot:
        hashes = {}
        for name in ['results.csv', 'gamma_pilot_results.csv', 'README.md']:
            source = args.snapshot / name
            payload = source.read_bytes()
            (evidence / ('larsoft-' + name)).write_bytes(payload)
            hashes[name] = {'source': str(source.resolve()), 'sha256': hashlib.sha256(payload).hexdigest()}
        (evidence / 'larsoft-provenance.json').write_text(json.dumps({
            'snapshot_date': '2026-09-09', 'reused_not_rerun': True, 'sources': hashes,
            'traffic_board_channels': 32, 'sampling_hz': 62_500_000,
            'adc_bits': 14, 'record_bytes': 960,
            'fullstream_channels_per_logical_stream': 4, 'fullstream_streams_per_link': 2,
            'fullstream_links_per_board': 4, 'fullstream_blocks_per_record': 35,
            'fullstream_header_words': 5, 'fullstream_payload_words': 245,
            'limits': 'Homogeneous population means; no physical board map. Candidate traffic assumes one record per candidate before loss, continuation or merging. Full stream includes source-defined record headers, excludes network overhead. Gamma extension is a pilot, not a complete background prediction.'
        }, indent=2) + '\n')
    with (evidence / 'larsoft-results.csv').open() as stream:
        intrinsic = list(csv.DictReader(stream))
    with (evidence / 'larsoft-gamma_pilot_results.csv').open() as stream:
        gamma = {row['population']: row for row in csv.DictReader(stream)}
    if args.summary:
        payload = args.summary.read_bytes()
        summary_manifest = json.loads((args.summary.parent / 'manifest.json').read_text())
        entry = next(item for item in summary_manifest['outputs'] if item['path'] == args.summary.name)
        if hashlib.sha256(payload).hexdigest() != entry['sha256']:
            raise ValueError('Original LArSoft summary does not match its manifest')
        (evidence / 'larsoft-original-summary.json').write_bytes(payload)
        (evidence / 'larsoft-original-manifest.json').write_text(json.dumps(summary_manifest, indent=2) + '\n')
    original = evidence / 'larsoft-original-summary.json'
    if original.exists():
        original_rows = json.loads(original.read_text())['classes']
        mapping = {'HD_APA_integrated': ('FD-HD', 'apa-integrated'),
                   'VD_cathode': ('FD-VD', 'cathode'),
                   'VD_long_wall': ('FD-VD', 'long-wall'),
                   'VD_short_wall': ('FD-VD', 'short-wall')}
        for row in intrinsic:
            detector, module_class = mapping[row['population']]
            checked = next(item for item in original_rows if item['detector'] == detector
                           and item['module_class'] == module_class and item['frame_samples'] == 512)
            for frozen, exact in [(float(row['candidate_mean_khz_per_channel']), checked['intrinsic_candidate_rate_hz_per_channel'] / 1000),
                                  (float(gamma[row['population']]['combined_candidate_khz_per_channel']), checked['candidate_rate_hz_per_channel'] / 1000)]:
                if abs(frozen - exact) > 0.000501:
                    raise ValueError('Frozen LArSoft rate differs from the original result')
    base = np.array([float(row['candidate_mean_khz_per_channel']) for row in intrinsic])
    combined = np.array([float(gamma[row['population']]['combined_candidate_khz_per_channel']) for row in intrinsic])
    labels = ['HD', 'VD cathode', 'VD long wall', 'VD short wall']
    from palette import colors
    color = colors()
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 18, 'pdf.fonttype': 42,
                         'text.color': color['text'], 'axes.labelcolor': color['text'],
                         'xtick.color': color['text'], 'ytick.color': color['text'],
                         'axes.edgecolor': color['border']})
    (ROOT / 'figures').mkdir(exist_ok=True)

    def canvas():
        fig, ax = plt.subplots(figsize=(12.4, 4.8), facecolor=color['background'])
        ax.set_facecolor(color['background'])
        ax.spines[['top', 'right']].set_visible(False)
        ax.grid(axis='x', color=color['border'], alpha=0.45, zorder=0)
        ax.set_yticks(np.arange(4), labels)
        ax.invert_yaxis()
        return fig, ax

    fig, ax = canvas()
    for values, offset, role, name in [(base, -0.18, 'paper', 'Intrinsic LAr'),
                                      (combined, 0.18, 'sky', '+ gamma pilot')]:
        bars = ax.barh(np.arange(4) + offset, values, height=0.32, color=color[role], label=name, zorder=3)
        ax.bar_label(bars, fmt='%.1f', padding=5, fontsize=16)
    ax.set_xlim(0, 117)
    ax.set_xlabel('Candidate rate [kHz/channel]')
    ax.legend(loc='lower right', facecolor=color['background'], edgecolor=color['border'], fontsize=15)
    fig.tight_layout(pad=1.1)
    fig.savefig(ROOT / 'figures/larsoft-rates.pdf', facecolor=fig.get_facecolor())
    plt.close(fig)

    # 32 channels * kHz/ch * 1000 * 960 bytes/record * 8 bits/byte / 1e9.
    traffic_base = base * 32 * 1000 * 960 * 8 / 1e9
    traffic_combined = combined * 32 * 1000 * 960 * 8 / 1e9
    fig, ax = canvas()
    for values, offset, role, name in [(traffic_base, -0.18, 'paper', 'Intrinsic LAr'),
                                      (traffic_combined, 0.18, 'sky', '+ gamma pilot')]:
        bars = ax.barh(np.arange(4) + offset, values, height=0.32, color=color[role], label=name, zorder=3)
        ax.bar_label(bars, fmt='%.1f', padding=5, fontsize=16)
    fullstream_records = 28 * (245 + 5) / 245
    ax.axvline(fullstream_records, color=color['coral'], linestyle='--', linewidth=2)
    ax.text(fullstream_records, -0.6, 'Full stream\n28.57 Gbit/s', ha='center', va='bottom', fontsize=16, color=color['coral'])
    ax.set_ylim(3.6, -1.15)
    ax.set_xlim(0, 34)
    ax.set_xlabel('Offered record traffic [Gbit/s per 32-channel board]')
    ax.legend(loc='lower right', facecolor=color['background'], edgecolor=color['border'], fontsize=14)
    fig.tight_layout(pad=1.1)
    fig.savefig(ROOT / 'figures/traffic.pdf', facecolor=fig.get_facecolor())
    plt.close(fig)

    with (ROOT / 'traffic.csv').open('w') as stream:
        writer = csv.writer(stream)
        writer.writerow(['population', 'board_channels', 'intrinsic_record_demand_gbps', 'gamma_pilot_record_demand_gbps', 'fullstream_14bit_raw_gbps', 'fullstream_records_gbps'])
        for index, row in enumerate(intrinsic):
            writer.writerow([row['population'], 32, traffic_base[index], traffic_combined[index], 28, fullstream_records])
    print('Rendered LArSoft snapshot and full-stream payload comparison for 32 channels')


if __name__ == '__main__':
    main()

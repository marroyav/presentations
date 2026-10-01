#!/usr/bin/env python3
"""Clean illustrative waveform with grouped RTL descriptor calculations."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from palette import colors

ROOT = Path(__file__).resolve().parent
C = colors()
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 17,
    'pdf.fonttype': 42, 'text.color': C['text'], 'axes.labelcolor': C['text'],
    'xtick.color': C['text'], 'ytick.color': C['text'], 'axes.edgecolor': C['border']})
x = np.arange(512)
def pulse(start, rise, decay):
    t = np.maximum(x - start, 0)
    shape = (1 - np.exp(-t / rise)) * np.exp(-t / decay)
    return shape / shape.max()

# Positive polarity; no noise or measured detector-data claim.
baseline, threshold = 4000, 100
adc = baseline + np.rint(1000 * pulse(63, 4, 70) + 300 * pulse(280, 3, 32)).astype(int)
a = np.maximum(adc - baseline, 0)
runs, start = [], None
for n, value in enumerate(np.append(a, 0)):
    if value > threshold and start is None:
        start = n
    elif value <= threshold and start is not None:
        samples = a[start:n]
        runs.append(dict(start=start, end=n, integral=int(samples.sum()),
                         peak=int(samples.max()), offset=int(samples.argmax()),
                         duration=min(n - start, 511)))
        start = None
assert len(runs) == 2 and runs[0]['start'] == 64
fig, ax = plt.subplots(figsize=(14.4, 6.1), facecolor=C['background'])
ax.set_facecolor(C['background'])
ax.plot(x, a, color=C['editorial-accent'], lw=2.6)
ax.axhline(threshold, color=C['paper'], lw=1.1, ls='--')
ax.text(500, 125, 'Threshold = 100 ADC', ha='right', fontsize=15, color=C['paper'])
ax.axvspan(0, 64, color=C['paper'], alpha=0.08)
arrow = {'arrowstyle': '->', 'color': C['text-muted'], 'lw': 1.2}
for i, run in enumerate(runs):
    s, e, p = run['start'], run['end'], run['start'] + run['offset']
    role = 'editorial-accent' if i == 0 else 'sky'
    ax.fill_between(x[s:e], 0, a[s:e], color=C[role], alpha=0.25)
    ax.scatter([s, p], [a[s], a[p]], color=C[role], s=45, zorder=5)
    ax.vlines([s, e], -80, [a[s], threshold], color=C[role], ls=':', lw=1.2)
    text_x = 120 if i == 0 else 330
    text_y = 990
    ax.annotate(f'Peak {i+1}: max(a) = {run["peak"]} ADC', (p, a[p]),
                xytext=(text_x, text_y), arrowprops=arrow, fontsize=17, color=C[role])
    ax.annotate(f'Area = Σa[n] = {run["integral"]:,}\nADC·samples',
                (s + (e-s)*0.42, float(a[int(s+(e-s)*0.42)])*0.45),
                xytext=(text_x, text_y-210), arrowprops=arrow, fontsize=17, color=C[role])
    ax.annotate('', (s, -85), (e, -85),
                arrowprops={'arrowstyle': '|-|', 'color': C[role], 'lw': 1.4})
    ax.text((s+e)/2 if i == 0 else 360, -115, f'Duration = {e} − {s}\n= {run["duration"]} samples',
            ha='center', va='top', fontsize=14, color=C[role])
    ax.text(text_x, text_y-480,
            f'Start = {s}\nTo maximum = {p} − {s}\n= {run["offset"]} samples',
            fontsize=15, color=C[role])
ax.annotate('', (0, -330), (64, -330),
            arrowprops={'arrowstyle': '|-|', 'color': C['paper'], 'lw': 1.3})
ax.text(75, -340, '64 pretrigger samples before the rising edge = 1.024 µs',
        fontsize=16, va='center', color=C['paper'])
ax.text(4, 1170, 'a[n] = max(ADC[n] − baseline, 0)     Baseline = 4000 ADC', fontsize=17)
ax.set(xlim=(-5, 512), ylim=(-420, 1260), xlabel='Sample in the frame (16 ns/sample)',
       ylabel='Amplitude above baseline [ADC counts]')
ax.set_xticks([0, 64, 128, 256, 384, 512])
ax.set_yticks([0, 500, 1000])
ax.spines[['top', 'right']].set_visible(False)
fig.tight_layout(pad=1)
for ext in ('pdf', 'png'):
    fig.savefig(ROOT / f'figures/descriptor-time.{ext}', dpi=160, facecolor=fig.get_facecolor())
plt.close(fig)
(ROOT / 'evidence/descriptor-example.json').write_text(json.dumps({
    'illustration': True, 'baseline_adc': baseline, 'threshold_adc': threshold,
    'sample_ns': 16, 'positive_polarity': True, 'descriptors': runs}, indent=2) + '\n')
print(runs)

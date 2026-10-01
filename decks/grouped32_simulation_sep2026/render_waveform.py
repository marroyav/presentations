#!/usr/bin/env python3
"""Draw an illustrative pulse/afterpulse split across contiguous 512-sample records.

The pulse shapes and amplitudes are explanatory, not a detector measurement or
an RTL replay. Sample indices and the requested 64-sample pretrigger are exact.
"""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent
from palette import colors
C = colors()
x = np.arange(1024)
# Pretrigger precedes the rising edge, not the later peak maximum.
t = np.maximum(x - 64, 0)
pulse = (1 - np.exp(-t / 4)) * np.exp(-t / 60)
pulse /= pulse.max()
peak = int(np.argmax(pulse))
assert peak == 75
afterpulse = 0.40 * np.where(x < 490, np.exp(-0.5 * ((x - 490) / 15.0) ** 2), np.exp(-(x - 490) / 105.0))
y = pulse + afterpulse
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 17, 'pdf.fonttype': 42,
                     'text.color': C['text'], 'axes.labelcolor': C['text'],
                     'xtick.color': C['text'], 'ytick.color': C['text'], 'axes.edgecolor': C['border']})
fig, ax = plt.subplots(figsize=(14.4, 3.6), facecolor=C['background'])
ax.set_facecolor(C['background'])
ax.axvspan(0, 64, color=C['paper'], alpha=0.13)
ax.axvspan(512, 1024, color=C['sky'], alpha=0.06)
ax.plot(x[:513], y[:513], color=C['editorial-accent'], lw=2.8)
ax.plot(x[512:], y[512:], color=C['sky'], lw=2.8)
ax.axvline(512, color=C['text-muted'], linestyle='--', lw=1.2)
ax.axvline(64, ymin=0.08, ymax=0.73, color=C['paper'], linestyle=':', lw=1.1)
ax.scatter([peak], [y[peak]], color=C['paper'], s=65, zorder=5)
ax.scatter([512], [y[512]], color=C['sky'], edgecolor=C['background'], s=50, zorder=5)
arrow = {'arrowstyle': '->', 'color': C['text-muted'], 'lw': 1.2}
ax.annotate('Peak detected', xy=(peak, y[peak]), xytext=(160, 1.00), arrowprops=arrow, fontsize=18)
ax.annotate('Second pulse', xy=(490, y[490]), xytext=(290, 0.60), arrowprops=arrow, fontsize=18)
ax.annotate('The next window\nkeeps the tail', xy=(600, y[600]), xytext=(690, 0.56), arrowprops=arrow, fontsize=18, color=C['sky'])
ax.annotate('', xy=(0, -0.055), xytext=(64, -0.055), arrowprops={'arrowstyle': '|-|', 'color': C['paper'], 'lw': 1.2})
ax.annotate('64 samples before the rising edge', xy=(32, -0.055), xytext=(135, -0.10), arrowprops=arrow, fontsize=15)
for lo, hi, label, role in [(0, 512, 'Window 1: samples 0-511', 'editorial-accent'),
                             (512, 1024, 'Window 2: samples 512-1023', 'sky')]:
    ax.plot([lo, hi], [1.22, 1.22], color=C[role], lw=6, solid_capstyle='butt')
    ax.text((lo + hi) / 2, 1.27, label, ha='center', va='bottom', fontsize=17, color=C[role])
ax.set_xlim(0, 1024)
ax.set_ylim(-0.17, 1.41)
ax.set_xticks([0, 64, 256, 512, 768, 1024])
ax.set_yticks([0, 0.5, 1.0])
ax.set_xlabel('Sample number (16 ns/sample)')
ax.set_ylabel('Signal [a.u.]')
ax.spines[['top', 'right']].set_visible(False)
ax.grid(axis='y', color=C['border'], alpha=0.25)
fig.tight_layout(pad=1.0)
(ROOT / 'figures').mkdir(exist_ok=True)
fig.savefig(ROOT / 'figures/pulse-windows.pdf', facecolor=fig.get_facecolor())
fig.savefig(ROOT / 'figures/pulse-windows.png', dpi=150, facecolor=fig.get_facecolor())
plt.close(fig)
print('Rendered illustrative 64-pretrigger / 512-sample continuation waveform')

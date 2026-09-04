#!/usr/bin/env python3
"""Render the presentation-scale dead-time comparison from simulator CSVs."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def load(path: Path) -> tuple[np.ndarray, np.ndarray]:
    with path.open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    rate = np.array([float(row["rate_hz_per_channel"]) for row in rows]) / 1000.0
    dead = np.array([float(row["dead_fraction_mean"]) for row in rows]) * 100.0
    return rate, dead


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sim-root", required=True, type=Path)
    args = parser.parse_args()
    source = args.sim_root / "data/output/analysis"
    series = [
        ("1024 samples", "deadtime_arch_1024_cpp.csv", "#f4f0e6"),
        ("512 samples", "deadtime_arch_512_cpp.csv", "#58c4dd"),
        ("512 + 50% overlap", "deadtime_arch_512_ring50_cpp.csv", "#F68D2E"),
    ]

    fig, ax = plt.subplots(figsize=(9.8, 5.5), constrained_layout=True)
    fig.patch.set_facecolor("#101820")
    ax.set_facecolor("#101820")
    for label, filename, color in series:
        rate, dead = load(source / filename)
        ax.plot(rate, dead, color=color, lw=3.2, label=label)

    ax.axvline(4.6, color="#F68D2E", lw=1.3, ls="--", alpha=0.8)
    ax.text(5.15, 32.5, "Model point\n4.6 kHz/channel", color="#F68D2E", fontsize=11)
    ax.set_xlim(0, 20.2)
    ax.set_ylim(0, 40)
    ax.set_xlabel("Input trigger rate [kHz/channel]", color="#f4f0e6", fontsize=13)
    ax.set_ylabel("Rejected triggers [%]", color="#f4f0e6", fontsize=13)
    ax.tick_params(colors="#f4f0e6", labelsize=11)
    for spine in ax.spines.values():
        spine.set_color("#6f7d85")
    ax.grid(color="#6f7d85", alpha=0.22, linewidth=0.8)
    legend = ax.legend(frameon=False, fontsize=12, loc="upper left")
    for text in legend.get_texts():
        text.set_color("#f4f0e6")

    out = Path(__file__).resolve().parent / "figures" / "deadtime_1024_512_ring50.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor=fig.get_facecolor())


if __name__ == "__main__":
    main()

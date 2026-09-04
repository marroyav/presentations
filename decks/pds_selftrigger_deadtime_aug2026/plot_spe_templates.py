#!/usr/bin/env python3
"""Render the pinned common Waffles cathode template used in production."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def load(path: Path) -> np.ndarray:
    values = np.loadtxt(path, dtype=float)
    scale = np.max(np.abs(values))
    if scale == 0:
        raise ValueError(f"template is empty: {path}")
    return values / scale


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--analysis-root", required=True, type=Path)
    args = parser.parse_args()
    source = (
        args.analysis_root
        / "data/spe-templates/waffles-np02-c-6e6274d/derived/waffles_np02_c_common_spe.dat"
    )
    curves = [("Common C-channel model", load(source), "#F68D2E")]

    fig, ax = plt.subplots(figsize=(10.5, 4.4), constrained_layout=True)
    fig.patch.set_facecolor("#101820")
    ax.set_facecolor("#101820")
    for label, values, color in curves:
        ax.plot(np.arange(values.size), values, lw=2.8, label=label, color=color)
    ax.axvline(512, color="#f4f0e6", lw=1.2, ls="--", alpha=0.8)
    ax.text(520, 0.91, "512-sample boundary", color="#f4f0e6", fontsize=11)
    ax.set_xlabel("Template sample", color="#f4f0e6", fontsize=12)
    ax.set_ylabel("Normalized SPE amplitude", color="#f4f0e6", fontsize=12)
    ax.tick_params(colors="#f4f0e6", labelsize=10)
    for spine in ax.spines.values():
        spine.set_color("#6f7d85")
    ax.grid(color="#6f7d85", alpha=0.22, linewidth=0.8)
    legend = ax.legend(frameon=False, fontsize=11, loc="upper right")
    for text in legend.get_texts():
        text.set_color("#f4f0e6")

    out = Path(__file__).resolve().parent / "figures" / "waffles_common_c_template.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor=fig.get_facecolor())


if __name__ == "__main__":
    main()

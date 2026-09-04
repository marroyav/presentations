#!/usr/bin/env python3
"""Render the matched activity and candidate-trace dead-time results."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


INK = "#101820"
PAPER = "#f4f0e6"
SKY = "#58c4dd"
ORANGE = "#F68D2E"
MUTED = "#9aa6ad"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def style(fig: plt.Figure, ax: plt.Axes) -> None:
    fig.patch.set_facecolor(INK)
    ax.set_facecolor(INK)
    ax.tick_params(colors=PAPER, labelsize=10)
    ax.xaxis.label.set_color(PAPER)
    ax.yaxis.label.set_color(PAPER)
    for spine in ax.spines.values():
        spine.set_color("#6f7d85")
    ax.grid(axis="y", color="#6f7d85", alpha=0.22, linewidth=0.8)


def activity_plot(activity_csv: Path, output: Path) -> None:
    data = rows(activity_csv)
    selected = {
        (row["detector"], row["source"], row["module_class"]): float(row["mean_candidate_rate_hz_per_channel"])
        for row in data
        if row["source"] in {"intrinsic-lar", "internal-combined"}
        and ((row["detector"] == "FD-HD" and row["module_class"] == "apa-integrated")
             or (row["detector"] == "FD-VD" and row["module_class"] == "cathode"))
    }
    labels = ["Intrinsic LAr", "All internal"]
    sources = ["intrinsic-lar", "internal-combined"]
    hd = [selected[("FD-HD", source, "apa-integrated")] / 1000 for source in sources]
    vd = [selected[("FD-VD", source, "cathode")] / 1000 for source in sources]
    x = np.arange(len(labels))
    width = 0.32
    fig, ax = plt.subplots(figsize=(8.6, 4.8), constrained_layout=True)
    style(fig, ax)
    bars_hd = ax.bar(x - width / 2, hd, width, color=SKY, label="FD-HD")
    bars_vd = ax.bar(x + width / 2, vd, width, color=ORANGE, label="FD-VD cathode")
    ax.set_xticks(x, labels)
    ax.set_ylabel("Candidates [kHz/channel]")
    ax.set_ylim(0, 125)
    legend = ax.legend(frameon=False, loc="upper left")
    for text in legend.get_texts(): text.set_color(PAPER)
    for left, right, h, v in zip(bars_hd, bars_vd, hd, vd):
        ax.text(left.get_x() + left.get_width()/2, h + 2, f"{h:.1f}", ha="center", color=PAPER, fontsize=10)
        ax.text(right.get_x() + right.get_width()/2, v + 2, f"{v:.1f}", ha="center", color=PAPER, fontsize=10)
        ax.text((left.get_x() + right.get_x() + right.get_width())/2, max(h, v) + 9,
                f"VD/HD = {v/h:.2f}", ha="center", color=ORANGE, fontsize=11, fontweight="bold")
    fig.savefig(output, facecolor=fig.get_facecolor())


def deadtime_plot(deadtime_csv: Path, output: Path) -> None:
    data = rows(deadtime_csv)
    wanted = [
        ("FD-HD", "apa-integrated", "HD"),
        ("FD-VD", "cathode", "VD cathode"),
        ("FD-VD", "long-wall", "VD long wall"),
        ("FD-VD", "short-wall", "VD short wall"),
    ]
    selected = {
        (row["detector"], row["module_class"], int(row["frame_samples"])): 100 * float(row["dead_fraction"])
        for row in data if row["source"] == "intrinsic-lar"
    }
    labels = [label for _, _, label in wanted]
    long = [selected[(detector, module_class, 1024)] for detector, module_class, _ in wanted]
    short = [selected[(detector, module_class, 512)] for detector, module_class, _ in wanted]
    x = np.arange(len(labels))
    width = 0.34
    fig, ax = plt.subplots(figsize=(9.2, 5.0), constrained_layout=True)
    style(fig, ax)
    bars_long = ax.bar(x - width/2, long, width, color=PAPER, label="1024 samples")
    bars_short = ax.bar(x + width/2, short, width, color=ORANGE, label="512 samples")
    ax.set_xticks(x, labels)
    ax.set_ylabel("Candidates rejected while channel is busy [%]")
    ax.set_ylim(0, 72)
    legend = ax.legend(frameon=False, loc="upper right")
    for text in legend.get_texts(): text.set_color(PAPER)
    for bars in (bars_long, bars_short):
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height + 1.2, f"{height:.1f}%",
                    ha="center", color=PAPER, fontsize=9)
    fig.savefig(output, facecolor=fig.get_facecolor())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--analysis-root", required=True, type=Path)
    args = parser.parse_args()
    figures = Path(__file__).resolve().parent / "figures"
    figures.mkdir(exist_ok=True)
    activity_plot(
        args.analysis_root / "output/materials/waffles-c-fdvd-fdhd-source-matched-activity-v1/source_class_candidate_activity.csv",
        figures / "larsoft_activity_comparison.pdf",
    )
    deadtime_plot(
        args.analysis_root / "output/materials/waffles-c-candidate-trace-deadtime-v1/trace_deadtime_summary.csv",
        figures / "larsoft_trace_deadtime.pdf",
    )


if __name__ == "__main__":
    main()

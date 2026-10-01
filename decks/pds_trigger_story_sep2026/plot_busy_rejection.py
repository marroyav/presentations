#!/usr/bin/env python3
"""Historical new-frame rejection plot, withdrawn from the deck on 2026-09-18.

This does not measure capture dead time or uncaptured photon signals. Retained
for reproduction of the original counter only; see analysis/capture_deadtime.py.
"""

import csv
import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "evidence/activity.csv"
TOKENS = ROOT.parents[1] / "templates/dune-professional/design-tokens.json"


def main():
    colors = {key: value["hex"] for key, value in json.loads(TOKENS.read_text())["colors"].items()}
    with SOURCE.open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    cathode = next(row for row in rows if row["population"] == "VD_cathode")
    rate = [float(row["candidate_mean_khz_per_channel"]) * 1000 for row in rows]
    cathode_rate = float(cathode["candidate_mean_khz_per_channel"]) * 1000

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 16, "pdf.fonttype": 42,
                         "text.color": colors["text"], "axes.labelcolor": colors["text"],
                         "xtick.color": colors["text-muted"], "ytick.color": colors["text-muted"]})
    fig, ax = plt.subplots(figsize=(12.4, 4.5), facecolor=colors["background"])
    ax.set_facecolor(colors["background"])
    ax.spines[["top", "right"]].set_visible(False)
    for spine in ax.spines.values():
        spine.set_color(colors["border"])
    ax.set_axisbelow(True)
    ax.grid(axis="y", color=colors["border"], alpha=0.4)
    ax.axvline(cathode_rate, color=colors["border"], linestyle="--", linewidth=1.5)
    for row, x in zip(rows, rate):
        ax.plot([x, x], [float(row["dead_512_percent"]), float(row["dead_1024_percent"])],
                color=colors["border"], linewidth=1.5, zorder=2)
    for samples, marker, role in [(1024, "o", "paper"), (512, "D", "sky")]:
        values = [float(row[f"dead_{samples}_percent"]) for row in rows]
        ax.scatter(rate, values, s=105, marker=marker, color=colors[role],
                   label=f"{samples} samples", zorder=3)
        value = float(cathode[f"dead_{samples}_percent"])
        ax.annotate(f"{value:.0f}%", (cathode_rate, value), xytext=(13, 0),
                    textcoords="offset points", va="center", color=colors[role],
                    fontsize=22, fontweight="bold")
    ax.text(cathode_rate, 70, "VD cathode", ha="center", color=colors["text"], fontsize=17)
    ax.set_xlim(0, 103000)
    ax.set_ylim(0, 76)
    ax.set_xticks([0, 25000, 50000, 75000, 100000])
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax.set_yticks([0, 20, 40, 60])
    ax.set_xlabel("Mean candidate activity [Hz/channel]", labelpad=9)
    ax.set_ylabel("Candidates rejected\nwhile busy [%]", labelpad=10)
    ax.legend(loc="upper left", frameon=False, fontsize=17)
    fig.subplots_adjust(left=0.13, right=0.96, bottom=0.23, top=0.94)
    figures = ROOT / "figures"
    figures.mkdir(exist_ok=True)
    fig.savefig(figures / "busy-rejection.pdf", facecolor=fig.get_facecolor(),
                metadata={"Title": "Intrinsic-LAr channel-only candidate busy rejection"})
    plt.close(fig)
    (ROOT / "evidence/busy-plot-provenance.json").write_text(json.dumps({
        "source": "activity.csv", "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "renderer": "plot_busy_rejection.py", "new_simulation": False,
        "x": "Population mean candidate rate, Hz/channel",
        "y": "Candidates rejected by channel-local busy gate, percent",
        "threshold": "> 0.7 PE", "background": "Nominal intrinsic-LAr mixture; no gamma overlay",
        "sample_clock_hz": 62500000, "busy_cycles": {"1024": 1037, "512": 525},
        "busy_microseconds": {"1024": 16.592, "512": 8.4},
        "interpretation": "Each marker is a population replay result, not a universal rate curve. Vertical segments pair the same candidates at two frame lengths. No shared readout or buffer/continuation gains included."
    }, indent=2) + "\n")


if __name__ == "__main__":
    main()

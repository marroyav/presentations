#!/usr/bin/env python3
"""Sweep capture dead time and FIFO-blocked time through finite shared readout.

This is a rate-sensitivity study, not a replacement for the correlated VD
activity-trace replay summarized in capture_loss_vd.csv.
"""
import argparse
import csv
import math
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RATES = (1000, 2500, 5000, 7500, 10000, 12500, 15000, 17500, 20000,
         22500, 25000, 27500, 30000, 35000, 40000, 45000, 50000, 60000,
         75000, 87000, 100000, 125000, 150000, 200000)
FRAMES = {1024: (232, 1037), 512: (120, 525)}
# Shared two-lane readout imposes the firmware-derived ~7.9 Gbit/s ceiling.
# The superseded ideal downstream drain is NOT an actual Hermes RTL model.
STAGES = {"daphne_fifo": ("Finite shared readout", [])}
REPEATS = 5
WARMUP = 500_000
MEASURE = 5_000_000


def run(binary: Path, rate: int, frame: int, stage: str, repeat: int) -> dict:
    words, busy = FRAMES[frame]
    prefix = ROOT / "analysis/results" / f"freq-{rate}-{frame}-{stage}-r{repeat}"
    capture = prefix.with_suffix(".capture.csv")
    raw = prefix.with_suffix(".raw.csv")
    cmd = [str(binary), "--architecture", "legacy", "--rate-list", str(rate),
           "--repeats", "1", "--seed-start", str(20260918 + 101 * repeat),
           "--channels", "32", "--lanes", "2", "--channels-per-lane", "16",
           "--frame-samples", str(frame), "--record-words", str(words),
           "--builder-busy-cycles", str(busy), "--warmup-cycles", str(WARMUP),
           "--measure-cycles", str(MEASURE), "--capture-out", str(capture),
           "--raw-csv-out", str(raw)]
    cmd.extend(STAGES[stage][1])
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
    with capture.open() as f:
        coverage = next(csv.DictReader(f))
    with raw.open() as f:
        counters = next(csv.DictReader(f))
    capture.unlink(); raw.unlink()
    return {
        "rate_hz_per_channel": rate, "frame_samples": frame, "stage": stage,
        "repeat": repeat,
        "dead_time_percent": 100 * int(coverage["missing_ticks"]) /
            int(coverage["observation_channel_ticks"]),
        "missing_signal_percent": 100 * int(coverage["missing_candidates"]) /
            int(coverage["candidates"]) if int(coverage["candidates"]) else 0,
        "rejected_request_percent": 100 * (int(counters["generated_total"]) -
            int(counters["accepted_total"])) / int(counters["generated_total"]),
        "fifo_dead_time_percent": 100 * int(coverage["fifo_missing_ticks"]) /
            int(coverage["observation_channel_ticks"]),
        "generated_requests": int(counters["generated_total"]),
        "accepted_packets": int(counters["accepted_total"]),
        "sent_packets": int(counters["sent_total"]),
        "frame_output_gbps": int(counters["sent_word_total"]) * 64 / (MEASURE / 62.5e6) / 1e9,
        "accepted_rate_khz_per_channel": int(counters["accepted_total"]) /
            (MEASURE / 62.5e6) / 32 / 1000,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path, default=ROOT / "analysis/fifo_capture_sim")
    parser.add_argument("--plot-only", action="store_true")
    args = parser.parse_args()
    out = ROOT / "analysis/results"
    out.mkdir(parents=True, exist_ok=True)
    csv_path = out / "frequency_sweep.csv"
    if not args.plot_only:
        rows = [run(args.binary.resolve(), rate, frame, stage, repeat)
                for rate in RATES for frame in FRAMES for stage in STAGES
                for repeat in range(REPEATS)]
        with csv_path.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=rows[0].keys())
            w.writeheader(); w.writerows(rows)
    else:
        with csv_path.open() as f:
            rows = list(csv.DictReader(f))

    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    colors = {1024: "#58C4DD", 512: "#F68D2E"}
    background, ink, muted = "#101820", "#F4F0E6", "#B6C2CA"
    plt.rcParams.update({"font.size": 12, "text.color": ink,
                         "axes.labelcolor": ink, "xtick.color": muted,
                         "ytick.color": muted, "axes.edgecolor": "#52616B"})
    fig, ax = plt.subplots(figsize=(12.8, 5.3))
    fig.patch.set_facecolor(background)
    ax.set_facecolor(background)
    summaries = []
    for frame, (words, busy) in FRAMES.items():
        total, fifo, errors = [], [], []
        for rate in RATES:
            subset = [r for r in rows if int(r["frame_samples"]) == frame and
                      int(r["rate_hz_per_channel"]) == rate]
            def average(field):
                return sum(float(r[field]) for r in subset) / len(subset)
            mu = average("dead_time_percent")
            sem = math.sqrt(sum((float(r["dead_time_percent"]) - mu)**2
                                for r in subset) / (len(subset)-1) / len(subset))
            total.append(mu); fifo.append(average("fifo_dead_time_percent")); errors.append(sem)
            summaries.append(dict(frame_samples=frame, rate_hz_per_channel=rate,
                                  dead_time_percent=mu, fifo_dead_time_percent=fifo[-1],
                                  frame_output_gbps=average("frame_output_gbps")))
        x = [r/1000 for r in RATES]
        ax.errorbar(x, total, yerr=errors, color=colors[frame], lw=2.8, capsize=2)
        ax.plot(x, fifo, color=colors[frame], lw=2.0, ls="--", alpha=.85)
        ax.fill_between(x, fifo, total, color=colors[frame], alpha=.10)
        # Mean offered load after the fixed assembly gate equals the interface budget.
        capacity = 8 * words / (words + 2)
        accepted_ceiling = capacity * 1e9 / (32 * words * 64)
        knee = accepted_ceiling / (1 - accepted_ceiling * busy / 62.5e6) / 1000
        ax.axvline(knee, color=colors[frame], lw=1.1, ls=":", alpha=.75)
        ax.text(knee, 79, f"{frame}: ~{knee:.0f} kHz", color=colors[frame],
                fontsize=10, ha="center")
        y = total[RATES.index(87000)]
        ax.scatter([87], [y], color=colors[frame], s=35, zorder=5)
        ax.annotate(f"{frame} / 5: {y:.1f}%", (87, y), xytext=(12, 9),
                    textcoords="offset points", color=colors[frame], fontsize=12,
                    bbox=dict(facecolor=background, edgecolor="none", pad=1))
    ax.axvline(87, color=muted, lw=1.1, ls="--", alpha=.85)
    ax.text(89, 5, "87 kHz/channel\nat 0.7 PE", fontsize=11, color=muted)
    ax.set(xlim=(0, 205), ylim=(0, 84),
           xlabel="Input activity (kHz/channel)", ylabel="Blocked, uncaptured time (%)")
    ax.set_xticks([0, 25, 50, 75, 100, 125, 150, 175, 200])
    ax.set_yticks(range(0, 81, 20))
    ax.grid(axis="y", color="#52616B", alpha=.4, lw=.6)
    ax.spines[["top", "right"]].set_visible(False)
    handles = [Line2D([0],[0], color=colors[f], lw=3, label=f"{f} / 5") for f in FRAMES]
    handles += [Line2D([0],[0], color=ink, lw=2, label="Total dead time"),
                Line2D([0],[0], color=ink, lw=2, ls="--", label="Time blocked by the output FIFO")]
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(.5,.075),
               ncol=4, frameon=False, fontsize=11, labelcolor=ink)
    fig.text(.5,.025,"Dotted markers: mean offered load reaches the ~7.9 Gbit/s shared-readout budget. "
             "Bursts cause loss earlier.",ha="center",fontsize=10,color=muted)
    fig.subplots_adjust(left=.075,right=.98,top=.97,bottom=.26)
    fig.savefig(ROOT / "figures/frequency_deadtime.pdf", bbox_inches="tight")
    fig.savefig(ROOT / "figures/frequency_deadtime.png", dpi=180, bbox_inches="tight")
    with (out / "frequency_sweep_summary.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=summaries[0].keys()); w.writeheader(); w.writerows(summaries)
    for r in summaries:
        if r["rate_hz_per_channel"] == 87000:
            print(r)


if __name__ == "__main__":
    main()

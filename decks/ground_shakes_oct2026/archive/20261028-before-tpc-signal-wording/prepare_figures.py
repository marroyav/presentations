#!/usr/bin/env python3
"""Make readable slide plots from pinned, existing ground-shake results.

Normal use reads the small evidence bundle. --refresh selects the displayed
values again from the sibling analysis directory and records its input hashes.
This script does not decode detector data, refit models or fill recording gaps.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ANALYSIS = HERE.parents[2] / "ground-shake-data/analysis"
EVIDENCE = HERE / "evidence"
FIGURES = HERE / "figures"
TOKENS = ROOT / "templates/dune-professional/design-tokens.json"


def sha(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def write_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def refresh() -> None:
    sources = {}

    def source(name):
        path = ANALYSIS / name
        sources[name] = {"sha256": sha(path), "bytes": path.stat().st_size}
        return path

    def read(name):
        return json.loads(source(name).read_text())

    campaign = read("report-20261015/report-data.json")
    charge = read("charge-light-matching/report-data.json")
    electrical = read("electrical-pattern-20261023/report-data.json")
    sequence = read("electrical-pattern-20261023/sequence-results.json")
    metrics = read("electrical-pattern-20261023/sequence-event-metrics.json")
    dcs = read("dcs-association/dcs-matches.json")
    # Record the definitions as well as the displayed numbers.
    for name in [
        "all-runs/README.txt", "all-runs/all-runs-summary.csv",
        "aligned-detectors/README.txt", "shared-precursor/README.txt",
        "electrical-pattern-20261023/README.txt",
        "electrical-pattern-20261023/fit.py",
        "charge-light-matching/README.txt",
        "charge-light-matching/event_mixing.py",
        "charge-light-matching/event-mixing-results.json",
        "dcs-association/README.txt", "dcs-association/plot_dcs.py",
    ]:
        source(name)

    arrays = {}
    with np.load(source("aligned-detectors/aligned-data.npz")) as z:
        t = z["time_us"]
        mask = (t >= -277.048) & (t <= 102.048)
        arrays["example_time_us"] = t[mask]
        for kind in ["charge", "PDS"]:
            arrays[f"example_{kind}"] = z[f"20576_APA1_{kind}"][:, mask]

    with np.load(source("shared-precursor/traces.npz")) as z:
        t = z["r32731_e33_time_us"]
        mask = (t >= -250) & (t <= -20)
        arrays["slow_time_us"] = t[mask]
        for apa in [1, 2]:
            arrays[f"slow_APA{apa}"] = z[f"r32731_e33_APA{apa}_median_ADC"][mask]

    for run in [32731, 32739]:
        clear = [r for r in metrics
                 if r["run"] == run and r["TPC_both_precursors_above_reference_noise"]]
        arrays[f"coherence_{run}"] = np.array([
            [r["TPC"]["1"]["sign_directed_late_precursor_ADC"],
             -r["TPC"]["2"]["sign_directed_late_precursor_ADC"]]
            for r in clear
        ])
    assert sum(len(arrays[f"coherence_{r}"]) for r in [32731, 32739]) == 1355
    assert len(metrics) == 1376
    assert sum(r["events"] for r in campaign["run_screen"]) == 1531
    assert sum(r["screened_shake_candidates"] for r in campaign["run_screen"]) == 1516

    # Same 256 ns differences and masks as the 23 October analysis.
    # This is a recorded pulse example, not a new electrical decomposition.
    pulse_us = -183.296
    with np.load(source("electrical-pattern-20261023/cache/r32731_e33.npz")) as z:
        adc, rail, channels = z["adc"], z["rail"], z["channels"]
        time = (np.arange(8192) - 4096 + .5) * .256
        edge_time = (time[:-1] + time[1:]) / 2
        edges = np.diff(adc, axis=1)
        edges[rail[:, 1:] | rail[:, :-1] | (np.abs(edges) > 2000)] = np.nan
        view = (edge_time >= pulse_us - 3) & (edge_time < pulse_us + 8)
        arrays["pulse_time_us"] = edge_time[view] - pulse_us
        for channel in [13, 14, 16, 15]:
            index = int(np.flatnonzero(channels == channel)[0])
            arrays[f"pulse_ch{channel}"] = edges[index, view]

    with np.load(source("charge-light-matching/event-mixed-drift-histograms.npz")) as z:
        arrays["lag_edges_us"] = z["lag_edges_us"]
        for run in [32731, 32739]:
            arrays[f"mix_{run}"] = z[f"run{run}"]

    dcs_info = {}
    with np.load(source("dcs-association/july-dcs-series.npz")) as z:
        for run in [27938, 27951]:
            rows = [r for r in dcs["events"] if r["run"] == run]
            event_times = np.array([
                dt.datetime.fromisoformat(r["TPC_onset_utc"]).timestamp() for r in rows
            ])
            center = float(np.median(event_times))
            arrays[f"dcs_{run}_events_s"] = event_times - center
            dcs_info[str(run)] = {
                "center_UTC": dt.datetime.fromtimestamp(center, dt.timezone.utc).isoformat(),
                "candidate_count": len(rows), "reference_values_V": {},
            }
            for tag in [15, 5, 12]:
                t, v = z[f"tag{tag}_utc_epoch_s"], z[f"tag{tag}_value"]
                ref = (t >= center - 300) & (t < center - 30)
                assert np.any(ref), (run, tag)
                baseline = float(np.median(v[ref]))
                selected = np.abs(t - center) <= 60
                arrays[f"dcs_{run}_{tag}_time_s"] = t[selected] - center
                arrays[f"dcs_{run}_{tag}_delta_V"] = v[selected] - baseline
                dcs_info[str(run)]["reference_values_V"][str(tag)] = baseline

    EVIDENCE.mkdir(exist_ok=True)
    np.savez_compressed(EVIDENCE / "plot-data.npz", **arrays)
    stats = {
        "run_screen": campaign["run_screen"],
        "charge_light": charge,
        "electrical_pattern": electrical,
        "PDS_only_TPC_prediction": sequence["PDS_only_TPC_prediction"],
        "clock_test": next(r for r in sequence["fixed_delay_clock_tests"]
                           if r["split"] == "other_run" and r["TPC_APA"] == 1
                           and r["threshold_ADC"] == 2 and r["PDS_pulse"] == "first"),
        "TPC_coherence": sequence["TPC_coherence"],
        "DCS": dcs_info,
        "pulse_example": {"run": 32731, "event": 33, "time_from_shake_us": pulse_us},
    }
    write_json(EVIDENCE / "statistics.json", stats)
    write_json(EVIDENCE / "source-manifest.json", {
        "created_UTC": dt.datetime.now(dt.timezone.utc).isoformat(),
        "source_root": str(ANALYSIS),
        "sources": sources,
        "frozen_files": {name: sha(EVIDENCE / name)
                         for name in ["plot-data.npz", "statistics.json"]},
        "status": "Existing exploratory results; no new detector analysis or data acquisition.",
    })


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    if args.refresh:
        refresh()

    manifest = json.loads((EVIDENCE / "source-manifest.json").read_text())
    for name, expected in manifest["frozen_files"].items():
        assert sha(EVIDENCE / name) == expected, f"Frozen evidence changed: {name}"
    stats = json.loads((EVIDENCE / "statistics.json").read_text())
    z = np.load(EVIDENCE / "plot-data.npz")
    colors = json.loads(TOKENS.read_text())["colors"]
    color = lambda name: colors[name]["hex"]
    blue, orange = color("editorial-muted"), color("editorial-accent-deep")
    ink, gray, white = color("editorial-text"), color("border"), color("editorial-canvas")
    rule = color("editorial-rule")
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 18,
        "axes.titlesize": 20, "axes.labelsize": 18,
        "xtick.labelsize": 17, "ytick.labelsize": 17, "legend.fontsize": 16,
        "text.color": ink, "axes.labelcolor": ink, "axes.edgecolor": gray,
        "xtick.color": ink, "ytick.color": ink,
        "figure.facecolor": white, "axes.facecolor": white,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.formatter.useoffset": False, "pdf.fonttype": 42,
        "lines.linewidth": 2.3,
    })
    FIGURES.mkdir(exist_ok=True)
    outputs = {}

    def save(fig, name):
        for ext in ["pdf", "png"]:
            path = FIGURES / f"{name}.{ext}"
            fig.savefig(path, dpi=180)
            outputs[str(path.relative_to(HERE))] = sha(path)
        plt.close(fig)

    def grid(ax):
        ax.grid(axis="y", color=rule, alpha=.65, lw=.7)
        ax.set_axisbelow(True)

    # 1. One recorded event; the color limits match the existing aligned plot.
    fig, axs = plt.subplots(1, 2, figsize=(13, 3.95), layout="constrained")
    cmap = LinearSegmentedColormap.from_list("signed_signal", [blue, white, orange])
    cmap.set_bad(rule)
    t = z["example_time_us"]
    for ax, kind, label, limit in zip(axs, ["charge", "PDS"], ["Charge · APA1", "PDS · APA1"], [500, 200]):
        values = z[f"example_{kind}"]
        im = ax.imshow(values, origin="lower", aspect="auto", interpolation="nearest",
                       extent=[t[0] - 1.024, t[-1] + 1.024, -.5, len(values) - .5],
                       cmap=cmap, vmin=-limit, vmax=limit, rasterized=True)
        ax.set_title(label)
        ax.set(xlim=(-275, 100), xlabel="Time from trigger (µs)", ylabel="Channel row")
        ax.set_xticks([-200, -100, 0, 100])
        ax.set_yticks([0, 1280, 2559] if kind == "charge" else [0, 20, 39])
        ax.axvline(-180, color=ink, ls="--", lw=1.4)
        ax.axvline(0, color=ink, lw=1.4)
        cb = fig.colorbar(im, ax=ax, pad=.02, fraction=.046, ticks=[-limit, 0, limit])
        cb.set_label("ADC change", fontsize=17)
    save(fig, "01-charge-and-pds")

    # 2. Signed waveform and full clear-record scatter, without a fit line.
    fig, axs = plt.subplots(1, 2, figsize=(13, 3.95), layout="constrained")
    for apa, c, ls in [(1, blue, "-"), (2, orange, "--")]:
        axs[0].plot(z["slow_time_us"], z[f"slow_APA{apa}"], color=c, ls=ls, label=f"APA{apa}")
    axs[0].set(title="Run 32731 · event 33", xlabel="Time from main shake (µs)",
               ylabel="Median ADC change", xlim=(-250, -20))
    axs[0].axhline(0, color=gray, lw=.8)
    axs[0].legend(frameon=False)
    grid(axs[0])
    for run, c, marker in [(32731, blue, "o"), (32739, orange, "x")]:
        points = z[f"coherence_{run}"]
        axs[1].scatter(points[:, 0], points[:, 1], s=14, alpha=.4, color=c,
                       marker=marker, label=f"Run {run}", linewidths=.8)
    axs[1].set(title="1,355 of 1,376 November records", xlabel="APA1 change (ADC)",
               ylabel="APA2 change (ADC)")
    axs[1].legend(frameon=False, markerscale=2)
    grid(axs[1])
    save(fig, "02-opposite-charge-signs")

    # 3. One preselected pulse, plotted as recorded 256 ns signal differences.
    fig, axs = plt.subplots(1, 2, figsize=(13, 3.95), layout="constrained", sharex=True)
    for ch, c, ls in [(13, blue, "-"), (14, orange, "--"), (16, gray, ":")]:
        axs[0].plot(z["pulse_time_us"], z[f"pulse_ch{ch}"], color=c, ls=ls, label=f"Input {ch}")
    axs[1].plot(z["pulse_time_us"], z["pulse_ch15"], color=blue, label="Input 15")
    for ax, title in zip(axs, ["Reported disconnected inputs", "Connected input"]):
        ax.set(title=title, xlabel="Time from selected pulse (µs)",
               ylabel="Signal change\n(ADC per 256 ns)", xlim=(-3, 8))
        ax.axvline(0, color=gray, ls=":", lw=1)
        ax.axhline(0, color=gray, lw=.7)
        ax.legend(frameon=False, loc="lower right")
        grid(ax)
    save(fig, "03-disconnected-inputs")

    # 4. Published out-of-run errors; no model refit or changed cohort.
    pred = next(r for r in stats["PDS_only_TPC_prediction"] if r["split"] == "other_run")
    clock = stats["clock_test"]
    fig, axs = plt.subplots(1, 2, figsize=(13, 3.95), layout="constrained")
    panels = [
        ([pred["constant_training_median_error_ADC"], pred["mean_absolute_error_ADC"]],
         ["Constant\nestimate", "Early\nPDS data"], "TPC precursor size · 477 events", "Mean error (ADC)", ".2f"),
        ([clock["shake_clock_only_MAE_us"], clock["fixed_PDS_delay_MAE_us"]],
         ["Known\nshake time", "Early\nPDS time"], "TPC precursor timing · 225 events", "Mean timing error (µs)", ".1f"),
    ]
    for ax, (values, labels, title, ylabel, fmt) in zip(axs, panels):
        bars = ax.bar([0, 1], values, width=.56, color=[blue, orange])
        ax.bar_label(bars, labels=[format(v, fmt) for v in values], padding=5, fontsize=20)
        ax.set_xticks([0, 1], labels)
        ax.set(title=title, ylabel=ylabel, ylim=(0, max(values) * 1.23))
        grid(ax)
    save(fig, "04-pds-prediction")

    # 5. Same fixed 50 µs bins and exposure denominator as the source plot.
    fig, axs = plt.subplots(1, 2, figsize=(13, 3.95), layout="constrained", sharey=True)
    edges = z["lag_edges_us"]
    centers = ((edges[:-1] + edges[1:]) / 2).reshape(-1, 5).mean(axis=1)

    def per_time(numerator, denominator):
        n = numerator.reshape(-1, 5).sum(axis=1)
        d = denominator.reshape(-1, 5).sum(axis=1)
        return np.divide(n, d, out=np.full_like(n, np.nan), where=d > 0) * 100

    for ax, run in zip(axs, [32731, 32739]):
        h = z[f"mix_{run}"]
        ax.plot(centers, per_time(h[0], h[1]), color=blue, label="Same event")
        ax.plot(centers, per_time(h[2], h[3]), color=orange, ls="--", label="Other events")
        ax.axvline(0, color=gray, lw=.8)
        ax.set(title=f"Run {run}", xlabel="Charge time − PDS time (µs)",
               xlim=(-100, 650), ylim=(0, 20))
        ax.set_xticks([0, 200, 400, 600])
        ax.legend(frameon=False, loc="upper left")
        grid(ax)
    axs[0].set_ylabel("Charge features per 100 µs\nof usable comparison time")
    save(fig, "05-charge-light-timing")

    # 6. Native voltage samples; no resampling or interpolated values.
    fig, axs = plt.subplots(2, 2, figsize=(13, 4.65), layout="constrained", sharex=True)
    for col, run in enumerate([27938, 27951]):
        axs[0, col].plot(z[f"dcs_{run}_15_time_s"], z[f"dcs_{run}_15_delta_V"],
                         ".-", color=blue, lw=1.2, ms=7)
        n = stats["DCS"][str(run)]["candidate_count"]
        axs[0, col].set_title(f"Run {run} · {n} candidate" + ("s" if n != 1 else ""))
        for tag, label, c, marker in [(5, "APA1", blue, "o"), (12, "APA2", orange, "x")]:
            axs[1, col].plot(z[f"dcs_{run}_{tag}_time_s"], z[f"dcs_{run}_{tag}_delta_V"] * 1000,
                             marker=marker, color=c, lw=1.2, ms=5, label=label)
        axs[1, col].legend(frameon=False, ncol=2, loc="lower left", fontsize=16)
        axs[1, col].set_xlabel("Time from event / burst centre (s)")
        for ax in axs[:, col]:
            for t in z[f"dcs_{run}_events_s"]:
                ax.axvline(t, color=gray, ls=":", lw=1.1, alpha=.85)
            ax.set_xlim(-60, 60)
            ax.set_xticks([-60, -30, 0, 30, 60])
            grid(ax)
    axs[0, 0].set_ylabel("Cathode\nchange (V)")
    axs[1, 0].set_ylabel("Wire bias\nchange (mV)")
    save(fig, "06-july-voltage")
    z.close()
    write_json(EVIDENCE / "figure-manifest.json", {
        "script_sha256": sha(Path(__file__)), "design_tokens_sha256": sha(TOKENS),
        "frozen_files": manifest["frozen_files"], "figures": outputs,
        "checks": ["Frozen input hashes match", "Seven-run total: 1,531 saved events",
                   "Charge screen: 1,516 candidates", "Clear November charge pattern: 1,355 / 1,376",
                   "No interpolation across missing samples", "No new fits or detector decoding"],
    })
    print("Built six figures from pinned results (PDF and PNG).")


if __name__ == "__main__":
    main()

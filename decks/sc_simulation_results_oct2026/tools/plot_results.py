"""Render the updated local VD/HD curves; simulation stays in sc_emu."""
import csv
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
tokens = json.loads((ROOT.parents[1] / "templates/dune-professional/design-tokens.json").read_text())["colors"]
c = {k: v["hex"] for k, v in tokens.items()}
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 14, "axes.labelsize": 14,
    "figure.facecolor": c["background"], "axes.facecolor": c["background"],
    "text.color": c["text"], "axes.labelcolor": c["text"],
    "xtick.color": c["text-muted"], "ytick.color": c["text-muted"],
    "axes.edgecolor": c["border"], "pdf.fonttype": 42,
})
rows = list(csv.DictReader((ROOT / "evidence/updated-process-curves.csv").open()))
fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.1), layout="constrained")
for ax in axes:
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_xticks([1, 2, 3, 4, 6, 8])
    ax.set_xlabel("OPC-UA processes on ONE host")
    ax.grid(axis="y", color=c["border"], alpha=.35)
    ax.axvline(2, color=c["text-muted"], linestyle="--", alpha=.55)
for detector, color in (("vd", c["sky"]), ("hd", c["coral"])):
    data = [r for r in rows if r["detector"] == detector]
    x = [int(r["processes"]) for r in data]
    axes[0].plot(x, [float(r["churn_values_per_second"])/1000 for r in data],
                 color=color, marker="o", lw=2.5, label=detector.upper())
    axes[1].plot(x, [float(r["server_rss_mb"]) for r in data],
                 color=color, marker="o", lw=2.5, label=detector.upper())
for ax in axes:
    ax.legend(frameon=False, labelcolor=c["text"])
axes[0].set_ylabel("Read rate (thousand values/s)")
axes[0].set_ylim(0, 145)
axes[0].set_title("Throughput flattens after two", loc="left", fontsize=16)
axes[1].set_ylabel("Total server-process RSS (MB)")
axes[1].set_ylim(0, 1100)
axes[1].set_title("Each process adds memory", loc="left", fontsize=16)
fig.savefig(ROOT / "figures/process-curve.pdf")
plt.close(fig)

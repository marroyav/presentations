#!/usr/bin/env python3
"""Build this boundary review only; no hash checks or unrelated deck builds."""
from pathlib import Path
import subprocess
import sys

deck = Path(__file__).resolve().parent
root = deck.parents[1]
for source in sorted((deck / "diagrams").glob("*.dot.in")):
    for extension in ("pdf", "svg"):
        output = source.with_name(source.name.removesuffix(".dot.in") + "." + extension)
        subprocess.run([sys.executable, str(root / "scripts/render_diagram.py"), str(source), str(output)], check=True)
subprocess.run(["tectonic", "-C", "--chatter", "minimal", "--keep-logs", "main.tex"], cwd=deck, check=True)

#!/usr/bin/env python3
"""Render a tokenized Graphviz template to vector PDF or SVG."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TOKENS = ROOT / "templates/dune-professional/design-tokens.json"
TOKEN_RE = re.compile(r"\{\{([a-z0-9-]+)\}\}")
SUPPORTED_FORMATS = {"pdf", "svg"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Replace {{color-role}} tokens and render a Graphviz diagram."
    )
    parser.add_argument("source", type=Path, help="Input .dot.in file")
    parser.add_argument("output", type=Path, help="Output .pdf or .svg file")
    parser.add_argument("--tokens", type=Path, default=DEFAULT_TOKENS)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_format = args.output.suffix.removeprefix(".").lower()
    if output_format not in SUPPORTED_FORMATS:
        print(
            f"Unsupported output format {output_format!r}; choose PDF or SVG.",
            file=sys.stderr,
        )
        return 2
    if shutil.which("dot") is None:
        print("Graphviz 'dot' is not available on PATH.", file=sys.stderr)
        return 2

    token_data = json.loads(args.tokens.read_text(encoding="utf-8"))
    colors = {
        name: definition["hex"] for name, definition in token_data["colors"].items()
    }
    source = args.source.read_text(encoding="utf-8")
    unknown = sorted(set(TOKEN_RE.findall(source)) - colors.keys())
    if unknown:
        print(
            "Unknown design token(s): " + ", ".join(unknown),
            file=sys.stderr,
        )
        return 2

    rendered_source = TOKEN_RE.sub(lambda match: colors[match.group(1)], source)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    process = subprocess.run(
        ["dot", f"-T{output_format}", "-o", str(args.output)],
        input=rendered_source,
        text=True,
        capture_output=True,
        check=False,
    )
    if process.returncode != 0:
        print(process.stderr.rstrip(), file=sys.stderr)
        return process.returncode
    if process.stderr.strip():
        print(process.stderr.rstrip(), file=sys.stderr)
    print(f"Rendered {args.source} -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

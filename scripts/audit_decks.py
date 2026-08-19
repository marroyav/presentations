#!/usr/bin/env python3
"""Lightweight static audit for shared-template presentation decks."""

from __future__ import annotations

import re
import sys
from pathlib import Path


FRAME_TITLE_RE = re.compile(r"\\begin\{frame\}(?:\[[^\]]*\])?\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}")
TITLE_RE = re.compile(r"\\title(?:\[[^\]]*\])?\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}")
VSPACE_RE = re.compile(r"\\vspace\*?\{")


def strip_tex(text: str) -> str:
    text = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?", "", text)
    text = text.replace("{", "").replace("}", "")
    text = text.replace("\\", "")
    return " ".join(text.split())


def audit_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    rel = path.as_posix()
    warnings: list[str] = []

    if "beamerthemeDUNEProfessional.sty" not in text:
        warnings.append(f"{rel}: does not load the shared DUNEProfessional template")

    for match in TITLE_RE.finditer(text):
        title = strip_tex(match.group(1))
        if len(title) > 72:
            warnings.append(f"{rel}: deck title is long ({len(title)} chars): {title}")

    for match in FRAME_TITLE_RE.finditer(text):
        title = strip_tex(match.group(1))
        if len(title) > 68:
            warnings.append(f"{rel}: frame title is long ({len(title)} chars): {title}")

    vspaces = len(VSPACE_RE.findall(text))
    if vspaces > 10:
        warnings.append(f"{rel}: has {vspaces} manual vspace commands; prefer template cards/grids")

    if "\\definecolor" in text:
        warnings.append(f"{rel}: defines local colors; prefer shared semantic color roles")

    return warnings


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path("decks")
    files = sorted(root.glob("*/main.tex"))
    if not files:
        print(f"No decks found under {root}", file=sys.stderr)
        return 1

    warnings: list[str] = []
    for path in files:
        warnings.extend(audit_file(path))

    if warnings:
        print("Presentation audit warnings:")
        for warning in warnings:
            print(f"- {warning}")
        return 1

    print(f"Presentation audit passed for {len(files)} deck(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))


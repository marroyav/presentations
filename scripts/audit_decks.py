#!/usr/bin/env python3
"""Static audit for shared-template presentation decks.

Hard failures identify framework drift. Advisories flag editorial or density
issues that still need human review.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


FRAME_TITLE_RE = re.compile(r"\\begin\{frame\}(?:\[[^\]]*\])?\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}")
TITLE_RE = re.compile(r"\\title(?:\[[^\]]*\])?\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}")
VSPACE_RE = re.compile(r"\\vspace\*?\{")
FRAME_RE = re.compile(
    r"\\begin\{frame\}(?:\[[^\]]*\])?(?:\{(?P<title>[^{}]*)\})?"
    r"(?P<body>.*?)\\end\{frame\}",
    re.DOTALL,
)
COLUMNS_RE = re.compile(
    r"\\begin\{columns\}(?:\[[^\]]*\])?(.*?)\\end\{columns\}", re.DOTALL
)
ITEM_RE = re.compile(r"\\item(?:<[^>]+>)?(?:\[[^\]]*\])?")
LEGACY_HUE_RE = re.compile(
    r"\b(?:DuneOrange|DuneCyan|DuneMint|DuneYellow|DuneRed|DuneViolet)\b"
)
BASE_SIZE_RE = re.compile(r"\\documentclass\[([^\]]*)\]\{beamer\}")
PROJECTOR_SMALL_RE = re.compile(r"\\(?:tiny|scriptsize)\b")


def strip_tex(text: str) -> str:
    text = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?", "", text)
    text = text.replace("{", "").replace("}", "")
    text = text.replace("\\", "")
    return " ".join(text.split())


def strip_comments(text: str) -> str:
    return re.sub(r"(?<!\\)%.*$", "", text, flags=re.MULTILINE)


def audit_file(path: Path) -> tuple[list[str], list[str]]:
    text = strip_comments(path.read_text(encoding="utf-8"))
    rel = path.as_posix()
    errors: list[str] = []
    advisories: list[str] = []

    if "beamerthemeDUNEProfessional.sty" not in text:
        errors.append(f"{rel}: does not load the shared DUNEProfessional template")

    for match in TITLE_RE.finditer(text):
        title = strip_tex(match.group(1))
        if len(title) > 72:
            advisories.append(f"{rel}: deck title is long ({len(title)} chars): {title}")

    for match in FRAME_TITLE_RE.finditer(text):
        title = strip_tex(match.group(1))
        if len(title) > 68:
            advisories.append(f"{rel}: frame title is long ({len(title)} chars): {title}")

    base_size = BASE_SIZE_RE.search(text)
    if base_size and re.search(r"(?:^|,)\s*(?:8|9|10)pt\s*(?:,|$)", base_size.group(1)):
        advisories.append(
            f"{rel}: uses a compact Beamer base size; new decks should use 11pt"
        )

    vspaces = len(VSPACE_RE.findall(text))
    if vspaces > 10:
        advisories.append(
            f"{rel}: has {vspaces} manual vspace commands; prefer template cards/grids"
        )

    if "\\definecolor" in text or "\\colorlet" in text:
        errors.append(f"{rel}: defines local colors; use the shared design tokens")

    if re.search(r"\{(?:HTML|RGB|rgb|cmyk)\}\{", text):
        errors.append(f"{rel}: contains a literal color value outside the shared token file")

    dense_frames = 0
    long_lists = 0
    diagram_without_caption = 0
    projector_small_frames = 0
    four_column_frames = 0
    for frame in FRAME_RE.finditer(text):
        body = frame.group("body")
        visible = strip_tex(body)
        if len(visible) > 1050:
            dense_frames += 1
        if len(ITEM_RE.findall(body)) > 7:
            long_lists += 1
        if (
            ("\\begin{tikzpicture}" in body or "\\includegraphics" in body)
            and "\\DuneDiagramCaption" not in body
        ):
            diagram_without_caption += 1
        if PROJECTOR_SMALL_RE.search(body):
            projector_small_frames += 1
        if any(
            columns.group(1).count("\\begin{column}") >= 4
            and "\\DuneNumberBlock" not in columns.group(1)
            for columns in COLUMNS_RE.finditer(body)
        ):
            four_column_frames += 1

    if dense_frames:
        advisories.append(
            f"{rel}: {dense_frames} frame(s) exceed the source-density guide; review at projector size"
        )
    if long_lists:
        advisories.append(
            f"{rel}: {long_lists} frame(s) have more than seven bullets; split or prioritize"
        )
    if diagram_without_caption:
        advisories.append(
            f"{rel}: {diagram_without_caption} visual frame(s) lack \\DuneDiagramCaption"
        )
    if projector_small_frames:
        advisories.append(
            f"{rel}: {projector_small_frames} frame(s) use \\tiny or \\scriptsize; "
            "split content instead of shrinking projected text"
        )
    if four_column_frames:
        advisories.append(
            f"{rel}: {four_column_frames} frame(s) use four or more columns; "
            "prefer a two-by-two grid or another slide"
        )

    legacy_hues = len(LEGACY_HUE_RE.findall(text))
    if legacy_hues:
        advisories.append(
            f"{rel}: uses {legacy_hues} legacy hue token(s); migrate new edits to shared tokens/components"
        )

    return errors, advisories


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path("decks")
    files = sorted(root.glob("*/main.tex"))
    if not files:
        print(f"No decks found under {root}", file=sys.stderr)
        return 1

    errors: list[str] = []
    advisories: list[str] = []
    for path in files:
        file_errors, file_advisories = audit_file(path)
        errors.extend(file_errors)
        advisories.extend(file_advisories)

    if advisories:
        print("Presentation audit advisories:")
        for advisory in advisories:
            print(f"- {advisory}")

    if errors:
        print("Presentation audit failures:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Presentation audit passed for {len(files)} deck(s); review advisories above.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

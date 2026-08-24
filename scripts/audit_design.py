#!/usr/bin/env python3
"""Check that presentation tokens, theme colors, and contrast pairs agree."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOKENS_PATH = ROOT / "templates/dune-professional/design-tokens.json"
THEME_PATH = ROOT / "templates/dune-professional/beamerthemeDUNEProfessional.sty"
HEX_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")
TEX_COLOR_RE = re.compile(
    r"\\definecolor\{(?P<name>[^}]+)\}\{HTML\}\{(?P<hex>[0-9A-Fa-f]{6})\}"
)


def relative_luminance(hex_color: str) -> float:
    channels = [int(hex_color[index : index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [
        value / 12.92
        if value <= 0.04045
        else ((value + 0.055) / 1.055) ** 2.4
        for value in channels
    ]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast_ratio(first: str, second: str) -> float:
    first_luminance = relative_luminance(first)
    second_luminance = relative_luminance(second)
    light = max(first_luminance, second_luminance)
    dark = min(first_luminance, second_luminance)
    return (light + 0.05) / (dark + 0.05)


def main() -> int:
    tokens = json.loads(TOKENS_PATH.read_text(encoding="utf-8"))
    theme_text = THEME_PATH.read_text(encoding="utf-8")
    theme_colors = {
        match.group("name"): f"#{match.group('hex').upper()}"
        for match in TEX_COLOR_RE.finditer(theme_text)
    }
    errors: list[str] = []

    for role, definition in tokens["colors"].items():
        value = definition["hex"].upper()
        tex_name = definition["tex"]
        if not HEX_RE.fullmatch(value):
            errors.append(f"{role}: invalid hex color {value}")
            continue
        actual = theme_colors.get(tex_name)
        if actual is None:
            errors.append(f"{role}: {tex_name} is missing from the Beamer theme")
        elif actual != value:
            errors.append(
                f"{role}: token is {value}, but {tex_name} in the theme is {actual}"
            )

    results: list[str] = []
    for check in tokens["contrast_checks"]:
        foreground = check["foreground"]
        background = check["background"]
        minimum = float(check["minimum"])
        ratio = contrast_ratio(
            tokens["colors"][foreground]["hex"],
            tokens["colors"][background]["hex"],
        )
        results.append(
            f"{foreground}/{background} {ratio:.2f}:1 (minimum {minimum:.1f}:1)"
        )
        if ratio + 1e-9 < minimum:
            errors.append(
                f"{foreground}/{background}: {ratio:.2f}:1 is below {minimum:.1f}:1"
            )

    if errors:
        print("Design-token audit failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Design tokens match {THEME_PATH.relative_to(ROOT)}.")
    print("Checked contrast pairs:")
    for result in results:
        print(f"- {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

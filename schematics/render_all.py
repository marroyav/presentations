"""Render all standalone concept schematics and their layout manifest."""

from __future__ import annotations

import json
from pathlib import Path

from .concepts.sipm_parallel import build as build_sipm_parallel
from .concepts.supercell_composition import build as build_supercell_composition
from .style import DEFAULT_STYLE


OUTPUT_DIR = Path(__file__).with_name("output")
MANIFEST_PATH = OUTPUT_DIR / "layout-manifest.json"
BUILDERS = (
    ("S09-01-sipm-parallel.svg", build_sipm_parallel),
    ("S14-01-supercell-composition.svg", build_supercell_composition),
)


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    artifacts = []
    for filename, builder in BUILDERS:
        sheet = builder()
        artifacts.append(sheet.save(OUTPUT_DIR / filename))
        print(f"rendered {OUTPUT_DIR / filename}")
    manifest = {
        "schema_version": 1,
        "style": DEFAULT_STYLE.to_dict(),
        "artifacts": artifacts,
    }
    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {MANIFEST_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

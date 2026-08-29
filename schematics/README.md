# Clean standalone schematics

This directory produces diagrams as engineering artifacts first. A deck may
consume the reviewed SVG later, but slide dimensions, colors, and narrative
furniture never control the source drawing.

The first two pilots exercise both supported illustrative languages:

- `S09-01-sipm-parallel.svg`: circuit symbols and electrical connections;
- `S14-01-supercell-composition.svg`: equipment hierarchy and containment.

Both are illustrative source reconstructions, not electrically authoritative
designs. Anything intended to define real hardware belongs in KiCad and must
pass ERC before its exported SVG/PDF is described as verified.

## Visual contract

Every standalone sheet must satisfy all of these rules:

1. exactly one concept and one reading direction;
2. one canonical `1.25` stroke width for symbols, wires, boundaries, and
   junction outlines;
3. one font family (`DejaVu Sans`) and a hard 10-point minimum;
4. orthogonal routes on a 0.25-unit grid;
5. rendered symbol/text bounds registered before routing, with explicit
   clearances and no route through an unrelated object;
6. repetition encoded once with a multiplicity or ellipsis;
7. monochrome hierarchy created by whitespace, fill, and gray—not line weight;
8. native SVG only: no raster images or HTML `foreignObject` content.

The renderer cannot silently repair a crowded drawing. The wrapper reserves
the actual SchemDraw bounding box of each symbol group, marker, block, and text
label before routing begins. The layout registry rejects overlapping regions,
off-grid routes, diagonal segments, unjoined wire crossings or overlaps, and
routes that enter an unrelated object.
The SVG audit then independently checks the committed font, minimum type size,
stroke width, vector-only content, metadata, hash, and recorded layout.

Text is converted to paths with the pinned ZiaMath/ZiaFont stack and its
bundled DejaVu Sans font. The SVG therefore renders identically on Windows,
Linux, and browsers without depending on an installed font. Accessible title,
description, and manifest text remain machine-readable.

## Render and audit

From the repository root:

```sh
python3 -m venv .venv-schematics
.venv-schematics/bin/pip install -r schematics/requirements.txt
make schematic-concepts PYTHON=.venv-schematics/bin/python
```

The audit needs only the Python standard library and can run without
SchemDraw:

```sh
make audit-schematic-concepts
```

Add a concept as a small builder under `schematics/concepts/`, register it in
`render_all.py`, and commit both its source and generated SVG. Add every block,
symbol group, marker, and text label before the first route; the API rejects
late objects so clearance checks cannot depend on call order. Keep coordinates
local to that one concept; reusable policy belongs in `style.json`, `sheet.py`,
and `geometry.py`.

## Renderer boundary

SchemDraw is intentionally limited here to small illustrative circuits and
simple system structures. It gives deterministic vector symbols, anchors, and
central font/stroke control, but it does not understand electrical nets or
perform collision avoidance by itself.

Use the other lanes when the artifact changes category:

- **KiCad** for hardware-authority schematics, ERC, footprints, BOM, netlists,
  and manufacturing handoff;
- **D2 with ELK** for a larger pure block/system topology that benefits from
  automatic orthogonal layout, followed by the same SVG audit and visual
  review;
- **diagrams.net Desktop** when careful GUI composition and reusable custom
  libraries matter more than text diffs; commit both `.drawio` and SVG source;
- **WireViz** only for cable assemblies, connectors, conductors, and pinouts.

No renderer removes the final visual-review gate.

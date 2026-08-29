# Electrical schematic framework

The presentation repository supports two deliberately separate schematic
products. They may share symbols and provenance, but they must never share an
unqualified claim of electrical authority.

## 1. Presentation system diagrams

Use TikZ and CircuitikZ for system, test-stand, and readout diagrams that combine
physical boundaries, instruments, signal flow, repeated channels, and selected
circuit detail.

The visual benchmark is slides 12--14 of
[HD & VD Mezzanine QA/QC](https://indico.fnal.gov/event/74170/contributions/342404/attachments/198858/276941/HD_VD_MEZZANINE_QA_QC.pdf).
Those slides contain flattened grayscale artwork; this framework recreates the
drawing language as editable vector source instead of copying its pixels.

Style contract:

- white canvas with black and secondary-gray artwork;
- 0.6--0.8 pt orthogonal wires with small arrowheads;
- rounded outlines for physical equipment and simple rectangular board/card
  boundaries;
- left-to-right signal flow, with control and data returns routed around the
  outside;
- ANSI circuit symbols, direct values and identifiers, and explicit junctions;
- compact sans-serif equipment labels and serif italic electrical variables;
- stacked outlines, channel ranges, ellipses, and multiplication markers for
  repeated circuitry;
- no colored functional cards, decorative badges, or prose panels inside the
  engineering artwork.

These diagrams are reviewable technical communication. Unless backed by an EDA
source, they must be labeled `vector-redraw-reference` with connectivity
`transcribed-not-verified`.

## 2. Hardware-authority schematics

Use KiCad for designs intended to define or validate real hardware. The native
project owns symbols, pins, nets, hierarchy, values, footprints, and electrical
rules. Presentation files consume revision-stamped PDF or SVG exports; they do
not redraw or recolor the verified sheet.

Required export contract:

```text
KiCad source at an immutable revision
  -> ERC report and canonical netlist
  -> optional PCB DRC with schematic parity
  -> black-and-white PDF and SVG
  -> provenance manifest with hashes
  -> presentation inclusion
```

The manifest records the source repository and revision, source path, tool
version, export command, selected sheet, ERC/DRC disposition, reviewer, and
artifact digest. Only this lane may use `erc-clean` or `human-reviewed` without
the vector-redraw qualifier.

The audit admits those authority statuses only for `eda-export` PDF or SVG
artifacts. Each such artifact must record `source_repository`,
`source_revision`, `source_path`, `tool_version`, `export_command`, and SHA-256
digests for both the ERC report and canonical netlist; the verification block
must name a reviewer and use the normalized ERC disposition `clean` or
`dispositioned`. An `erc-clean` claim specifically requires `clean`.

## AI-assisted authoring boundary

An AI assistant may:

1. extract components, values, labels, nets, interfaces, boundaries, repeated
   structures, and unresolved evidence into a structured draft;
2. generate or revise TikZ/CircuitikZ presentation diagrams;
3. generate a proposed KiCad design for review;
4. run deterministic builds, hash checks, visual regression, netlist comparison,
   and ERC/DRC tools;
5. preserve uncertainty instead of guessing a connection or value.

An AI-generated drawing is not electrically verified merely because it compiles
or looks plausible. Promotion to hardware authority requires an EDA-native
source, clean or explicitly dispositioned ERC, and a named human review.

## Repository integration

```text
decks/<deck>/
  diagrams/*.tikz.tex       editable presentation-system drawings
  schematics.json           source, status, and content hashes
  main.tex                  presentation composition only

hardware source repository/
  *.kicad_sch               authoritative design
  build/*.erc.json          machine-readable verification
  build/*.pdf, *.svg        revision-stamped presentation exports
```

`make schematics` validates status vocabulary, source containment, vector-source
classification, absence of raster includes in redraws, and content hashes.
`make check` combines that gate with the design and presentation audits.

## Development sequence

1. Complete the LIDINE redraw pilot as three coherent monochrome system sheets.
2. Extract reusable enclosure, repeated-channel, instrument, connector,
   operator, and storage primitives into a small diagram component library.
3. Define a versioned semantic input schema so an assistant edits topology and
   annotations separately from coordinates and slide furniture.
4. Add normalized vector-render comparisons and projector-size contact sheets
   to CI.
5. Pilot one real KiCad design and gate its exports with ERC, a netlist digest,
   and human review before allowing an authoritative caption.

Acceptance is based on topology traceability, legibility, deterministic vector
output, and honest verification status---not on visual similarity alone.

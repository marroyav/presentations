# VD detector protection — white design version

Design revision: 10 November 2026. The engineering content comes from the
28 October I&I deck, including the native TikZ conversion made on 10 November.
This version retains twenty main topics and fifteen backup slides.

## Audience and outcome

For the I&I workshop and the VD subsystem teams. Readers need the SC/DPS
responsibilities, the proposed protection paths, and the remaining hardware and
interface work. The intended outcome is to agree responsibilities, trace each
interlock to its input and protected load, and prepare the hardware review.

The proposed assignments and protection rules remain proposals. This design
revision adds no hardware test, installation finding or engineering approval.

## Design

This version follows the shared framework, diagram and writing guides:

- `\DuneUseWhite`: white slides, dark text and a simple page number.
- Titles state the point; the existing Detector divider keeps its section title.
- Native TikZ diagrams use dark outlines, explicit labels and unfilled nodes.
- Captions explain arrow direction, dashed paths and unresolved interfaces.
- Normal prose uses the 11-point baseline. Diagram labels and inventory lists
  use `\small`; captions use `\footnotesize`.
- Reference panel drawings and operator screenshots retain their source colours.

The design rules are in [the framework guide](../../docs/framework-guide.md),
[the diagram guide](../../docs/diagram-guide.md) and
[the theme reference](../../templates/dune-professional/README.md).

## Files and build

From the repository root:

```sh
make decks/dps_integration_status_white_nov2026/main.pdf
```

Edit slide text in `main.tex` and `backup-slides.tex`. The five main system
diagrams live in `diagrams/*.tikz.tex`; their common appearance is defined in
`diagrams/styles.tex`. The site map and detailed DAPHNE reference also use TikZ.
All diagrams compile with the deck.

`sources.json` and `sources-and-notes.txt` retain the source identities and
engineering qualifications. `verification-latest.txt` points to the build,
content and visual checks. `review/` contains the final slide previews.

The [original dark deck](../dps_integration_status_oct2026/main.pdf) remains
available for comparison. Its source and PDF are unchanged by this revision.

## Evidence kept in scope

The working totals remain 336 microTCA crates across TDE and DAQ/timing combined,
34 PDS LV feeds, and 80 PoF boxes with 400 voltage/temperature readings. Proposed,
documented and unresolved interfaces retain their original status. The detailed
device hierarchy remains a working inventory, rather than an IP register or a
completed purchasing bill of materials.

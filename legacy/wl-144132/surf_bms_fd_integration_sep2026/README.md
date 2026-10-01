# SURF–DUNE facility interface

[Current presentation — five slides](main.pdf) · [LaTeX source](main.tex) · [Speaker notes](speaker_notes.md)

The deck covers the proposed connection, alarm ownership, facility conditions,
protocol candidates, and integration work. The first two slides retain the
three-zone architecture and branching alarm flow from the earlier diagrams,
with shorter labels and editable TikZ geometry.

## Editing and build

```sh
make
```

`main.tex` contains the slides. `deck-style.tex` controls typography and DUNE
colors: 18 pt titles, 10.5 pt body text, and 9.2 pt diagram node labels.
The drawings are in `figures/architecture.tex` and `figures/alarm-flow.tex`.
`make rebuild` forces a fresh PDF; `make latexmk` uses a local XeLaTeX installation.
Included fonts and SyncTeX support direct text and layout editing.

## Companion documents

[Two-page note and one-page overview](../../dune-docs-analysis/reports/surf_bms_integration/publication/concise/README.md)

## Preserved editions

- [Original ten-slide deck](archive/ten-slide/main.pdf), with its complete source and assets.
- [Earlier five-slide deck with larger type](concise/main.pdf), unchanged.

The original vector PDFs remain in `figures/`; their SVG sources remain in the
SURF BMS report package. The current deck uses the native TikZ adaptations.

The material describes a proposal, not an installed interface or a validated
protection design. Hardware placement and procurement are outside its scope.

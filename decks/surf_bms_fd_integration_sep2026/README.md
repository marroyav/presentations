# SURF–DUNE facility interface

[Presentation — title and five content slides](main.pdf) · [LaTeX source](main.tex) · [Speaker notes](speaker_notes.md)

## Audience and purpose

For SURF/source-system owners and the DUNE Slow Controls, DAQ, DPS and operations
teams. The deck supports a short discussion of which facility signals DUNE
receives, who responds, and how the interface behaves during loss and recovery.
It describes a proposal, not an installed or validated protection design.

## Build

From the repository root:

```sh
make decks/surf_bms_fd_integration_sep2026/main.pdf
make audit
```

The root build discovers this deck automatically. For an offline rebuild using
the local Tectonic cache:

```sh
make decks/surf_bms_fd_integration_sep2026/main.pdf \
  TECTONIC_FLAGS='-C --keep-logs --keep-intermediates --synctex'
```

## Editing

`main.tex` contains the title page and five content slides. Its `\DeckDate`
command sets the date on the title page and content-slide footers.
`deck-style.tex` retains the light layout and smaller type: 18 pt slide headings
and 10.5 pt body text, with 9.2 pt diagram labels. The title page uses 22 pt type.
All visible text uses bundled JetBrains Mono, including bold and italic styles;
its SIL Open Font License is included in `fonts/JetBrainsMono-OFL.txt`.
The shared framework supplies the audited `DuneEditorial*` palette.

The earlier three-zone architecture and branching alarm-flow layouts remain
editable in `figures/architecture.tex` and `figures/alarm-flow.tex`. The native
vector drawings do not depend on the old presentation repository.

## Companion material and preservation

- [Two-page interface note](../../../wl-144132/dune-docs-analysis/reports/surf_bms_integration/publication/concise/interface_note.pdf)
- [One-page overview](../../../wl-144132/dune-docs-analysis/reports/surf_bms_integration/publication/concise/overview.pdf)

This is the maintained deck in the `presentations` repository. The earlier
copies under `wl-144132/daphne_presentations/surf_bms_fd_integration_sep2026/`
remain unchanged. All files needed to build this deck are in this repository;
the companion documents are optional links to the local document collection.
The preceding [sans-serif PDF](previous/sans-serif.pdf) is also preserved here.

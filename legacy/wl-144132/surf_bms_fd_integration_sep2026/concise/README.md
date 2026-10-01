# SURF–DUNE facility interface

[Five-slide presentation](main.pdf) · [LaTeX source](main.tex) · [Speaker notes](speaker_notes.md)

Companion reading: [two-page note and one-page overview](../../../dune-docs-analysis/reports/surf_bms_integration/publication/concise/README.md).

The deck presents the proposed interface, alarm ownership, facility conditions,
protocol candidates and the agreements needed to define the integration. It is
intended for a short technical discussion. Proposed functions and protocol
candidates do not establish a deployed SURF interface or a validated protection
design.

All diagram elements are native TikZ in `main.tex`. Text, coordinates and arrow
styles can be edited directly. The DUNE blue and orange accents are defined near
the beginning of the file; dark text carries the content. Liberation Sans fonts
are included in `fonts/`.

Build with the cached Tectonic bundle:

```sh
make
```

Or use a local XeLaTeX installation:

```sh
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
```

The original ten-slide presentation and its assets remain in the parent
directory.

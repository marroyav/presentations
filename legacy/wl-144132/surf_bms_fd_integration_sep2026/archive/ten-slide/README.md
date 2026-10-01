# SURF facility status and DUNE response

For the shorter discussion deck, see the [five-slide presentation](concise/main.pdf)
and its [editable LaTeX source](concise/main.tex). The presentation below is preserved.

This directory contains a ten-slide DUNE Far Detector architecture deck about
the interface between SURF facility information and DUNE controls and
protection.

The deck uses a self-contained, light 16:9 Beamer design. Its colors and
diagram grammar follow the DUNE FD palette B editorial system. Liberation Sans
is included locally so the presentation has stable typography across build
hosts.

## Build

The default build uses the locally available Tectonic executable and its
cached TeX bundle:

```sh
make
```

The equivalent direct command is:

```sh
/home/neutrino/.local/bin/tectonic -C --keep-logs main.tex
```

A host with XeLaTeX and `latexmk` can instead use:

```sh
make latexmk
```

The generated presentation is `main.pdf`.

## Included source assets

The three vector diagrams in `figures/` are copied from the SURF BMS
integration package in `dune-docs-analysis/reports/surf_bms_integration/`:

- `01_bms_dcs_dps_boundary.pdf`
- `02_alarm_authority_hierarchy.pdf`
- `03_failure_response_map.pdf`

Their canonical editable sources are the corresponding SVG files in that
package. Changes to the diagrams belong in the diagram generator and are then
copied into this deck.

The DUNE color logo comes from `dune_dark_template_lab/logos/`. The four
Liberation Sans font files come from the Liberation 2 distribution installed
on the build host.

## Content boundary

The presentation describes functions, ownership, information flow, failure
behavior, and architecture acceptance. Detailed implementation planning stays
in the accompanying engineering material.

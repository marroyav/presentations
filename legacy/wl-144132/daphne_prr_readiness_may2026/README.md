# DAPHNE PRR Readiness Draft

Draft presentation for the DUNE/DAPHNE Production Readiness Review.

## Build

```sh
cd ~/repo/Latex/presentations/daphne_prr_readiness_may2026
latexmk -pdf main.tex
```

If `latexmk` is unavailable:

```sh
pdflatex main.tex
pdflatex main.tex
```

## Source Scope

This deck intentionally stays high level. It uses detailed local work as backup
evidence rather than putting the full technical argument into every slide.

Primary local inputs:

- `~/repo/projects/`
- `~/repo/daphne-firmware/docs/`
- `~/repo/daphne_mezz_xc_sim/docs/`
- `~/repo/Latex/presentations/daphne_deadtime_apr2026/`
- `~/repo/Latex/presentations/daq_daphne_pds_integration_may2026/`
- `~/repo/fddetdataformats`
- `~/repo/rawdatautils`
- `~/repo/daphnemodules`
- `~/repo/waffles`

Main evidence still needed before a final PRR packet:

- controlled readiness matrix with owners and evidence links
- before/after mezzanine noise data for the new filtering change
- accepted dead-time requirement and operating model
- reviewed DAQ descriptor schema and package tests
- named owner group for peak descriptor to trigger primitive validation

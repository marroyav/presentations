# DAPHNE-SC Development, June 2026

Dark-template Beamer deck explaining the proposed `daphne-sc` migration from a
Linux-only control implementation to a Linux + RPU split.

The deck uses the shared updated dark template in `../dune_dark_template_lab/`
and local logo assets in `logos/`.

Build from this directory with the user-local Tectonic install:

```sh
~/.local/bin/tectonic main.tex
```

Or, on a machine with a normal TeX Live install:

```sh
xelatex -interaction=nonstopmode -halt-on-error main.tex
xelatex -interaction=nonstopmode -halt-on-error main.tex
```

Source basis:

- `../../daphne_slow_controls_plan/main.tex`
- current dark Beamer template in `../dune_dark_template_lab/`

Main message:

- Linux remains the integration surface for protobuf, OPC-UA, Ignition, DAQ
  handoff, topology, history, and audit logging.
- The RPU becomes the deterministic board-local supervisor for permits,
  watchdogs, latched faults, and safe-state sequencing.
- DPS PLC or supply-side inhibit remains the hard detector-protection path for
  actions that must survive Linux, ZMQ, OPC-UA, Ignition, or network failure.

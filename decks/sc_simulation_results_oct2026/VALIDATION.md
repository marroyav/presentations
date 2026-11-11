# Presentation validation — 6 October 2026

The deck has been synthesized from 24 to 8 slides around the latest local
VD/HD measurements and queue projections. Historical results are context only.

- Monitoring metrics and queue times checked against saved `sc_emu` JSON reports.
- Vector plot regenerated from the simulation repository's curve CSV, with
  source SHA-256 recorded in `evidence/figure-provenance.json`.
- Command examples point to `sc_emu`; raw simulation source/results stay there.
- PDF rebuilt with Tectonic; all 8 slides visually reviewed. Final TeX log
  has no overfull or underfull boxes.
- Repository presentation audit and `git diff --check` passed.

[Simulation validation](../../../sc_emu/VALIDATION.md) documents the actual runs,
61 recovered tests and the repository relocation. Presentation build/layout
checks are independent of simulation execution.

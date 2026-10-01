# DAPHNE Conference Deck - May 2026

Concise DAPHNE presentation for Lead, South Dakota, Wednesday, May 20, 2026.

## Current Structure

1. What is being presented and why it matters.
2. Talk structure: context, three claims, and production gates.
3. DAPHNE system handoff from mezzanines to DAQ.
4. Evidence claim 1: SNR, pulse shape, and dynamic range.
5. Evidence claim 2: new DAPHNE noise closure.
6. Integration claim 3: firmware data product, DAQ baseline, and `pds-run`.
7. PRR closure matrix and final takeaway.

## Source Material

- Desktop source deck: `/Users/marroyav/Desktop/collab_meeting_may_2026.pptx`
  - slide 1: mezzanine scope and board images
  - slide 2: SNR plots and cold-box summary
  - slide 3: pulse-shape compensation and undershoot summary
  - slide 4: dynamic-range plots and saturation summary
  - slide 5: new DAPHNE noise and filter plots
- Existing LaTeX assets:
  - runtime data-flow diagram now rebuilt as native TikZ in `main.tex`
  - narrative adapted from `../daq_daphne_pds_integration_may2026/main.tex`
  - PRR framing adapted from `../daphne_prr_readiness_may2026/main.tex`

The small `dune_dark_template_lab/` directory is vendored so the GitHub copy can
compile from the repository root.

## Build

```sh
latexmk -pdf -interaction=nonstopmode main.tex
```

Render check:

```sh
pdftoppm -png -r 120 main.pdf /tmp/daphne_conference_review/page
```

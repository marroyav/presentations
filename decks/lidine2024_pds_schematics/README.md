# LIDINE 2024 DUNE PDS schematics

Deck slug: `lidine2024_pds_schematics`

This is a deliberately narrow import pilot: every rendered slide contains one
electrical schematic extracted from the published source presentation. It tests
the framework's readability, attribution, artifact freshness, and verification
language for image-only engineering material.

## Audience

- Primary audience: DUNE PDS electronics engineers and presentation-framework
  maintainers.
- What they already know: The source presentation describes the Phase I DUNE
  Photon Detection System and its SiPM readout.
- What they need from this talk: A projector-readable gallery of the source's
  strict circuit schematics, without surrounding detector photos, plots, or
  narrative slides.

## Outcome

- One-sentence takeaway: The framework can present externally sourced circuit
  images clearly while preserving their origin and refusing to imply electrical
  verification that the images cannot support.
- Decision or action requested: Review whether the three extracts remain
  legible at projector size and whether an editable EDA reconstruction is worth
  commissioning.
- Owner and completion condition: The pilot is complete when the deck builds,
  all asset hashes pass, each source page is recorded, and visual inspection
  confirms that no label is clipped.

## Scope

- In scope: The strict circuit schematics embedded on source slides 9, 14, and
  18.
- Explicitly out of scope: Mechanical drawings, detector layouts, photographs,
  plots, the generic PoF/SoF architecture on slide 19, and the repeated
  electro-optical block diagram on slides 20--21.
- Electrical status: Image-derived reference only. There is no native netlist,
  symbol library, footprint mapping, ERC report, or component verification.

## Evidence and provenance

- Source contribution: [DUNE Photon Detection System](https://indico.cern.ch/event/1390649/contributions/6061526/),
  Gabriel Botogoske (INFN), on behalf of the DUNE Collaboration, LIDINE 2024,
  27 August 2024.
- Source PDF: [LIDINE2024-dune pds.pdf](https://indico.cern.ch/event/1390649/contributions/6061526/attachments/2916523/5118380/LIDINE2024-dune%20pds.pdf).
- Extraction: The original embedded JPEG objects were copied losslessly; the
  files were not screenshot, cropped, recompressed, or AI-redrawn.
- Machine-readable record: `schematics.json` records the source PDF digest,
  original page/object identifiers, dimensions, classification, and asset
  digests.
- Rights note: The source page does not state an asset license. These attributed
  extracts are retained for this evaluation pilot and should not be treated as
  unrestricted stock artwork.

## Build and verification

From the repository root:

```sh
make schematics
make decks/lidine2024_pds_schematics/main.pdf
```

Run the full repository checks with:

```sh
make check
```

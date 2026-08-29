# LIDINE 2024 DUNE PDS schematic redraws

Deck slug: `lidine2024_pds_schematics`

This pilot reconstructs the published circuit figures as three coherent,
repo-native vector system sheets. No source pixels appear in the final
presentation. CircuitikZ provides conventional electrical symbols; TikZ
provides physical boundaries, repeated channels, connector allocations, signal
lanes, and uncertainty annotations.

## Audience

- Primary audience: DUNE PDS electronics engineers and presentation-framework
  maintainers.
- What they already know: The source presentation describes the Phase I DUNE
  Photon Detection System and its SiPM readout.
- What they need from this talk: Projector-readable circuit drawings that are
  visually consistent, technically conservative, and maintainable as source.

## Outcome

- One-sentence takeaway: Low-resolution reference figures can become polished,
  searchable vector diagrams without inventing values or implying EDA sign-off.
- Decision or action requested: Review the reconstructed topology and resolve
  the explicitly marked uncertainties before considering a KiCad implementation.
- Owner and completion condition: The pilot is complete when all vector sources
  build, asset hashes pass, every topology is visually inspected, and no raster
  schematic remains in the deck.

## Scope

- In scope: The SiPM equivalent circuit on source slide 9, the SuperCell cold
  signal path and DAPHNE interconnect on slide 14, and the 20-SiPM passive
  ganging/differential output network on slide 18.
- Explicitly out of scope: Mechanical drawings, detector layouts, photographs,
  plots, the generic PoF/SoF architecture on slide 19, and the repeated
  electro-optical block diagram on slides 20--21.
- Electrical status: Vector redraw from published references. Connectivity is
  transcribed and reviewed for internal consistency, but there is no native
  netlist, symbol library, footprint mapping, ERC report, or hardware-owner
  approval.

## Redraw policy

- Use only topology, labels, values, and interface assignments supported by the
  published references.
- Omit unspecified component values, tolerances, ratings, models, and grounding
  connections rather than guessing.
- Keep ambiguous soft-bond endpoints explicitly unresolved.
- Show repeated channels through multiplicity and a representative channel
  instead of reducing legibility with copied detail.
- Use monochrome engineering line art on white: thin orthogonal wiring, compact
  direct labels, nested equipment boundaries, and left-to-right signal flow.
- Keep presentation color in the slide furniture, outside the engineering
  artwork.
- Follow the authority boundary in the
  [electrical schematic framework](../../docs/schematic-framework.md): these
  system drawings do not replace KiCad source and ERC for real hardware.

## Evidence and provenance

- Source contribution: [DUNE Photon Detection System](https://indico.cern.ch/event/1390649/contributions/6061526/),
  Gabriel Botogoske (INFN), on behalf of the DUNE Collaboration, LIDINE 2024,
  27 August 2024.
- Source PDF: [LIDINE2024-dune pds.pdf](https://indico.cern.ch/event/1390649/contributions/6061526/attachments/2916523/5118380/LIDINE2024-dune%20pds.pdf).
- Visual benchmark: slides 12--14 of
  [HD & VD Mezzanine QA/QC](https://indico.fnal.gov/event/74170/contributions/342404/attachments/198858/276941/HD_VD_MEZZANINE_QA_QC.pdf).
  The benchmark contains flattened grayscale diagrams; only its drafting
  language is adopted here, with new vector artwork built from the LIDINE
  topology.
- SiPM reference: A. Falcone et al., “Cryogenic SiPM arrays for the DUNE photon
  detection system,” NIM A 985 (2021) 164648,
  [doi:10.1016/j.nima.2020.164648](https://doi.org/10.1016/j.nima.2020.164648).
- Passive-ganging cross-check: DUNE Collaboration,
  [FD2-VD Technical Design Report](https://arxiv.org/abs/2312.03130),
  Section 6.5.2 and Figure 6.13.
- Machine-readable record: `schematics.json` records source pages, source PDF
  digest, redraw classification, and hashes of every vector source.
- Rights note: The references remain attributed. The vector code is an original
  reconstruction for this engineering-review pilot, not a claim of ownership
  over the underlying circuit designs.

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

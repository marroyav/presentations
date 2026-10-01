# DUNE presentations

Shared presentation framework for DUNE SC/DPS, DAPHNE, and related technical
decks. Beamer remains the PDF shell, while the repository now centralizes:

- audience/outcome briefs and a maintained starter deck;
- layout-first paper, sky, and coral surfaces with red reserved for hard danger;
- an 11-point Beamer baseline and projector-size density checks;
- section, statement, mosaic, comparison, pipeline, table, and decision layouts;
- tokenized Graphviz diagrams and shared TikZ styles;
- source audits for theme drift, density, long lists, and unexplained visuals.

Read [the framework guide](docs/framework-guide.md) for the research,
tool choices, authoring rules, and migration sequence. The
[theme reference](templates/dune-professional/README.md) documents the component
API, layout grammar, and color system. The
[electrical schematic framework](docs/schematic-framework.md) separates
standalone explanatory drawings from ERC-backed hardware-authority exports.

## Standalone schematics

Schematics are now developed as independent SVG artifacts before any slide is
considered. The first two one-concept pilots live in [`schematics/`](schematics/):

- a SiPM parallel-microcell equivalent circuit;
- a SuperCell composition diagram.

They share one outlined font, one `1.25` stroke width, a fixed orthogonal grid,
actual-geometry spacing reservations, and a vector-only audit. Render them in
an isolated environment with:

```sh
python3 -m venv .venv-schematics
.venv-schematics/bin/pip install -r schematics/requirements.txt
make schematic-concepts PYTHON=.venv-schematics/bin/python
```

Run the dependency-free audit of the committed outputs with:

```sh
make audit-schematic-concepts
```

## Build

```sh
make
```

The repository currently builds:

- `decks/scdps_repo_plan_aug2026/main.pdf`
- `decks/scdps_git_management_aug2026/main.pdf`
- `decks/scdps_software_ownership_aug2026/main.pdf`
- `decks/daphne_pab_qualification_aug2026/main.pdf`
- `decks/pds_selftrigger_deadtime_aug2026/main.pdf`
- `decks/detector_wide_interaction_matrix_sep2026/main.pdf`
- `decks/lidine2024_pds_schematics/main.pdf`
- [SURF–DUNE facility interface](decks/surf_bms_fd_integration_sep2026/main.pdf)
- [PDS activity and DAPHNE load](decks/pds_activity_to_daphne_load_sep2026/main.pdf)
- [PDS data acquisition and local trigger conditions — 17 September 2026](decks/pds_trigger_story_sep2026/main.pdf)
- [Self-trigger, with full-stream fidelity — 15 September 2026](decks/grouped32_simulation_sep2026/main.pdf)
- [FD detector-protection boundaries](decks/fd_dps_boundaries_sep2026/main.pdf)

The [SURF–DUNE deck](decks/surf_bms_fd_integration_sep2026/README.md) includes a
dated title page followed by five content slides on facility monitoring, alarm
ownership, detector protection, protocols, and integration. It uses JetBrains
Mono throughout, with the light layout and editable architecture and alarm-flow
diagrams retained.

The detector-interlock deck also includes a
[plain-language collaboration guide](decks/detector_wide_interaction_matrix_sep2026/human/README.md)
and a [searchable matrix by subsystem](decks/detector_wide_interaction_matrix_sep2026/human/index.html).
These cover all 40 rows of the reviewed DPS draft, including open decisions.

## Audit

```sh
make audit
```

The audit fails on theme or color drift and reports editorial advisories that
need human judgment. Run the complete framework and deck validation with:

```sh
make check
```

Original vector redraws, image-derived references, and EDA-exported electrical
schematics carry a `schematics.json` provenance manifest. Validate the recorded
source classification and asset hashes independently with:

```sh
make schematics
```

## Create a deck

```sh
make new-deck \
  SLUG=my_topic_sep2026 \
  TITLE="My topic" \
  AUTHOR="Your name"
```

Complete the generated audience/outcome brief before drafting slides. Run
`make diagrams` after changing any `diagrams/*.dot.in` source.

## Framework starter

`make starter` builds `examples/framework_starter/main.pdf`, which demonstrates
the recommended narrative structure, varied slide languages, and Graphviz
pipeline.

## Project terminology

See the [FD protection and facility-interface glossary](../dune-docs-analysis/reports/project-glossary.md)
in the sibling `dune-docs-analysis` workspace for organization/system distinctions,
source links and unresolved ownership questions. This local link requires that workspace.

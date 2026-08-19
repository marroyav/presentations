# DUNE presentations

Shared presentation workspace for DUNE SC/DPS, DAPHNE, and related technical
decks.

The first reusable template is `templates/dune-professional`. It keeps Beamer
as the PDF shell but centralizes the layout rules:

- fixed title and frame-title safe areas;
- auto-shrinking title/subtitle boxes;
- named DUNE color roles;
- reusable cards, pills, and diagram node styles;
- a lightweight source audit for title length and manual layout drift.

## Build

```sh
make
```

The repository currently builds:

- `decks/scdps_repo_plan_aug2026/main.pdf`

## Audit

```sh
make audit
```

The audit is intentionally conservative. It flags decks that do not load the
shared template and calls out long titles or heavy manual spacing that should
usually be handled through the template macros.

## Add a Deck

Create a new directory under `decks/`, copy the structure of
`decks/scdps_repo_plan_aug2026/main.tex`, and keep local styling in the shared
template unless a deck has a documented special reason to diverge.


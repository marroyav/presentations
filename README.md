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
API, layout grammar, and color system.

## Build

```sh
make
```

The repository currently builds:

- `decks/scdps_repo_plan_aug2026/main.pdf`
- `decks/scdps_git_management_aug2026/main.pdf`
- `decks/scdps_software_ownership_aug2026/main.pdf`

## Audit

```sh
make audit
```

The audit fails on theme or color drift and reports editorial advisories that
need human judgment. Run the complete framework and deck validation with:

```sh
make check
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

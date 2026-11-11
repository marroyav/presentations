# Presentation title

Deck slug: `presentation_slug`

Complete this brief before adding slides. It is the deck's editorial contract.

## Audience

- Primary audience:
- What they already know:
- What they need from this talk:

## Outcome

- One-sentence takeaway:
- Decision or action requested:
- Owner and completion condition:

## Scope

- In scope:
- Explicitly out of scope:

## Evidence

- Authoritative sources:
- Measurements or test results:
- Important uncertainty:

## Build

From the repository root:

```sh
make
```

Graphviz sources live in `diagrams/*.dot.in`. Use only tokens from
`templates/dune-professional/design-tokens.json`; `make diagrams` renders them
to vector PDF.

## Visual guidance

This starter uses `\DuneUseWhite`: white slides, dark labels, and minimal
furniture. The example plot uses constructed values and makes no measurement
claim. Replace it with evidence from the owning analysis.

Read the [plotting guide](../../docs/plotting-guide.md) and
[diagram guide](../../docs/diagram-guide.md) before adding figures.

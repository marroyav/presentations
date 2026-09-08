# DUNE Professional presentation theme

This theme provides a layout-first visual language for DUNE/Fermilab technical
decks. The dark canvas stays consistent, while slide composition alternates
between editorial claims, filled mosaics, diagrams, comparisons, pipelines,
tables, section breaks, and decision closes.

## Color system

| Visual layer | Use | Token / block name |
|---|---|---|
| Paper | Sources, definitions, reference material, neutral proof | `DunePaper` / `paper` |
| Sky | Interfaces, flows, system context, supporting structure | `DuneSky` / `sky` |
| Coral | Ownership, the active path, decisions, requested action | `DuneCoral` / `coral` |
| Ink | Supporting dark block when a light fill would compete | `ink` |
| Red | A genuine hard danger or prohibited condition only | `danger` |

The canonical values are in `design-tokens.json`. The build audit confirms that
the JSON values match the Beamer theme and that every declared text/background
pair meets its contrast target.

These are compositional layers, not a status taxonomy. A normal slide uses one
dominant light fill; a comparison or diagram may use two or three because the
layout makes their relationship explicit. Never assign a new hue to every
category. Use full blocks deliberately instead of scattering colored pills.

For example:

```tex
\DuneColorBlock{sky}{SYSTEM CONTEXT}{One shared interface}
  {The producer and every consumer use the same reviewed schema.}

\DuneColorBlock{coral}{THE ASK}{Approve the canonical contract}
  {Name the owner and the completion condition.}
```

## Components

The migrated SURF interface deck retains its reviewed light layout through the
opt-in `DuneEditorial*` tokens in the same registry. They preserve its DUNE
blue/orange accents and dark text. Its layout overrides do not change the
default theme or other decks; meaningful diagram edges use dark ink, while the
pale rules and blue accent are decorative.

- `\DuneSectionPage{eyebrow}{title}{subtitle}`: full-canvas rhythm break.
- `\DuneBigStatement{eyebrow}{claim}{support}`: editorial opening or close.
- `\DuneColorBlock{style}{kicker}{title}{body}`: full visual block.
- `\DuneFixedColorBlock{style}{height}{kicker}{title}{body}`: aligned mosaic block.
- `\DuneNumberBlock` and `\DuneCompactNumberBlock`: process or argument stages.
- `\DuneCompactColorBlock`: shorter band or stacked-lane block.
- `\DuneDiagramCaption{...}`: visible explanation of a diagram's meaning.
- `\DuneSourceLine{descriptive label}{URL}`: compact, descriptive source link.
- `\DuneTakeaway`, `\DuneCallout`, `\DuneCard`, and `\DuneFixedCard`: compatibility
  components; do not build an entire new deck from one of these shapes.

The maintained starter demonstrates the intended variation. Repeating a layout
is fine when the audience should compare slides; repetition should be a choice,
not the framework default.

## Typography

The theme follows Fermilab's in-house guidance by preferring Helvetica Neue,
Helvetica, and compatible substitutes. By default, JetBrains Mono is used for code.
The fallback chain keeps builds portable when licensed fonts are unavailable.

A deck that bundles its own fonts can define `\DuneFontSetup` before loading
the theme. This optional hook replaces only font initialization; the normal
fallback chain is unchanged for every deck without the hook.

New decks use an `11pt` Beamer base. Normal prose stays at that size; card copy
may step down once to `\small`, and supporting table/caption text may use
`\footnotesize`. Do not put meaningful slide content in `\scriptsize` or
`\tiny`. If text does not fit:

1. Shorten it.
2. Replace four columns with a two-by-two grid.
3. Split the slide.
4. Move reference detail to backup slides or a companion document.

The audit flags compact base sizes, direct projector-small text, and grids with
four or more columns.

## Diagrams

Use TikZ for a small explanatory composition whose layout is part of the
argument. Use a tokenized `*.dot.in` Graphviz source for dependency graphs,
system topology, or any diagram where automatic layout is valuable.

```dot
digraph example {
  graph [bgcolor="{{background}}"];
  source [fillcolor="{{paper}}", fontcolor="{{on-accent}}"];
  interface [fillcolor="{{sky}}", fontcolor="{{on-accent}}"];
  owner [fillcolor="{{coral}}", fontcolor="{{on-accent}}"];
  source -> interface -> owner [color="{{sky}}"];
}
```

Run `make diagrams` to generate vector PDFs. Keep the source and generated PDF
together so a deck remains buildable and reviewable.

## Compatibility names

`DuneOrange`, `DuneCyan`, `DuneMint`, `DuneYellow`, `DuneRed`, and
`DuneViolet` remain available for older decks. Do not use them in new material;
they describe hues rather than meaning.

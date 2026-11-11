# DUNE Professional presentation theme

New decks use a white canvas, dark text, and restrained accents. The maintained
starter enables this profile after loading the shared theme:

```tex
\DuneUseWhite
```

The profile removes decorative title bands, background marks, and large logos.
It keeps a simple title, content area, and page number. Existing decks retain
the dark profile unless they call this command. Check deck-local overrides and
embedded figures before switching an existing deck.

## Color system

Use `DuneText` for primary text and `DuneTextMuted` for supporting text and
connections. In the white profile these map to the checked `editorial-text` and
`editorial-muted` tokens on `editorial-canvas`. Keep color for a useful distinction,
and pair it with a label, marker, or line pattern.

`design-tokens.json` retains the canonical dark values and the white editorial
palette. The white profile maps theme roles at runtime; it does not rewrite the
registry or existing external figures. The audit checks the declared palette
pairs. Inspect the final PDF to check composition and any mixed colors.

Paper, sky, coral, ink, and danger block components remain available for older
layouts. Use a fill only when it helps show grouping or meaning. A white deck
does not need a colored block around every statement.

## Components

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

The maintained starter demonstrates a figure-led white deck. Reuse layouts
when the audience needs to compare evidence.

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
  graph [bgcolor="{{editorial-canvas}}"];
  node [shape=box, color="{{editorial-muted}}",
        fontcolor="{{editorial-text}}"];
  edge [color="{{editorial-muted}}", fontcolor="{{editorial-text}}"];
  source -> interface [label="defines requirements"];
}
```

Run `make diagrams` to generate vector PDFs. Keep the source and generated PDF
together so a deck remains buildable and reviewable.

See the [plotting guide](../../docs/plotting-guide.md),
[diagram guide](../../docs/diagram-guide.md), and
[book source notes](../../docs/visual-display-source.md) for the design rules.

## Compatibility names

`DuneOrange`, `DuneCyan`, `DuneMint`, `DuneYellow`, `DuneRed`, and
`DuneViolet` remain available for older decks. Do not use them in new material;
they describe hues rather than meaning.

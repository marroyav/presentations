# Presentation framework guide

## Recommendation

Keep Beamer and Tectonic as the production PDF path, but treat them as the last
layer of a small presentation system:

1. Start from an audience/outcome brief.
2. Write assertion-style, sentence-case slide titles.
3. Use one shared visual theme and semantic design tokens.
4. Build diagrams from reviewable source with the same tokens.
5. Run source, token, contrast, and build checks before sharing the PDF.

This preserves the equations, tables, TikZ assets, and reliable PDF workflow in
the existing repositories. It also fixes the main source of drift: every copied
theme or locally named color currently becomes another design system.

## What the current repositories show

The older `work/latex/daphne_presentations` collection contains useful material
and several successful experiments, but it also contains copied Beamer themes,
deck-local TikZ styles, and multiple diagram pipelines. The newer
`work/presentations` repository already centralizes a dark theme and is the
right home for the framework.

Migration should therefore be incremental. New decks start here. Existing decks
move only when they need substantial revision; their content should not be
restyled in bulk just to claim migration progress.

## Editorial model

Google's technical-writing guidance applies well to technical presentations,
even though it is not a slide-design system:

- Define the audience, scope, and non-scope before drafting.
- Put the key point first.
- Prefer active voice so ownership is explicit.
- Keep one idea per sentence.
- Use parallel list items and numbered lists only when order matters.
- Use sentence case and descriptive titles.
- Introduce a diagram with a complete thought and explain its meaning in text.

For a decision deck, use the following narrative spine:

1. Recommendation or result.
2. Why the audience should care now.
3. Evidence and system explanation.
4. Risks, uncertainty, and boundaries.
5. Exact action, owner, and completion condition.

Slide titles should state conclusions such as “One contract serves both
consumers,” not labels such as “Architecture.” A person reading only the titles
should still understand the argument.

### Voice: clear enough to say aloud

Clarity wins. Technical accuracy does not require the voice of a policy
document. Write like a knowledgeable colleague explaining the work to people
in the room:

- Name the person, team, or system doing the action, then use a plain verb.
- Use `we`, `you`, and `our` when the relationship is real; they make ownership
  easier to follow.
- Turn abstract categories into the question the audience is asking: “What is
  really installed?” is clearer than “Installed reality.”
- Prefer familiar words such as `show`, `use`, `test`, `own`, and `decide` over
  noun-heavy phrases such as `operator representation`, `release evidence`, or
  `completion condition`.
- Keep the exact technical term when it matters, but explain it once in ordinary
  language.
- Put reference lists, edge cases, and policy wording in a companion document or
  backup slide unless the audience needs them to make the decision.

Use the read-aloud test before sharing: if a sentence would sound unnatural in
conversation, rewrite it. For example:

| Robotic | Clear and human |
|---|---|
| Protection authority remains separate | Seeing a problem is not the same as stopping it |
| The completion condition is observable | We are done when… |
| Installation defines identity | Tell us what is really installed |
| Repeatable release evidence | Test the normal case, the fault, and the recovery |

## Visual model

The earlier DUNE clear/dark decks work best when their layouts change with the
argument. This framework therefore treats color as a structural layer inside a
stable dark canvas, not as a colored status label attached to every idea:

| Visual layer | Use |
|---|---|---|
| Warm paper | Sources, definitions, reference material, neutral proof |
| Sky | Interfaces, flows, context, and supporting structure |
| Coral | Ownership, active path, decision, and requested action |
| Dark ink | Supporting material that should recede |
| Red | A genuine hard danger or prohibited condition only |

Sky and coral are high-luminance presentation tints of the established
blue/orange families; they are layout surfaces, not additional institutional
brand colors.

Paper, sky, and coral are high-contrast filled surfaces with dark text. They
create hierarchy through block size, placement, and relationship. A normal
slide uses one dominant fill; a comparison or diagram may combine them because
the layout itself explains the relationship. Green and gold remain optional
data-visualization tokens rather than standard slide furniture. Labels, shapes,
lines, and placement still carry the meaning when color is unavailable.

The deck should alternate slide languages: editorial claim, asymmetric mosaic,
section break, figure-led explanation, comparison, evidence table, pipeline,
and decision close. Repeating a composition is useful for a real comparison;
repeating it on every slide makes the deck feel like a form.

The palette audit checks normal text at 4.5:1 and meaningful graphical cues at
3:1. These are WCAG web thresholds, used here as measurable minimums; projected
slides often benefit from exceeding them.

## Typography and density

New decks use an `11pt` Beamer base. Because Beamer's PDF canvas is physically
smaller than a PowerPoint canvas, point values are not directly comparable
between the two formats; the practical rule is still simple: use the normal
size for prose and shrink at most one step for supporting material.

- Use `\normalsize` for bullets and explanatory prose.
- Let filled blocks and compatibility callouts use `\small` for short copy.
- Reserve `\footnotesize` for table detail and diagram captions.
- Never solve a crowded slide with `\scriptsize` or `\tiny`.
- Prefer two prose columns; use three only for short, parallel comparisons.
- Avoid four prose cards. Four short, ordered stages are acceptable when they
  form a clear pipeline; otherwise use a two-by-two grid or another slide.

Microsoft recommends presentation type equivalent to at least 18 points and
W3C recommends limiting slide text and making it readable from the back of the
room. The framework enforces the layout side of that guidance: shorten, split,
or move detail rather than silently reducing the type.

## Diagram tool policy

| Tool | Default use | Decision |
|---|---|---|
| TikZ | Small, bespoke explanation tightly integrated with a slide | Keep |
| Graphviz | Dependency, ownership, hierarchy, and architecture graphs | Default external renderer |
| Mermaid | Sequence/state diagrams already maintained in Markdown | Optional import path |
| PlantUML | Strict UML/C4 in a codebase that already uses it | Optional specialist tool |
| diagrams.net | Spatial hardware/site drawings requiring direct manipulation | Escape hatch; commit editable source and vector export |
| Screenshots | Real UI or physical evidence only | Never use for text or diagrams |

Graphviz is the default external tool because it is already installed, handles
directed technical topology well, and emits vector PDF without a browser. Its
`*.dot.in` files use the same token names as the Beamer theme.

Mermaid remains useful, especially for sequences and states, but its normal PDF
path introduces Node/Chrome or SVG conversion dependencies. Quarto itself warns
that LaTeX SVG conversion needs extra tools and can clip multiline labels. Add
Mermaid only when its diagram vocabulary provides a clear advantage.

## Why not replace LaTeX now

Quarto is the most credible future authoring layer. It can produce reveal.js,
PowerPoint, and Beamer presentations and has native Mermaid and Graphviz cells.
It is a good option for a later HTML companion format, especially because
Beamer currently does not provide tagged PDF support.

It is not the first migration step. Moving the existing decks to Markdown would
mix a content rewrite, a layout rewrite, and a build-system rewrite. Stabilize
the design tokens, components, diagram policy, and editorial checks first. A
small pilot can then test whether Quarto improves a real deck without losing the
precision needed for the technical figures.

Typst presentation packages are improving quickly, but the ecosystem still has
multiple competing packages and some explicitly make no compatibility
guarantees. Revisit Typst only as a separate pilot, not as a prerequisite for a
consistent framework.

## Workflow

Create a deck:

```sh
make new-deck SLUG=my_topic_sep2026 TITLE="My topic" AUTHOR="Your name"
```

Then complete the generated `README.md` brief before editing `main.tex`.

Build and review:

```sh
make diagrams
make
make audit
```

Use `make check` for the full framework starter, both current decks, palette
checks, and source audits.

Review the PDF at actual projector scale. Automated checks cannot decide
whether a diagram has too many concepts, whether a result deserves its own
slide, or whether the audience understands an acronym.

## Migration sequence

1. Use the framework for every new deck.
2. Move shared diagrams into tokenized Graphviz or shared TikZ styles when they
   next change.
3. Replace legacy hue tokens with shared layout components during substantive edits.
4. Move high-value old decks into this repository one at a time.
5. Pilot one Quarto/reveal.js companion deck only after the PDF framework is
   stable.

## Authoritative references

- [Google Technical Writing: documents, audience, scope, and key points](https://developers.google.com/tech-writing/one/documents)
- [Google developer documentation style highlights](https://developers.google.com/style/highlights)
- [Google guidance for accessible documentation](https://developers.google.com/style/accessibility)
- [Google guidance for diagrams, figures, and images](https://developers.google.com/style/images)
- [Google guidance for headings and titles](https://developers.google.com/style/headings)
- [Microsoft guidance on readable presentation type](https://support.microsoft.com/en-us/powerpoint/tips-for-creating-and-delivering-an-effective-presentation)
- [W3C guidance for accessible presentations](https://www.w3.org/WAI/teach-advocate/accessible-presentations/)
- [Fermilab graphics standards](https://www.fnal.gov/faw/designstandards/index.html)
- [Fermilab official color palette](https://www.fnal.gov/faw/designstandards/color-palette.html)
- [Fermilab font guidance](https://www.fnal.gov/faw/designstandards/fonts.html)
- [DUNE logos and presentation template](https://atwork.dunescience.org/logo-templates/)
- [WCAG 2.2 use of color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html)
- [WCAG 2.2 contrast minimum](https://www.w3.org/TR/WCAG22/#contrast-minimum)
- [WCAG 2.2 non-text contrast](https://www.w3.org/WAI/WCAG22/understanding/non-text-contrast.html)
- [Graphviz `dot` layout](https://graphviz.org/docs/layouts/dot/)
- [Graphviz PDF and SVG outputs](https://graphviz.org/docs/outputs/)
- [Mermaid theming](https://mermaid.js.org/config/theming.html)
- [Mermaid accessibility metadata](https://mermaid.js.org/config/accessibility.html)
- [Quarto presentations](https://quarto.org/docs/presentations/)
- [Quarto diagram support and PDF caveats](https://quarto.org/docs/authoring/diagrams.html)
- [Beamer package status](https://ctan.org/pkg/beamer)

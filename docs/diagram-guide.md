# Diagram guide

Show the relationship the audience needs to understand. Use a white background,
dark labels and connections, and a small set of shapes. Put the explanation
beside the relevant part of the diagram.

This guide applies Tufte’s ideas about clear labeling, useful marks, comparison,
and integrating words with graphics to system diagrams. That extension is a
repository design choice: the book concerns statistical graphics. See the
[source notes](visual-display-source.md).

## Define what the picture means

Write the question before drawing. Choose a system boundary and a level of
detail that answer it. Give the diagram a sentence title and a short caption
stating its meaning and any important omission.

Name actual systems and interfaces. Label each ambiguous connection with what
it carries or does, such as “waveform data” or “requests power off.” Explain
arrow direction. Distinguish a command, a data transfer, physical wiring, and
ownership; split them into separate views if combining them obscures meaning.

Do not imply that a conceptual connection is an installed cable, that a proposed
owner has agreed, or that a drawing has passed electrical checks. State proposed,
existing, unknown, and verified conditions in words beside the relevant object.

## Use position and labels first

- Give the main flow a clear direction. Align comparable stages and reserve
  space for labels before routing connections.
- Use one shape per kind of thing. Add a boundary only when containment has meaning.
- Keep connectors dark enough to follow on white. Pale separators are decoration,
  not suitable signal paths. Use arrowheads only where direction has meaning.
- Explain line patterns locally, for example solid for existing and dashed for
  proposed. Pair color with words or geometry.
- Place a label beside its symbol. If needed, use a short line from the label to
  the symbol. Keep that line separate from system connections.
- Route around labels and unrelated objects. Show junctions explicitly and make
  crossings unambiguous. Never hide a crossing with a white patch.
- Remove shadows, gradients, decorative icons, colored cards around every node,
  and repeated prose. Keep symbols, identifiers, ports, and boundaries that
  readers need to understand the system.

For before/after views, retain node positions, scale, labels, and line meanings
where possible. Highlight the change. Repeated layouts help readers compare;
a new composition for every view makes them relearn the picture.

## Choose the source and renderer

Use TikZ for small compositions integrated with a slide, and tokenized Graphviz
for dependency or topology graphs. Existing Mermaid or diagrams.net sources
remain useful when they suit the diagram; keep editable source and vector output.
White Graphviz diagrams should use `editorial-canvas`, `editorial-text`, and
`editorial-muted` tokens. See the maintained starter for a complete example.

For electrical drawings, follow the [schematic framework](schematic-framework.md).
It defines the separate illustrative and KiCad hardware-authority paths,
monochrome tokens, geometry checks, and provenance requirements. Its fixed stroke
width and electrical symbols take precedence over general slide styling.
Do not recolor a reviewed schematic to fit a slide.

## Review the exported diagram

Read the main path without narration. Check that every arrow and boundary has
one meaning and that the caption supports the slide’s claim. Check the drawing
against its source revision and mark unresolved interfaces.

Inspect the diagram in the final slide PDF, including in grayscale. Check label
size, clipping, crossings, and contrast after scaling. Keep editable source and
the reviewed PDF or SVG together. A successful render proves that the file builds;
it does not prove system connectivity, installation, or engineering approval.

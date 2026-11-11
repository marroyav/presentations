# Plotting guide

Make the comparison clear and keep the evidence intact. Use a white canvas,
dark labels, and enough space for the data. Start new decks with the white
profile described in the [theme reference](../templates/dune-professional/README.md).

These rules adapt Edward R. Tufte’s *The Visual Display of Quantitative
Information*, second edition. See the [source notes](visual-display-source.md)
for the pages reviewed and the distinction between the book and local rules.

## Choose the display for the question

| Question | Starting display | Keep visible |
|---|---|---|
| How does a quantity change with time? | Points and lines on a time axis | Gaps, sampling interval, time origin |
| How do channels or configurations compare? | Aligned dots or repeated panels | Same units, limits, ordering, and reference |
| How are two measurements related? | Scatter plot | Individual observations and relevant reference line |
| What is the distribution? | Histogram or empirical cumulative distribution | Sample count, binning or normalization, tails |
| What changed between two conditions? | Paired dots or a difference plot | Pairing, baseline, uncertainty |
| What are the exact values? | Compact table | Units, precision, conditions |

Repeated panels, often called small multiples, use the same visual form to
compare channels, runs, or conditions. Keep their scales and geometry the same.
If different scales are needed, label them clearly and explain the reason.
Repeat a layout when it helps comparison; do not vary it merely for visual rhythm.

## Preserve scale and context

- Name each quantity and its unit. State the run, channel selection, exposure,
  and cuts needed to interpret it, beside the plot or in its caption.
- Start bars at zero because their length encodes magnitude. A line or scatter
  plot may use a restricted range when the visible ticks make that range clear.
- Label logarithmic axes and transforms. Do not imply that equal distances on
  a log axis are equal absolute changes. State how zeros are handled.
- Use the same bin edges for compared histograms. Say whether heights represent
  counts, probability, density, or rate. Give the relevant exposure or denominator.
- Show missing data as gaps. Distinguish missing, excluded, and measured zero.
- Keep raw observations visible where practical. Label fits, simulations,
  smoothing, and aggregation; record their settings in the figure source.
- Define error bars or bands: spread, standard error, confidence interval, or
  another stated quantity. Give the interval level and sample count where relevant.
- Choose an aspect ratio that permits reading labels without exaggerating slopes.
  Preserve geometry when distance, angle, or spatial scale has physical meaning.
- Avoid decorative 3D, perspective, pictograms scaled in two dimensions for a
  one-dimensional quantity, and unrelated dual vertical axes.

For DAPHNE waveforms, state the time origin, sample interval, amplitude units,
and any baseline subtraction. For throughput, separate offered rate, accepted
rate, and loss; state the active channel count and measurement duration.
These are local engineering requirements, not quotations from Tufte.

## Let the data carry the emphasis

Use dark data marks on white. Add one accent for a selected series or reference
when it helps the reader. Give that series a direct label and a distinct marker
or line pattern. Keep the same encoding across panels and slides.

Place series names beside their lines when they fit without collisions. Use a
short legend when direct labels would obscure observations. Put important event
labels beside the relevant point. A line from a label to a point should end at
that point and avoid crossing other labels.

Remove shadows, ornamental borders, background textures, and repeated titles.
Use a light grid only where it helps read values. Keep ticks, units, uncertainty,
and necessary reference lines. Tufte’s data-ink principle means spending marks
on information; it does not mean making evidence faint or deleting useful context.

Use the deck’s font family where available. Judge label sizes after placing the
figure on the slide: a readable standalone plot can become unreadable when reduced.
Split dense figures into an overview and readable detail instead of shrinking text.

## Build a figure that can be checked

Keep the generating script, input identity, selection, and output together, or
link to the owning analysis repository and its revision. Export vector PDF for
Beamer and SVG when useful elsewhere. Rasterize dense data layers only when
needed; retain readable vector labels. Never enlarge a screenshot of a plot.

A caption should say what is compared, the main observation, and the limit on
that observation. Keep the source close to the figure. Label demonstration data
as illustrative so readers cannot mistake them for measurements.

Before sharing, check the numerical values against the source, compare scales
across panels, and inspect the final PDF at viewing size and in grayscale.
Confirm that labels do not collide and that the conclusion still follows when
the color is removed. Automated palette checks cannot verify the analysis.

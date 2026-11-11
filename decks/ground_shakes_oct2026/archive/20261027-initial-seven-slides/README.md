# Ground shakes

Seven short slides for Manuel's ProtoDUNE-HD review. Open [the presentation](main.pdf).

## Audience and outcome

The audience knows the detector but has not followed this analysis. The slides
name the runs, explain each plot and separate observations from possible causes.
The main result is a shared electrical response; the initiating cause and a
unique charge–light match remain unresolved. No approval or hardware change is
requested.

## Scope and evidence

The deck uses the local analysis from 15, 20 and 23 October 2026. The detector
data were recorded in July, October and November **2024**. It covers seven runs,
1,531 saved events and 1,516 automatic charge-screen candidates. These are
selected records, not a measurement of the shake rate.

Each plot has a visible caption. [SOURCES.md](SOURCES.md) records the cuts,
sample sizes and limits. `evidence/source-manifest.json` pins the original inputs
by SHA-256; `evidence/plot-data.npz` holds the displayed values. The plots use
these saved results without rerunning detector reconstruction or acquiring data.

## Build

From this directory:

```sh
python3 prepare_figures.py
tectonic --chatter minimal --keep-logs --keep-intermediates main.tex
```

From the repository root, the normal build also includes this deck:

```sh
make decks/ground_shakes_oct2026/main.pdf
```

To replace the frozen plot inputs from the local analysis, explicitly run:

```sh
python3 prepare_figures.py --refresh
```

This needs the sibling `ground-shake-data` directory. The normal figure build
needs only the checked-in evidence, NumPy, Matplotlib and the shared design
tokens. The PDF uses the shared DUNE Beamer theme.

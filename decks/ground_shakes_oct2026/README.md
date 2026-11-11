# Ground shakes

Open [the presentation](main.pdf). The 28 October review has six main slides
and three backups. It is written for readers who have not followed the detector
analysis. It follows the direct wording of the EDMS slides.
[Speaker notes](speaker-notes.txt) explain each plot.

[Compare APA1 with APA2](pds-spatial/apa1-comparison/viewer.html), or read the
[four-page comparison](pds-spatial/apa1-comparison/apa1-apa2-response.pdf).
The [synchronized APA1/APA2 player](pds-spatial/apa1-comparison/activity.html)
shows all four channels within each module, in physical order and by matching
AFE input, on one clock. Both views retain module and channel labels and use
the same measured values. Disconnected APA2 M8 remains visible, with its
recorded electrical response included.
The 3 November comparison shows activity and timing by physical module.
The precursor favours upper modules in both APAs: M3/M4 in APA1 and M1/M2 in
APA2. The main-shake distribution differs. Sparse APA1 recording prevents a
clear comparison of the sequence between stages. The electronics comparison
is linked separately.

[All-event APA2 histograms](pds-spatial/population/viewer.html) test whether the
largest response shifts from M6 toward the M1/M2 corner. They include all 1,377
available APA2 records with a main-shake time and compare stages on the same
recorded channels. The [four-page PDF](pds-spatial/population/apa2-all-event-histograms.pdf)
includes paired transitions, recording coverage and checks in each run.

[Play APA2 activity by physical section](pds-spatial/viewer.html), or open the
[maps and section histograms](pds-spatial/apa2-pds-sections.pdf). These use the
existing event 52 and event 33 maps and show recording coverage beside the signal.
The [original APA1/APA2 player](../../../ground-shake-data/analysis/whole-event-spatial/viewer.html)
contains all five mapped examples.

The deck starts from the EDMS findings. It presents the double pulses, the
PDS-to-shake timing histogram, charge–light matching and next checks.
The backups retain the data inventory, charge pattern and channel-fit scores.
Known charge and electrical behaviour is credited
to the earlier work. No cause or confirmed optical flash is claimed.

The timing correction keeps a repeated source location as a possible explanation.
Event mixing does not exclude a shared physical drift delay. The slow coherent
precursor marker is distinct from the arrival of localized drift charge.
The timing plot compares timestamps; it does not integrate TPC and PDS signals.

The [wider pulse-time histogram and packet coverage](../../../ground-shake-data/analysis/pds-shake-timing-20261028/extended-timing-and-coverage.pdf)
show why the full shape cannot yet be called Gaussian: this pulse selection
has no 21-channel coverage earlier than about 320 microseconds before the shake.

[SOURCES.md](SOURCES.md) links every claim to its evidence and methods.
The [dated EDMS comparison](evidence/baseline-comparison-20261028.json) distinguishes
reproduced observations, added measurements and unanswered questions.

## Build

From this directory:

```sh
python3 public_review.py
tectonic --chatter minimal --keep-logs --keep-intermediates main.tex
```

The first command uses frozen values and verifies their hashes. Use
`python3 public_review.py --refresh` only to reselect values from the sibling
analysis store. The earlier figures remain in `figures/`; their original
generation scripts and evidence are retained.

The root build also supports `make decks/ground_shakes_oct2026/main.pdf`.

## Earlier versions and evidence

- [27 October deck before this review](archive/20261028-before-public-review/main.pdf).
- [Initial seven-slide deck](archive/20261027-initial-seven-slides/main.pdf).
- [Original figure inputs](evidence/source-manifest.json).
- [Electrical and SC extension inputs](evidence/extension-manifest.json).
- [Public-review inputs](evidence/public-source-manifest.json).
- [Public-review figure hashes](evidence/public-figure-manifest.json).
- [Completed SC analysis](../../../ground-shake-data/analysis/sc-correlation-20261027/index.html).

The older validation records apply to their archived PDFs. The
[slide-removal validation](evidence/validation-20261028-drop-6-7-12-13.json)
records the current nine-page PDF. The
[TPC-signal wording validation](evidence/validation-20261028-tpc-signal-wording.json)
applies to the [preceding 13-page version](archive/20261028-before-drop-6-7-12-13/main.pdf). The
[slide-removal validation](evidence/validation-20261028-slide5-removed.json)
records the preceding version. The previous
[drift and histogram validation](evidence/validation-20261028-drift-histogram.json)
applies to the [14-page version](archive/20261028-before-removing-slide5/main.pdf). The preceding
[public review](archive/20261028-before-drift-clarification/main.pdf) is preserved.
The new histogram can be rebuilt with
`python3 ../../../ground-shake-data/analysis/pds-shake-timing-20261028/analyze.py`;
its inputs, record-level values and limitations are linked from SOURCES.md.

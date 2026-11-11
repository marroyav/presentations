# Ground shakes

Open [the presentation](main.pdf). The 28 October review has eight main slides
and five backups. It is written for readers who have not followed the detector
analysis. It follows the direct wording of the EDMS slides.
[Speaker notes](speaker-notes.txt) explain each plot.

The deck starts from the EDMS findings. It presents the double pulses, the
PDS-to-shake timing histogram, charge–light matching, the predictive electrical fit
and the limited SC comparison. Known charge and electrical behaviour is credited
to the earlier work. No cause or confirmed optical flash is claimed.

The timing correction keeps a repeated source location as a possible explanation.
Event mixing does not exclude a shared physical drift delay. The slow coherent
precursor marker is distinct from the arrival of localized drift charge.

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
[slide-removal validation](evidence/validation-20261028-slide5-removed.json)
records the current 13-page PDF. The previous
[drift and histogram validation](evidence/validation-20261028-drift-histogram.json)
applies to the [14-page version](archive/20261028-before-removing-slide5/main.pdf). The preceding
[public review](archive/20261028-before-drift-clarification/main.pdf) is preserved.
The new histogram can be rebuilt with
`python3 ../../../ground-shake-data/analysis/pds-shake-timing-20261028/analyze.py`;
its inputs, record-level values and limitations are linked from SOURCES.md.

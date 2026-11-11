# Ground shakes: what this analysis adds

Open [the presentation](main.pdf). The 28 October review has nine main slides
and five backups. It is written for readers who have not followed the detector
analysis. [Speaker notes](speaker-notes.txt) explain the plot sequence.

The deck starts from the EDMS findings. It presents the double pulses, the
first-pulse timing test, charge–light matching, the predictive electrical fit
and the limited SC comparison. Known charge and electrical behaviour is credited
to the earlier work. No cause or confirmed optical flash is claimed.

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
[public-review validation](evidence/validation-20261028-public-review.json)
records the final PDF, source identity and layout checks.

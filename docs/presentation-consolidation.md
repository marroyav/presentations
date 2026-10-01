# Presentation recovery and branch consolidation

Completed from the September 25, 2026 workstation backup on October 1, 2026.
The canonical repository is `https://github.com/marroyav/presentations`,
and its maintained branch is `main`.

## Recovered content

- `decks/`, `templates/`, `scripts/`, `docs/`, `examples/` and `schematics/`
  contain the current presentation workspace, including all four previously
  missing September decks and the framework changes needed to rebuild them.
- `legacy/wl-144132/` retains the later DAPHNE presentation workspace.
- `legacy/latex/` retains the earlier LaTeX workspace and its differing deck
  versions. The two snapshots are preserved separately rather than choosing
  one revision and losing the other.
- [The legacy catalogue](../legacy/README.md) links every historical deck's PDFs.
- [The original current-workspace README](recovery/archived-current-README.md)
  is retained alongside the maintained root index.

Sources, saved PDFs, assets, speaker notes and supporting evidence are included.
Generated TeX intermediates, Python caches and nested Git administrative files
are excluded. Every selected archive file was SHA256 verified at extraction.
[The recovery manifest](recovery/full-recovery-manifest.json) records the
original archive paths and checksums. Checksums describe the extraction bytes;
subsequent PDF builds and comment-whitespace cleanup can change current files.

The earlier recovery commit preserves the local regenerated PDFs and original
September files before the complete archived workspace was imported. Git
history therefore retains both states. The legacy `daphne_presentations` main
history is joined with an explicit history-preserving merge; its content is
imported into the `legacy/` directories, leaving the current root layout intact.

## Retired development lines

`dev/lidine2024-schematic-import-pilot` was already at `0863834`, the same
commit as the former main tip. It contributes no unmerged commits. Its archival
tag is published before the redundant remote branch is removed.

| Archive tag | Preserved state |
| --- | --- |
| `archive/dev-lidine2024-schematic-import-pilot-20261001` | Retired development branch |
| `archive/local-pdf-stash-20261001` | Saved regenerated-PDF stash |
| `archive/legacy-latex-20261001` | Earlier legacy repository at `51265bc` |
| `archive/legacy-daphne-presentations-20261001` | Later legacy repository at `77e9ef7` |

Future presentation edits belong on `main` or short-lived branches created
from it. Historical snapshots and archive tags remain available for reference.
The separate legacy GitHub repository is a provenance source; this operation
does not delete or modify that external repository.

## Validation

The root `make check` validates and rebuilds the maintained decks. Historical
PDFs are preserved as received; they are not silently rewritten to the current
theme. The PDS capture/dead-time analysis tests are run separately with:

```sh
python3 -m unittest discover -s decks/pds_trigger_story_sep2026/analysis -p 'test_*.py'
```

The root index and legacy catalogue are the entry points for the combined set.

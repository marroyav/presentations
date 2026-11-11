# VD detector protection

I&I presentation, 28 October 2026. Twenty main slides and fifteen backups.
The main slide order is unchanged. The language is shorter and detailed source
comments are kept in the notes. The four new backup pages list devices by system.

The device count is **336 microTCA crates across TDE and DAQ/timing combined**.
PDS still uses 34 LV feeds and 80 PoF boxes, with 400 voltage/temperature readings.

Files:
- `main.pdf`: presentation.
- `device-hierarchy.html`: interactive device hierarchy, made with Markmap.
- `device-hierarchy.txt` and `.csv`: full hierarchy, interfaces and source/status data.
- `diagrams/*.tikz.tex`: editable overview, DAPHNE, PoF, laser and rack diagrams.
- `diagrams/styles.tex`: diagram sizes and styles, using the shared framework's TikZ styles and colours.
- `edms-export-review-20261028.txt`: comparison with the newly downloaded EDMS export.
- `sources.json`: source identities, revisions, locations and hashes.
- `sources-and-notes.txt`: speaker notes and engineering detail.
- `verification-latest.txt`: latest immutable verification record.

All authored system diagrams use native TikZ and compile with the slides.
The device hierarchy includes
known network endpoints, attached hardware and external-system interfaces. It is
not an IP-address register or a completed purchasing bill of materials.

Build: `make decks/dps_integration_status_oct2026/main.pdf` from the repository root.
Earlier versions remain in `archive/`.

## Edit a diagram

Edit the label or connection in the matching `diagrams/*.tikz.tex` file, then
run the build command above. The build detects diagram changes automatically.
For example, the SDSTA label on slide 2 is in `diagrams/overview.tikz.tex`:

```tex
\node[dps node,text width=3.5cm] (sdsta) at (0,0)
  {SDSTA SCADA\\Interface under study};
```

The five source files are `overview`, `daphne`, `pof`, `lasers` and `racks`.
The site maps use `site-boundaries.tex`; the detailed DAPHNE backup uses
`daphne-icd-reference.tex`. The remaining small diagrams are in `main.tex` and
`backup-slides.tex`. Reference drawings and operator screenshots remain PDFs.

The earlier draw.io sources, SVG exports, renderer and diagram PDFs are retained
in the archive before the 10 November 2026 TikZ conversion. They are no longer
build inputs. No browser, draw.io or Playwright step is needed to build the deck.

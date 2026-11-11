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
- `diagrams/dps-public.drawio`: editable overview, DAPHNE, PoF, laser and rack diagrams.
- `edms-export-review-20261028.txt`: comparison with the newly downloaded EDMS export.
- `sources.json`: source identities, revisions, locations and hashes.
- `sources-and-notes.txt`: speaker notes and engineering detail.
- `verification-latest.txt`: latest immutable verification record.

Draw.io SVG exports are rendered as vector PDFs by `diagrams/render_drawio.py`.
The other diagrams retain their native TikZ source. The device hierarchy includes
known network endpoints, attached hardware and external-system interfaces. It is
not an IP-address register or a completed purchasing bill of materials.

Build: `make decks/dps_integration_status_oct2026/main.pdf` from the repository root.
Earlier versions remain in `archive/`.

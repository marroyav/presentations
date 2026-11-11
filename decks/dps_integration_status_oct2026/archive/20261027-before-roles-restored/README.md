# VD detector protection

I&I workshop draft, 27 October 2026. Eight main slides and nine backup slides.

The argument: BDE already provides a PLC design, distributed panels and software.
Extend that design to the rest of VD, test the added protection paths, and take
the hardware and purchasing package to review in June 2027.

The main talk explains the existing design, proposed CUC location, VD additions,
SC/DPS control boundary, prototype and procurement work, and proposed team.
The backup slides hold the rack allocations, panel drawings, component counts,
power estimates, PDU behaviour and subsystem inventories.

Scope: VD. HD may later use an extension or a separate PLC.
CUC placement, added interfaces and work assignments are proposals. The parts
and power records describe design allocations and estimates, not an installed
or qualified VD system.

`sources-and-notes.txt` contains the opening and slide-by-slide speaker notes.
`source-review.txt` records the technical findings. `sources.json` identifies
the source revisions, file hashes, locations and derived quantities.

Build: `make decks/dps_integration_status_oct2026/main.pdf`.
Latest checks: the record named in `verification-latest.txt`.
Previous drafts and their verification records are preserved in `archive/`.

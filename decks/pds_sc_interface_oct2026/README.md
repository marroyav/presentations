# SC–PDS–DPS interface

Draft 1.9 · 14 October 2026 · ten main slides and two backup slides.

The audience needs to understand the connections, ownership, selected variables
and unfinished integration work. The deck opens with the SC–PDS–DPS title and responsibilities. Its overview
places all five equipment interfaces at the same level below one SC-facing
OPC UA boundary. It then reuses the DAPHNE control-path diagram from the local ICD.

## Diagrams

- `diagrams/daphne-icd.tikz.tex` is copied verbatim from section 3.1 of
  `/home/arroyave/work/icd-sc-pds/sections/03_protocols_services.tex`, repository
  revision `bfb2a8b725d9a5a3b7a517f4f9e15fb953eed1f8`.
- `diagrams/system-overview.tikz.tex` shows DAPHNE, the PDS calibration box,
  PoF, WIENER and PDU as peers behind the same OPC UA boundary. Native protocols
  belong behind the services/adapters, not on a separate SC connection.
- `diagrams/icd-style.tex` supplies the ICD's box-and-arrow styles using the
  shared dark presentation palette. The diagram source remains verbatim;
  label-background styling follows the canvas. Both figures are native TikZ.
  Diagram captions and slide annotations are omitted; context and provenance remain in the notes.

The diagram content is the ICD design, not a claim of full deployment. Its
OPC UA bridge routing, arbitration and board publications remain separate from
the smaller implemented interface reviewed on develop. The original ICD is a
local draft 0.2 dated 17 September 2026, pending review and approval.

## Editorial approach

Use familiar names, one purpose per slide and short, direct sentences. Keep
implementation exceptions in backup material. Reuse the existing figure.
Guidance reviewed 14 October 2026:

- [Government Design Principles](https://www.gov.uk/guidance/government-design-principles)
- [Writing for user interfaces](https://www.gov.uk/service-manual/design/writing-for-user-interfaces)

## Scope and evidence

The variable inventory is corrected workbook v1.1: 159 rows/patterns, 59 Control,
100 Publish; 22 mappings/readers pending. Counts are not physical channel totals
or proof of complete OPC UA export. PDS calibration box is the display name;
the source workbook tab identifier remains SSP.

Implementation baseline: daphne-os develop `edc61f1`, daphnemodules develop
`ba6fd3c`, explicitly local Hermes `d7de1de`, calibration-box register code/map,
WIENER integration guide and PX3 SC bindings. Exact paths and hashes are in
`evidence.json`. No device reads/writes or protection qualification were done.

PoF now uses the corrected working inventory of 8T+8V. WIENER power consumption still needs a
measurement definition and reader. Unknown SC metadata stays blank.

## Files and build

`main.pdf` is the presentation; `main.tex` and `diagrams/*.tex` are editable.
`speaker-notes.txt` supplies a short script. `validation.json` records build,
count, figure-identity and visual checks. `build_system_counts.py` creates the
system-expansion workbook (requires openpyxl) and `system-counts.tex` for the deck. Earlier versions remain in Downloads.

From this directory:

```sh
python3 build_system_counts.py
python3 prepare_evidence.py
tectonic --chatter minimal --keep-logs main.tex
```

The evidence script uses the Python standard library. All diagrams render in
Tectonic; no external diagram renderer is required. PDFs open in Zen.

## PoF I/O sizing slide

Slide 5 uses the corrected eight-channel inventory: 8 T + 8 V. Readout uses
2 eight-channel input terminals. One mixed digital terminal supplies the
single box enable/disable output, bringing the draft to **3 I/O terminals per PoF box**.
An incoming hardwired enable/disable signal can use one input on that same terminal.
The box enable is the user-specified control scope; electrical interfaces remain assumptions.
Model links are on the slide. `pof-io-sizing.json` records the arithmetic and
sources. `pof-integration-notes.txt` records the reuse approach and limits.
The PoF team presentation has been reviewed; its 4–7 V + one RTD scope differs
from the labelled 8 T + 8 V working case. No proposed control
signals were added to the implemented-variable inventory. The box enable is a
proposed interface, pending mapping and implementation.

## Rack-draft totals

Slide 6 uses `FD2 MiniRack combined!A1,B8,B11,F8,F11` and
`Power Summary!B17` in the May 2025 rack workbook: **40 mini-racks,
2 PoF boxes per rack, 8 drivers per box = 80 boxes and 640 drivers**.
The user working case gives 640 T + 640 V + 80 enables = 1,360 signal
points. Two temperature, two voltage and one shared digital terminal per
rack give **5 terminals/rack, 200 overall**. These physical counts are separate
from the workbook's 159 variable rows/patterns. Notes retain electrical
assumptions, excluded infrastructure and the later 40/42-rack discrepancy.

## Whole-system variable expansion

The FD-VD draft uses 42 boards, 32 used channels and four used AFE groups per
board, two data links per board (user input), eight calibration boxes, 80 PoF
boxes and 58 assigned WIENER output channels. The count is **20,804 allocated
logical interface instances: 10,838 Control + 9,966 Publish**. It is a draft
planning subtotal, not a deployed or fully typed OPC UA node inventory.

The PDU draft assigns one PDU to each of 40 shared top-plate mini-racks and
four PDS power racks: 40 candidate PX3-5147R units × 8 outlets plus four
PX3-5170V-E2F5 units × 30 outlets = 440 outlets. The reference profile is
repeated over the 44 racks: four temperatures, one leak detector and one smoke
assembly per rack. DocDB 32655-v8 p.21 explicitly reports four Celsius sensors
on the reference unit; repeating it is a draft allocation. Five directly
sourced contact-state fields per smoke interface count as 220 fields, not
220 smoke detectors. Vendor submittals are in `source-evidence/`.

The completed total is **20,804 + 6B + 12M + W**, where B is total Hermes input
buffers, M is populated HD-mezzanine AFE instances and W is defined WIENER
power-measurement instances. These inputs stay blank rather than becoming
silent zeroes. V2 alternatives are excluded from the V3 case. Using all
40 register-addressable channels and five AFE groups per board instead gives
23,828 before the same unallocated additions. The original 159 variable
definitions are unchanged; the proposed single PoF box enable is counted
separately in the system projection. Exact per-definition arithmetic is in
`system-counts.json` and workbook v1.2, on System Inputs / System Expansion /
System Totals. This scope includes PDS interfaces and shared top racks, not
all detector, DAQ-server and central SC racks.

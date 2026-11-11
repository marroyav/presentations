# VD detector protection

I&I workshop draft, 27 October 2026. Twelve main slides and seven backup slides.

The talk starts with the system definitions and four DPS inputs: FFDG BMS,
SDSTA BMS, cryogenics and detector. The detector diagram separates SC and the
subsystems. SC communicates with the DPS PLC over OPC UA and owns the logs.
The PLC arbitrates protection and sends permits/inhibits to the subsystems.

The existing BDE description, panel drawings, parts and Ignition screens come
before the proposal to extend the BDE PLC design to VD. The PDU control chain
is Ignition → DPS PLC → PDU, with local interlocks and status returned to SC.
PDS LV count: 34. These points follow Manuel's architecture corrections in
`architecture-inputs-20261027.txt`.

The remaining slides cover added interfaces, tests, the June 2027 review and
procurement, and proposed work assignments. Backup slides retain the detailed
rack allocations, bias-panel parts, power estimates and site-inspection work.

Scope: VD. HD can later use an extension or a separate PLC. CUC placement and
team assignments remain proposals. Source drawings and calculations do not
establish an installed or qualified VD system.

`sources-and-notes.txt` supplies the connected explanation for each slide.
`source-review.txt` records the engineering findings. `sources.json` records
source revisions, file hashes, quantities and the current architecture inputs.

Build: `make decks/dps_integration_status_oct2026/main.pdf`.
Latest checks: the record named in `verification-latest.txt`.
Previous drafts and their verification records are preserved in `archive/`.

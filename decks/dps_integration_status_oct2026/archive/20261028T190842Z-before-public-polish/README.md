# VD detector protection

I&I workshop draft, 27 October 2026. Twenty main slides and eleven backups.

The deck follows Manuel's system sequence. It starts with responsibilities and
the SC/DPS overview, then FFDG BMS, SDSTA BMS and cryogenics. The consortium
interlock matrix introduces the review on slide 6; DPS logic follows on slide 7.
Slide 8 is the requested empty Detector divider. BDE, PDS/DAPHNE, PoF, HV,
CalCI thermometry, lasers, purity monitors and racks follow in that order.
The last three main slides cover tests, procurement and responsibilities.

The same vertical service map is used on the two BMS slides. It distinguishes
wider SDSTA site services from DUNE building services at 4850/4910. It is a
schematic service boundary, not a surveyed section or an installed BMS point
inventory. The SDSTA hardware and protocol survey remains open.

All facility information enters SC in the overview. SC and DPS communicate
through OPC UA. Detector control/status uses OPC UA through SC; DPS controls
PDUs and WIENER supplies over SNMP and remote I/O over EtherCAT. Dedicated
BDE/bias wired inhibits remain visible in the system examples. Cryogenics is
in the CUC and appears as one system to DUNE despite its internal divisions.

PoF now uses Manuel's confirmed case: four voltage readings and one chassis
temperature per box, or 400 readings across 80 boxes. This replaces the earlier
8-temperature/8-voltage case in this deck. Inhibition uses the PDU; an additional
box-enable input is an option to investigate. PDS LV scope remains 34 feeds.
TDE remains 20 racks with current PDU control and optional future interfaces.

The DAPHNE/DAQ diagram is adapted from the local working SC–PDS–DPS ICD. Its
complete service figure is in the backups. The main slide omits server-deployment
details. The PrM slide keeps the proposed DAQ-tagging rule and the older bias-off
requirement visible as an unresolved ICD conflict.

`sources-and-notes.txt` follows all 31 slides. `source-review.txt` records the
findings and limits; `sources.json` records source revisions and hashes.
Build: `make decks/dps_integration_status_oct2026/main.pdf`.
Latest checks: the record named in `verification-latest.txt`.
Earlier revisions remain in `archive/`.

# VD detector protection

I&I workshop draft, 27 October 2026. Fourteen main slides and eight backup slides.

The talk connects the existing BDE/HV hardware to the VD procurement work.
For each matrix inhibit, trace the source, input connection, controller,
actuator/load and feedback. The result is the hardware already covered,
additions with quantities, and open choices that change those quantities.

The original definitions and four input domains remain. The detector overview
shows OPC UA through SC, SNMP control/status for PDUs and WIENER supplies, and
the dedicated BDE/bias EtherCAT and wired-inhibit paths. SC owns the logs.
FFDG uses the API through Batavia and SC; SDSTA remains under investigation.
The CUC PLC location is proposed. Bridge-server implementation is outside scope.

Two examples make the review concrete: the BDE cooling input-to-inhibit path,
and rack infrastructure as its own system. Rack/PDU/sensor hardware is counted
once; subsystem loads reference the PDU outlets. The following slides use that
review to explain subsystem/facility additions, prototype tests, panel space,
power and procurement before June 2027.

Scope: VD. The BDE baseline is ten groups of eight WIECs. PDS LV count is 34.
PoF controller alternatives are Opta PLC and Beckhoff PLC. TDE has PDU control
now; crate status and external inhibit remain future options. HD can later
extend the system or use another PLC.

The path review is underway; this deck does not claim a complete new-I/O count,
installed VD wiring or hardware qualification. The six-fan WIEC interface is
compared with the four-fan ICEBERG reference without calling the difference a
VD procurement quantity. The power backup uses the component fan load rather
than presenting the earlier linear HD extrapolation as a VD panel budget.

`sources-and-notes.txt` gives the connected explanation for each slide.
`source-review.txt` records findings and limits. `sources.json` records the
source revisions, file hashes, quantities and architecture basis.

Build: `make decks/dps_integration_status_oct2026/main.pdf`.
Latest checks: the record named in `verification-latest.txt`.
Earlier decks, notes and evidence remain in `archive/`.

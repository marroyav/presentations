# Source basis

Snapshot: 22 September 2026. No live installation or acceptance claim is made.

| Label | Source | What it supports |
|---|---|---|
| U1 | Manuel's instructions in this conversation | Overall design, implementation and delivery responsibility for HD and VD DPS. |
| U2 | Manuel's September 22 corrections | No UPS for TPC/PDS warm electronics; UPS required for DAQ, SC and DPS. Necessary networking included as a functional dependency in the draft. |
| U3 | Manuel's September 22 architecture correction | Slow Controls is a parallel path for monitoring and configuration. It must not embed DPS logic. This direction governs the new diagrams and draft. |
| U4 | [8 September presentation, slide 2](../surf_bms_fd_integration_sep2026/main.pdf) and Manuel's explicit confirmation of its facility-to-DPS connection | Architecture baseline: approved facility state → supervised DPS input → DPS action → detector functions; separate monitoring above and DPS status upward to SC. The original slide is retained intact. Its older trip-link note concerns implementation detail, not an invitation to redefine the architecture. |
| U5 | Manuel's Raritan and smoke-sensor clarification | Raritan PDU control is the proposed common detector power-control endpoint; smoke sensors are available protective inputs. Coverage of individual loads remains to be mapped. |
| U6 | Manuel's September 22 CUC power assumption | The yellow SC-rack block shares the DAQ UPS-backed power domain in the CUC. Detailed circuits and loads remain open. This does not identify the physical SC rack room or allocate every DPS load. |
| S1 | [July 20–23 electrical review](../../../wl-144132/dune-docs-analysis/source-material/power-and-electrical-updates/2026-07-20_23_EE_Meeting_Notes.docx) | Normal detector distribution and grounding; CUC DAQ UPS planning; SC UPS use; separate backup domains; unbacked DAQ chillers; named participants and July actions. Meeting intent, not an approved one-line. |
| S2 | [DUNE-doc-33801-v1, FDC TTO](https://docs.dunescience.org/cgi-bin/sso/ShowDocument?docid=33801&version=1) | PDF p. 16 places some software interlocks in SC: this conflicts with U3 and is an explicit reconciliation item, not the architecture adopted here. §§6.6.3 and 6.7.3: local TPC/BDE protection connects to global DPS. pp. 18, 45–46: outstanding transition details and SC/DPS interfaces. |
| S3 | [DUNE-doc-34374-v1, SC interface collection](https://docs.dunescience.org/cgi-bin/sso/ShowDocument?docid=34374&version=1) | TPC/BDE PLC interfaces to PL506/ISEG/PTC; HVS dependency on cryogenic conditions. Use the attachments' revision/approval status before adopting individual requirements. |
| S4 | [PDS interface v1, EDMS 3309688](../../../wl-144132/dune-docs-analysis/source-material/power-and-electrical-updates/2025-10-14_EDMS-3309688_DUNE_ICD_SC_PDS_v1.docx) | Subsystem/SC division and PoF hardware-interlock expectation. Still marked for approval; it does not establish the final laser-protection implementation. |
| S5 | [DUNE-doc-28208-v13, Mission Support volume](https://docs.dunescience.org/cgi-bin/sso/ShowDocument?docid=28208&version=13) | FY25 proposed ISD/SDS operating arrangements; pp. 39–40 and 62–74. Utility-maintenance boundary p. 63. |
| S6 | [DUNE-doc-9333-v5, SDSTA–FFDG MOU](https://docs.dunescience.org/cgi-bin/sso/ShowDocument?docid=9333&version=5) | Institutional scope, leased-space distinctions and coordination. Document authorship supports routing contacts, not individual acceptance authority. |
| S7 | Supplied September 10 deliverables proposal and email discussion | Starting names for local technical coordination and resource discussion; effort remains proposed. |
| S8 | [DUNE-doc-32655-v8, PX3 Rack Protection Setup](https://docs.dunescience.org/cgi-bin/sso/ShowDocument?docid=32655&version=8) | Hardware precedent: smoke sensor, sensor hub, switched outlets and local PDU logic. Author: Brandon Howe. Its Ignition-primary protection allocation conflicts with U3; this draft reuses the hardware basis, not that logic allocation. |

The facility-to-DPS connection is defined by U4. Its detailed hardware allocation, the monitoring implementation and complete UPS load coverage remain to be documented. Other prior analysis diagrams are supporting working material. The controlled BSI turnover package was not accessible in the captured session.

Diagram interpretation:

- **01:** the original two-line facility diagram, adopted as the architecture baseline. Its original date/page label are preserved. The earlier generated alternative is retained only in previous/.
- **02:** identified interface endpoints, including the facility source and supervised DPS input from U4. Solid lines identify defined interfaces, not verified installation. The power lane omits protective-earth, bonding and detailed distribution hardware.
- **03:** power planning domains. Solid lines are recorded plans or user-confirmed constraints; dashed lines identify a required but unassigned DPS backup feed. SC's final circuit/location remains unresolved. Separate facility and cryogenic sources are summarized, not electrically interconnected by the drawing.
- **04:** local rack example using the same two-line structure as 01. Sensor/PDU hardware is documented; the allocation of protection logic to DPS/local protection is the proposed design. This is a functional view, not sensor wiring to a particular PLC.

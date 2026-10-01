# FD detector protection interface — scope and boundaries

Draft 0.1 · 22 September 2026 · HD and VD · Prepared for Manuel Arroyave

**Purpose:** connect a harmful condition to the correct detector action, with an identified owner at each end.

**Architecture baseline:** [How facility signals reach DUNE](diagrams/01_reference_architecture.pdf), slide 2 of Manuel's 8 September presentation. The facility connection is defined: **approved facility state → supervised DPS input → DPS action → detector functions**. Monitoring follows the separate upper line. DPS reports status upward to SC. The remaining work details and assigns this connection.

**Proposed ownership at the boundary:**

| Part | Responsibility |
|---|---|
| Facility source and its output | Facility system owner supplies and maintains the agreed condition. |
| Supervised DPS input and protection logic | Manuel/DPS receives the condition, detects input faults and applies the agreed detector response. |
| Detector action endpoint | Subsystem owner provides and validates the means of acting on its equipment. |
| Monitoring/configuration path | SC team displays and records state and provides permitted configuration. No DPS logic runs here. |
| Interconnecting hardware | Facility and DPS teams assign installation, maintenance and acceptance at the agreed endpoints. |

**Local rack example:** smoke detection supplies the condition; DPS/local protection decides; the Raritan PDU switches the assigned outlets; the connected equipment is the protected load. SC monitors the sensor and outlet state and provides permitted configuration in parallel. Rack smoke and the facility fire alarm remain distinct inputs.

The working assumption is that a Raritan PDU provides the common protective power-control endpoint wherever removing AC is the correct action. The outlet-to-equipment map identifies exceptions requiring a dedicated inhibit or sequence and any essential loads kept powered. “Most loads” is a planning assumption, not a verified coverage count. [U5]

The existing rack setup documents smoke sensors, a sensor hub and PDU switching. It currently assigns primary protection logic to Ignition with local PDU fallback; that logic allocation must change to meet the SC/DPS separation specified here. Retain the hardware evidence and review the logic separately. [S8, U3]

This is the opening scope section of the control interface document. Proposed responsibilities and behavior require agreement. Source-backed design intent does not establish installed or accepted interfaces. Source labels refer to [SOURCES.md](SOURCES.md).

## 1. Five starting rules

1. **The subsystem defines its safe envelope.** Its experts identify damage conditions, acceptable states and the means of reaching them. Cross-system consequences are reviewed with DPS.
2. **The source owner owns the condition.** Facility and cryogenics teams operate their systems and define the information they provide. A copied alarm does not transfer authority over that system.
3. **DPS owns and executes the agreed detector response.** Manuel integrates HD/VD protection. Protective logic runs in DPS and local protection controllers. Slow Controls is a parallel path for monitoring and configuration; it contains no DPS logic. [U1, U3]
4. **Every action has an endpoint.** Identify the subsystem controller, inhibit input or power device that executes it, and the evidence that the requested state was reached.
5. **Failure and recovery are part of the interface.** Define the response to missing power, missing or invalid information, unsuccessful action and restoration for each protection function. This rule does not prescribe one universal trip or automatic-restart policy.

Rules 1–5 form the responsibility contract for this draft. Rule 3 follows Manuel's architecture direction. The older FDC TTO wording places some software interlocks in SC; that allocation must be reconciled with this design rather than carried forward silently. [S2, U3]

## 2. Definitions that prevent scope confusion

| Term | Meaning in this document |
|---|---|
| Facility systems | Electrical distribution, HVAC, fire/ODH and other conventional services relevant to detector operation. Their operating authority is system- and handover-specific. |
| Cryogenics controls | Controls for the cryogenic plant and cryostat process. DPS consumes agreed conditions; the cryogenics owner retains control of that process. |
| Slow Controls / DCS | The parallel monitoring, configuration, alarm and archive path. It observes protection status and may request permitted configuration changes. It does not evaluate or execute DPS logic. |
| DPS | The overall detector-protection function, including local protection and coordination between systems. Its logic executes independently of SC. It is not synonymous with one central PLC or server. |
| Subsystem/local protection | Protection implemented near or within TPC, PDS, HV, rack or other equipment. Local functions remain identified parts of the overall protection design. |
| DAQ | Data acquisition and its run/shutdown response. Stopping acquisition does not by itself prove that detector equipment is safe. |
| Physical boundary | A named pair of hardware endpoints, or a specified power/grounding transition. A software or organizational boundary is recorded separately. |
| Ownership | State whether this means design, operation, maintenance, reset authority or acceptance. Equipment location alone does not identify all five. |

The protection path is **source condition → DPS/local protection → protective action**. The parallel SC path observes source/equipment/DPS state and handles permitted configuration. DPS-required inputs must remain available through the specified protection path when SC is unavailable. Configuration requests remain subject to checks in the receiving system and cannot override the DPS protective decision. Logical separation does not by itself prove independent power, sensors or network paths; those dependencies require physical allocation.

In the reference facility diagram, the monitoring exchange is read-only. SC configuration concerns permitted detector/DPS settings through their defined interfaces; it does not grant write access to the facility BMS. The lower line's detector-action endpoint is separate from the local protection functions with which the overall DPS must interface.

## 3. Physical interfaces we can identify now

| Interface | What the records identify | What remains unestablished |
|---|---|---|
| Normal power → detector distribution | July review places double-shielded transformers on the cryogenic mezzanine and describes the downstream detector-ground distribution. [S1] | Approved device/panel schedule and the exact responsibility demarcation. This drawing does not replace the protective-earth/bonding design. |
| Local TPC/BDE protection → equipment | The TPC/BDE ICD identifies PLC enable/inhibit interfaces to PL506 and ISEG channels and communication with PTC equipment. [S3] | Final channel allocation, hardware realization, wiring and acceptance. |
| Rack smoke → PDU → equipment | Smoke sensor/hub and Raritan switched-outlet hardware are documented. DPS control of the PDU is the proposed common action path. [U5, S8] | Assignment of DPS/local logic, outlet-to-load map, essential-load exclusions and required dedicated-inhibit exceptions. |
| Local TPC/BDE protection → overall DPS | The FDC TTO plan explicitly requires local protection to interface with global DPS. [S2, §§6.6.3/6.7.3] | The physical handoff and allocation of each local/global action. |
| Cryogenics → HV protection | The HVS ICD identifies cryogenic conditions requiring HVS action. [S3] | The source and receiver terminals/controllers that carry each protective condition. A functional dependency alone does not establish a cable. |
| Facility → DPS | Approved facility state → supervised DPS input → DPS action → detector functions, as defined in Manuel's reference diagram. [U4] | Signal allocation, hardware details and named installation/maintenance/acceptance responsibility. The architecture is the baseline. |
| Facility → SC monitoring | BMS/Metasys → read-only exchange → facility reader → SC → operators, in parallel with DPS. [U4] | Detailed export implementation and service ownership. |
| PDS/PoF → controls/protection | The PDS ICD names PoF control equipment, electrical DPS inputs/connections and expected hardware laser interlocks. [S4] | The final laser-inhibit mechanism and its relationship to the normal controller, personnel protection and detector protection. |
| UPS → DAQ/SC/DPS dependencies | CUC DAQ backup and SC use are discussed in July; the proposed shutdown path depends on a PLC and switches. DAQ/SC/DPS backup is required by Manuel. [S1, U2] | The complete backed-up circuit/load map and the allocation of all necessary DPS/SC components. |

The planned ISD utility-maintenance boundary is separately described as extending from the first Fermilab switch/primary transformer to the primary-side terminals of the final transformer. [S5, p. 63] This proposed maintenance boundary must be mapped to actual equipment; it is not automatically the same boundary as detector grounding, lease ownership or DPS responsibility.

## 4. Power and authority boundaries

**TPC and PDS warm electronics have no UPS. DAQ, SC and DPS require UPS support, including the dependencies needed for their assigned functions.** [U2]

Working assumption confirmed by Manuel: **SC rack power shares the DAQ UPS-backed distribution in the CUC.** This closes the source-domain assumption for SC; individual circuits and load allocation remain to be detailed. It does not place SC racks in the UPS room or assign the DPS feed automatically. [U6]

Facility backup and cryogenics backup remain separate from the CUC DAQ/SC domain. SC use of the UPS was discussed without resizing. DAQ-barrack chillers are unbacked, so power continuity and cooling continuity require separate treatment. The July 250 kW basis and 350 kW quote remain unreconciled; neither is a final rating in this draft. [S1]

SDSTA, the construction project and Fermilab receiving organizations have different roles. The MOU and operations plan do not establish one universal transfer date or one owner for every system. ISD/SDS allocations in the FY25 plan are proposed operating arrangements. Record the responsible organization for the relevant installation/operating phase and its acceptance evidence. [S5, S6]

For PoF, assign ownership separately for normal laser operation, detector-equipment protection and personnel laser safety. The normal-control PLC choice does not settle the other two responsibilities. [S4]

## 5. What must be agreed before detailing a connection

For each interface, identify **the source, the receiver, the condition, the permitted action, the outcome check, and the owners**. Record which documents establish each item and which decisions remain open. One line should state its behavior on loss and recovery.

The source team confirms its condition and operating authority; the subsystem team confirms its limits and action endpoint; Manuel integrates the detector response; SC/DAQ confirm their assigned functions; the relevant facility and project authorities confirm operation, maintenance and acceptance. Named review contacts are proposed in [RESPONSIBILITIES.md](RESPONSIBILITIES.md).

A boundary is ready for detailed design when both sides agree what crosses it and who is responsible. Protocol and register choices follow that agreement.

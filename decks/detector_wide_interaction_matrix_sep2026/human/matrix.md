# DUNE interlocks in everyday detector language

Collaboration review v0.2 · 2026-09-08 · 40 of 40 source rows included

Discussion draft. The actions below are proposals or summaries of reviewed sources; use approved detector procedures for operation.

[Start here](README.md) · [Find your subsystem](subsystems.md) · [Search and filter](index.html) · [Review findings](review-notes.md)

Each row answers: what happened, what we propose, and how settled the source is. The detailed entries below include the reason, teams, stage differences and return conditions.

## What protects people or equipment?

| Situation | Proposed action | Source status |
|---|---|---|
| [S-001: People are working in an affected area](#s-001) | Apply the site's approved access and isolation procedure before work or energization. | Decision needed |
| [S-002: A hazardous laser is requested or its access checks fail](#s-002) | The laser-safety system allows or stops emission according to its approved design, regardless of PDS or run state. | Decision needed |
| [P-001: HV is requested before cryogenics confirms readiness](#p-001) | Do not start cathode HV until cryogenics and HV confirm the agreed conditions. A general 'filled' label is not enough. | Source + open details |
| [P-002: Liquid-argon level reaches the HV protection limit](#p-002) | Shut down the affected cathode HV through the agreed protection system and notify the affected teams. | Source + open details |
| [P-003: A relief valve opens or an agreed boiling-risk condition occurs](#p-003) | Shut down the affected cathode HV for the conditions listed in the approved cryogenics/HV rule. | Source + open details |
| [P-004: Cathode HV has an abnormal current excursion](#p-004) | Apply the approved HV shutdown rule, prevent an immediate restart and tell PDS and DAQ what happened. | Source + open details |
| [P-006: A fire alarm affects HV or detector power](#p-006) | Apply the approved fire response. The HVS interface calls for all HVS supplies off, including cathode and CRP/field-cage/APA bias. | Source + open details |
| [P-007: Smoke is detected in a rack](#p-007) | The rack protection shuts down the agreed loads and identifies the affected rack. | Source + open details |
| [P-008: Water is detected in a rack](#p-008) | Remove power from the loads specified by the rack's approved leak-protection rule. | Source + open details |
| [P-009: A rack overheats or loses required cooling](#p-009) | Apply the agreed rack or device response: shut down the affected loads when the protection condition is reached. | Source + open details |
| [P-010: A rack protection sensor or controller fails](#p-010) | Show the failed protection clearly and apply the response agreed for that particular failure. | Decision needed |
| [P-011: A PDS supply exceeds an agreed electrical limit](#p-011) | The approved protection switches off the affected supply or output group and confirms the resulting state. | Source + open details |
| [P-012: PDS power, readout or calibration equipment overheats](#p-012) | Apply the device's agreed automatic protective action and report which equipment is affected. | Source + open details |
| [P-017: A required protection signal becomes unreliable](#p-017) | Apply the agreed response for that protection signal and show what is missing. The response of equipment already on must be defined per rule. | Decision needed |
| [P-018: An APA, CRP or field-cage supply exceeds its safe limits](#p-018) | Switch off the affected output or the group approved by the owners, and check the measured result. | Source + open details |

## Which activities or changes must wait?

| Situation | Proposed action | Source status |
|---|---|---|
| [P-005: Cathode HV shuts down: linked field-cage outputs follow](#p-005) | Shut down the associated field-cage termination supplies as specified by the HVS interface. | Classification needs review |
| [O-001: Camera illumination and PDS are requested together](#o-001) | Block the second request. If light appears unexpectedly, switch off or block the light where possible, alert operations and mark the affected data. | Source conflict |
| [O-002: An external laser and PDS are requested together](#o-002) | Block the second request. Keep the laser's personnel-safety checks in force independently. | Source + open details |
| [O-004: Timing is not ready for the requested run](#o-004) | Block a new step that needs the missing timing. If timing fails during a run, follow the agreed run response and mark affected data. | Draft proposal |
| [O-005: A control connection or service is lost](#o-005) | Block commands that cannot be verified and show the unknown state. Required equipment protection must survive the failures specified for it. | Draft proposal |
| [O-006: Two people or systems request conflicting changes](#o-006) | Accept changes only from the agreed owner for that setting and activity; report why another request was refused. | Draft proposal |
| [H-001: Experts are using a detector region needed by a new run](#h-001) | Hold the new run or configuration until the test owner hands the region back, or run coordination agrees a controlled transition. | Source + open details |
| [O-008: A temporary protection exception is active](#o-008) | Show the affected rule, equipment, responsible person and expiry; hold normal operation unless the approved exception permits it. | Draft proposal |
| [O-009: We cannot identify which equipment a signal or command affects](#o-009) | Hold new activation until the connection is verified. An active protection fault follows its pre-agreed conservative response. | Draft proposal |
| [O-010: The cause of a protective shutdown has cleared](#o-010) | Have the responsible owner inspect and reset the affected system, confirm actual states and request a deliberate restart. | Draft proposal |
| [O-011: A requested HV or APA/CRP state differs from the agreed run or test](#o-011) | Follow the agreed sequence for that detector and activity. Hold a new transition that is not covered by the procedure. | Source + open details |

## What may continue with a data-quality record?

| Situation | Proposed action | Source status |
|---|---|---|
| [Q-001: A purity monitor operates while PDS records data](#q-001) | Keep PDS running. Record the affected time and detector region so analysis can identify those data. | Source conflict |
| [Q-002: PDS uses its own calibration light](#q-002) | Use the agreed PDS/DAQ calibration sequence and record the pulse settings, time and affected region. | Source + open details |
| [Q-003: HV changes during data taking](#q-003) | Record the HV state and affected interval; stop, pause or continue according to the agreed run plan. | Source + open details |
| [Q-004: Cryogenic conditions change within equipment-safe limits](#q-004) | Record the agreed indicators and affected interval so data quality can be assessed. | Source + open details |
| [Q-005: Cathode, APA, CRP or field-cage settings change the data conditions](#q-005) | Record measured settings and the time and region affected. Pause or continue according to the run plan; data quality alone does not demand a hardware trip. | Source + open details |

## What needs to operate together?

| Situation | Proposed action | Source status |
|---|---|---|
| [C-001: Power-over-fiber supplies the applicable vertical-drift PDS](#c-001) | Allow the required power-over-fiber source while PDS is active, with its own equipment and applicable laser-safety protection. | Source + open details |

## Which detector interactions still need a decision?

| Situation | Proposed action | Source status |
|---|---|---|
| [P-013: TPC electronics has a fan, heater or condensation problem](#p-013) | Use the response agreed for the particular problem. The available interface does not yet choose every alarm or shutdown action. | Decision needed |
| [P-014: Mains power is lost while anode bias and electronics are on](#p-014) | The required order is still a question for the electrical and detector owners. Do not claim that a software command alone guarantees it. | Decision needed |
| [P-015: Cold electronics is requested during filling or a warm test](#p-015) | Follow an owner-approved test or operating procedure. The matrix does not grant a new permission or impose one universal shutdown rule. | Decision needed |
| [P-016: The grounding monitor reports a problem](#p-016) | Alert the electrical/grounding expert and apply the approved response for the reported problem. | Decision needed |
| [O-003: A light source has no agreed classification](#o-003) | Hold the new conflicting activity until the source and PDS owners agree how it may be used. | Draft proposal |
| [O-007: A calibration or instrumentation device needs to move](#o-007) | Use the device's approved movement procedure and hold requests outside it. | Decision needed |
| [P-019: Cathode HV is lost while other detector systems remain on](#p-019) | Record actual states, notify experts and hold new unapproved transitions. Apply only the protective actions already approved for that detector configuration. | Decision needed |

## What did ProtoDUNE operators do?

| Situation | Proposed action | Source status |
|---|---|---|
| [H-002: ProtoDUNE shifters followed a manual HV-current recovery](#h-002) | Use the old sequence as evidence for discussion. Each proposed shutdown or data-taking step needs its own present-day justification. | Past practice only |

## Read the source status

- **Source + open details:** A reviewed source supports the general behavior. Production details still need agreement.
- **Source conflict:** The proposed rule and an existing document disagree. Owners must reconcile them.
- **Classification needs review:** The action is in a source, but the stated reason needs to be classified correctly.
- **Decision needed:** The responsible teams have not settled the required conditions or response.
- **Draft proposal:** A proposed operating rule that still needs agreement and detailed implementation.
- **Past practice only:** Historical behavior, not a present-day detector requirement.

## Details for each rule

<a id="s-001"></a>
### S-001 · People are working in an affected area

**Why it matters:** Protect people from the hazardous equipment in that work area.

**What we propose:** Apply the site's approved access and isolation procedure before work or energization.

**Before returning:** The authorized work-control role releases the area and the required equipment checks are repeated.

| Stage | What this means |
|---|---|
| Installation | Verify isolation before work. |
| Commissioning and integration | Check both access permission and the approved test plan. |
| Run | Use the approved operations access procedure. |

**Teams to agree the rule:** Installation, integration and run coordination; Rack power, cooling and electrical services; High voltage and field cage; Lasers, calibration and movable devices; Detector Protection System (DPS) and Slow Controls.

**Decision needed. Still to agree:** Name the exact site procedure, work boundary and responsible role.

**Evidence:** Site access, work-control and laser-safety requirements: exact references still needed.

<a id="s-002"></a>
### S-002 · A hazardous laser is requested or its access checks fail

**Why it matters:** Protect people near the laser and its beam path.

**What we propose:** The laser-safety system allows or stops emission according to its approved design, regardless of PDS or run state.

**Before returning:** The authorized laser-safety role confirms the conditions for restart.

| Stage | What this means |
|---|---|
| Installation | Use the approved laser installation procedure. |
| Commissioning and integration | Test the laser-safety checks before emission. |
| Run | Keep the laser-safety system active during calibration. |

**Teams to agree the rule:** Lasers, calibration and movable devices; Installation, integration and run coordination; Detector Protection System (DPS) and Slow Controls.

**Decision needed. Still to agree:** Identify the laser, access zone, protective devices and restart procedure.

**Evidence:** Site access, work-control and laser-safety requirements: exact references still needed.

<a id="p-001"></a>
### P-001 · HV is requested before cryogenics confirms readiness

**Why it matters:** The required liquid-argon coverage and cryogenic conditions must be established before HV starts.

**What we propose:** Do not start cathode HV until cryogenics and HV confirm the agreed conditions. A general 'filled' label is not enough.

**Before returning:** Confirm the actual cryogenic state and the approved HV startup checks.

| Stage | What this means |
|---|---|
| Installation | Keep HV isolated except for an explicitly approved test. |
| Commissioning and integration | Check cryogenic readiness before each authorized HV test. |
| Run | Require the agreed cryogenic confirmation before starting HV. |

**Teams to agree the rule:** Cryogenics; High voltage and field cage; Detector Protection System (DPS) and Slow Controls; Installation, integration and run coordination.

**Source + open details. Still to agree:** Agree the fill/coverage measurements, acceptable age of the readings, thresholds and affected region.

**Evidence:** [HVS interface, EDMS 3315615/1, section 5](https://edms.cern.ch/document/3315615/1); DPS interaction register v0.1 (working source).

<a id="p-002"></a>
### P-002 · Liquid-argon level reaches the HV protection limit

**Why it matters:** Loss of the required coverage creates an HV equipment-protection concern.

**What we propose:** Shut down the affected cathode HV through the agreed protection system and notify the affected teams.

**Before returning:** Investigate the level change; confirm safe conditions; deliberately restart through the approved sequence.

| Stage | What this means |
|---|---|
| Installation | Check the level-to-HV protection connection. |
| Commissioning and integration | Test the low-level shutdown at the approved scope. |
| Run | Keep the low-level protection active while HV is on. |

**Teams to agree the rule:** Cryogenics; High voltage and field cage; Photon detection system (PDS); Data acquisition, timing and data quality; Detector Protection System (DPS) and Slow Controls.

**Source + open details. Still to agree:** Confirm the reference geometry, threshold, response time and affected HV supply. A prototype number is not a universal detector limit.

**Evidence:** [HVS interface, EDMS 3315615/1, section 5](https://edms.cern.ch/document/3315615/1); ProtoDUNE shifter-channel evidence review, 3 September 2026.

<a id="p-003"></a>
### P-003 · A relief valve opens or an agreed boiling-risk condition occurs

**Why it matters:** These cryogenic conditions can make energized HV unsafe for equipment.

**What we propose:** Shut down the affected cathode HV for the conditions listed in the approved cryogenics/HV rule.

**Before returning:** Cryogenics and HV investigate, confirm recovery and authorize a deliberate restart.

| Stage | What this means |
|---|---|
| Installation | Identify and check the relevant cryogenic inputs. |
| Commissioning and integration | Test each agreed cryogenic shutdown condition. |
| Run | Keep the agreed cryogenic protection active. |

**Teams to agree the rule:** Cryogenics; High voltage and field cage; Detector Protection System (DPS) and Slow Controls; Installation, integration and run coordination; Data acquisition, timing and data quality.

**Source + open details. Still to agree:** List the qualifying conditions, signals, response times and shutdown scope.

**Evidence:** [HVS interface, EDMS 3315615/1, section 5](https://edms.cern.ch/document/3315615/1).

<a id="p-004"></a>
### P-004 · Cathode HV has an abnormal current excursion

**Why it matters:** An electrical fault may require rapid HV protection.

**What we propose:** Apply the approved HV shutdown rule, prevent an immediate restart and tell PDS and DAQ what happened.

**Before returning:** Keep the fault record; have the HV expert investigate and follow the approved recovery sequence.

| Stage | What this means |
|---|---|
| Installation | Establish test limits and the affected supply. |
| Commissioning and integration | Test the shutdown and retain the current record. |
| Run | Apply the approved automatic HV protection. |

**Teams to agree the rule:** High voltage and field cage; Cryogenics; Photon detection system (PDS); Data acquisition, timing and data quality; Detector Protection System (DPS) and Slow Controls.

**Source + open details. Still to agree:** Approve the current limit and duration for each operating state, the response time and linked outputs.

**Evidence:** [HVS interface, EDMS 3315615/1, section 5](https://edms.cern.ch/document/3315615/1); ProtoDUNE shifter-channel evidence review, 3 September 2026.

<a id="p-005"></a>
### P-005 · Cathode HV shuts down: linked field-cage outputs follow

**Why it matters:** The HVS interface specifies this coordinated shutdown to avoid incorrect HV current readings. That reason alone does not establish equipment damage.

**What we propose:** Shut down the associated field-cage termination supplies as specified by the HVS interface.

**Before returning:** Check both measured states and use the approved restoration order.

| Stage | What this means |
|---|---|
| Installation | Check which field-cage supplies belong to each cathode. |
| Commissioning and integration | Test the coordinated shutdown and the return sequence. |
| Run | Apply the agreed linked shutdown when cathode HV stops. |

**Teams to agree the rule:** High voltage and field cage; TPC electronics and APA/CRP teams; Detector Protection System (DPS) and Slow Controls.

**Classification needs review. Still to agree:** Confirm the linked channels and timing. Review the register's equipment-damage label against the stated source rationale.

**Evidence:** [HVS interface, EDMS 3315615/1, section 5](https://edms.cern.ch/document/3315615/1).

<a id="p-006"></a>
### P-006 · A fire alarm affects HV or detector power

**Why it matters:** Protect people and equipment under the facility's fire response.

**What we propose:** Apply the approved fire response. The HVS interface calls for all HVS supplies off, including cathode and CRP/field-cage/APA bias.

**Before returning:** Wait for the facility's release and the equipment owners' recovery checks.

| Stage | What this means |
|---|---|
| Installation | Map the fire response to the installed equipment. |
| Commissioning and integration | Test the approved fire-to-power actions. |
| Run | Apply the approved facility and HVS fire response. |

**Teams to agree the rule:** Rack power, cooling and electrical services; High voltage and field cage; TPC electronics and APA/CRP teams; Installation, integration and run coordination; Detector Protection System (DPS) and Slow Controls.

**Source + open details. Still to agree:** Agree detector-wide power zones, any essential loads and the full response beyond HVS.

**Evidence:** [HVS interface, EDMS 3315615/1, section 5](https://edms.cern.ch/document/3315615/1); [Rack-protection study, DUNE-doc-32655 v7](https://docs.dunescience.org/cgi-bin/private/ShowDocument?docid=32655).

<a id="p-007"></a>
### P-007 · Smoke is detected in a rack

**Why it matters:** Smoke may indicate a damaging rack fault or fire.

**What we propose:** The rack protection shuts down the agreed loads and identifies the affected rack.

**Before returning:** Inspect the rack and follow the authorized reset; power does not return just because the alarm clears.

| Stage | What this means |
|---|---|
| Installation | Check the sensor and the loads it protects. |
| Commissioning and integration | Test smoke detection and the actual power response. |
| Run | Keep rack protection available and report the shutdown cause. |

**Teams to agree the rule:** Rack power, cooling and electrical services; Detector Protection System (DPS) and Slow Controls; Installation, integration and run coordination; Photon detection system (PDS); TPC electronics and APA/CRP teams; Data acquisition, timing and data quality.

**Source + open details. Still to agree:** Confirm the production design, loads, essential exceptions and response time.

**Evidence:** [Rack-protection study, DUNE-doc-32655 v7](https://docs.dunescience.org/cgi-bin/private/ShowDocument?docid=32655).

<a id="p-008"></a>
### P-008 · Water is detected in a rack

**Why it matters:** Water can damage energized equipment.

**What we propose:** Remove power from the loads specified by the rack's approved leak-protection rule.

**Before returning:** Inspect the leak and equipment before an authorized restart.

| Stage | What this means |
|---|---|
| Installation | Check leak-sensor placement and power connections. |
| Commissioning and integration | Test detection and the affected power outputs. |
| Run | Keep the approved leak protection active. |

**Teams to agree the rule:** Rack power, cooling and electrical services; Detector Protection System (DPS) and Slow Controls; Installation, integration and run coordination; Photon detection system (PDS); TPC electronics and APA/CRP teams; Data acquisition, timing and data quality.

**Source + open details. Still to agree:** Agree sensor locations, affected loads, timing and inspection criteria.

**Evidence:** [Rack-protection study, DUNE-doc-32655 v7](https://docs.dunescience.org/cgi-bin/private/ShowDocument?docid=32655).

<a id="p-009"></a>
### P-009 · A rack overheats or loses required cooling

**Why it matters:** Equipment may exceed its safe temperature.

**What we propose:** Apply the agreed rack or device response: shut down the affected loads when the protection condition is reached.

**Before returning:** Restore cooling, inspect as required and confirm temperatures before restart.

| Stage | What this means |
|---|---|
| Installation | Check cooling and temperature monitoring. |
| Commissioning and integration | Test cooling loss and overtemperature response. |
| Run | Protect loads using their agreed limits. |

**Teams to agree the rule:** Rack power, cooling and electrical services; Detector Protection System (DPS) and Slow Controls; Photon detection system (PDS); TPC electronics and APA/CRP teams; Data acquisition, timing and data quality.

**Source + open details. Still to agree:** Set limits and delays for the actual equipment; identify any essential loads allowed to remain powered.

**Evidence:** [Rack-protection study, DUNE-doc-32655 v7](https://docs.dunescience.org/cgi-bin/private/ShowDocument?docid=32655); [The ProtoDUNE Single Phase Detector Control System (2019)](https://doi.org/10.1051/epjconf/201921401024).

<a id="p-010"></a>
### P-010 · A rack protection sensor or controller fails

**Why it matters:** Equipment must not silently lose a protection function it relies on.

**What we propose:** Show the failed protection clearly and apply the response agreed for that particular failure.

**Before returning:** Repair and test the protection before returning affected equipment to its approved operating state.

| Stage | What this means |
|---|---|
| Installation | Identify failure indications and check connections. |
| Commissioning and integration | Disconnect or simulate each relevant failed input. |
| Run | Use the approved response for the failed protection path. |

**Teams to agree the rule:** Rack power, cooling and electrical services; Detector Protection System (DPS) and Slow Controls; Installation, integration and run coordination.

**Decision needed. Still to agree:** Specify which failures stop running loads. Losing a monitoring display is not automatically the same as losing local protection.

**Evidence:** [Rack-protection study, DUNE-doc-32655 v7](https://docs.dunescience.org/cgi-bin/private/ShowDocument?docid=32655); [The CERN Detector Safety System for the LHC Experiments](https://cds.cern.ch/record/1054106).

<a id="p-011"></a>
### P-011 · A PDS supply exceeds an agreed electrical limit

**Why it matters:** Abnormal current or voltage can damage PDS equipment.

**What we propose:** The approved protection switches off the affected supply or output group and confirms the resulting state.

**Before returning:** PDS investigates, clears the cause and authorizes the required checks before restart.

| Stage | What this means |
|---|---|
| Installation | Check supply-to-channel connections and limits. |
| Commissioning and integration | Test the electrical fault response and readback. |
| Run | Apply the agreed PDS supply protection. |

**Teams to agree the rule:** Photon detection system (PDS); Rack power, cooling and electrical services; Detector Protection System (DPS) and Slow Controls; Data acquisition, timing and data quality.

**Source + open details. Still to agree:** Specify limits, duration, output grouping and reset conditions for each supply.

**Evidence:** [PDS interface, EDMS 3309688/1, section 5 (contains disputed optical rules)](https://edms.cern.ch/document/3309688/1).

<a id="p-012"></a>
### P-012 · PDS power, readout or calibration equipment overheats

**Why it matters:** Temperature can threaten PDS equipment, including power-over-fiber hardware.

**What we propose:** Apply the device's agreed automatic protective action and report which equipment is affected.

**Before returning:** Restore the cooling or repair the fault; confirm the device's recovery conditions.

| Stage | What this means |
|---|---|
| Installation | Check the installed sensors and cooling. |
| Commissioning and integration | Test each device's overtemperature response. |
| Run | Keep device protection active during physics and calibration. |

**Teams to agree the rule:** Photon detection system (PDS); Rack power, cooling and electrical services; Lasers, calibration and movable devices; Detector Protection System (DPS) and Slow Controls; Data acquisition, timing and data quality.

**Source + open details. Still to agree:** Identify sensors, limits, affected outputs and recovery for each device.

**Evidence:** [PDS interface, EDMS 3309688/1, section 5 (contains disputed optical rules)](https://edms.cern.ch/document/3309688/1).

<a id="p-013"></a>
### P-013 · TPC electronics has a fan, heater or condensation problem

**Why it matters:** The consequences differ between loss of cooling, heater faults and condensation.

**What we propose:** Use the response agreed for the particular problem. The available interface does not yet choose every alarm or shutdown action.

**Before returning:** The electronics owner confirms the problem is resolved and the appropriate checks pass.

| Stage | What this means |
|---|---|
| Installation | Check fans, heaters and environmental measurements. |
| Commissioning and integration | Establish the response for each type of fault. |
| Run | Apply the agreed device-specific actions. |

**Teams to agree the rule:** TPC electronics and APA/CRP teams; Rack power, cooling and electrical services; Cryogenics; Detector Protection System (DPS) and Slow Controls; Data acquisition, timing and data quality.

**Decision needed. Still to agree:** Decide separately which conditions need attention and which must switch off equipment, with limits and timing.

**Evidence:** [TPC electronics/BDE interface, EDMS 3293079/1](https://edms.cern.ch/document/3293079/1).

<a id="p-014"></a>
### P-014 · Mains power is lost while anode bias and electronics are on

**Why it matters:** If one must switch off before the other, that order must remain possible during the power failure.

**What we propose:** The required order is still a question for the electrical and detector owners. Do not claim that a software command alone guarantees it.

**Before returning:** Follow the approved recovery after power returns and check the actual equipment states.

| Stage | What this means |
|---|---|
| Installation | Record power connections and any backup supplies. |
| Commissioning and integration | Measure the behavior during a representative power-loss test. |
| Run | Use only the power-loss behavior that owners have accepted. |

**Teams to agree the rule:** Rack power, cooling and electrical services; TPC electronics and APA/CRP teams; High voltage and field cage; Detector Protection System (DPS) and Slow Controls.

**Decision needed. Still to agree:** Establish whether an order is required; then measure how long the electronics remains supported and how long bias removal takes.

**Evidence:** SC/DPS software integration plan, interaction matrix and power-loss example.

<a id="p-015"></a>
### P-015 · Cold electronics is requested during filling or a warm test

**Why it matters:** The allowed temperature and immersion conditions have not been established for every electronics system.

**What we propose:** Follow an owner-approved test or operating procedure. The matrix does not grant a new permission or impose one universal shutdown rule.

**Before returning:** Confirm the allowed environment and the electronics checks for that procedure.

| Stage | What this means |
|---|---|
| Installation | Use the approved checkout conditions. |
| Commissioning and integration | Review each intended cryogenic test state. |
| Run | Use the electronics' approved operating conditions. |

**Teams to agree the rule:** TPC electronics and APA/CRP teams; Cryogenics; Detector Protection System (DPS) and Slow Controls; Installation, integration and run coordination.

**Decision needed. Still to agree:** List the permitted warm, gas, liquid, filling and draining conditions for each relevant device.

**Evidence:** [TPC electronics/BDE interface, EDMS 3293079/1](https://edms.cern.ch/document/3293079/1).

<a id="p-016"></a>
### P-016 · The grounding monitor reports a problem

**Why it matters:** A warning about grounding may affect noise, equipment or both; the action depends on the actual condition.

**What we propose:** Alert the electrical/grounding expert and apply the approved response for the reported problem.

**Before returning:** The responsible owner investigates and confirms the conditions for return.

| Stage | What this means |
|---|---|
| Installation | Check grounding and monitor installation. |
| Commissioning and integration | Classify warnings and test the agreed responses. |
| Run | Use the agreed escalation and protection rules. |

**Teams to agree the rule:** Rack power, cooling and electrical services; High voltage and field cage; TPC electronics and APA/CRP teams; Photon detection system (PDS); Detector Protection System (DPS) and Slow Controls; Installation, integration and run coordination.

**Decision needed. Still to agree:** Distinguish noise warnings from damaging faults and decide which equipment, if any, must stop.

**Evidence:** [The ProtoDUNE Single Phase Detector Control System (2019)](https://doi.org/10.1051/epjconf/201921401024); ProtoDUNE shifter-channel evidence review, 3 September 2026.

<a id="p-017"></a>
### P-017 · A required protection signal becomes unreliable

**Why it matters:** A missing or unreliable reading cannot serve as confirmation that a protected condition is satisfied.

**What we propose:** Apply the agreed response for that protection signal and show what is missing. The response of equipment already on must be defined per rule.

**Before returning:** Repair the signal path and verify its operation before releasing the affected restriction.

| Stage | What this means |
|---|---|
| Installation | Check sensor identity, connections and fault indication. |
| Commissioning and integration | Test missing, delayed and contradictory protection inputs. |
| Run | Keep protection failures visible and follow their agreed response. |

**Teams to agree the rule:** Detector Protection System (DPS) and Slow Controls; Rack power, cooling and electrical services; Cryogenics; High voltage and field cage; Photon detection system (PDS); TPC electronics and APA/CRP teams; Data acquisition, timing and data quality.

**Decision needed. Still to agree:** Agree which signal failures block startup or stop equipment, and the acceptable detection time.

**Evidence:** [The CERN Detector Safety System for the LHC Experiments](https://cds.cern.ch/record/1054106); SC/DPS software integration plan, interaction matrix and power-loss example.

<a id="o-001"></a>
### O-001 · Camera illumination and PDS are requested together

**Why it matters:** These activities must take turns in the affected optical region.

**What we propose:** Block the second request. If light appears unexpectedly, switch off or block the light where possible, alert operations and mark the affected data.

**Before returning:** Confirm illumination is actually off and allow the agreed settling time before PDS resumes.

| Stage | What this means |
|---|---|
| Installation | Record ownership of any light and PDS test. |
| Commissioning and integration | Test both request orders and the light-off handback. |
| Run | Keep camera illumination and the agreed PDS state from overlapping. |

**Teams to agree the rule:** Cameras and illumination; Photon detection system (PDS); High voltage and field cage; Data acquisition, timing and data quality; Installation, integration and run coordination; Detector Protection System (DPS) and Slow Controls.

**Source conflict. Still to agree:** Define the excluded PDS state and affected region. Reconcile the old interface's bias-off wording; a damage-based PDS trip is not established by the historical exclusion alone.

**Evidence:** [PDS interface, EDMS 3309688/1, section 5 (contains disputed optical rules)](https://edms.cern.ch/document/3309688/1); ProtoDUNE shifter-channel evidence review, 3 September 2026.

<a id="o-002"></a>
### O-002 · An external laser and PDS are requested together

**Why it matters:** Ionisation or alignment laser activity must take turns with PDS in the affected region.

**What we propose:** Block the second request. Keep the laser's personnel-safety checks in force independently.

**Before returning:** Confirm emission is off and the shutter is in its approved closed state before PDS returns; record any accidental overlap.

| Stage | What this means |
|---|---|
| Installation | Coordinate laser work with PDS tests. |
| Commissioning and integration | Test both request orders and the laser handback. |
| Run | Keep external-laser emission and the agreed PDS state from overlapping. |

**Teams to agree the rule:** Lasers, calibration and movable devices; Photon detection system (PDS); Data acquisition, timing and data quality; Installation, integration and run coordination; Detector Protection System (DPS) and Slow Controls.

**Source + open details. Still to agree:** Define the excluded PDS state, optical region, confirmation signals and settling time.

**Evidence:** ProtoDUNE shifter-channel evidence review, 3 September 2026.

<a id="q-001"></a>
### Q-001 · A purity monitor operates while PDS records data

**Why it matters:** The overlap reduces PDS measurement quality; it does not require PDS bias removal in this draft.

**What we propose:** Keep PDS running. Record the affected time and detector region so analysis can identify those data.

**Before returning:** No PDS restart is required for this overlap. Record when the effect ends; arrange quiet intervals when scientifically useful.

| Stage | What this means |
|---|---|
| Installation | Label any affected engineering data. |
| Commissioning and integration | Allow and record deliberate overlap. |
| Run | Allow overlap and mark affected data; PDS bias stays on. |

**Teams to agree the rule:** Purity monitors; Cryogenics; Photon detection system (PDS); Data acquisition, timing and data quality; Installation, integration and run coordination; Detector Protection System (DPS) and Slow Controls.

**Source conflict. Still to agree:** Agree timing precision, affected channels and settling time. Correct the old PDS interface text that requires bias off.

**Evidence:** [The ProtoDUNE Single Phase Detector Control System (2019)](https://doi.org/10.1051/epjconf/201921401024); [PDS interface, EDMS 3309688/1, section 5 (contains disputed optical rules)](https://edms.cern.ch/document/3309688/1); ProtoDUNE shifter-channel evidence review, 3 September 2026; DPS interaction register v0.1 (working source).

<a id="q-002"></a>
### Q-002 · PDS uses its own calibration light

**Why it matters:** This light is intentional and must be identifiable in the data.

**What we propose:** Use the agreed PDS/DAQ calibration sequence and record the pulse settings, time and affected region.

**Before returning:** End calibration and confirm the agreed return to ordinary data taking.

| Stage | What this means |
|---|---|
| Installation | Use the agreed calibration checkout. |
| Commissioning and integration | Record the test configuration and light pulses. |
| Run | Use a declared calibration activity and label its data. |

**Teams to agree the rule:** Photon detection system (PDS); Lasers, calibration and movable devices; Data acquisition, timing and data quality; Detector Protection System (DPS) and Slow Controls.

**Source + open details. Still to agree:** Agree allowed run types, recorded information and settling time.

**Evidence:** [PDS interface, EDMS 3309688/1, section 5 (contains disputed optical rules)](https://edms.cern.ch/document/3309688/1).

<a id="c-001"></a>
### C-001 · Power-over-fiber supplies the applicable vertical-drift PDS

**Why it matters:** These PDS channels need power-over-fiber to operate.

**What we propose:** Allow the required power-over-fiber source while PDS is active, with its own equipment and applicable laser-safety protection.

**Before returning:** Follow the PDS power and protection checks for the affected channels.

| Stage | What this means |
|---|---|
| Installation | Check the power-over-fiber connections and protection. |
| Commissioning and integration | Test the dependency and device protection. |
| Run | Keep the required power source available to its PDS channels. |

**Teams to agree the rule:** Photon detection system (PDS); Rack power, cooling and electrical services; Detector Protection System (DPS) and Slow Controls; Data acquisition, timing and data quality.

**Source + open details. Still to agree:** Identify the supplied channels, protection limits and recovery. Keep this source distinct from an external calibration laser.

**Evidence:** [PDS interface, EDMS 3309688/1, section 5 (contains disputed optical rules)](https://edms.cern.ch/document/3309688/1); DPS interaction register v0.1 (working source).

<a id="o-003"></a>
### O-003 · A light source has no agreed classification

**Why it matters:** Its effect on PDS and its allowed use are unknown.

**What we propose:** Hold the new conflicting activity until the source and PDS owners agree how it may be used.

**Before returning:** Name the light source, its purpose and its affected region, then follow the agreed rule.

| Stage | What this means |
|---|---|
| Installation | Identify each installed light source. |
| Commissioning and integration | Review a new source before testing it with other systems. |
| Run | Allow only activities covered by an agreed rule. |

**Teams to agree the rule:** Cameras and illumination; Lasers, calibration and movable devices; Photon detection system (PDS); Data acquisition, timing and data quality; Installation, integration and run coordination; Detector Protection System (DPS) and Slow Controls.

**Draft proposal. Still to agree:** Complete the light-source list; distinguish camera light, external laser, PDS calibration and power-over-fiber.

**Evidence:** DPS interaction register v0.1 (working source).

<a id="q-003"></a>
### Q-003 · HV changes during data taking

**Why it matters:** A ramp, trip or recovery changes the conditions represented by the data.

**What we propose:** Record the HV state and affected interval; stop, pause or continue according to the agreed run plan.

**Before returning:** Confirm the required stable conditions before returning to the intended physics run.

| Stage | What this means |
|---|---|
| Installation | Label any HV test data. |
| Commissioning and integration | Record before-and-after states around a ramp. |
| Run | Apply the agreed run response and mark affected data. |

**Teams to agree the rule:** High voltage and field cage; Photon detection system (PDS); TPC electronics and APA/CRP teams; Data acquisition, timing and data quality; Detector Protection System (DPS) and Slow Controls.

**Source + open details. Still to agree:** Agree acceptable physics conditions and the run response. HV equipment protection is handled by the separate protection rules.

**Evidence:** [HVS interface, EDMS 3315615/1, section 5](https://edms.cern.ch/document/3315615/1); ProtoDUNE shifter-channel evidence review, 3 September 2026.

<a id="q-004"></a>
### Q-004 · Cryogenic conditions change within equipment-safe limits

**Why it matters:** Pressure, temperature, purity or circulation changes can affect the interpretation of data.

**What we propose:** Record the agreed indicators and affected interval so data quality can be assessed.

**Before returning:** Record when the conditions again meet the agreed physics criteria.

| Stage | What this means |
|---|---|
| Installation | Record relevant conditions during tests. |
| Commissioning and integration | Study and label the effects of cryogenic changes. |
| Run | Mark affected data according to the agreed physics criteria. |

**Teams to agree the rule:** Cryogenics; Purity monitors; TPC electronics and APA/CRP teams; Photon detection system (PDS); Data acquisition, timing and data quality.

**Source + open details. Still to agree:** Set data-quality criteria separately from equipment-protection limits.

**Evidence:** [The ProtoDUNE Single Phase Detector Control System (2019)](https://doi.org/10.1051/epjconf/201921401024); DPS interaction register v0.1 (working source).

<a id="o-004"></a>
### O-004 · Timing is not ready for the requested run

**Why it matters:** The requested synchronized data taking may not work correctly.

**What we propose:** Block a new step that needs the missing timing. If timing fails during a run, follow the agreed run response and mark affected data.

**Before returning:** Restore and verify timing, then follow the agreed reconfiguration procedure.

| Stage | What this means |
|---|---|
| Installation | Check timing connections and device identity. |
| Commissioning and integration | Test loss and restoration of timing. |
| Run | Require the timing needed by the selected run type. |

**Teams to agree the rule:** Data acquisition, timing and data quality; Photon detection system (PDS); TPC electronics and APA/CRP teams; Detector Protection System (DPS) and Slow Controls.

**Draft proposal. Still to agree:** Agree the timing-ready definition and the in-run stop, pause or continue policy.

**Evidence:** SC/DPS software integration plan, interaction matrix and power-loss example.

<a id="o-005"></a>
### O-005 · A control connection or service is lost

**Why it matters:** Commands may no longer reach equipment and displayed values may be old.

**What we propose:** Block commands that cannot be verified and show the unknown state. Required equipment protection must survive the failures specified for it.

**Before returning:** Read the actual equipment state after reconnection; do not replay old power commands automatically.

| Stage | What this means |
|---|---|
| Installation | Identify the connections needed for each test. |
| Commissioning and integration | Test connection loss and reconnection. |
| Run | Show unknown states and follow the agreed run response. |

**Teams to agree the rule:** Detector Protection System (DPS) and Slow Controls; Data acquisition, timing and data quality; Photon detection system (PDS); TPC electronics and APA/CRP teams; Rack power, cooling and electrical services.

**Draft proposal. Still to agree:** Agree how long each reading remains usable and what an ongoing run should do.

**Evidence:** SC/DPS software integration plan, interaction matrix and power-loss example.

<a id="o-006"></a>
### O-006 · Two people or systems request conflicting changes

**Why it matters:** Equipment should not receive competing instructions.

**What we propose:** Accept changes only from the agreed owner for that setting and activity; report why another request was refused.

**Before returning:** Resolve who owns the task and confirm the actual settings before proceeding.

| Stage | What this means |
|---|---|
| Installation | Name the person in charge of each checkout. |
| Commissioning and integration | Test conflicting requests and explicit handover. |
| Run | Use the agreed ownership of power, protection and run settings. |

**Teams to agree the rule:** Data acquisition, timing and data quality; Detector Protection System (DPS) and Slow Controls; Photon detection system (PDS); TPC electronics and APA/CRP teams; Installation, integration and run coordination.

**Draft proposal. Still to agree:** Name the owner for each type of setting and the expert-work handover. Seeing a value does not grant permission to change it.

**Evidence:** SC/DPS software integration plan, interaction matrix and power-loss example.

<a id="o-007"></a>
### O-007 · A calibration or instrumentation device needs to move

**Why it matters:** Allowed motion depends on detector state, position and the particular device.

**What we propose:** Use the device's approved movement procedure and hold requests outside it.

**Before returning:** Confirm the actual position and the checks needed before other detector activities resume.

| Stage | What this means |
|---|---|
| Installation | Record the installed device and movement limits. |
| Commissioning and integration | Test movement only in the approved detector conditions. |
| Run | Use the agreed movement and return procedure. |

**Teams to agree the rule:** Lasers, calibration and movable devices; High voltage and field cage; TPC electronics and APA/CRP teams; Photon detection system (PDS); Installation, integration and run coordination; Detector Protection System (DPS) and Slow Controls; Data acquisition, timing and data quality.

**Decision needed. Still to agree:** List the devices, allowed positions, HV conditions and any credible damage mechanism.

**Evidence:** DPS interaction register v0.1 (working source).

<a id="h-001"></a>
### H-001 · Experts are using a detector region needed by a new run

**Why it matters:** A new run could interrupt an active test or overwrite its settings.

**What we propose:** Hold the new run or configuration until the test owner hands the region back, or run coordination agrees a controlled transition.

**Before returning:** Record who has finished, which equipment is ready and who now has control.

| Stage | What this means |
|---|---|
| Installation | Name the work owner and affected area. |
| Commissioning and integration | Make each test reservation visible. |
| Run | Check ownership before starting or reconfiguring a run. |

**Teams to agree the rule:** Installation, integration and run coordination; Data acquisition, timing and data quality; Photon detection system (PDS); TPC electronics and APA/CRP teams; High voltage and field cage; Lasers, calibration and movable devices; Detector Protection System (DPS) and Slow Controls.

**Source + open details. Still to agree:** Agree how reservations, expiry and handback are recorded.

**Evidence:** ProtoDUNE shifter-channel evidence review, 3 September 2026; SC/DPS software integration plan, interaction matrix and power-loss example.

<a id="h-002"></a>
### H-002 · ProtoDUNE shifters followed a manual HV-current recovery

**Why it matters:** This records what operators did in one historical configuration.

**What we propose:** Use the old sequence as evidence for discussion. Each proposed shutdown or data-taking step needs its own present-day justification.

**Before returning:** Use the currently approved procedure for the detector concerned.

| Stage | What this means |
|---|---|
| Installation | No additional operating permission follows from this history. |
| Commissioning and integration | Use the history to identify questions and tests. |
| Run | Follow the approved current recovery procedure. |

**Teams to agree the rule:** High voltage and field cage; Photon detection system (PDS); Data acquisition, timing and data quality; Installation, integration and run coordination; Detector Protection System (DPS) and Slow Controls.

**Past practice only. Still to agree:** Determine which historical steps protected equipment and which coordinated data taking; do not copy the sequence as a universal DUNE rule.

**Evidence:** ProtoDUNE shifter-channel evidence review, 3 September 2026.

<a id="o-008"></a>
### O-008 · A temporary protection exception is active

**Why it matters:** The detector is not in its ordinary approved operating configuration.

**What we propose:** Show the affected rule, equipment, responsible person and expiry; hold normal operation unless the approved exception permits it.

**Before returning:** Remove the exception and complete the required checks before ordinary operation resumes.

| Stage | What this means |
|---|---|
| Installation | Keep exceptions within approved work control. |
| Commissioning and integration | Record the test scope, owner, expiry and restoration checks. |
| Run | Keep any approved exception visible to operations. |

**Teams to agree the rule:** Installation, integration and run coordination; Detector Protection System (DPS) and Slow Controls; Rack power, cooling and electrical services; Data acquisition, timing and data quality.

**Draft proposal. Still to agree:** Specify which exceptions are allowed and who may approve them. Existing non-bypassable safety functions remain in force.

**Evidence:** DPS interaction register v0.1 (working source); SC/DPS software integration plan, interaction matrix and power-loss example.

<a id="o-009"></a>
### O-009 · We cannot identify which equipment a signal or command affects

**Why it matters:** An action could reach the wrong channel, rack or detector region.

**What we propose:** Hold new activation until the connection is verified. An active protection fault follows its pre-agreed conservative response.

**Before returning:** Correct and verify the equipment mapping before releasing the restriction.

| Stage | What this means |
|---|---|
| Installation | Record and verify installed connections. |
| Commissioning and integration | Test signals and commands against the actual equipment. |
| Run | Require a verified mapping for the requested activity. |

**Teams to agree the rule:** Installation, integration and run coordination; Detector Protection System (DPS) and Slow Controls; Rack power, cooling and electrical services; Data acquisition, timing and data quality; High voltage and field cage; Photon detection system (PDS); TPC electronics and APA/CRP teams.

**Draft proposal. Still to agree:** Agree the installed-equipment record and the response when that record is missing or inconsistent.

**Evidence:** SC/DPS software integration plan, interaction matrix and power-loss example; DPS interaction register v0.1 (working source).

<a id="o-010"></a>
### O-010 · The cause of a protective shutdown has cleared

**Why it matters:** The equipment and run configuration still need to be checked before use.

**What we propose:** Have the responsible owner inspect and reset the affected system, confirm actual states and request a deliberate restart.

**Before returning:** DAQ applies and checks the required configuration before operations resumes the intended run.

| Stage | What this means |
|---|---|
| Installation | Recheck the work and isolation conditions. |
| Commissioning and integration | Test recovery as well as the original fault. |
| Run | Confirm recovery and fresh configuration before resuming. |

**Teams to agree the rule:** Installation, integration and run coordination; Detector Protection System (DPS) and Slow Controls; High voltage and field cage; Photon detection system (PDS); TPC electronics and APA/CRP teams; Rack power, cooling and electrical services; Data acquisition, timing and data quality.

**Draft proposal. Still to agree:** Name who may reset each rule and the required inspection, sequence and run checks.

**Evidence:** SC/DPS software integration plan, interaction matrix and power-loss example; DPS interaction register v0.1 (working source).

<a id="p-018"></a>
### P-018 · An APA, CRP or field-cage supply exceeds its safe limits

**Why it matters:** An electrical or thermal fault can damage the equipment served by that supply.

**What we propose:** Switch off the affected output or the group approved by the owners, and check the measured result.

**Before returning:** Investigate the fault and follow the approved supply and detector recovery checks.

| Stage | What this means |
|---|---|
| Installation | Verify supply-to-detector connections and protection settings. |
| Commissioning and integration | Test the affected output and any approved linked group. |
| Run | Use the agreed supply protection and recovery. |

**Teams to agree the rule:** High voltage and field cage; TPC electronics and APA/CRP teams; Rack power, cooling and electrical services; Detector Protection System (DPS) and Slow Controls; Data acquisition, timing and data quality.

**Source + open details. Still to agree:** Agree limits, shared output groups, response time and any required linked actions.

**Evidence:** [HVS interface, EDMS 3315615/1, section 5](https://edms.cern.ch/document/3315615/1); [TPC electronics/BDE interface, EDMS 3293079/1](https://edms.cern.ch/document/3293079/1).

<a id="p-019"></a>
### P-019 · Cathode HV is lost while other detector systems remain on

**Why it matters:** The required response of APA/CRP bias, TPC electronics and affected PDS is not established by one universal rule.

**What we propose:** Record actual states, notify experts and hold new unapproved transitions. Apply only the protective actions already approved for that detector configuration.

**Before returning:** Owners confirm the allowed combination of states and the recovery sequence.

| Stage | What this means |
|---|---|
| Installation | Identify the independent supplies and affected connections. |
| Commissioning and integration | Study the proposed linked actions in approved tests. |
| Run | Use approved actions; an open row grants no new operating permission. |

**Teams to agree the rule:** High voltage and field cage; TPC electronics and APA/CRP teams; Photon detection system (PDS); Rack power, cooling and electrical services; Detector Protection System (DPS) and Slow Controls; Data acquisition, timing and data quality; Installation, integration and run coordination.

**Decision needed. Still to agree:** Resolve horizontal-drift and vertical-drift cases separately, including relevant PDS power arrangements, damage mechanism, timing and shutdown order.

**Evidence:** [HVS interface, EDMS 3315615/1, section 5](https://edms.cern.ch/document/3315615/1); ProtoDUNE shifter-channel evidence review, 3 September 2026; DPS interaction register v0.1 (working source).

<a id="o-011"></a>
### O-011 · A requested HV or APA/CRP state differs from the agreed run or test

**Why it matters:** A valid commissioning combination may be unsuitable for the intended physics run.

**What we propose:** Follow the agreed sequence for that detector and activity. Hold a new transition that is not covered by the procedure.

**Before returning:** Have the relevant owners reconcile the measured states before declaring the detector ready for that run.

| Stage | What this means |
|---|---|
| Installation | Use the approved checkout sequence. |
| Commissioning and integration | Use a named test plan and record each state change. |
| Run | Require the combination of states agreed for the selected run. |

**Teams to agree the rule:** High voltage and field cage; TPC electronics and APA/CRP teams; Photon detection system (PDS); Data acquisition, timing and data quality; Installation, integration and run coordination; Detector Protection System (DPS) and Slow Controls.

**Source + open details. Still to agree:** Approve the combinations, ordering and stability checks for each stage and detector type.

**Evidence:** ProtoDUNE shifter-channel evidence review, 3 September 2026; DPS interaction register v0.1 (working source).

<a id="q-005"></a>
### Q-005 · Cathode, APA, CRP or field-cage settings change the data conditions

**Why it matters:** Analysis needs to know which detector configuration produced the data.

**What we propose:** Record measured settings and the time and region affected. Pause or continue according to the run plan; data quality alone does not demand a hardware trip.

**Before returning:** Record the return to the intended stable configuration.

| Stage | What this means |
|---|---|
| Installation | Label the test settings in engineering data. |
| Commissioning and integration | Record data before and after each approved change. |
| Run | Mark any departure from the configuration agreed for the run. |

**Teams to agree the rule:** High voltage and field cage; TPC electronics and APA/CRP teams; Photon detection system (PDS); Data acquisition, timing and data quality; Lasers, calibration and movable devices; Detector Protection System (DPS) and Slow Controls.

**Source + open details. Still to agree:** Agree physics ranges, stability time and the boundary between runs or data intervals. Coordinate this row with the HV-specific row Q-003.

**Evidence:** ProtoDUNE shifter-channel evidence review, 3 September 2026; DPS interaction register v0.1 (working source).

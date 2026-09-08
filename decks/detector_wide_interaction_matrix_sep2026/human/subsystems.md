# Find your subsystem

Collaboration review v0.2 · 2026-09-08

Start with your team. These are the teams to consult, not an already approved assignment of responsibility. A rule can appear under several teams because they need to agree it together.

[Start here](README.md) · [Full matrix](matrix.md) · [Searchable guide](index.html) · [Review form](review-form.md)

## Cryogenics

Tell HV when the cryostat is ready, and when that changes.

**Tell the other teams:** The agreed fill and coverage check, relevant cryogenic faults, and changes that affect data quality.

**Agree with the other teams:** Which measurements authorize HV; which conditions stop it; how quickly; and what must be checked before restart.

| Rule to review | What it means for coordination |
|---|---|
| [P-001: HV is requested before cryogenics confirms readiness](matrix.md#p-001) | Do not start cathode HV until cryogenics and HV confirm the agreed conditions. A general 'filled' label is not enough. |
| [P-002: Liquid-argon level reaches the HV protection limit](matrix.md#p-002) | Shut down the affected cathode HV through the agreed protection system and notify the affected teams. |
| [P-003: A relief valve opens or an agreed boiling-risk condition occurs](matrix.md#p-003) | Shut down the affected cathode HV for the conditions listed in the approved cryogenics/HV rule. |
| [P-004: Cathode HV has an abnormal current excursion](matrix.md#p-004) | Apply the approved HV shutdown rule, prevent an immediate restart and tell PDS and DAQ what happened. |
| [P-013: TPC electronics has a fan, heater or condensation problem](matrix.md#p-013) | Use the response agreed for the particular problem. The available interface does not yet choose every alarm or shutdown action. |
| [P-015: Cold electronics is requested during filling or a warm test](matrix.md#p-015) | Follow an owner-approved test or operating procedure. The matrix does not grant a new permission or impose one universal shutdown rule. |
| [P-017: A required protection signal becomes unreliable](matrix.md#p-017) | Apply the agreed response for that protection signal and show what is missing. The response of equipment already on must be defined per rule. |
| [Q-001: A purity monitor operates while PDS records data](matrix.md#q-001) | Keep PDS running. Record the affected time and detector region so analysis can identify those data. |
| [Q-004: Cryogenic conditions change within equipment-safe limits](matrix.md#q-004) | Record the agreed indicators and affected interval so data quality can be assessed. |

## High voltage and field cage

Start only with the required cryogenic and detector checks.

**Tell the other teams:** Requested and measured states, ramping, faults, affected detector region, and the reason for a shutdown.

**Agree with the other teams:** The approved startup and shutdown sequence, linked field-cage outputs, and the still-open response of other systems to a cathode trip.

| Rule to review | What it means for coordination |
|---|---|
| [S-001: People are working in an affected area](matrix.md#s-001) | Apply the site's approved access and isolation procedure before work or energization. |
| [P-001: HV is requested before cryogenics confirms readiness](matrix.md#p-001) | Do not start cathode HV until cryogenics and HV confirm the agreed conditions. A general 'filled' label is not enough. |
| [P-002: Liquid-argon level reaches the HV protection limit](matrix.md#p-002) | Shut down the affected cathode HV through the agreed protection system and notify the affected teams. |
| [P-003: A relief valve opens or an agreed boiling-risk condition occurs](matrix.md#p-003) | Shut down the affected cathode HV for the conditions listed in the approved cryogenics/HV rule. |
| [P-004: Cathode HV has an abnormal current excursion](matrix.md#p-004) | Apply the approved HV shutdown rule, prevent an immediate restart and tell PDS and DAQ what happened. |
| [P-005: Cathode HV shuts down: linked field-cage outputs follow](matrix.md#p-005) | Shut down the associated field-cage termination supplies as specified by the HVS interface. |
| [P-006: A fire alarm affects HV or detector power](matrix.md#p-006) | Apply the approved fire response. The HVS interface calls for all HVS supplies off, including cathode and CRP/field-cage/APA bias. |
| [P-014: Mains power is lost while anode bias and electronics are on](matrix.md#p-014) | The required order is still a question for the electrical and detector owners. Do not claim that a software command alone guarantees it. |
| [P-016: The grounding monitor reports a problem](matrix.md#p-016) | Alert the electrical/grounding expert and apply the approved response for the reported problem. |
| [P-017: A required protection signal becomes unreliable](matrix.md#p-017) | Apply the agreed response for that protection signal and show what is missing. The response of equipment already on must be defined per rule. |
| [O-001: Camera illumination and PDS are requested together](matrix.md#o-001) | Block the second request. If light appears unexpectedly, switch off or block the light where possible, alert operations and mark the affected data. |
| [Q-003: HV changes during data taking](matrix.md#q-003) | Record the HV state and affected interval; stop, pause or continue according to the agreed run plan. |
| [O-007: A calibration or instrumentation device needs to move](matrix.md#o-007) | Use the device's approved movement procedure and hold requests outside it. |
| [H-001: Experts are using a detector region needed by a new run](matrix.md#h-001) | Hold the new run or configuration until the test owner hands the region back, or run coordination agrees a controlled transition. |
| [H-002: ProtoDUNE shifters followed a manual HV-current recovery](matrix.md#h-002) | Use the old sequence as evidence for discussion. Each proposed shutdown or data-taking step needs its own present-day justification. |
| [O-009: We cannot identify which equipment a signal or command affects](matrix.md#o-009) | Hold new activation until the connection is verified. An active protection fault follows its pre-agreed conservative response. |
| [O-010: The cause of a protective shutdown has cleared](matrix.md#o-010) | Have the responsible owner inspect and reset the affected system, confirm actual states and request a deliberate restart. |
| [P-018: An APA, CRP or field-cage supply exceeds its safe limits](matrix.md#p-018) | Switch off the affected output or the group approved by the owners, and check the measured result. |
| [P-019: Cathode HV is lost while other detector systems remain on](matrix.md#p-019) | Record actual states, notify experts and hold new unapproved transitions. Apply only the protective actions already approved for that detector configuration. |
| [O-011: A requested HV or APA/CRP state differs from the agreed run or test](matrix.md#o-011) | Follow the agreed sequence for that detector and activity. Hold a new transition that is not covered by the procedure. |
| [Q-005: Cathode, APA, CRP or field-cage settings change the data conditions](matrix.md#q-005) | Record measured settings and the time and region affected. Pause or continue according to the run plan; data quality alone does not demand a hardware trip. |

## TPC electronics and APA/CRP teams

Agree which combinations of detector states are allowed.

**Tell the other teams:** Actual APA/CRP bias and electronics states, readiness, cooling problems, and the detector region affected.

**Agree with the other teams:** Allowed states during filling and tests; response to cathode or mains-power loss; and which fan, heater or condensation problems need a shutdown.

| Rule to review | What it means for coordination |
|---|---|
| [P-005: Cathode HV shuts down: linked field-cage outputs follow](matrix.md#p-005) | Shut down the associated field-cage termination supplies as specified by the HVS interface. |
| [P-006: A fire alarm affects HV or detector power](matrix.md#p-006) | Apply the approved fire response. The HVS interface calls for all HVS supplies off, including cathode and CRP/field-cage/APA bias. |
| [P-007: Smoke is detected in a rack](matrix.md#p-007) | The rack protection shuts down the agreed loads and identifies the affected rack. |
| [P-008: Water is detected in a rack](matrix.md#p-008) | Remove power from the loads specified by the rack's approved leak-protection rule. |
| [P-009: A rack overheats or loses required cooling](matrix.md#p-009) | Apply the agreed rack or device response: shut down the affected loads when the protection condition is reached. |
| [P-013: TPC electronics has a fan, heater or condensation problem](matrix.md#p-013) | Use the response agreed for the particular problem. The available interface does not yet choose every alarm or shutdown action. |
| [P-014: Mains power is lost while anode bias and electronics are on](matrix.md#p-014) | The required order is still a question for the electrical and detector owners. Do not claim that a software command alone guarantees it. |
| [P-015: Cold electronics is requested during filling or a warm test](matrix.md#p-015) | Follow an owner-approved test or operating procedure. The matrix does not grant a new permission or impose one universal shutdown rule. |
| [P-016: The grounding monitor reports a problem](matrix.md#p-016) | Alert the electrical/grounding expert and apply the approved response for the reported problem. |
| [P-017: A required protection signal becomes unreliable](matrix.md#p-017) | Apply the agreed response for that protection signal and show what is missing. The response of equipment already on must be defined per rule. |
| [Q-003: HV changes during data taking](matrix.md#q-003) | Record the HV state and affected interval; stop, pause or continue according to the agreed run plan. |
| [Q-004: Cryogenic conditions change within equipment-safe limits](matrix.md#q-004) | Record the agreed indicators and affected interval so data quality can be assessed. |
| [O-004: Timing is not ready for the requested run](matrix.md#o-004) | Block a new step that needs the missing timing. If timing fails during a run, follow the agreed run response and mark affected data. |
| [O-005: A control connection or service is lost](matrix.md#o-005) | Block commands that cannot be verified and show the unknown state. Required equipment protection must survive the failures specified for it. |
| [O-006: Two people or systems request conflicting changes](matrix.md#o-006) | Accept changes only from the agreed owner for that setting and activity; report why another request was refused. |
| [O-007: A calibration or instrumentation device needs to move](matrix.md#o-007) | Use the device's approved movement procedure and hold requests outside it. |
| [H-001: Experts are using a detector region needed by a new run](matrix.md#h-001) | Hold the new run or configuration until the test owner hands the region back, or run coordination agrees a controlled transition. |
| [O-009: We cannot identify which equipment a signal or command affects](matrix.md#o-009) | Hold new activation until the connection is verified. An active protection fault follows its pre-agreed conservative response. |
| [O-010: The cause of a protective shutdown has cleared](matrix.md#o-010) | Have the responsible owner inspect and reset the affected system, confirm actual states and request a deliberate restart. |
| [P-018: An APA, CRP or field-cage supply exceeds its safe limits](matrix.md#p-018) | Switch off the affected output or the group approved by the owners, and check the measured result. |
| [P-019: Cathode HV is lost while other detector systems remain on](matrix.md#p-019) | Record actual states, notify experts and hold new unapproved transitions. Apply only the protective actions already approved for that detector configuration. |
| [O-011: A requested HV or APA/CRP state differs from the agreed run or test](matrix.md#o-011) | Follow the agreed sequence for that detector and activity. Hold a new transition that is not covered by the procedure. |
| [Q-005: Cathode, APA, CRP or field-cage settings change the data conditions](matrix.md#q-005) | Record measured settings and the time and region affected. Pause or continue according to the run plan; data quality alone does not demand a hardware trip. |

## Photon detection system (PDS)

Take turns with camera lights and external lasers; keep running during purity measurements.

**Tell the other teams:** The exact PDS state that excludes external light, the region affected, equipment faults, and readiness to resume.

**Agree with the other teams:** Light-off confirmation and settling time; purity-monitor data labels; equipment protection limits; and the conflicting wording in the old PDS interface.

| Rule to review | What it means for coordination |
|---|---|
| [P-002: Liquid-argon level reaches the HV protection limit](matrix.md#p-002) | Shut down the affected cathode HV through the agreed protection system and notify the affected teams. |
| [P-004: Cathode HV has an abnormal current excursion](matrix.md#p-004) | Apply the approved HV shutdown rule, prevent an immediate restart and tell PDS and DAQ what happened. |
| [P-007: Smoke is detected in a rack](matrix.md#p-007) | The rack protection shuts down the agreed loads and identifies the affected rack. |
| [P-008: Water is detected in a rack](matrix.md#p-008) | Remove power from the loads specified by the rack's approved leak-protection rule. |
| [P-009: A rack overheats or loses required cooling](matrix.md#p-009) | Apply the agreed rack or device response: shut down the affected loads when the protection condition is reached. |
| [P-011: A PDS supply exceeds an agreed electrical limit](matrix.md#p-011) | The approved protection switches off the affected supply or output group and confirms the resulting state. |
| [P-012: PDS power, readout or calibration equipment overheats](matrix.md#p-012) | Apply the device's agreed automatic protective action and report which equipment is affected. |
| [P-016: The grounding monitor reports a problem](matrix.md#p-016) | Alert the electrical/grounding expert and apply the approved response for the reported problem. |
| [P-017: A required protection signal becomes unreliable](matrix.md#p-017) | Apply the agreed response for that protection signal and show what is missing. The response of equipment already on must be defined per rule. |
| [O-001: Camera illumination and PDS are requested together](matrix.md#o-001) | Block the second request. If light appears unexpectedly, switch off or block the light where possible, alert operations and mark the affected data. |
| [O-002: An external laser and PDS are requested together](matrix.md#o-002) | Block the second request. Keep the laser's personnel-safety checks in force independently. |
| [Q-001: A purity monitor operates while PDS records data](matrix.md#q-001) | Keep PDS running. Record the affected time and detector region so analysis can identify those data. |
| [Q-002: PDS uses its own calibration light](matrix.md#q-002) | Use the agreed PDS/DAQ calibration sequence and record the pulse settings, time and affected region. |
| [C-001: Power-over-fiber supplies the applicable vertical-drift PDS](matrix.md#c-001) | Allow the required power-over-fiber source while PDS is active, with its own equipment and applicable laser-safety protection. |
| [O-003: A light source has no agreed classification](matrix.md#o-003) | Hold the new conflicting activity until the source and PDS owners agree how it may be used. |
| [Q-003: HV changes during data taking](matrix.md#q-003) | Record the HV state and affected interval; stop, pause or continue according to the agreed run plan. |
| [Q-004: Cryogenic conditions change within equipment-safe limits](matrix.md#q-004) | Record the agreed indicators and affected interval so data quality can be assessed. |
| [O-004: Timing is not ready for the requested run](matrix.md#o-004) | Block a new step that needs the missing timing. If timing fails during a run, follow the agreed run response and mark affected data. |
| [O-005: A control connection or service is lost](matrix.md#o-005) | Block commands that cannot be verified and show the unknown state. Required equipment protection must survive the failures specified for it. |
| [O-006: Two people or systems request conflicting changes](matrix.md#o-006) | Accept changes only from the agreed owner for that setting and activity; report why another request was refused. |
| [O-007: A calibration or instrumentation device needs to move](matrix.md#o-007) | Use the device's approved movement procedure and hold requests outside it. |
| [H-001: Experts are using a detector region needed by a new run](matrix.md#h-001) | Hold the new run or configuration until the test owner hands the region back, or run coordination agrees a controlled transition. |
| [H-002: ProtoDUNE shifters followed a manual HV-current recovery](matrix.md#h-002) | Use the old sequence as evidence for discussion. Each proposed shutdown or data-taking step needs its own present-day justification. |
| [O-009: We cannot identify which equipment a signal or command affects](matrix.md#o-009) | Hold new activation until the connection is verified. An active protection fault follows its pre-agreed conservative response. |
| [O-010: The cause of a protective shutdown has cleared](matrix.md#o-010) | Have the responsible owner inspect and reset the affected system, confirm actual states and request a deliberate restart. |
| [P-019: Cathode HV is lost while other detector systems remain on](matrix.md#p-019) | Record actual states, notify experts and hold new unapproved transitions. Apply only the protective actions already approved for that detector configuration. |
| [O-011: A requested HV or APA/CRP state differs from the agreed run or test](matrix.md#o-011) | Follow the agreed sequence for that detector and activity. Hold a new transition that is not covered by the procedure. |
| [Q-005: Cathode, APA, CRP or field-cage settings change the data conditions](matrix.md#q-005) | Record measured settings and the time and region affected. Pause or continue according to the run plan; data quality alone does not demand a hardware trip. |

## Cameras and illumination

Check with PDS before turning on camera lights.

**Tell the other teams:** Whether illumination is actually on or off, which lights are involved, and where their light can reach.

**Agree with the other teams:** How the second request is blocked, how light-off is confirmed, and what to do if light appears unexpectedly. The rule concerns illumination; camera power alone is not a proven conflict.

| Rule to review | What it means for coordination |
|---|---|
| [O-001: Camera illumination and PDS are requested together](matrix.md#o-001) | Block the second request. If light appears unexpectedly, switch off or block the light where possible, alert operations and mark the affected data. |
| [O-003: A light source has no agreed classification](matrix.md#o-003) | Hold the new conflicting activity until the source and PDS owners agree how it may be used. |

## Lasers, calibration and movable devices

Name the source and its purpose before applying a light rule.

**Tell the other teams:** External-laser emission and shutter state, PDS calibration activity, or device position and movement.

**Agree with the other teams:** The affected region, PDS handoff, laser-safety checks, permitted movement and the calibration record needed by analysis.

| Rule to review | What it means for coordination |
|---|---|
| [S-001: People are working in an affected area](matrix.md#s-001) | Apply the site's approved access and isolation procedure before work or energization. |
| [S-002: A hazardous laser is requested or its access checks fail](matrix.md#s-002) | The laser-safety system allows or stops emission according to its approved design, regardless of PDS or run state. |
| [P-012: PDS power, readout or calibration equipment overheats](matrix.md#p-012) | Apply the device's agreed automatic protective action and report which equipment is affected. |
| [O-002: An external laser and PDS are requested together](matrix.md#o-002) | Block the second request. Keep the laser's personnel-safety checks in force independently. |
| [Q-002: PDS uses its own calibration light](matrix.md#q-002) | Use the agreed PDS/DAQ calibration sequence and record the pulse settings, time and affected region. |
| [O-003: A light source has no agreed classification](matrix.md#o-003) | Hold the new conflicting activity until the source and PDS owners agree how it may be used. |
| [O-007: A calibration or instrumentation device needs to move](matrix.md#o-007) | Use the device's approved movement procedure and hold requests outside it. |
| [H-001: Experts are using a detector region needed by a new run](matrix.md#h-001) | Hold the new run or configuration until the test owner hands the region back, or run coordination agrees a controlled transition. |
| [Q-005: Cathode, APA, CRP or field-cage settings change the data conditions](matrix.md#q-005) | Record measured settings and the time and region affected. Pause or continue according to the run plan; data quality alone does not demand a hardware trip. |

## Purity monitors

Publish when and where a purity measurement affects PDS data.

**Tell the other teams:** Actual start and stop times, affected region, and whether the activity record is reliable.

**Agree with the other teams:** Timing precision, the affected PDS channels and any settling time. Arrange a quiet interval only when a measurement needs one.

| Rule to review | What it means for coordination |
|---|---|
| [Q-001: A purity monitor operates while PDS records data](matrix.md#q-001) | Keep PDS running. Record the affected time and detector region so analysis can identify those data. |
| [Q-004: Cryogenic conditions change within equipment-safe limits](matrix.md#q-004) | Record the agreed indicators and affected interval so data quality can be assessed. |

## Rack power, cooling and electrical services

Protect the affected equipment and explain what lost power.

**Tell the other teams:** Rack or supply faults, cooling and power availability, the loads affected, and the state of protection equipment.

**Agree with the other teams:** Which loads switch off, which essential loads may stay on, response time, power-loss ordering and inspection before restart.

| Rule to review | What it means for coordination |
|---|---|
| [S-001: People are working in an affected area](matrix.md#s-001) | Apply the site's approved access and isolation procedure before work or energization. |
| [P-006: A fire alarm affects HV or detector power](matrix.md#p-006) | Apply the approved fire response. The HVS interface calls for all HVS supplies off, including cathode and CRP/field-cage/APA bias. |
| [P-007: Smoke is detected in a rack](matrix.md#p-007) | The rack protection shuts down the agreed loads and identifies the affected rack. |
| [P-008: Water is detected in a rack](matrix.md#p-008) | Remove power from the loads specified by the rack's approved leak-protection rule. |
| [P-009: A rack overheats or loses required cooling](matrix.md#p-009) | Apply the agreed rack or device response: shut down the affected loads when the protection condition is reached. |
| [P-010: A rack protection sensor or controller fails](matrix.md#p-010) | Show the failed protection clearly and apply the response agreed for that particular failure. |
| [P-011: A PDS supply exceeds an agreed electrical limit](matrix.md#p-011) | The approved protection switches off the affected supply or output group and confirms the resulting state. |
| [P-012: PDS power, readout or calibration equipment overheats](matrix.md#p-012) | Apply the device's agreed automatic protective action and report which equipment is affected. |
| [P-013: TPC electronics has a fan, heater or condensation problem](matrix.md#p-013) | Use the response agreed for the particular problem. The available interface does not yet choose every alarm or shutdown action. |
| [P-014: Mains power is lost while anode bias and electronics are on](matrix.md#p-014) | The required order is still a question for the electrical and detector owners. Do not claim that a software command alone guarantees it. |
| [P-016: The grounding monitor reports a problem](matrix.md#p-016) | Alert the electrical/grounding expert and apply the approved response for the reported problem. |
| [P-017: A required protection signal becomes unreliable](matrix.md#p-017) | Apply the agreed response for that protection signal and show what is missing. The response of equipment already on must be defined per rule. |
| [C-001: Power-over-fiber supplies the applicable vertical-drift PDS](matrix.md#c-001) | Allow the required power-over-fiber source while PDS is active, with its own equipment and applicable laser-safety protection. |
| [O-005: A control connection or service is lost](matrix.md#o-005) | Block commands that cannot be verified and show the unknown state. Required equipment protection must survive the failures specified for it. |
| [O-008: A temporary protection exception is active](matrix.md#o-008) | Show the affected rule, equipment, responsible person and expiry; hold normal operation unless the approved exception permits it. |
| [O-009: We cannot identify which equipment a signal or command affects](matrix.md#o-009) | Hold new activation until the connection is verified. An active protection fault follows its pre-agreed conservative response. |
| [O-010: The cause of a protective shutdown has cleared](matrix.md#o-010) | Have the responsible owner inspect and reset the affected system, confirm actual states and request a deliberate restart. |
| [P-018: An APA, CRP or field-cage supply exceeds its safe limits](matrix.md#p-018) | Switch off the affected output or the group approved by the owners, and check the measured result. |
| [P-019: Cathode HV is lost while other detector systems remain on](matrix.md#p-019) | Record actual states, notify experts and hold new unapproved transitions. Apply only the protective actions already approved for that detector configuration. |

## Data acquisition, timing and data quality

Know whether a run may start and which data need a label.

**Tell the other teams:** Run type, timing readiness, configuration identity, the detector region in use and the recorded activity intervals.

**Agree with the other teams:** When to stop, pause or continue a run; who can change settings; how analysis receives quality information; and fresh configuration after recovery.

| Rule to review | What it means for coordination |
|---|---|
| [P-002: Liquid-argon level reaches the HV protection limit](matrix.md#p-002) | Shut down the affected cathode HV through the agreed protection system and notify the affected teams. |
| [P-003: A relief valve opens or an agreed boiling-risk condition occurs](matrix.md#p-003) | Shut down the affected cathode HV for the conditions listed in the approved cryogenics/HV rule. |
| [P-004: Cathode HV has an abnormal current excursion](matrix.md#p-004) | Apply the approved HV shutdown rule, prevent an immediate restart and tell PDS and DAQ what happened. |
| [P-007: Smoke is detected in a rack](matrix.md#p-007) | The rack protection shuts down the agreed loads and identifies the affected rack. |
| [P-008: Water is detected in a rack](matrix.md#p-008) | Remove power from the loads specified by the rack's approved leak-protection rule. |
| [P-009: A rack overheats or loses required cooling](matrix.md#p-009) | Apply the agreed rack or device response: shut down the affected loads when the protection condition is reached. |
| [P-011: A PDS supply exceeds an agreed electrical limit](matrix.md#p-011) | The approved protection switches off the affected supply or output group and confirms the resulting state. |
| [P-012: PDS power, readout or calibration equipment overheats](matrix.md#p-012) | Apply the device's agreed automatic protective action and report which equipment is affected. |
| [P-013: TPC electronics has a fan, heater or condensation problem](matrix.md#p-013) | Use the response agreed for the particular problem. The available interface does not yet choose every alarm or shutdown action. |
| [P-017: A required protection signal becomes unreliable](matrix.md#p-017) | Apply the agreed response for that protection signal and show what is missing. The response of equipment already on must be defined per rule. |
| [O-001: Camera illumination and PDS are requested together](matrix.md#o-001) | Block the second request. If light appears unexpectedly, switch off or block the light where possible, alert operations and mark the affected data. |
| [O-002: An external laser and PDS are requested together](matrix.md#o-002) | Block the second request. Keep the laser's personnel-safety checks in force independently. |
| [Q-001: A purity monitor operates while PDS records data](matrix.md#q-001) | Keep PDS running. Record the affected time and detector region so analysis can identify those data. |
| [Q-002: PDS uses its own calibration light](matrix.md#q-002) | Use the agreed PDS/DAQ calibration sequence and record the pulse settings, time and affected region. |
| [C-001: Power-over-fiber supplies the applicable vertical-drift PDS](matrix.md#c-001) | Allow the required power-over-fiber source while PDS is active, with its own equipment and applicable laser-safety protection. |
| [O-003: A light source has no agreed classification](matrix.md#o-003) | Hold the new conflicting activity until the source and PDS owners agree how it may be used. |
| [Q-003: HV changes during data taking](matrix.md#q-003) | Record the HV state and affected interval; stop, pause or continue according to the agreed run plan. |
| [Q-004: Cryogenic conditions change within equipment-safe limits](matrix.md#q-004) | Record the agreed indicators and affected interval so data quality can be assessed. |
| [O-004: Timing is not ready for the requested run](matrix.md#o-004) | Block a new step that needs the missing timing. If timing fails during a run, follow the agreed run response and mark affected data. |
| [O-005: A control connection or service is lost](matrix.md#o-005) | Block commands that cannot be verified and show the unknown state. Required equipment protection must survive the failures specified for it. |
| [O-006: Two people or systems request conflicting changes](matrix.md#o-006) | Accept changes only from the agreed owner for that setting and activity; report why another request was refused. |
| [O-007: A calibration or instrumentation device needs to move](matrix.md#o-007) | Use the device's approved movement procedure and hold requests outside it. |
| [H-001: Experts are using a detector region needed by a new run](matrix.md#h-001) | Hold the new run or configuration until the test owner hands the region back, or run coordination agrees a controlled transition. |
| [H-002: ProtoDUNE shifters followed a manual HV-current recovery](matrix.md#h-002) | Use the old sequence as evidence for discussion. Each proposed shutdown or data-taking step needs its own present-day justification. |
| [O-008: A temporary protection exception is active](matrix.md#o-008) | Show the affected rule, equipment, responsible person and expiry; hold normal operation unless the approved exception permits it. |
| [O-009: We cannot identify which equipment a signal or command affects](matrix.md#o-009) | Hold new activation until the connection is verified. An active protection fault follows its pre-agreed conservative response. |
| [O-010: The cause of a protective shutdown has cleared](matrix.md#o-010) | Have the responsible owner inspect and reset the affected system, confirm actual states and request a deliberate restart. |
| [P-018: An APA, CRP or field-cage supply exceeds its safe limits](matrix.md#p-018) | Switch off the affected output or the group approved by the owners, and check the measured result. |
| [P-019: Cathode HV is lost while other detector systems remain on](matrix.md#p-019) | Record actual states, notify experts and hold new unapproved transitions. Apply only the protective actions already approved for that detector configuration. |
| [O-011: A requested HV or APA/CRP state differs from the agreed run or test](matrix.md#o-011) | Follow the agreed sequence for that detector and activity. Hold a new transition that is not covered by the procedure. |
| [Q-005: Cathode, APA, CRP or field-cage settings change the data conditions](matrix.md#q-005) | Record measured settings and the time and region affected. Pause or continue according to the run plan; data quality alone does not demand a hardware trip. |

## Installation, integration and run coordination

Make it clear who is using each part of the detector.

**Tell the other teams:** Active work, the named test owner, affected area, agreed exceptions and the handback to operations.

**Agree with the other teams:** The work and test procedure for each stage, exception expiry, escalation and the checks before returning to a run.

| Rule to review | What it means for coordination |
|---|---|
| [S-001: People are working in an affected area](matrix.md#s-001) | Apply the site's approved access and isolation procedure before work or energization. |
| [S-002: A hazardous laser is requested or its access checks fail](matrix.md#s-002) | The laser-safety system allows or stops emission according to its approved design, regardless of PDS or run state. |
| [P-001: HV is requested before cryogenics confirms readiness](matrix.md#p-001) | Do not start cathode HV until cryogenics and HV confirm the agreed conditions. A general 'filled' label is not enough. |
| [P-003: A relief valve opens or an agreed boiling-risk condition occurs](matrix.md#p-003) | Shut down the affected cathode HV for the conditions listed in the approved cryogenics/HV rule. |
| [P-006: A fire alarm affects HV or detector power](matrix.md#p-006) | Apply the approved fire response. The HVS interface calls for all HVS supplies off, including cathode and CRP/field-cage/APA bias. |
| [P-007: Smoke is detected in a rack](matrix.md#p-007) | The rack protection shuts down the agreed loads and identifies the affected rack. |
| [P-008: Water is detected in a rack](matrix.md#p-008) | Remove power from the loads specified by the rack's approved leak-protection rule. |
| [P-010: A rack protection sensor or controller fails](matrix.md#p-010) | Show the failed protection clearly and apply the response agreed for that particular failure. |
| [P-015: Cold electronics is requested during filling or a warm test](matrix.md#p-015) | Follow an owner-approved test or operating procedure. The matrix does not grant a new permission or impose one universal shutdown rule. |
| [P-016: The grounding monitor reports a problem](matrix.md#p-016) | Alert the electrical/grounding expert and apply the approved response for the reported problem. |
| [O-001: Camera illumination and PDS are requested together](matrix.md#o-001) | Block the second request. If light appears unexpectedly, switch off or block the light where possible, alert operations and mark the affected data. |
| [O-002: An external laser and PDS are requested together](matrix.md#o-002) | Block the second request. Keep the laser's personnel-safety checks in force independently. |
| [Q-001: A purity monitor operates while PDS records data](matrix.md#q-001) | Keep PDS running. Record the affected time and detector region so analysis can identify those data. |
| [O-003: A light source has no agreed classification](matrix.md#o-003) | Hold the new conflicting activity until the source and PDS owners agree how it may be used. |
| [O-006: Two people or systems request conflicting changes](matrix.md#o-006) | Accept changes only from the agreed owner for that setting and activity; report why another request was refused. |
| [O-007: A calibration or instrumentation device needs to move](matrix.md#o-007) | Use the device's approved movement procedure and hold requests outside it. |
| [H-001: Experts are using a detector region needed by a new run](matrix.md#h-001) | Hold the new run or configuration until the test owner hands the region back, or run coordination agrees a controlled transition. |
| [H-002: ProtoDUNE shifters followed a manual HV-current recovery](matrix.md#h-002) | Use the old sequence as evidence for discussion. Each proposed shutdown or data-taking step needs its own present-day justification. |
| [O-008: A temporary protection exception is active](matrix.md#o-008) | Show the affected rule, equipment, responsible person and expiry; hold normal operation unless the approved exception permits it. |
| [O-009: We cannot identify which equipment a signal or command affects](matrix.md#o-009) | Hold new activation until the connection is verified. An active protection fault follows its pre-agreed conservative response. |
| [O-010: The cause of a protective shutdown has cleared](matrix.md#o-010) | Have the responsible owner inspect and reset the affected system, confirm actual states and request a deliberate restart. |
| [P-019: Cathode HV is lost while other detector systems remain on](matrix.md#p-019) | Record actual states, notify experts and hold new unapproved transitions. Apply only the protective actions already approved for that detector configuration. |
| [O-011: A requested HV or APA/CRP state differs from the agreed run or test](matrix.md#o-011) | Follow the agreed sequence for that detector and activity. Hold a new transition that is not covered by the procedure. |

## Detector Protection System (DPS) and Slow Controls

Make the agreed action happen and show a useful reason.

**Tell the other teams:** Protection availability, blocked requests, actual equipment state, faults and the steps still needed for restart.

**Agree with the other teams:** A named subsystem owner, the affected equipment, the required response time and a test of each action. Keep required protection working through the failures it must handle.

| Rule to review | What it means for coordination |
|---|---|
| [S-001: People are working in an affected area](matrix.md#s-001) | Apply the site's approved access and isolation procedure before work or energization. |
| [S-002: A hazardous laser is requested or its access checks fail](matrix.md#s-002) | The laser-safety system allows or stops emission according to its approved design, regardless of PDS or run state. |
| [P-001: HV is requested before cryogenics confirms readiness](matrix.md#p-001) | Do not start cathode HV until cryogenics and HV confirm the agreed conditions. A general 'filled' label is not enough. |
| [P-002: Liquid-argon level reaches the HV protection limit](matrix.md#p-002) | Shut down the affected cathode HV through the agreed protection system and notify the affected teams. |
| [P-003: A relief valve opens or an agreed boiling-risk condition occurs](matrix.md#p-003) | Shut down the affected cathode HV for the conditions listed in the approved cryogenics/HV rule. |
| [P-004: Cathode HV has an abnormal current excursion](matrix.md#p-004) | Apply the approved HV shutdown rule, prevent an immediate restart and tell PDS and DAQ what happened. |
| [P-005: Cathode HV shuts down: linked field-cage outputs follow](matrix.md#p-005) | Shut down the associated field-cage termination supplies as specified by the HVS interface. |
| [P-006: A fire alarm affects HV or detector power](matrix.md#p-006) | Apply the approved fire response. The HVS interface calls for all HVS supplies off, including cathode and CRP/field-cage/APA bias. |
| [P-007: Smoke is detected in a rack](matrix.md#p-007) | The rack protection shuts down the agreed loads and identifies the affected rack. |
| [P-008: Water is detected in a rack](matrix.md#p-008) | Remove power from the loads specified by the rack's approved leak-protection rule. |
| [P-009: A rack overheats or loses required cooling](matrix.md#p-009) | Apply the agreed rack or device response: shut down the affected loads when the protection condition is reached. |
| [P-010: A rack protection sensor or controller fails](matrix.md#p-010) | Show the failed protection clearly and apply the response agreed for that particular failure. |
| [P-011: A PDS supply exceeds an agreed electrical limit](matrix.md#p-011) | The approved protection switches off the affected supply or output group and confirms the resulting state. |
| [P-012: PDS power, readout or calibration equipment overheats](matrix.md#p-012) | Apply the device's agreed automatic protective action and report which equipment is affected. |
| [P-013: TPC electronics has a fan, heater or condensation problem](matrix.md#p-013) | Use the response agreed for the particular problem. The available interface does not yet choose every alarm or shutdown action. |
| [P-014: Mains power is lost while anode bias and electronics are on](matrix.md#p-014) | The required order is still a question for the electrical and detector owners. Do not claim that a software command alone guarantees it. |
| [P-015: Cold electronics is requested during filling or a warm test](matrix.md#p-015) | Follow an owner-approved test or operating procedure. The matrix does not grant a new permission or impose one universal shutdown rule. |
| [P-016: The grounding monitor reports a problem](matrix.md#p-016) | Alert the electrical/grounding expert and apply the approved response for the reported problem. |
| [P-017: A required protection signal becomes unreliable](matrix.md#p-017) | Apply the agreed response for that protection signal and show what is missing. The response of equipment already on must be defined per rule. |
| [O-001: Camera illumination and PDS are requested together](matrix.md#o-001) | Block the second request. If light appears unexpectedly, switch off or block the light where possible, alert operations and mark the affected data. |
| [O-002: An external laser and PDS are requested together](matrix.md#o-002) | Block the second request. Keep the laser's personnel-safety checks in force independently. |
| [Q-001: A purity monitor operates while PDS records data](matrix.md#q-001) | Keep PDS running. Record the affected time and detector region so analysis can identify those data. |
| [Q-002: PDS uses its own calibration light](matrix.md#q-002) | Use the agreed PDS/DAQ calibration sequence and record the pulse settings, time and affected region. |
| [C-001: Power-over-fiber supplies the applicable vertical-drift PDS](matrix.md#c-001) | Allow the required power-over-fiber source while PDS is active, with its own equipment and applicable laser-safety protection. |
| [O-003: A light source has no agreed classification](matrix.md#o-003) | Hold the new conflicting activity until the source and PDS owners agree how it may be used. |
| [Q-003: HV changes during data taking](matrix.md#q-003) | Record the HV state and affected interval; stop, pause or continue according to the agreed run plan. |
| [O-004: Timing is not ready for the requested run](matrix.md#o-004) | Block a new step that needs the missing timing. If timing fails during a run, follow the agreed run response and mark affected data. |
| [O-005: A control connection or service is lost](matrix.md#o-005) | Block commands that cannot be verified and show the unknown state. Required equipment protection must survive the failures specified for it. |
| [O-006: Two people or systems request conflicting changes](matrix.md#o-006) | Accept changes only from the agreed owner for that setting and activity; report why another request was refused. |
| [O-007: A calibration or instrumentation device needs to move](matrix.md#o-007) | Use the device's approved movement procedure and hold requests outside it. |
| [H-001: Experts are using a detector region needed by a new run](matrix.md#h-001) | Hold the new run or configuration until the test owner hands the region back, or run coordination agrees a controlled transition. |
| [H-002: ProtoDUNE shifters followed a manual HV-current recovery](matrix.md#h-002) | Use the old sequence as evidence for discussion. Each proposed shutdown or data-taking step needs its own present-day justification. |
| [O-008: A temporary protection exception is active](matrix.md#o-008) | Show the affected rule, equipment, responsible person and expiry; hold normal operation unless the approved exception permits it. |
| [O-009: We cannot identify which equipment a signal or command affects](matrix.md#o-009) | Hold new activation until the connection is verified. An active protection fault follows its pre-agreed conservative response. |
| [O-010: The cause of a protective shutdown has cleared](matrix.md#o-010) | Have the responsible owner inspect and reset the affected system, confirm actual states and request a deliberate restart. |
| [P-018: An APA, CRP or field-cage supply exceeds its safe limits](matrix.md#p-018) | Switch off the affected output or the group approved by the owners, and check the measured result. |
| [P-019: Cathode HV is lost while other detector systems remain on](matrix.md#p-019) | Record actual states, notify experts and hold new unapproved transitions. Apply only the protective actions already approved for that detector configuration. |
| [O-011: A requested HV or APA/CRP state differs from the agreed run or test](matrix.md#o-011) | Follow the agreed sequence for that detector and activity. Hold a new transition that is not covered by the procedure. |
| [Q-005: Cathode, APA, CRP or field-cage settings change the data conditions](matrix.md#q-005) | Record measured settings and the time and region affected. Pause or continue according to the run plan; data quality alone does not demand a hardware trip. |

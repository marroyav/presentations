# Speaker notes: DUNE detector-wide interlocks

Collaboration review v0.2 · 8 September 2026 · 18 slides

Aim for a short discussion with detector experts. Use the slides to agree what
should happen. Use the companion guide when a team asks about its individual
rules or evidence. The whole deck is a proposal for review.

| Slide | What to say |
|---|---|
| 1. DUNE detector-wide interlocks | “We need a common picture of which detector activities can run together and what happens when a condition changes.” |
| 2. Three different responses | “Protecting equipment, taking turns and marking affected data need different responses. Purity-monitor activity does not require PDS bias off in this proposal.” |
| 3. Read a row like a sentence | “Read the event, the action and the return condition. The rule number lets us connect comments to the detailed engineering draft.” |
| 4. LAr level before HV availability | “HV is unavailable until the measured LAr level is reliably above the specified minimum and covers all required instrumentation, including the cathode. Voltage-setting, enabling and ramping stay blocked. This prerequisite exists before an HV request. Satisfying it does not automatically switch HV on, and the other HV checks must also pass.” |
| 5. Equipment faults | “The equipment team identifies what could be damaged. The protection action names the affected supply or group, its limits and its response time.” |
| 6. Camera lights | “The second request waits, whichever activity started first. PDS must define the exact hardware state that excludes light. Being left out of DAQ is not automatically the same as that hardware state.” |
| 7. External lasers | “Agree the handback as well as the start. Verify emission-off and shutter closure. Laser personnel protection applies throughout.” |
| 8. Purity monitors | “Keep PDS running and record when and where the measurement affects its data. The old interface document says bias off; that source disagreement is an explicit correction item.” |
| 9. Light-source matrix | “The name of the source matters. PDS calibration light and power-over-fiber have different purposes and rules from camera or external-laser illumination.” |
| 10. TPC state questions | “These questions need detector and electrical expertise. We have no approved universal answer for cathode-loss response or power-loss ordering. Existing approved procedures remain the basis for tests and operation.” |
| 11. Rack dependencies | “A rack fault can affect equipment owned by several teams. We need the real load list and an agreed response, including any essential loads allowed to remain powered.” |
| 12. DAQ | “Tell DAQ whether an activity must wait or whether data can continue with an appropriate record. Define what an ongoing run does as well as what a new run may do.” |
| 13. Expert handback | “ProtoDUNE already did this through people and messages. Keep the owner and affected region visible. The evidence comes from the existing September 3 review; this revision did not perform a new Slack search.” |
| 14. Detector stages | “Installation, commissioning/integration and running each need an appropriate procedure. Commissioning permits a defined test, not an unrestricted exception to the rules.” |
| 15. Missing information | “An unreliable protection input and missing data-quality information are different problems. Each needs an agreed response; uncertainty alone is not a universal detector trip instruction.” |
| 16. Recovery | “A cleared alarm or returning connection does not prove the detector is ready. The equipment owner and DAQ each have checks before the run resumes.” |
| 17. Decisions still needed | “Find the row for your system and identify the owner of the missing answer. Cooling, grounding and moving devices remain in the complete matrix even though the light examples are easier to explain.” |
| 18. Review request | “Tell us the detector condition, consequence, action and return checks in your own words. The integration team can translate the agreed behavior into signals, controls and tests.” |

## If asked about the field-cage rule

The reviewed HVS interface explicitly requests associated field-cage
termination supplies off when cathode HV shuts down. It gives prevention of
incorrect HV current readings as the reason. The guide retains that action and
flags the engineering draft's equipment-damage label for review. Do not extend
that statement into an automatic trip of all other detector systems.

## If asked for an exact threshold or time

Refer to the responsible owner and the controlled procedure for that detector
configuration. This deck intentionally does not turn prototype examples into
production thresholds. The [full guide](human/index.html) records what remains
to be supplied for each rule.

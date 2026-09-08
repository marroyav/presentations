# Tell us what your subsystem needs

Complete one short record for each interaction. Write as you would explain it
to another detector team. Numbers and engineering details can be attached once
the behavior is agreed.

| Question | Your answer |
|---|---|
| Which subsystem and rule are you reviewing? | |
| What event or requested activity starts the rule? | |
| Which equipment or detector region does it affect? | |
| Could it harm people or equipment, prevent an activity, or reduce data quality? Why? | |
| Can the two activities run together? Under which conditions? | |
| What must be checked before starting? | |
| What happens if the condition changes while equipment is already on? | |
| Which team or system takes that action, and how quickly? | |
| What should happen if the needed information is missing? | |
| How do we know the action really happened? | |
| What checks are needed before returning to operation, and who authorizes that? | |
| What differs during installation, commissioning/integration and a run? | |
| Which document, measurement or experience supports the answer? | |
| What is still unknown, and who will resolve it? | |

## Example: purity monitor and PDS

“The purity-monitor team records when a measurement starts and ends and which
region it affects. PDS continues acquiring. DAQ records enough information for
analysis to identify the affected PDS data. PDS bias remains on. The two teams
still need to agree timing precision, affected channels and the end of the
disturbance. If the activity record is missing, the affected data quality is
unknown; that missing record does not by itself require a bias trip.”

This is a proposed rule. The current PDS interface wording needs to be corrected
before this proposal can become the approved detector procedure.

## Example: camera light and PDS

“The two activities take turns. If PDS is in the agreed excluded state, a
request to switch on the camera light is refused. If the light is already on,
the new PDS request waits. Before PDS resumes, the camera team confirms that
illumination is actually off. The teams agree the affected optical region,
settling time and response to an unexpected overlap.”

The exact excluded PDS state still needs the PDS team's decision. Record the
actual hardware condition required, not only whether a detector is listed in
the run configuration.

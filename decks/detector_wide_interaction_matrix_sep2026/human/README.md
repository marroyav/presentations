# DUNE interlocks: start here

Collaboration review v0.2 · 8 September 2026

This guide is for detector experts across the collaboration. It describes the
proposed rules for operating systems together, the reasons for those rules,
and the decisions that still need the subsystem teams. It is a discussion
draft, not an approved operating procedure.

**Start with the [short PDF guide](guide.pdf), find your subsystem in the
[searchable guide](index.html), or read the [subsystem pages](subsystems.md).** The [full matrix](matrix.md) covers all 40
rows in the DPS planning register. The [slides](../main.pdf) introduce the same
ideas in a short talk.

## Three examples explain the distinction

| Situation | What we propose | Why |
|---|---|---|
| LAr level has not been established above the required minimum | HV remains unavailable: voltage-setting, enabling and ramping are blocked | The LAr must cover all required instrumentation, including the cathode |
| Camera lights or an external laser are requested while PDS is active | Make the activities take turns; block the second request | Keep incompatible detector activities apart |
| A purity monitor operates while PDS records data | Keep PDS running and mark the affected time and region | The measurement quality is reduced; this overlap does not require PDS bias off |

For cathode HV, **sufficient LAr level is a prerequisite for availability**.
The measured level must be reliably above the specified minimum, covering all
required instrumentation, including the cathode. This restriction exists before
anyone requests HV or sets its voltage. Meeting the level requirement allows
operation only once the other HV checks also pass; it does not switch HV on.
The shutdown response to a falling level while HV is already on is a separate
rule, P-002.

PDS means the photon detection system. Here, **“PDS active” is a placeholder**:
PDS must specify exactly which powered, biased or acquiring state the light
exclusion applies to. Leaving PDS out of a run must not silently be treated as
proof that its hardware is in the required state.

The external-laser rule concerns ionisation and alignment sources. PDS-owned
calibration light has its own declared calibration procedure. Power-over-fiber
is needed by the applicable vertical-drift PDS channels and stays under its own
protection rules.

## Read each row as a sentence

“**When this happens**, **this team or system takes this action**, **because of
this consequence**. Before returning, **these checks must pass**.”

For example: “When camera lights are already on, the new PDS request waits.
The camera team confirms that illumination is off, and PDS checks the agreed
return conditions before starting.” The same exclusion applies when PDS starts
first: the request to turn on the light waits. A request to turn something off
is not the same as confirmation that it is off.

Read the source-status text as well as the action. “Source + open details” means
a reviewed document supports the general behavior, but the production limits,
scope or implementation still need agreement. “Decision needed” does not mean
safe or forbidden in every circumstance: use the approved procedure for the
activity concerned. No row in this guide grants a new operating permission.

## The detector stage changes the procedure

| Stage | What the teams need to know |
|---|---|
| Installation | Who is working, what is isolated, and which limited tests are authorized |
| Commissioning and integration | Who owns the test, which detector states it permits, and how equipment returns to normal operation |
| Run | Whether the requested run is allowed, which protection is available, and what conditions must be recorded with the data |

Commissioning can include deliberate overlap where the rule permits it, such
as purity-monitor studies. It does not provide a general exception to the
PDS/camera-light or PDS/external-laser exclusions. Maintenance and recovery use
the relevant approved work or test procedure.

## What each team contributes

The subsystem team explains what its equipment needs and what could go wrong.
The teams affected by a rule agree the action and how to return to operation.
Detector Protection (DPS) implements the required protective response with the
relevant equipment owners. Slow Controls presents equipment state, coordinates
agreed equipment actions and records the reason for a restriction. Data
acquisition (DAQ) manages the run and receives the conditions needed to label
and interpret the data.

The detailed ownership of a setting is still agreed individually. Monitoring a
setting does not give another system authority to change it.

For each rule, answer the [short review form](review-form.md): what happens,
what it affects, why it matters, what should happen next, and who checks the
return. The integration team can then translate those answers into the
technical interface and tests.

## Two source disagreements need explicit review

The PDS interface version reviewed here still requests bias removal during
purity-monitor activity. This guide follows the requested proposal: **continue
PDS operation and label affected data**. That disagreement needs a controlled
document correction. The camera-light wording also needs reconciliation with
the proposed rule that blocks the second request.

The HVS interface specifies switching off associated field-cage termination
supplies when cathode HV stops, and gives prevention of erroneous current
readings as its reason. We retain the specified action while flagging the
engineering register's damage classification for review. A universal cathode
trip response for APA/CRP bias, electronics and affected PDS remains open.

See the [review findings and sources](review-notes.md) for the evidence and the
remaining questions. The documents distinguish a source requirement, a proposed
rule and historical ProtoDUNE practice throughout.

## Files and updates

The plain-language text lives in [rules.json](rules.json). It is an editorial
view of the DPS register, not a replacement engineering register. The generated
guide, full matrix and subsystem pages share that text. The
[source snapshot](source-map.json) records every original row's classification,
response and evidence status, together with the original file hash.

From the presentations repository, rebuild with:

```sh
python3 scripts/build_interlock_guide.py
make decks/detector_wide_interaction_matrix_sep2026/main.pdf
```

Rebuild the short PDF handout with `python3 scripts/build_interlock_guide.py --pdf`
(requires a local Chromium browser). It contains the overview and two subsystem
summaries per page. The HTML guide's “Print this view” button can separately
print the complete rules for a selected subsystem or search.

To recheck coverage against a newer working DPS register:

```sh
python3 scripts/build_interlock_guide.py \
  --register /path/to/daphne_slow_controls_plan/planning/detector_wide_interaction_register_v0_1.csv
```

The build refuses missing or duplicate rule IDs. Review changes in the source
snapshot before publishing an updated guide. The supplied snapshot is of the
local working DPS draft; it does not imply that those files have been released
or approved upstream.

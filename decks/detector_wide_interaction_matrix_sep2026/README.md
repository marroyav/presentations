# DUNE detector-wide interlocks

Deck slug: `detector_wide_interaction_matrix_sep2026`

**Current edition:** collaboration review v0.2, 8 September 2026.
Read the [presentation](main.pdf), [speaker notes](speaker-notes.md), or
[plain-language guide](human/README.md) and [short PDF handout](human/guide.pdf). The [searchable matrix](human/index.html)
has all 40 existing rules and 11 subsystem views, with installation,
commissioning/integration and run guidance.

## Audience

- Primary audience: DUNE subsystem coordinators, detector integration, Slow Controls, DPS, DAQ, cryogenics, HVS, TPC electronics, PDS, and run coordination.
- What they already know: their own detector subsystem and the informal operating constraints used at ProtoDUNE.
- What they need from this talk: what their subsystem must check, which activities can run together, what happens after a fault, and which decisions need their input. No Slow Controls expertise is assumed.

## Outcome

- One-sentence takeaway: each detector interaction needs a clear reason, an agreed action, named teams and a checked return to operation.
- Decision or action requested: review the rows for your subsystem and supply the missing detector conditions, action, timing and recovery checks.
- Owner and completion condition: subsystem and technical-coordination owners sign each rule after its physical consequence, enforcement path, recovery, and test are complete.

## Scope

- In scope: detector-wide protection, PDS optical exclusions, purity-monitor data quality, HV and bias state constraints, lifecycle-specific enforcement, human-interlock evidence, testing, ownership, and traceability.
- Explicitly out of scope: final voltage values, detector-wide trip timing, PLC code, cable/channel maps, and claims that have not passed the relevant hazard or electrical analysis.
- Also out of scope: explaining detector technologies or how cathode HV, APA bias, or CRP bias works. Those systems appear only where an interlock rule depends on their state.

## Evidence

- Reviewed interface versions: SC--HVS ICD EDMS 3315615/1; SC--TPC Electronics/BDE ICD EDMS 3293079/1; SC--PDS specification EDMS 3309688/1. Their general requirements and unresolved or conflicting wording are distinguished in the companion guide.
- Historical evidence: access-controlled ProtoDUNE NP02 and NP04 shifter-assistant messages recorded in `protodune_slack_interlock_evidence_v0_1.md`.
- Controlled draft: `detector_wide_interaction_register_v0_1.csv` and `detector_wide_interaction_framework_v0_1.md` under `/home/neutrino/work/wl-144132/daphne_slow_controls_plan/planning/`.
- Important uncertainty: the available HVS ICD couples cathode/drift-HV shutdown to mapped field-cage terminations, but does not establish a universal cathode-loss trip for APA bias, CRP bias, BDE/TDE, or PDS/PoF.
- Review correction: the HVS source gives prevention of incorrect current readings as the reason for its field-cage shutdown rule. The guide preserves the action and flags the engineering register's equipment-damage classification for review.
- Source conflict: the old PDS interface's purity-monitor bias-off wording conflicts with the proposed data-quality-only rule. The guide follows the requested proposal and explicitly asks for the source correction.

## Editorial choices

- One claim per slide; assertion-style titles carry the story.
- Start with concrete detector situations and plain actions. Controls implementation terminology is kept in the engineering material.
- Small matrices answer one question each. The companion guide provides complete source-row coverage and team-specific entry points.
- Red is reserved for a genuinely damaging or prohibited condition.
- Color never carries meaning without words or symbols.

## Build

From `/home/neutrino/work/presentations`:

```sh
make decks/detector_wide_interaction_matrix_sep2026/main.pdf
python3 scripts/build_interlock_guide.py --check
python3 scripts/audit_decks.py decks
```

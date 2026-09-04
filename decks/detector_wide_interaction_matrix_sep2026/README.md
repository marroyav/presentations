# DUNE detector-wide interlocks

Deck slug: `detector_wide_interaction_matrix_sep2026`

## Audience

- Primary audience: DUNE subsystem coordinators, detector integration, Slow Controls, DPS, DAQ, cryogenics, HVS, TPC electronics, PDS, and run coordination.
- What they already know: their own detector subsystem and the informal operating constraints used at ProtoDUNE.
- What they need from this talk: a reviewable detector-wide interlock framework that separates protection, operational exclusion, and data-quality effects.

## Outcome

- One-sentence takeaway: DUNE should maintain one controlled cross-detector rule register, while using different enforcement for detector protection, incompatible operations, and data-quality effects.
- Decision or action requested: approve the vocabulary, consequence/control grammar, initial PDS rules, and the owner-led path for closing unresolved HD/VD voltage couplings.
- Owner and completion condition: subsystem and technical-coordination owners sign each rule after its physical consequence, enforcement path, recovery, and test are complete.

## Scope

- In scope: detector-wide protection, PDS optical exclusions, purity-monitor data quality, HV and bias state constraints, lifecycle-specific enforcement, human-interlock evidence, testing, ownership, and traceability.
- Explicitly out of scope: final voltage values, detector-wide trip timing, PLC code, cable/channel maps, and claims that have not passed the relevant hazard or electrical analysis.
- Also out of scope: explaining detector technologies or how cathode HV, APA bias, or CRP bias works. Those systems appear only where an interlock rule depends on their state.

## Evidence

- Authoritative sources: SC--HVS ICD EDMS 3315615/1; SC--TPC Electronics/BDE ICD EDMS 3293079/1; SC--PDS specification EDMS 3309688/1.
- Historical evidence: access-controlled ProtoDUNE NP02 and NP04 shifter-assistant messages recorded in `protodune_slack_interlock_evidence_v0_1.md`.
- Controlled draft: `detector_wide_interaction_register_v0_1.csv` and `detector_wide_interaction_framework_v0_1.md` under `/home/neutrino/work/wl-144132/daphne_slow_controls_plan/planning/`.
- Important uncertainty: the available HVS ICD couples cathode/drift-HV shutdown to mapped field-cage terminations, but does not establish a universal cathode-loss trip for APA bias, CRP bias, BDE/TDE, or PDS/PoF.

## Editorial choices

- One claim per slide; assertion-style titles carry the story.
- Plain language first; acronyms are expanded before use.
- Tables are small audience views, not the controlled source of truth.
- Red is reserved for a genuinely damaging or prohibited condition.
- Color never carries meaning without words or symbols.

## Build

From `/home/neutrino/work/presentations`:

```sh
make decks/detector_wide_interaction_matrix_sep2026/main.pdf
python3 scripts/audit_decks.py decks/detector_wide_interaction_matrix_sep2026
```

# Review findings and source boundaries

8 September 2026 · Collaboration review v0.2

## What made the previous version difficult to read

The 19-slide deck introduced the rule register, classification codes and
implementation concepts before giving each detector team a clear account of
its own actions. Terms such as *mutex*, *admission*, *final element*, *safe
envelope* and *two-axis grammar* required control-system knowledge. Some slides
combined several decisions in one table, and most equipment teams had no short
entry point. The public matrix covered representative cases without showing
the complete set of 40 source rows.

The revised deck starts with familiar detector situations. The companion guide
has one entry for every original row and an index for all 11 team groupings.
Each entry says what happens, why it matters, what the proposed response is,
what differs by stage and what remains undecided. Color reinforces printed
words; it never means “safe” by itself. The rule numbers remain unchanged so
comments can be traced back to the engineering draft.

## Technical points that must stay visible

| Point | Reviewed evidence | Treatment in this revision |
|---|---|---|
| LAr level before HV availability | Collaboration clarification, 8 September 2026: sufficient coverage is required before voltage setting or HV operation is available | P-001 is a standing prerequisite: measured LAr must be reliably above the specified minimum and cover all required instrumentation, including the cathode. It is independent of an HV request; the already-on low-level response remains P-002 |
| Purity monitor / PDS | The old PDS interface asks for bias off; the existing framework and user direction call for continued PDS operation with data-quality records | Q-001 explicitly keeps bias on for this interaction and marks the source conflict |
| Camera illumination / PDS | ProtoDUNE practice supports exclusion; the old PDS interface includes bias-off language and a copied purity-monitor sentence in the camera paragraph | O-001 proposes taking turns, requires an exact PDS state and verified light-off, and marks the unresolved source wording |
| External laser / PDS | The recorded NP04 handoffs took PDS out for laser operation and checked shutter closure before return | O-002 retains the firm exclusion; hardware state and timing still need agreement |
| Field-cage response to cathode shutdown | HVS section 5 specifies associated field-cage supplies off to prevent erroneous current readings | P-005 keeps the specified action but flags its equipment-damage classification for review |
| Cathode loss / other detector systems | The available sources and historical sequences do not establish a universal automatic trip of APA/CRP bias, electronics or PDS | P-019 remains a decision, separately for horizontal and vertical drift; it does not grant permission to continue |
| Power loss / anode bias / electronics | The integration plan explicitly makes the ordering question conditional | P-014 asks whether an order is needed and how it would be achieved during the failure; no software guarantee is assumed |
| Cold-electronics environment; fans/heaters; grounding; movement | Inputs or historical concerns exist, but several actual responses remain unspecified | P-013, P-015, P-016 and O-007 remain visible decisions with responsible teams |
| Missing information | A lost monitoring connection and a failed protection input are different conditions | O-005 covers commands and visibility; P-010/P-017 require an agreed response for the specific protection failure |
| HV quality records | Q-003 and Q-005 overlap in scope | Both IDs are retained; owners should coordinate them or consolidate them in the next engineering revision |

These are editorial and requirements-review findings. The source CSV has not
been silently reclassified or rewritten. In particular, P-005 still carries its
original classification in the preserved source snapshot, while the readable
view explains why review is needed.

P-001 was explicitly clarified in the local working register on 8 September
2026 following collaboration feedback. Its earlier request-triggered wording
did not make HV unavailability clear enough. The requirement now precedes
voltage-setting, enabling and ramping. The numerical minimum, reference point,
coverage margin and measurement checks remain for the responsible teams to
specify. The snapshot and all generated views include this correction.

## What the DPS work contributes

The SC/DPS integration plan contributes the dependencies beyond light sources:
rack faults, shared equipment ownership, timing and communication loss,
power-loss ordering, explicit fault recovery and tests of the installed
response. Its interface-request form asks for the responsible owner,
measurements, action, timing and failure behavior. The short review form in
this guide asks those questions in detector language first.

The August PDS interface review also distinguishes ownership of run settings
from equipment availability and protection. This guide retains that distinction
without teaching the software architecture or changing the owner of a setting.

## Sources used

The reviewed working repository is
`/home/neutrino/work/wl-144132/daphne_slow_controls_plan`. Its relevant files were
local uncommitted work when reviewed, so a remote branch must not be cited as
proof of their exact content. The committed presentation companion includes a
hash and selected original fields in [source-map.json](source-map.json).

| Material | Version or location reviewed | What it supports |
|---|---|---|
| Interaction register | `planning/detector_wide_interaction_register_v0_1.csv`, 40 rows | Row IDs, candidate actions, stage rules, owners and open fields |
| Interaction framework | `planning/detector_wide_interaction_framework_v0_1.md`, 3 September 2026 | Protection / operations / data-quality distinction and draft decisions |
| Public matrix and atlas | `planning/detector_wide_public_matrix_v0_1.md`; `planning/detector_wide_matrix_atlas_v0_1.html` | Existing presentation choices and representative cases |
| SC/DPS integration plan | `sc_dps_software_integration_plan.tex`, interaction-matrix section and power-loss example | Ownership, tests, failures and recovery |
| ProtoDUNE evidence log | `planning/protodune_slack_interlock_evidence_v0_1.md`, reviewed 3 September 2026 | Selected historical actions in NP02 and NP04; no new Slack search was performed for this revision |
| [HVS interface](https://edms.cern.ch/document/3315615/1) | Reviewed local extraction of revision 1.0, section 5 | Cryogenic/HV protection, excess-current notification, linked field-cage shutdown and HVS fire response |
| [PDS interface](https://edms.cern.ch/document/3309688/1) | Reviewed local extraction of revision 1.0, 14 October 2025, section 5 | Supply and temperature protection; optical-rule conflicts |
| [TPC electronics/BDE interface](https://edms.cern.ch/document/3293079/1) | Revision 1.4 as referenced by the engineering draft | Electronics inputs and open cause/action questions |
| PDS interface review comments | `SC_PDS_ICD_v1_review_comments.md`, 17 August 2026; local snapshot S11 in `operations-variable-ownership-20260908` | Ownership distinctions and explicit review of the old NP02 compatibility matrix |
| [Rack-protection study](https://docs.dunescience.org/cgi-bin/private/ShowDocument?docid=32655) | DUNE-doc-32655 v7, as referenced by the engineering draft | Prototype rack protection; production limits remain open |

The numbered interface revisions are the versions reviewed, not a claim that
they are the latest approved documents. EDMS, DocDB and Slack links may require
collaboration access. No numerical prototype threshold has been promoted into
a detector-wide operating instruction.

## Why several small matrices work

The method follows the useful part of CERN's cause-and-effect approach:
connect a specific condition to a specific action, keep operational and safety
uses distinct, and retain links to verification. CERN's paper also explains
why a matrix for current conditions needs additional descriptions for complex
sequences. Here the matrix is written in ordinary sentences and recovery is
shown separately. This is an editorial adaptation for a detector audience,
not a claim that the readable guide is an executable safety specification.
[B. Fernández et al., ICALEPCS 2019, MOPHA041](https://accelconf.web.cern.ch/icalepcs2019/papers/mopha041.pdf).

The previous framework attributed that paper to different authors. The citation
above follows the paper's actual title page. Its notation and software details
belong in engineering material rather than the main collaboration slides.

## Ready for collaboration review when

Every team can find its rows, say whether the described behavior is correct,
name the people who must agree it and identify what is still missing. A rule
becomes ready for implementation only after the relevant owners resolve its
open fields, reconcile its sources and accept the required verification.

## Checks completed for this edition

The presentation has 18 slides and the short PDF guide has seven pages. Both
were visually reviewed. The slide build has no overflow or missing-character
warnings. The readable views match all 40 source IDs and all 11 team groupings;
local document links resolve. Browser checks exercised every subsystem filter,
combined stage/search selection, details, reset, the empty-result message and
mobile width. The repository's complete presentation and schematic checks also
passed; pre-existing editorial advisories in other decks remain unchanged.

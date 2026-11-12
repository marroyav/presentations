# VD detector protection system — I&I meeting, November 2026

Current draft: 15 main slides, followed by a Backups transition (slide 16)
and 37 backup slides. Main slides 12–13 show the critical consortium interlocks
and group actions. Slide 14 covers the Batavia and SURF test benches; slide 15
sets the information target for late January 2027 and the comprehensive design
target for mid-April 2027. The Detector walkthrough remains in backups 22–33.
The matrix excerpt, delivery checks and hardware-review detail are in backups
51–53. Earlier versions remain in Git and `archive/`.

## Purpose

Start from what we know about rack PDUs and the TPC/BDE protection system. Find
all hardware connections needed by the DPS brain, collect the consortia and LBNF
inputs, and develop the full VD DPS concept by extending the existing BDE approach.

The new slides distinguish the current basis, missing information, design ideas
and decisions. The proposed responsibilities and protection rules remain proposals.

## Meeting updates

- A title page identifies Manuel Arroyave and the November 2026 I&I meeting.
- The title and transitions carry a large grey DUNE logo on the left, with
  the title text, Detector or Backups on the right. All three have no footer.
- Content slides and backups use only a black Fermilab logo in the footer,
  alongside the existing meeting date and page number.
- The current system name is SDSTA SCADA. Historical source names remain in the
  source records and the original email.
- The overview groups SC and DPS in one box. The three facility systems remain
  outside it; reception at SC, the PLC or both remains open. Cryogenics is bidirectional.
- Slide 5 proposes the BDE PLC architecture as the DPS brain: industrial hardware,
  modular expansion, vendor support and distributed panels across the roughly 70 m
  mezzanine. The sketch distinguishes EtherCAT from supervisory Ethernet.
- Main slide 7 briefly reports progress on FFDG BMS and SDSTA SCADA before
  Cryogenics. FFDG status can inform operator decisions; hard interlocks are not
  assumed. The SDSTA update names Oro Hondo ventilation.
- The FFDG and SDSTA detail slides are retained as backups 18–21.
- Slide 6 presents a collaboration demo using the Raritan PDU in the
  dune-fd-test01 setup: single-outlet switching, a discrete contact output and
  local event-rule/LuaPLC logic. The fitted actuator, firmware and PLC input
  remain to confirm. The original rack/TDE slide is retained as backup 49.
- Fire detection, fire alarms and emergency response remain outside DPS control.
  A possible equipment-status feed to responders needs a recipient agreement.
- The FFDG and SDSTA commissioning discussions are reported inputs. Service
  commitments, protection use, variable lists and network access remain open.
- Backup 28 follows PoF and groups DAPHNE with the PDS calibration box.
  It retains the 34-feed working scope; channel and inhibit assignments remain open.
- Main slides 12–13 highlight the group actions. BDE is nearly complete,
  as reported by Manuel; PDS must assess purity-monitor inhibition versus tagging
  and define PoF inhibition. CalCI/PDS must agree the laser handshake. HVS,
  Cryogenics and CalCI must map protection inputs and shutdown dependencies;
  TDE/DPS must define the external PDU protection interface.
- Main slide 14 pairs the reported Batavia demonstrator work with
  `dune-fd-test01` in the SURF Nevada room. Both benches have explicit next work
  and a common protection-path test goal. No new test result is reported.
- Main slide 15 gives the requested planning targets: gather consortium and LBNF
  information by late January 2027; complete a comprehensive DPS design by
  mid-April 2027. Individual group commitments and installation dates are separate.
- Backup 27 labels PDU switching and box-enable as candidate PoF inhibition paths.
  PDS still needs to define the path, scope, response time, feedback and recovery.
- Backup 50 shows the full conditions/action matrix. The complete five-page
  [matrix companion](figures/interlock-matrix-v0.2.pdf) retains its sources,
  decisions and readiness notes. Backups 51–53 retain the earlier matrix excerpt,
  delivery measures and hardware-review preparation.

## Source material and working files

`commissioning-update-20261110.txt` retains the full user-supplied email. The email
is undated; it was supplied in this conversation on 10 November. Its relative
six-month transition statement has no confirmed start date. Its security wording
is retained as source context, not adopted as a verified architecture claim.

`connection-register-template.csv` is an empty collection template. It has fields
for both hardware endpoints, connectors/channels, signal type, action, feedback,
response time, lost-signal behaviour, responsibility and source revision. It is
not a completed hardware inventory.

`sources.json` and `sources-and-notes.txt` keep the engineering references and
qualifications. `verification-latest.txt` identifies the latest build and review
record. `review/` contains the current slide previews and index.

## Edit and build

The speaking scripts follow main slides 1–15:

- `speaker-script-fast.txt`: about four minutes.
- `speaker-script-15min.md`: an expanded version with rehearsal timing cues,
  targeting fifteen minutes.

Slides 16–53 are for questions. The scripts retain the Detector, facility and
original rack/TDE paragraphs as optional backup notes.

From the repository root:

```sh
make decks/dps_integration_status_white_nov2026/main.pdf
```

Edit the main sequence in `main.tex`, the added meeting slides in
`meeting-updates.tex`, and technical backups in `backup-slides.tex`. The title,
footer, meeting date and transition layout are in `deck-style.tex`.

The system diagrams are native TikZ in `diagrams/`. Backups 26 and 36 both use
`diagrams/daphne-icd-reference.tex`, which keeps CCM/opmon and Hermes separate.
`diagrams/styles.tex` uses the shared framework's styles and colours. The site
map also compiles with the deck. The PDS LV slide uses `diagrams/pds-lv.tikz.tex`;
the PLC proposal uses `diagrams/plc-brain.tikz.tex`. The PDU demonstration uses
`diagrams/raritan-demo.tikz.tex`; its vendor references and verification limits
are in `raritan-capabilities-review-20261111.json`.

Edit the two interlock summaries and test-bench slide in `consortium-actions.tex`,
and the dated work plan in `meeting-updates.tex`.
`consortium-actions-20261112.json` maps group actions to the source material.

Edit the backup matrix excerpt in `diagrams/interlock-matrix-excerpt.tex`.
`interlock-matrix-excerpt.json` retains the selected source records and hashes.
`milestone-delivery-checks.json` records the proposed checks; it contains no
current completion counts or new hardware-test results.

The [original October deck](../dps_integration_status_oct2026/main.pdf) is unchanged.
The shared white profile, [framework guide](../../docs/framework-guide.md) and
[diagram guide](../../docs/diagram-guide.md) still apply; the date and logos are
deck-local additions requested for this meeting.

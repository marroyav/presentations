# VD detector protection system — I&I meeting, November 2026

Current draft: 28 main slides, including the title and Detector transition,
followed by a Backups transition and 16 backup slides in the same PDF.
The responsibilities slide is the first backup. All 35 earlier slides and
technical details are retained, following Manuel's instruction to keep everything
for now. The earlier white version is saved in `archive/`.

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
- Fire detection, fire alarms and emergency response remain outside DPS control.
  A possible equipment-status feed to responders needs a recipient agreement.
- The FFDG and SDSTA commissioning discussions are reported inputs. Service
  commitments, protection use, variable lists and network access remain open.
- A PDS LV slide follows PoF and groups DAPHNE with the PDS calibration box.
  It retains the 34-feed working scope; channel and inhibit assignments remain open.
- A progress-and-plans slide before Detector pairs the reported Batavia
  demonstrator work with dune-fd-test01 in the SD Nevada room. The local setup
  includes PDU/sensors/relay/GIZMo, Ignition, OPC UA bridges and emulators;
  expansion along the Batavia model remains planned.

The milestones remain collecting the hardware connections and reviewing the full
DPS concept. Dates are open and will be agreed with the consortia and LBNF.
The hardware-review and facility-interface schedule also remains open.

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

Two speaking scripts follow main slides 1–28:

- `speaker-script-fast.txt`: about four minutes.
- `speaker-script-15min.md`: an expanded version with rehearsal timing cues,
  targeting fifteen minutes.

Slides 29–45 remain backups for questions.

From the repository root:

```sh
make decks/dps_integration_status_white_nov2026/main.pdf
```

Edit the main sequence in `main.tex`, the added meeting slides in
`meeting-updates.tex`, and technical backups in `backup-slides.tex`. The title,
footer, meeting date and transition layout are in `deck-style.tex`.

The system diagrams are native TikZ in `diagrams/`. Slides 18 and 33 both use
`diagrams/daphne-icd-reference.tex`, which keeps CCM/opmon and Hermes separate.
`diagrams/styles.tex` uses the shared framework's styles and colours. The site
map also compiles with the deck. The PDS LV slide uses `diagrams/pds-lv.tikz.tex`.

The [original October deck](../dps_integration_status_oct2026/main.pdf) is unchanged.
The shared white profile, [framework guide](../../docs/framework-guide.md) and
[diagram guide](../../docs/diagram-guide.md) still apply; the date and logos are
deck-local additions requested for this meeting.

# VD detector protection system — I&I meeting, November 2026

Current draft: 28 main slides, including the title and Detector transition,
followed by 15 technical backups in the same PDF. All 35 earlier slides and
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
- The title carries a large grey DUNE logo on the right. The transition has the
  grey DUNE logo on the left and Detector on the right. Both have no footer.
- Content slides and backups use only a black Fermilab logo in the footer,
  alongside the existing meeting date and page number.
- The current system name is SDSTA SCADA. Historical source names remain in the
  source records and the original email.
- Fire detection, fire alarms and emergency response remain outside DPS control.
  A possible equipment-status feed to responders needs a recipient agreement.
- The FFDG and SDSTA commissioning discussions are reported inputs. Service
  commitments, protection use, variable lists and network access remain open.

The proposed dates are **31 January 2027** for collecting the hardware connections
and **31 March 2027** for reviewing the full DPS concept. These are discussion
proposals, not agreed deadlines. The earlier June 2027 hardware-review target is
retained.

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

From the repository root:

```sh
make decks/dps_integration_status_white_nov2026/main.pdf
```

Edit the main sequence in `main.tex`, the added meeting slides in
`meeting-updates.tex`, and technical backups in `backup-slides.tex`. The title,
footer, meeting date and transition layout are in `deck-style.tex`.

The system diagrams are native TikZ in `diagrams/`. Slides 18 and 31 both use
`diagrams/daphne-icd-reference.tex`, which keeps CCM/opmon and Hermes separate.
`diagrams/styles.tex` uses the shared framework's styles and colours. The site
map also compiles with the deck.

The [original October deck](../dps_integration_status_oct2026/main.pdf) is unchanged.
The shared white profile, [framework guide](../../docs/framework-guide.md) and
[diagram guide](../../docs/diagram-guide.md) still apply; the date and logos are
deck-local additions requested for this meeting.

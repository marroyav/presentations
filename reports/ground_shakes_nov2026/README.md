# Ground shakes: a short report

Open [the two-page PDF](main.pdf). It explains the measurements and completed
analyses in plain language. It summarizes existing results; it does not decode
more data or fit a new physics model.

## Build

From the presentation repository root:

```sh
make ground-shakes-report
```

`build_report.py` checks the saved counts and map order before writing
`values.tex`. It creates a new dated evidence record with input hashes, source
state, commands and verification limits. Tectonic builds the PDF. The report
needs the sibling `ground-shake-data` and `ground-shake-recovery-20261015`
workspaces to repeat the input checks. The PDF itself is standalone.

## Findings and their sources

All analysis paths below are in the sibling ground-shake-data workspace.

| Report claim | Source and scope |
|---|---|
| 1,531 records; 1,516 charge-screen candidates; 1,179 with selected early PDS activity | [Inventory and counts](../../../ground-shake-data/analysis/all-runs/all-runs-summary.csv), [method](../../../ground-shake-data/analysis/all-runs/README.txt). Seven runs: 27938, 27951, 30201, 30202, 32730, 32731, 32739. Selection is conditional on saved records, not detector live time. |
| 101 of 716 have at least two selected early pulses | [Pair result](../../../ground-shake-data/analysis/double-pulse-display/results.json), [method](../../../ground-shake-data/analysis/double-pulse-display/README.txt). Run 32731, endpoint 109; 21-channel edge clusters; times in [−300, −100) microseconds relative to the charge-threshold shake marker. No optical classification. |
| Partial electrical prediction | [Fit results](../../../ground-shake-data/analysis/electrical-pattern-20261023/results.json), [method](../../../ground-shake-data/analysis/electrical-pattern-20261023/README.txt). Reported disconnected inputs 13/14/16; run 32731 training and run 32739 validation. Disconnection comes from the historical slides and user evidence; its engineering report and run coverage are not independently established. Residuals do not prove light. |
| A delay pattern survives event mixing | [Mixing result](../../../ground-shake-data/analysis/charge-light-matching/event-mixing-results.json), [interpretation correction](../../../ground-shake-data/analysis/charge-light-matching/interpretation-20261028.json). Substituting PDS pulse trains from other events retains their phases relative to each shake. A repeated physical source can preserve a drift-delay peak. No unique charge–light assignment or source position follows. |
| Upper modules favour slow activity | [Module results](../../../ground-shake-data/analysis/apa1-apa2-response-20261103/module-results.json), [method](../../../ground-shake-data/analysis/apa1-apa2-response-20261103/MODULES.txt). In −120 to −20 microseconds, M3/M4 is strongest in 39/49 usable October APA1 events; M1/M2 in 1,210/1,224 November APA2 events. At least two simultaneous connected inputs per module; these are waveform fluctuations, not calibrated light yield. |
| Shared electronics group has more similar main response | [AFE comparison](../../../ground-shake-data/analysis/afe-comparison-20261103/README.txt). Matched four-input comparison uses the same recorded times and includes disconnected M8 inputs. Greater within-AFE main-shake correlation in 105/105 usable APA1 events and 849/957 APA2 events. This does not isolate crosstalk from a common disturbance or physical position. |
| No module always starts first | [Latest module timing results](../../../ground-shake-data/analysis/module-first-histogram-20261104/results.json), [method](../../../ground-shake-data/analysis/module-first-histogram-20261104/README.txt). Uses 14 APA1 and 478 APA2 selected early pulses, including APA2 M8 for electrical behaviour; 12/14 and 280/478 have tied leading modules at the primary threshold. Threshold checks change ties. Missing modules are not late; instrument delays are uncalibrated. This does not measure the start of the slow precursor. |
| No clear voltage/current association across both November runs | [Slow-controls analysis](../../../ground-shake-data/analysis/sc-correlation-20261027/README.txt). 32 usable monitors × three features in 1,376 November records; no same-direction adjusted rank association of magnitude at least 0.30 in both runs with 60-second bins. Minute-scale checks cannot exclude fast transients; no PDS/DAPHNE supply tags were included. |

## Orientation review

The source is the local recovered PDF of **EDMS 3493627 v1**, A. Cervera's
*NP04 Ground Bounce discussion*, July 2026, historical status “In Work”.
[Version-pinned EDMS record](https://edms.cern.ch/document/3493627/1).
The check establishes agreement with this historical source, not a current
approved wiring or installation drawing.

- Page 18: APA2 geographical map; field cage at the right; top-right channel
  109:20. The photograph is explicitly mirrored left to right to match the plots.
- Page 20: correct October APA1 map, endpoint 104. Each of the 40 positions
  was read from the source figure and compared with the map and extracted order.
  The bottom row reads 26, 24, 23, 21; it is easy to misread at reduced size.
- Page 21: deliberate APA1 rearrangement into APA2 channel order. It is an
  electronics comparison, not an APA1 geographical map.
- Both maps have M1 at the top and M10 at the bottom. These module numbers
  are not DAPHNE channel numbers. July APA1 used different wiring and is not
  assigned October's physical map in this report.
- The two stacks on page 2 are separate source-map views. Their side-by-side
  placement is not a detector floor plan. No beam direction, compass direction,
  drift coordinate or surveyed distance is inferred.

The check script stores the full independent transcription and verifies all
80 positions against both analysis maps and the saved extracted channel order.
It also checks the recovered PDF's SHA-256 against its earlier identity record.
[Landmark provenance and limits](../../../ground-shake-data/analysis/detector-landmarks-20261103/README.txt)
provide the earlier geometry lookup. No new engineering or physics approval is claimed.

## Writing and review

The report follows GOV.UK guidance on [clear language](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-language/)
and [clear structure](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-structure/),
reviewed on 5 November 2026: lead with the finding, explain terms, use short
sentences, and keep detailed methods here. The PDF uses white pages, dark text
and a source-based diagram. The final two pages were rendered and inspected
for readable text, layout, clipping and correct orientation.

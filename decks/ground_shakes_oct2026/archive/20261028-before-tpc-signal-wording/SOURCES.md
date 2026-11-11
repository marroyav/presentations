# Sources, evidence and what is new

The presentation separates earlier observations from added tests. None of the
local analyses has established a cause, a unique 3D charge–light match, or a
confirmed optical origin for the disturbance.

## Baseline documents

The main baseline is **EDMS 3493627 v1**, *Presentations*, containing A. Cervera's
*NP04 Ground Bounce discussion*, 20 July 2026, 85 pages. Its recorded status was
“In Work”. We reviewed the recovered PDF and its extracted text, including the
topology and early-pulse figures. A current EDMS check failed because the CERN
ticket had expired; this review does not claim that v1 is the latest revision.

- [Version-pinned EDMS record](https://edms.cern.ch/document/3493627/1).
- [Recovered PDF](../../../ground-shake-recovery-20261015/edms/ground_shake_200726.pdf).
- [Recorded identity](../../../ground-shake-recovery-20261015/edms/3493627.json).
- [Dated comparison of claims](evidence/baseline-comparison-20261028.json).

We also inspected the four-page Google Slides export associated with **EDMS
3493642 v1**, captured on 28 October 2026. It contains a warm-gas example at a
reported 42 kV, a link to TPC study plans, and an empty “Coupling between
daphnes” section. The associated Google file is mutable; the snapshot is not
an approved EDMS revision.

- [Evolving-material snapshot](../../../ground-shake-recovery-20261015/edms/snapshots/20261028/3493642-evolving-material.pdf).
- [Retrieval and hash record](../../../ground-shake-recovery-20261015/edms/snapshots/20261028/retrieval.json).

The separately linked historical Indico presentations and TPC planning document
were not all accessible or reviewed. “Added here” means an added measurement or
test relative to the inspected documents, not a claim of field-wide priority.

## What the source slides already establish or discuss

| Topic | EDMS 3493627 v1 pages | Status of our contribution |
| --- | --- | --- |
| Slow charge precursor and opposite APA signs | 9, 14, 79 | Reproduction and enlarged count |
| Disconnected PDS inputs and electrical component | 13, 23, 31, 59 | Known effect; added predictive tests |
| Electronics-dependent channel pattern | 21, 25 | Known pattern; added per-channel scores |
| Early sharp PDS activity and coincidences | 40–41 | Added pair counts and timing measurements |
| HV dependence and preliminary bias-off effect | 10, 34–35, 58, 70, 85 | Our November SC screen asks a narrower question |
| Search for real charge/light and drift interpretation | 29, 39–42 | Event-mixing comparison; shared drift delays remain possible |
| Analogue observations | 17, 62, 65–67 | Independent decoding is software validation |

The old presentation overstated novelty by leading with known charge and
electrical observations. The revised deck credits that baseline explicitly.

## Slide 1: scope and claims

The local inventory contains 1,531 saved records from runs 27938, 27951, 30201,
30202, 32730, 32731 and 32739, recorded in July, October and November 2024.
The automatic charge screen has 1,516 candidates, five records below cut and
ten unassessable records. The selected files do not measure detector live time
or a normal-operation shake rate.

[Run inventory and definitions](../../../ground-shake-data/analysis/all-runs/README.txt)
and [counts](../../../ground-shake-data/analysis/all-runs/all-runs-summary.csv).

## Slide 2: sharp pulses, slow precursor and main shake

The example is run 32731, event 33. The top panel shows raw ADC values on the
connected DAPHNE 109 input 47, as saved in 256 ns bins. Rail bins and missing
samples remain gaps. No pedestal is invented across missing packets. The
selected multichannel pulse times are −183.296 and −160.768 microseconds.

The middle panel shows the two saved full-APA charge medians in 2.048 microsecond
bins, each relative to its median in [−300, −260) microseconds. Only the interval
before −20 microseconds is displayed. The bottom shows APA1 on the full amplitude
scale. ADC counts are readout units, not calibrated photons or energy.

Time zero is the large-charge threshold proxy used in the earlier analysis,
not the first physical disturbance. These panels illustrate observed order in
one record. They do not prove a causal chain. The slow charge feature was
already known from EDMS; this figure explains terminology.

[Extraction and timing method](../../../ground-shake-data/analysis/electrical-pattern-20261023/README.txt)
and [saved event metrics](../../../ground-shake-data/analysis/electrical-pattern-20261023/sequence-event-metrics.json).

## Slide 3: double pulses

The two panels show the same connected input 47 in run 32731 events 33 and 52.
Selected times are −183.296/−160.768 and −242.688/−177.152 microseconds. Gaps
remain missing. Exact separations of the selected coarse times are 22.528 and
65.536 microseconds; the slide rounds them to 23 and 66.

The existing pair inventory contains 101 records with at least two candidates
out of 716 local charge-screen candidates. Eighty have exactly two. Records
with more candidates contribute several consecutive pairs, giving 125 pairs.

Selection: one fixed endpoint, DAPHNE 109; at least 21 channels in a negative-edge
cluster; pulse times in [−300, −100) microseconds. The 2.048 microsecond timing
bins and 10 microsecond cluster merging limit timing precision and suppress
closer pairs. Readout selection and the bounded window affect the distribution.
There is no matched normal-operation pair distribution, optical classification
or significance calculation. These early pairs are distinct in time from the
post-main reflections in EDMS page 9.

[Pair inventory](../../../ground-shake-data/analysis/double-pulse-display/results.json)
and [method and limits](../../../ground-shake-data/analysis/double-pulse-display/README.txt).

## Slide 4: PDS pulse time minus main-shake time

New histogram: [analysis and limits](../../../ground-shake-data/analysis/pds-shake-timing-20261028/results.json),
[record-level values](../../../ground-shake-data/analysis/pds-shake-timing-20261028/event-times.csv)
and [reproduction script](../../../ground-shake-data/analysis/pds-shake-timing-20261028/analyze.py).
The figure uses the wider existing sharp-pulse screen, not the earlier
[−300, −100) microsecond selection. That earlier selection alone guarantees
that all retained pulses fall in a 200 microsecond window.

Time zero is the start of the strongest connected charge-screen component
with at least 50% of sampled channels above 1,000 ADC on both APAs. The
horizontal axis is PDS time minus this main-shake onset proxy. Negative means
before the main shake. It is not a reconstructed electron drift delay.

Keep DAPHNE 109 fixed. Candidates are the existing fast-edge coincidences on
at least 21 channels, searched in [−4,000, −20) microseconds where recorded.
Retain candidates before the existing APA1 sustained 2 ADC precursor marker.
Choose one per record by its largest median peak negative edge on recorded
connected inputs, excluding reported disconnected channels 11, 13, 14 and 16.
The edge is a difference between 256 ns cached ADC bins, maximized within
±4.096 microseconds of each candidate. At least 21 inputs must have a valid
edge. This ranks recorded sharpness, not calibrated photon yield or pulse integral.

| Run | Charge candidates | Usable precursor marker | Pulse before marker | Amplitude-ranked records | Median time (µs) | Central 90% (µs) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 32731 | 716 | 702 | 239 | 237 | −230.400 | −308.224 to −123.085 |
| 32739 | 662 | 646 | 168 | 167 | −220.160 | −308.224 to −125.952 |

The total observed range is −316.416 to −72.704 microseconds. Of 404 selected
values, 51 are outside the old [−300, −100) window. Twenty-microsecond display
bins retain every selected record. Picking the first candidate before the
marker instead gives medians −238.592 and −237.568 microseconds, with 239 and
168 records. Both choices give a broad observed spread.

This subset is conditional on a measurable precursor, a detected sharp pulse,
and enough recorded inputs to rank size. Of 1,378 charge candidates, two lack
the existing sequence metrics; 1,348 have a usable precursor marker. Three of
407 records with an earlier candidate have no candidate with enough valid
edge samples for ranking. These are missing values, not zero pulses.

Individual channels sometimes record samples earlier than −320 microseconds.
This does not establish continuous 21-channel coverage. Self-triggered packet
gaps and the coincidence threshold can hide earlier pulses. The requirement
to precede the precursor also restricts timing. No hard −320 microsecond
readout boundary, detection efficiency or physical delay width is inferred.
Other run/endpoint timing summaries are saved in the analysis JSON; they lack
the same precursor selection and are not pooled into the November histogram.

## Backup: first pulse versus the coherent precursor marker

The first pulse means the first retained candidate in the stated selection
window, not necessarily the first physical pulse. The charge marker is a
sustained 2 ADC change in APA1, using five 2.048 microsecond bins, an amplitude/
noise cut and exclusion of left-censored crossings.

| Run / record | First selected pulse (µs) | Charge marker (µs) |
| --- | ---: | ---: |
| 32731 / 33 | −183.296 | −111.872 |
| 32731 / 52 | −242.688 | −107.776 |
| 32739 / 5 | −128.000 | −151.808 |

The clock comparison learns a median pulse-to-marker delay of 40.704 microseconds
on the training sample of run 32731. On 225 eligible run 32739 records its mean
absolute error is 66.0571 microseconds. The training median charge phase relative
to the known main shake is −148.224 microseconds; that comparison gives
33.4234 microseconds error. These are retrospective timing tests, not predictions
of shake occurrence. Missing early readout and diagnostic thresholds prevent a
claim that the first physical pulse cannot have a role.

This marker follows the coherent APA-median signal. It is not the arrival
time of charge from a localized interaction. These clock errors therefore
do not test, or exclude, a fixed physical drift distance.

The revised figure script independently recomputes both errors from the saved
event metrics. No fit coefficients or event selection were changed.

[Clock tests](../../../ground-shake-data/analysis/electrical-pattern-20261023/sequence-results.json)
and [frozen displayed values](evidence/public-review-data.json).

## Slide 5: event mixing

The full search uses all 1,516 charge candidates and 821 selected early PDS
candidates in 598 records. Of these PDS candidates, 820 have suitable donor
events for mixing. The figure shows the two November runs.

Each charge record and its usable time are retained. PDS pulse trains come from
up to ten other selected records in the same run, source file and assembly.
Weights preserve the target pulse count. The broad peak near +325 microseconds
survives this substitution. This does not establish a unique event-specific
charge–light assignment. It also does not exclude a recurring physical source.

The substitution keeps pulse times relative to each event's main shake. Let
`p_i` be a physical light time and `q_i = p_i + tau_i` its matching charge time,
both relative to that shake. A mixed pair has delay
`q_i - p_j = tau_i + p_i - p_j`. If the light phases are similar, the mixed
distribution can retain a peak near the physical drift delay. This is an
algebraic limitation of the comparison, not evidence that a fixed source was found.

Repeated interactions at similar drift distance, repeated electrical pickup
and recording/selection structure remain possible explanations. Distinguish
them with reconstructed charge positions, run-specific field and timing
corrections, and a fixed-source model passed through the actual readout masks.
For two pulses from the same position, test for two charge responses with the
same pulse separation and a common drift delay. These tests remain to be done.

Prompt light provides an interaction-time reference; matching charge can
arrive much later after drift. The physical principle is described in the
[DUNE photon-detector timing paper](https://arxiv.org/abs/1803.06379).
A calibrated drift delay constrains the drift coordinate, not a unique 3D
position. We do not convert the present raw-feature peak into a source distance.
The dated [interpretation correction](../../../ground-shake-data/analysis/charge-light-matching/interpretation-20261028.json)
supersedes stronger wording in the original mixing-result limits; numerical
histograms and candidate selections are unchanged.

The vertical axis is compact charge-feature/PDS pairs per usable comparison time,
multiplied by 100 microseconds. It is not a normal detector rate. The 50 microsecond
bins are unchanged. Reused donors preclude a simple independent-event p-value.
November charge readout extends only to about +0.35 ms; excluded samples can hide
genuine charge. There is no fully recorded 4 ms pre-shake PDS window in any candidate.

[Matching summary](../../../ground-shake-data/analysis/charge-light-matching/report-data.json)
and [mixing method and counts](../../../ground-shake-data/analysis/charge-light-matching/event-mixing-results.json).

## Slide 6: predictive electrical test

The reported disconnected inputs are 13, 14 and 16. EDMS page 23 already discusses
the disconnected-input response. The new three-tap fit uses their signal changes
to predict changes on connected inputs. It is not a pure electrical subtraction.

Training: 505 records from run 32731. Testing: 209 held-out records from that run
and all 662 records from run 32739. The displayed comparison uses run 32739 and
identical target samples for actual and substituted references. Scores are
0.156856 and −0.047317, where score = 1 − squared error / squared observed change.
The figure shows 100 × square root(1 − score), giving 91.8% and 102.3%. A value
of 100% is the error from a zero-change prediction. The partial improvement does not locate a source or
measure a light/electrical fraction.

The median event score in the wider early-pulse test is only 0.021564; large
edges dominate the pooled score. The earlier main-trained fit scores −0.194353
on early pulses. Model simplicity, nonlinear response and clipping remain
possible reasons for that failure; it does not prove separate causes.

[Fit results](../../../ground-shake-data/analysis/electrical-pattern-20261023/results.json)
and [earlier arithmetic audit](../../../ground-shake-data/analysis/sc-correlation-20261027/previous-results-audit.json).

## Slide 7: SC result and its relationship to EDMS

All 109 successful native exports and 7,744,489 samples are accounted for.
All 1,531 saved records were bracketed against 34 monitors; the waveform test
uses 1,376 November records. Thirty-two monitors have adequate coverage for
three features: slow charge amplitude, reported-disconnected-input early PDS
edge size, and selected early-pulse fraction. Two ground monitors are too sparse.

SC levels use actual samples within ±30 seconds, without interpolation. Multiple
values at a timestamp retain their median, range and count, with min/max-envelope
sensitivity checks. File/minute bins have equal weight. The primary screen uses
within-file ranks after removal of linear time trends. Eligibility requires
20 adjusted bins, three usable files and four distinct SC levels in each run.

None of 96 eligible pairs has the same sign and magnitude at least 0.30 in both
runs with one-minute bins. This is a descriptive follow-up cutoff, not proof of
zero association. One filtered-current/slow-charge hint appears with two-minute
bins but fails the one-minute and timestamp-envelope checks. Five-minute bins
have insufficient coverage to decide.

EDMS pages 10 and 34–35 already report HV and wire-bias effects. This conditional
November waveform screen does not remeasure shake rate, compare all HV settings,
or repeat the October bias-off contrast. “SC is unrelated to shakes” and “HV has
no effect” are not supported.

[SC report](../../../ground-shake-data/analysis/sc-correlation-20261027/index.html),
[fixed methods](../../../ground-shake-data/analysis/sc-correlation-20261027/plan.json)
and [independent numerical validation](../../../ground-shake-data/analysis/sc-correlation-20261027/validation-20261027T201724054241Z.json).

## Slide 8 and backups

The suggested work follows the source slides' open questions. The existing
bias-ramp comparison checks archived voltage records, not the PDS waveform
response to the ramp. Full 3D charge reconstruction is unfinished. The local
inventory lacks independent matched November non-shake records and live time.

The charge count, channel scores and weak-amplitude prediction in the backups
retain the original values and limits. The amplitude errors reproduce exactly;
an old metadata field stored a timing constant instead of the amplitude training
median. The correct amplitude median is 11.0625 ADC. Historical results are
unchanged and the error is recorded in the linked arithmetic audit.

## Reproduction and review

Run `python3 public_review.py` to rebuild the five new figures from frozen values,
then compile `main.tex` with Tectonic. The original figures remain included.
`--refresh` deliberately reselects values from the local analysis and pins their
source hashes. No detector data are decoded or changed; no physics model is refitted.

[Speaker notes](speaker-notes.txt) explain each claim in plain language.
[Public-source manifest](evidence/public-source-manifest.json) pins the new inputs.
The [previous deck](archive/20261028-before-public-review/main.pdf) and its
[source notes](archive/20261028-before-public-review/SOURCES.md) are preserved.

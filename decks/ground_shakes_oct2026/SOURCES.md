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

### Wider window and the Gaussian question

We checked the actual DAPHNE109 packet headers in all 1,378 November charge
candidates. The pulse finder needs at least 21 distinct channels with enough
samples to evaluate its edge test within its two-bin timing tolerance. No
record has that coverage earlier than −318.464 microseconds. This applies to
the 21-channel selection, not to the first sample recorded on any channel.
Some individual channels do have earlier packets.

All 2,156 saved DAPHNE109 pulse candidates lie within the packet coverage
required by the finder. The original pulse search already extends from
−4,000 to −20 microseconds where data permit. The
[wider histogram and coverage plot](../../../ground-shake-data/analysis/pds-shake-timing-20261028/extended-timing-and-coverage.pdf)
shows −800 to 0 microseconds; expanding the axis adds no earlier pulse data.

We therefore cannot establish whether the full physical timing distribution
is Gaussian. Its early tail is not measured by this selection. Requiring a
pulse before the precursor also restricts its other side. Packet availability
depends on self-triggering, so dividing by coverage would not by itself recover
an unbiased distribution. No Gaussian fit or extrapolated tail is claimed.

[Packet coverage method](../../../ground-shake-data/analysis/pds-shake-timing-20261028/window_coverage.py),
[counts and limits](../../../ground-shake-data/analysis/pds-shake-timing-20261028/window-coverage.json)
and [wider-window result](../../../ground-shake-data/analysis/pds-shake-timing-20261028/extended-window-result.json).

## Slide 5: event mixing

“Selected TPC signals” means short groups of activity on neighbouring wires
that pass the automatic cuts. These groups may contain ionisation charge,
electrical pickup or both. They are not reconstructed tracks or confirmed
charge deposits. The previous label “charge features” did not make this clear.

The selection removes the channel pedestal and the median signal shared by
the APA. It requires a channel signal above the larger of 20 ADC and six times
the estimated baseline noise, with two quiet bins followed by two high bins.
It looks for three neighbouring collection-wire indices with activity in the
other two wire planes at a similar time. Nearby points are joined; retained
groups last at most 40 microseconds and span at most 64 collection channels.
This tests timing and local grouping, not a fitted 3D charge trajectory.

The TPC time is the bin containing the greatest number of selected activity
points in that group; it is not the start of the group or the time of its
largest ADC sample. Each group is paired with each selected PDS pulse in the
comparison. One group can therefore contribute more than once.
See the [selection and grouping code](../../../ground-shake-data/analysis/charge-light-matching/drift_matching.py)
and [criteria and limits](../../../ground-shake-data/analysis/charge-light-matching/drift-results.json).

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

The vertical axis is timing comparisons per usable comparison time,
multiplied by 100 microseconds. It is not a normal detector rate. The 50 microsecond
bins are unchanged. Reused donors preclude a simple independent-event p-value.
November charge readout extends only to about +0.35 ms; excluded samples can hide
genuine charge. There is no fully recorded 4 ms pre-shake PDS window in any candidate.

Here a comparison (previously called a “pair”) uses two timestamps: one from
a selected TPC group and one from a PDS pulse. Their difference adds one entry
to the histogram. No TPC/PDS waveform amplitudes are added or integrated.
The vertical value in a displayed bin is `100 * N / T`, where `N` counts those
entries and `T` is the usable TPC time in that delay bin, summed over the PDS
pulses, in microseconds. Donor weights apply to both `N` and `T` for the mixed
curve. This is not integrated charge, photon yield or the number of confirmed
particle interactions.

[Matching summary](../../../ground-shake-data/analysis/charge-light-matching/report-data.json)
and [mixing method and counts](../../../ground-shake-data/analysis/charge-light-matching/event-mixing-results.json).

## Slide 6: next checks

The suggested work follows the source slides' open questions. The existing
bias-ramp comparison checks archived voltage records, not the PDS waveform
response to the ramp. Full 3D charge reconstruction is unfinished. The local
inventory lacks independent matched November non-shake records and live time.

## Slides 7–8: data and the known charge pattern

The inventory and charge-count definitions are given under slides 1–2 above.
The backup keeps the original count of 1,355 clear opposite-sign precursors
among 1,376 November records. The SC inventory figure of 34 monitors and
7.74 million samples comes from the [completed SC analysis](../../../ground-shake-data/analysis/sc-correlation-20261027/index.html).

## Slide 9: the fit by channel

The reported disconnected inputs are 13, 14 and 16. Their signal changes are
used to predict changes on connected inputs. The model is fitted on run 32731
and the displayed channel scores use run 32739. A score of zero means no gain
over predicting no change; one means an exact prediction. This is a partial
prediction of recorded signals, not a separation of light from electrical pickup.

[Fit results](../../../ground-shake-data/analysis/electrical-pattern-20261023/results.json)
and [figure script](extend_figures.py) give the values and selection.

## Reproduction and review

The [synchronized APA1/APA2 player](pds-spatial/apa1-comparison/activity.html)
shows the four channels inside each module, in physical order and by matching
AFE input. Both panels use identical channel values and event counts; only
the ordering changes. APA2 M8 keeps its disconnected label and its recorded
electrical response, including channels 11, 13, 14 and 16.
The [methods and checks](../../../ground-shake-data/analysis/afe-comparison-20261103/README.txt)
define the channel medians, complete-bin requirements and changing event coverage.
The page also contains the AFE correlation results. A four-input comparison
using exactly the same recorded times finds stronger within-AFE main-shake
correlation in 105/105 usable APA1 events and 849/957 APA2 events. All five AFEs
are included, with the recorded disconnected inputs retained. Inputs within
each AFE come from different physical modules. This does not isolate crosstalk
from detector position or a shared disturbance. APA1 and APA2 use different runs.

The [APA1/APA2 comparison](pds-spatial/apa1-comparison/viewer.html) uses 125
October APA1 records and 1,376 November APA2 records. Its main view now uses
physical modules throughout. A module combines at least two simultaneously
recorded inputs for the precursor activity measurement. M3/M4 is strongest
in 39/49 usable APA1 events; M1/M2 in 1,210/1,224 APA2 events. Both responses
favour the upper modules. Module onset timing has 14 APA1 pulses, with ties in
12 at 20% pulse depth and all 14 at 50%. The
[module methods and event values](../../../ground-shake-data/analysis/apa1-apa2-response-20261103/MODULES.txt)
keep the physical-module aggregation distinct from the earlier snapshot maxima.

The [separate electronics comparison](pds-spatial/apa1-comparison/electronics.html)
also displays APA1 in matching APA2 electronics order.
Typical precursor fluctuations favour channels 30/32/36 in APA1 and mainly
20/22/24/26 in APA2. Comparing channels 20–27 with 30–37 at the same recorded
times preserves the difference in each run. This saved sample does not reproduce
the electronics-order similarity illustrated in historical EDMS slide 21.
The [methods and event tables](../../../ground-shake-data/analysis/apa1-apa2-response-20261103/README.txt)
define the fluctuation, recording, and timing rules and retain the input hashes.

APA1 has only three events with sufficient common channels at the −60 µs and
+10 µs snapshots. APA2 has 586; among 411 initially strongest in M1/M2, 377
become strongest in M5/M6/M7. This measures the changing largest recorded
response, not a moving source. APA1’s 15 usable early pulses have tied leaders
in 12 events at the 20% threshold and 14 at 50%; no measured channel always
leads. The physical mapping, native ADC values and timing were checked against
the previously independently decoded example archive.

The [population histograms](pds-spatial/population/viewer.html) extend the APA2
comparison to all 1,377 saved records with endpoint 109 and a main-shake time.
All 1,531 records remain accounted for; 15 have no alignment time and 139
aligned records do not contain APA2 endpoint 109. The first-pulse histogram
has 602 assessable events, of which 99 are strongest in M6. Within 533 events
with common channels at the first pulse and -60 µs, 86 are first strongest in
M6 and 60 of those become strongest in M1/M2. The same trend appears in both
November runs and after excluding the two illustrative events. These are
changes in the largest recorded signal, not source trajectories or onset
rankings. [Methods and event-level tables](../../../ground-shake-data/analysis/pds-spatial-population-20261028/README.txt)
define the 12-channel, four-module, 20-ADC requirements and recording checks.

The [APA2 spatial supplement](pds-spatial/apa2-pds-sections.pdf) and
[section player](pds-spatial/viewer.html) use the existing physical maps for run
32731, events 52 and 33. Each section is one PDS module. Its plotted value is
the maximum absolute baseline-subtracted signal among recorded connected
channels, with the contributing-channel count shown alongside it. No channel
sum or light-yield estimate is made. The [method and input hashes](pds-spatial/README.txt)
describe the 0.512 µs snapshots, fixed time-series bins and excluded rail flags.

The [leading-channel map](pds-spatial/leading-channels.pdf) adds a native 16 ns
timing check. It examines the first existing sharp PDS candidate in 1,009
November records. The plotted subset contains 407 pulses before the TPC
precursor, each with at least eight timed connected channels. Channels 22 and
25 are often among the earliest, but no assessed channel always leads.
At 20% and 50% pulse depth, respectively, 260 and 365 of the 407 events have
leaders tied within one sample. These are measured waveform timings without
channel-latency calibration, not a physical-source reconstruction.
[Methods, per-event values and validation](../../../ground-shake-data/analysis/pds-leading-channels-20261028/README.txt)
retain packet exclusions, channel denominators and the threshold comparison.

Run `python3 public_review.py` to rebuild the five new figures from frozen values,
then compile `main.tex` with Tectonic. The original figures remain included.
`--refresh` deliberately reselects values from the local analysis and pins their
source hashes. No detector data are decoded or changed; no physics model is refitted.

[Speaker notes](speaker-notes.txt) explain each claim in plain language.
[Public-source manifest](evidence/public-source-manifest.json) pins the new inputs.
The [previous deck](archive/20261028-before-public-review/main.pdf) and its
[source notes](archive/20261028-before-public-review/SOURCES.md) are preserved.

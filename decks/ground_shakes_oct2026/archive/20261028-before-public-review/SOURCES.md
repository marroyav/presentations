# Sources and limits

The slides summarize existing exploratory results. They do not establish the
cause of a shake, identify a pulse as scintillation, or prove that two signals
are unrelated. “No unique match” is narrower than “no correlation”.

The data directory is
[`ground-shake-data/analysis`](../../../ground-shake-data/analysis).
The links below refer to that sibling directory. The deck's frozen plot values
and source hashes are in [`evidence/`](evidence).

## 1. Runs and scope

Use the final seven-run inventory, not the earlier `run-sample-summary.json`,
which predates 20 additional run 32739 records.

| Run | Saved events | Charge assessable | Charge-screen candidates |
| --- | ---: | ---: | ---: |
| 27938 | 6 | 6 | 1 |
| 27951 | 19 | 10 | 10 |
| 30201 | 44 | 44 | 44 |
| 30202 | 83 | 83 | 83 |
| 32730 | 1 | 0 | 0 |
| 32731 | 716 | 716 | 716 |
| 32739 | 662 | 662 | 662 |
| Total | 1,531 | 1,521 | 1,516 |

The charge-only screen samples 80 channels per assembly. It requires at least
half the sampled channels to exceed 1,000 ADC counts together on both APA1 and
APA2. It searches the available charge window. The onset is a threshold-based
alignment reference, not a calibrated physical start time. The later charge
analysis uses all 5,120 channels across these two assemblies.

An early, sharp PDS screen flagged activity in 1,179 of the 1,516 candidates.
The other 337 records do not establish an absence of earlier light. No candidate
has a fully recorded 4 ms PDS window before the shake. A separate, narrower
selection used for charge–light matching found 821 early PDS pulse candidates
in 598 events. These counts use different cuts and must not be combined.

Sources: [run counts](../../../ground-shake-data/analysis/all-runs/all-runs-summary.csv),
[screen definitions](../../../ground-shake-data/analysis/all-runs/README.txt),
[charge analysis](../../../ground-shake-data/analysis/charge-light-matching/report-data.json).

## 2. Charge and PDS example

Run 27938, event 20576 is the independently identified July shake. The slide
shows APA1 only: all 2,560 charge channels and all 40 continuous PDS channels
from DAPHNE endpoints 104, 105 and 107. Rows retain the original hardware/module
order; they are not positions in the detector.

Values are the original channel-baseline-subtracted means in 2.048 µs bins.
The displayed interval is −275 to +100 µs relative to the recorded trigger.
Colour limits are ±500 ADC for charge and ±200 ADC for PDS, as in the source.
Large signals exceed those display limits. Grey denotes missing samples.
The dashed −180 µs guide is not a fitted pulse onset. No hardware latency
correction was made. ADC counts are not calibrated charge or photons.

Source: [aligned detector data and method](../../../ground-shake-data/analysis/aligned-detectors/README.txt).

## 3. Opposite slow charge changes

The waveform example is run 32731, event 33. It uses the saved native 0.512 µs
medians over all 2,560 channels in each assembly, with a fixed per-channel
baseline from −280 to −250 µs. Only −250 to −20 µs is displayed; there is no
new smoothing, rescaling or fit.

The population check uses 1,376 November records with DAPHNE 109, rather than
the 1,378 November charge-screen candidates. Two run 32731 records fall outside
that PDS extraction cohort. Both slow signals exceed the analysis noise cut in
705 of 714 run 32731 records and 650 of 662 run 32739 records. All 1,355 have
APA1 positive and APA2 negative. The other 21 are not classified as opposite
exceptions; they fail the “both clear” requirement.

The cut is |late amplitude| ≥ max(2 ADC, three times baseline robust noise)
on both assemblies. The late amplitude uses −80 to −20 µs relative to the
main-shake reference. The baseline is −300 to −260 µs for this population
check. The scatter restores the original APA2 sign. It is not a map of
reconstructed particle charge.

Sources: [example method](../../../ground-shake-data/analysis/shared-precursor/README.txt),
[population results](../../../ground-shake-data/analysis/electrical-pattern-20261023/sequence-results.json).

The median Pearson shape correlations after reversing APA2 are 0.964140 and
0.969820. They describe waveform agreement, not discovery significance.
Perfect shape correlation allows a different offset and amplitude.

## 4. Disconnected inputs

The example is DAPHNE 109 in run 32731, event 33, around the selected pulse
at −183.296 µs. Each saved bin is the median of 16 raw samples, spanning 256 ns.
The plot shows differences between adjacent bins, using the same masks as the
source: incomplete samples remain missing; bins next to ADC rail codes and
steps above 2,000 ADC are excluded. No waveform model is fitted for this slide.

Inputs 13, 14 and 16 were reported disconnected in the engineering evidence.
The original analysis has not independently pinned the report identity or its
run coverage. This qualification appears on the slide. A pulse on an unlit
input supports an electrical contribution, but an optical event could itself
cause electrical pickup. Neither a fitted component nor its residual is a
pure electrical/light measurement.

Source: [electrical-pattern method](../../../ground-shake-data/analysis/electrical-pattern-20261023/README.txt).

## 5. Electrical response across runs

The electrical fits use 505 training events from run 32731. The 209 remaining
events from that run and all 662 events from run 32739 are held out. The slide
uses only run 32739. Each three-tap fit predicts connected-input changes from
the recorded changes on reported disconnected inputs 13, 14 and 16.

On identical samples, actual references score 0.156856; references borrowed
from other events score −0.047317. The left plot shows the square root of one
minus each score: 0.918 and 1.023. This is root squared error divided by the
root squared size of the observed change. A value of 1 is the zero-change
guess; lower is better.

The right plot uses the broader valid sample set, rather than the paired
shuffling subset. An early-pulse-trained fit scores 0.196391 on early pulses;
a main-shake-trained fit scores −0.194353 there. Score means
1 − sum(squared error) / sum(squared observed change). It is not a measured
fraction of electrical pickup or light. Strong edges dominate the pooled
score; the median event score is 0.021564 over 418 events with at least 50
valid samples. A simple linear fit failing to transfer does not prove two
different initiating causes.

Source: [fit results](../../../ground-shake-data/analysis/electrical-pattern-20261023/results.json).

## 6. Electronics channel groups

The same early-trained fit, tested on run 32739, gives these per-channel scores:

| Connected input | AFE | Score |
| --- | ---: | ---: |
| 12 | 1 | 0.692058 |
| 15 | 1 | 0.484099 |
| 40 | 4 | 0.672376 |
| 42 | 4 | 0.666793 |
| 20 | 2 | 0.010959 |
| 22 | 2 | 0.025904 |
| 24 | 2 | 0.054873 |

An AFE is an eight-channel analogue front-end chip. The reference inputs
13/14/16 are in AFE1. These are selected connected inputs highlighted in the
existing analysis, not a survey of every detector channel. The uneven response
constrains a circuit explanation; it does not locate the initiating source.

Source: [fit method and channel mapping](../../../ground-shake-data/analysis/electrical-pattern-20261023/README.txt).

## 7. Delayed charge–light matching

This is the existing nominal same-assembly timing comparison. The slide shows
the two November runs, where the broad peak near +325 µs appears with both
the original PDS times and times borrowed from other selected events.

The comparison preserves the charge event and its usable recorded interval.
PDS pulse trains come from up to ten other events in the same run, source file
and assembly. Weights preserve the target pulse count. Across the full
four-run mixing analysis, 820 PDS candidates qualify; one has no donor.
The plots retain the source's fixed 50 µs bins. Height is the number of compact
charge-feature/PDS pairs divided by usable comparison time, multiplied by
100 µs. It is not a normal-running detector rate.

The early PDS selection is −300 to −100 µs from the charge-onset reference.
The charge search uses the full recorded windows and masks the main shake and
other unusable samples. November charge records end near +0.35 ms after the
shake. Missing or corrupted charge cannot reject a light hypothesis. Charge
features may include pickup. No reconstructed 3D track or calibrated light
match is claimed. Reused donors preclude a simple independent-event
significance calculation. Do not turn the peak into a source distance.

Sources: [charge–light summary](../../../ground-shake-data/analysis/charge-light-matching/report-data.json),
[mixing method and results](../../../ground-shake-data/analysis/charge-light-matching/event-mixing-results.json).

## 8. Expanded slow-control comparison

The previous event-level check covered 11 July candidates. The new analysis
checks all 109 successful canonical native exports: 7,744,489 samples from 34
monitors. It brackets all 1,531 saved event records and tests the existing
waveform measurements in 1,376 November records.

The monitors cover APA1/2 wire-bias voltage/current, cathode/HV-derived values
and 16 ground monitors. Ground monitors 13 and 15 are too sparse for the
November comparison. No direct DAPHNE/PDS supply monitor is included.

The three waveform measurements are slow charge amplitude, recorded early
edge size on reported disconnected PDS inputs, and the fraction of records
with a selected early DAPHNE 109 pulse. SC levels are medians of actual
timestamps within ±30 seconds. There is no interpolation or fill-forward.
The archive contains 935,127 timestamps with multiple different values.
Their median, full range and count are retained. Medians of their minima and
maxima give separate sensitivity checks.

Records are grouped by source file and UTC minute. Bins have equal weight;
amplitude and SC medians use paired valid events, and pulse flags become
fractions. Correlations use within-file ranks after removing linear time
trends from both quantities. Raw and unadjusted results are also saved.
Eligibility requires at least 20 adjusted bins, three usable source files
and four distinct SC levels in each run.

None of 96 eligible monitor/measurement pairs has the same sign and magnitude
at least 0.30 in both November runs with one-minute bins. This was a descriptive
follow-up threshold, not a significance test or proof of zero correlation.
Individual-run correlations do exist.

The right panel reports the exception found in the sensitivity checks:
filtered cathode current versus slow charge gives 0.330498 and 0.324884 with
two-minute bins, but 0.193898 and −0.044513 with one-minute bins. The two-minute
hint also fails the minimum/maximum timestamp-envelope checks. Five-minute
bins have insufficient within-file coverage to decide. Whole-file resampling
and leave-one-file-out ranges are recorded as sensitivity summaries, not
population confidence bounds.

Use the scoped conclusion: **We found no robust correlation between the
tested slow-control levels and waveform features in the recorded November
sample.** This does not test shake rate, exclude brief transients, or establish
that SC changes cannot initiate a shake. The archive includes October bias
ramps and November HV changes; July's stable-voltage observation must not be
extended to all runs. Absolute subsecond SC/DAQ alignment is unverified.

Sources: [new analysis and limits](../../../ground-shake-data/analysis/sc-correlation-20261027/index.html),
[fixed methods](../../../ground-shake-data/analysis/sc-correlation-20261027/plan.json),
[all associations](../../../ground-shake-data/analysis/sc-correlation-20261027/associations.json),
[sensitivity results](../../../ground-shake-data/analysis/sc-correlation-20261027/report-data.json).

## 9. Remaining tests and missing data

There are 348 held-out unexplained pulse windows available for further track
and shape checks. These are not identified optical events. Existing work uses
raw-ADC features and segment starts; it has not established geometrically
consistent 3D charge tracks and calibrated light matches. Run geometry,
timing and recorded coverage must be checked before that reconstruction.

The local inventory has five classified July controls and no independent
matched November non-shake sample. Records with the same boards, gains and
trigger conditions, plus measured live time, are needed to measure precursor
excess, false alarms or shake occurrence versus SC conditions.

No circuit simulation has reproduced a shake. The available vendor model
omits relevant ADC, crosstalk, supply-rejection and recovery effects. Installed
components, wiring and AFE settings need confirmation. The SC sampling cannot
replace fast measurements of supply, ground and reference signals.

Sources: [unexplained-window review](../../../ground-shake-data/analysis/electrical-pattern-20261023/README.txt),
[circuit-model limits](../../../ground-shake-data/analysis/daphne-coupling-model/README.txt).

## 10. Backup: July voltage records

The slide shows native cathode and U-wire voltage samples within ±60 seconds
of event 20576 in run 27938 and of the median candidate time in run 27951.
Each trace is relative to its own median in the preceding −300 to −30 seconds.
Lines only guide the eye; no samples are interpolated.

For the ±30-second checks, the cathode monitor ranges from 176,370.22 to
176,373.77 V around event 20576 and from 176,369.47 to 176,371.53 V across the
run 27951 burst windows. U-wire bias changes stay below 1 mV and 2 mV,
respectively. Typical native intervals are 2.003 s for the cathode monitor and
10.669/10.695 s for the two U-wire monitors. Ten candidates within about
26 seconds do not supply ten independent operating conditions.

These slow records show no large voltage ramp or trip at the checked times.
They cannot resolve a microsecond or sub-millisecond discharge. The absolute
DAQ-to-controls clock offset has not been independently calibrated below a
second. This is not a formal correlation test. Board-supply monitoring was not
available in this export.

Source: [DCS association result](../../../ground-shake-data/analysis/dcs-association/README.txt).

## 11. Backup: prediction checks

These are the previously saved tests on run 32739. Models use only training
events from run 32731. No event shown in the test contributed fit coefficients.
The two panels have different valid-record requirements and denominators.

| Check | Test records | Comparison | Using early PDS |
| --- | ---: | ---: | ---: |
| Slow charge amplitude: mean absolute error | 477 | 3.7588 ADC, constant estimate | 3.6052 ADC |
| APA1 sustained 2 ADC crossing: mean absolute error | 225 | 33.4234 µs, fixed phase from known main shake | 66.0571 µs, first PDS pulse plus fitted delay |

The amplitude improvement is 4.0873%, rounded to 4.1%. The amplitude model uses
the recorded disconnected-input edge size, selected pulse count and number of
responding channels. The timing test selects early PDS pulses from −300 to
−100 µs and excludes charge crossings already underway at the start of the
record. A 2 ADC crossing is a diagnostic threshold, not a particle arrival
time. The known-shake comparison is retrospective, not an early-warning system.

Source: [prediction results](../../../ground-shake-data/analysis/electrical-pattern-20261023/sequence-results.json).

The 27 October arithmetic audit reproduced both errors from the saved event
metrics. It also found a metadata-only error: `training_constant_ADC` had been
overwritten by a timing constant. The correct training amplitude median is
11.0625 ADC. This does not change the predictions or plotted errors. Historical
files are unchanged; see the [audit](../../../ground-shake-data/analysis/sc-correlation-20261027/previous-results-audit.json).

## Reproduction

`prepare_figures.py --refresh` freezes the original six plots' values and
records source SHA-256 hashes. Normal runs verify those frozen inputs.
`extend_figures.py` freezes the completed electrical-fit results and the new
SC comparison, then makes or copies plots 07–09. Its inputs and figure hashes
are recorded in `evidence/extension-manifest.json`.

The SC comparison is new analysis of existing exports and saved waveform
metrics. No raw detector or SC files are modified, new records acquired, or
detector physics models refitted. `main.tex` is the editable slide source;
the PDF follows the repository's DUNE theme. The original seven-slide deck
and its validation record are preserved under `archive/`.

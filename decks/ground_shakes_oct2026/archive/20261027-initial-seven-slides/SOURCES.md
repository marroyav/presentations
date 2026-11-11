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

## 5. Prediction checks

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

## 6. Delayed charge–light matching

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

## 7. July voltage records

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

## Reproduction

`prepare_figures.py --refresh` freezes the displayed values and records SHA-256
hashes of the source results, arrays and method files. Normal runs verify the
frozen input hashes before making the six figure pairs. No raw data are
modified, new records acquired, or physics models refitted. `main.tex` is the
editable slide source; the PDF follows the repository's DUNE theme.

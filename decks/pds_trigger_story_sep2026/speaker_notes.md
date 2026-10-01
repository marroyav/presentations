# PDS data acquisition and local trigger conditions for VD LE — speaker notes

The slides are the short story. These notes hold qualifications and sources,
so they do not become a second technical presentation. Suggested duration:
about seven minutes. All proposed mitigations retain selected waveforms with
peak descriptors; descriptor-only readout is not proposed.

## 1. PDS data acquisition and local trigger conditions for VD LE

“We want to keep useful light even when a channel is very busy. I will show
why the current trigger struggles, what we studied, and what we need to
decide together with DAQ.”

## 2. Current DAPHNE gateware: 1024 samples per frame

Slide 2 reports the meaningful sample-data rate requested by the presenter:
62.5 MSPS × 14 bits = 875 Mbit/s/channel. A 1024-sample frame covers
16.384 microseconds. The diagram labels local frame acceptance and places
peak descriptors above waveform samples. “S” in its interval label means samples.

“This is our starting point. A trigger asks DAPHNE to save a short waveform.
The FPGA also describes up to five peaks so DAQ can work with pulse times
without finding every peak again.”

The revised diagram starts from continuous digitized samples and highlights
the selected interval. The two fields are inside one record and travel
together to DAQ. This is a content diagram, not wire order or exact pipeline
latency. Multiple pulses can occur within the selected interval; it is not
one record per photon. The trigger mark is inside the interval to allow
pretrigger samples.

The waveform uses a simplified positive-polarity version of the measured
Waffles NP02 cathode-C SPE template used in the activity simulation: a narrow
maximum followed by a long, curved recovery. Amplitudes, spacing and baseline
variation remain illustrative; this is not a plotted detector trace.

The user identifies the current 1024-sample baseline. The local `daphne-os`
release record pins the self-trigger artifact to
`3f17f1bdb14f13fd64dac0d8866dc3dda9e8dd96`, ABI 2.0, and describes it as an
engineering release candidate. Do not imply universal installation or full
production qualification. The split repositories own OS/runtime (`daphne-os`)
and FPGA source/builds (`daphne-firmware`), respectively. A 1024-sample record
spans 16.384 microseconds at 62.5 MS/s; this is not the complete busy interval.

Sources: `evidence/baseline-release.md`; the grouped32 deck's five-slot
comparison in `backup.tex`; XC simulator README, “Frame assembly” and
“Peak descriptors.” Repository references:
[daphne-os](https://github.com/DUNE-DAQ/daphne-os) and
[pinned gateware](https://github.com/DUNE-DAQ/daphne-firmware/tree/3f17f1bdb14f13fd64dac0d8866dc3dda9e8dd96).

## 3. Five summaries may not describe every peak

“Keeping a waveform and describing all its pulses are different jobs. A busy
waveform can have more than five peaks. Those extra peaks can remain in the
samples but be absent from the summaries used by the online trigger.”

This is an illustrative capacity argument, not a measured overflow fraction.
The upper row now shows all seven peaks in the saved waveform; the lower row
contains only five descriptor slots. Matching numbers identify the same peaks
in both rows. The example assigns summaries to peaks 1–5 for clarity; it is
not a new validation of the legacy peak-selection order. There are no empty
sixth/seventh wire slots, and no loss of waveform samples in this illustration.
Finding overlapping pulses also depends on the peak-finder algorithm and
threshold. No claim is made that every physical photoelectron creates one
resolved peak. Moving five slots from 1024 to 512 samples gives up to ten
slots across two retained fragments; either fragment can still overflow.
The seven pulse shapes use the same measured-template morphology as slide 2;
their amplitudes and spacing are chosen for legibility, not as a data trace.

Sources: grouped32 `backup.tex` and `window-formats-source.md`. The latter's
descriptor-loss numbers use a simplified synthetic model, so they are
deliberately not on these slides.

## 4. Dead time can continue after the frame is complete

“Finishing a frame does not mean we can assemble the next one. At high
activity, output data can remain queued. New triggers are still rejected
until shared readout drains enough data to reopen admission.”

The revised timeline separates record assembly from a variable period of
output-queue admission blockage after completion. Its widths are illustrative,
not measured durations. A backlog is not inevitable after every record.
The queue need not be physically full or completely emptied: the decision
uses its programmed admission threshold.

Checked directly in `stc3_record_builder.vhd` at baseline `3f17f1b`:
`d31` returns to `wait4trig` after the final block (lines 227–232), but a new
record starts only with an event, enable and `prog_full_s = '0'` (177–182).
Events in `wait4trig` with `prog_full_s = '1'` increment `fulldrop_count_s`
(141–150), separate from assembly-busy rejection. The FIFO has depth 4096
and a programmed-full threshold of 200 (286–304). Thus the 1024-sample
builder may have completed while output occupancy still blocks assembly.
The copied source and its SHA-256 are in `evidence/`.

The fixed channel-local model uses 1,037 busy cycles for 1024 samples and
525 for 512. Rejected candidates are not equivalent to lost photons or lost
events: a later pulse may already be inside a retained record. Record-busy
rejection, descriptor overflow, retained-sample loss and physics efficiency
must remain separate. The fixed interval is not a cap on hardware dead time;
shared readout and link back-pressure can extend admission blockage.

Source: activity deck README and “What the present firmware replay actually
does” slide; [baseline record-builder source](https://github.com/DUNE-DAQ/daphne-firmware/blob/3f17f1bdb14f13fd64dac0d8866dc3dda9e8dd96/rtl/isolated/subsystems/trigger/stc3_record_builder.vhd).

## 5. Count the time when signal cannot be saved

“If a pulse is already inside a saved waveform, it is covered. We want to
count the gaps where acquisition is blocked and no retained frame saves the
signal. A later frame can recover some earlier activity through its pretrigger.”

The earlier 61.57% / 46.80% comparison counted rejected requests to start new
frames. It cannot be used as a capture-loss percentage. The corrected study
now includes output FIFO admission and lane readout, using a C++ architecture
model rather than cycle-accurate RTL.

The new numerator is blocked time outside the union of retained input-sample
intervals; its denominator is observation time. Quiet live waiting time is
excluded from the numerator. All channel exposures, including quiet channels,
belong in the denominator. A candidate's timestamp being covered does not
guarantee complete pulse charge or a descriptor; those need separate checks.

The diagram is illustrative and not to scale. The first frame starts before
its trigger. The next frame likewise retains pretrigger samples, recovering
the end of the blocked interval. Only the uncovered gap is colored as dead
time. Assembly/transport times must be mapped to the input-sample axis.

Inputs are the nominal `deap0964` atmospheric-argon shards and gamma pilot.
Eight 8.5-ms VD windows cover 1,344 channels (42 modeled boards, 32 channels
each). Candidate times are treated as local trigger times; later pretrigger
samples can recover a blocked interval. The denominator includes every
channel's observation time; quiet live time is excluded. A covered candidate
does not prove that the whole pulse charge or its descriptor was retained.

Source hashes, definitions and per-board output are in
`evidence/capture-loss-model.md` and
`evidence/capture-loss-VD-one-link.csv`.

## 6. We needed an activity estimate for each VD channel

“We did not have an agreed VD rate to design against. So we simulated
radioactive argon and gammas. The cathode channels were especially demanding:
about 87,000 candidate pulses per second, before the firmware rejects any.”

The missing agreed forecast is the presenter's context, not an independently
surveyed claim that no DUNE group has ever estimated a rate. Rounded headline:
87,000 (rounded) Hz/channel at the VD cathode versus 24,338 Hz/channel in HD, a factor 3.594.
These are means over all hardware channels in the named population.
Slide 5 uses Hz/channel explicitly for both the rounded 87,000 baseline and
the 92,000 gamma-inclusive estimate, as requested by the presenter.

The baseline is an intrinsic-liquid-argon mixture dominated by atmospheric
39Ar at 0.964 Bq/kg, with 85Kr/42Ar/42K. It is not an Ar-39-only result.
Software: dunesw v10_22_00d01, larsoft v10_22_00, art 3.14.04. Full HD-v6
and VD-v7 geometries. Threshold strictly greater than 0.7 photoelectrons;
no 10-MeV cut. Eight independent intrinsic shards per detector: HD 4.492 ms
each and VD 8.5 ms each. Same 16 Waffles NP02 cathode-C SPE templates; this
does not establish identical detector gain, noise, or PDE.

The physical gamma pilot includes cavern-wall, foam, cryostat-neutron-gamma
and cavern-neutron-gamma source families, one window each. Overlaid with the
intrinsic sample it gives 92.383 kHz per VD cathode channel. Reusing the gamma
window with each intrinsic shard does not create independent gamma exposure.
Source overlay uses candidate times, not analog waveform pileup. The separate
10,000-trial-per-technology stratified gamma study measured conditional
response, not an absolute physical rate.

Sources: copied `activity.csv` and `gamma-pilot.csv`; activity README; grouped32
`evidence/larsoft-provenance.json` and original summary/manifest. Missing
backgrounds, independent gamma repetitions, electronics noise, detector
systematics and actual board mapping remain open. Rounded means shown without
uncertainty bands; no complete VD background or hottest-board forecast.

## 7. Limited output capacity drives dead time up

The plot keeps input activity on the x axis and capture dead time on the y
axis. Solid lines show total blocked, uncaptured time. Dashed lines show the
subset also blocked by the output FIFO; these are overlapping conditions,
not exclusive causal fractions. Both exclude samples saved in any frame.

A fresh sweep has 24 rates from 1 to 200 kHz/channel, five seeds, 32 channels
and one link per board. At exactly 87 kHz/channel, total dead time is 55.09%
for 1024/5 and 40.28% for 512/5. FIFO-blocked uncaptured time is 53.04% and
36.35%. Frame output is 7.931 and 7.841 Gbit/s, respectively.

The dotted 23/44-kHz markers estimate where mean offered load after the
channel busy gate reaches the finite shared-readout budget. They use Poisson
r/(1+r*t_busy), not correlated VD traces. Random bursts cause FIFO rejection
before those mean-load crossings. This explains the rising curves without
inventing a discontinuity or imposing a new stall rate.

The previous Hermes overlay is withdrawn. It drained through an ideal
always-ready output and cannot establish actual Hermes backpressure. The
current plot includes the finite DAPHNE readout budget into Hermes; it does
not include UDP-ready stalls or transport overflow. Baseline 3f17f1b has no
packet-ready feedback and can discard on overflow. Newer fixed-packet
firmware does have packet-ready feedback. These paths need separate complete
transport replays before attributing a numerical loss to Hermes itself.

## 8. One link is still the bottleneck

“Helping the channel accept more pulses moves more work downstream. In this
VD cathode example, even the shorter records offer more data than one link
can carry. A deeper buffer can postpone that problem; it cannot remove it.”

The one-link agreement comes from the presenter. At their request, the
limits now come from the firmware feeding Hermes: two 64-bit lanes at
62.5 MHz, with two idle scan/pause cycles per frame. The 1024-sample
baseline sends 232 words in at least 234 clocks, giving 7.931624 Gbit/s
per link. The 512 path sends 120 in at least 122, giving 7.868852 Gbit/s.
The diagram marks each format's limit, rounded to three decimal places.
These are ideal frame-word rates into Hermes with output ready; extra
channel scanning and downstream backpressure can reduce them.
The displayed demand estimates
come from the intrinsic-plus-gamma pilot after the channel-local gate:

- 1024: 32 × 34,534 records/s × 1,856 bytes × 8 = 16.408 Gbit/s.
- 512: 32 × 48,297 records/s × 960 bytes × 8 = 11.870 Gbit/s.

All 32 channels are illustratively assigned the cathode mean. This is not
real board wiring or an achieved output measurement. Usable 10-Gbit/s payload
capacity is lower than line rate. In real firmware, back-pressure feeds back
into acceptance; these offered inputs cannot persist as lossless outputs.
Sources: `gamma-pilot.csv`, activity deck transport assumptions, and
[the pinned firmware rate derivation](evidence/hermes-link-budget.md).

## 9. More links buy capacity, with an infrastructure cost

“Another option is to keep more data and send it over two or four links.
We can keep the FPGA peak descriptors. But that choice reaches beyond
firmware: DAQ needs receiving servers and the CUC needs the power capacity.”

The slide uses the studied 512-sample sender as its explicitly labelled
reference: 7.869, 15.738 and 31.475 Gbit/s for one, two and four links,
rounded from 8 × 120/122 Gbit/s per link. Two 64-bit input lanes per link
run at 62.5 MHz; each frame takes 120 data clocks plus scan and pause.
Those are ideal frame-word budgets into Hermes, not Ethernet line rates or
measured delivered payload. All lanes must have ready frames and downstream
credits. Different formats have different budgets: the 1024 baseline gives
7.932 Gbit/s/link, and the following 256/5 candidate removes scan/pause gaps.
The grouped32 source maps eight internal lanes to four links; simulation
checked logical lanes, not sustained physical Ethernet. Two links may help
the displayed average-load example but are not proven sufficient for peaks,
uneven mapping or continued capture. Continuous 32-channel 512-sample
self-trigger records require about 30 Gbit/s before network overhead.
More external links do not fix descriptor overflow or an internal builder
bottleneck. New channel/link mapping, Ethernet/DAQ validation, receiving
resources and CUC power planning are needed. No server count or wattage
estimate is available in the input decks.

Sources: grouped32 `backup.tex`, `diagrams/links.dot.in`, README and
the grouped32 deck's `evidence/fullstream-source-check.md`, and
[the pinned firmware rate derivation](evidence/hermes-link-budget.md).
Current agreement and infrastructure
consequence: presenter-provided planning context.

## 10. Four links and gapless readout make 256 / 5 possible

“This design also removes the gaps between frames sent to Hermes. Each link
can accept up to 8 Gbit/s at that interface; the full 256 / 5 stream needs
7.875. Four links therefore fit the frame-data budget while keeping the
waveforms and up to five peak descriptors per frame.”

This is the built grouped256 candidate `e49c4aae`, not merely a suggestion
to truncate 1024-sample waveforms. Each record has 256 densely packed 14-bit
samples, five compact 64-bit descriptor slots and two common header words:
63 words, or 504 bytes. The 64 pretrigger samples and continuation preserve
the configured posttrigger coverage across accepted records. Format 4 requires
a corresponding DAQ decoder; the control interface remains ABI 2.

The implementation uses gapless internal readout and matching Hermes packet
reservation. This matters: the earlier 256/5 sensitivity table, which assumed
two idle cycles per frame, gave 101.56% dense internal lane occupancy. With
the implemented gapless service, the ideal four-channel occupancy is
4 × 63 / 256 = 98.4375%. These are internal lane budgets, not an achieved
Ethernet rate. A full stream of 32 such channels would offer 31.5 Gbit/s of
frame content before network overhead. Across four equally loaded links,
that requires 31.5 / 4 = 7.875 Gbit/s of usable frame-data throughput per link.
The built candidate explicitly enables GAPLESS_G. Its Hermes input buffer
accepts one valid 64-bit word per source clock, including adjacent frame
boundaries, after reserving room for the whole frame. With two sources per
link, the interface ceiling is 2 × 64 × 62.5 MHz = 8 Gbit/s/link.
The 7.875 Gbit/s demand fits within that ceiling; it must not be compared
against the older 512 scan/pause ceiling as if the implementations were
identical. Retaining two idle clocks with 63-word frames would instead give
only 7.754 Gbit/s/link and fail this dense-load budget.

This is a source-side budget, not measured sustained Ethernet delivery.
The existing buffer, descriptor and qualification limits still apply;
backpressure can reduce acceptance. Full-chain delivery needs validation.
The slide follows the link/infrastructure tradeoff because the full
32-channel continuous stream needs all four balanced links at the calculated
full-load budget. The VD activity-trace loss for 256/5 has not been measured.
The production RTL mapping uses four links and the available replay bench
uses synthetic stresses, not these LArSoft waveforms.

The revised figure shows one accepted frame: descriptor slots above the
waveform samples. It represents frame content, not wire timing or a continuous
capture sequence. Other header fields are omitted. A frame need not contain
five peaks: up to five descriptor slots are valid. The 256 samples span
4.096 microseconds at 62.5 MSPS. No artificial waveform is drawn, and no fixed
number of continuation frames is implied. Five slots in each retained 256
samples gives up to twenty across 1024 retained samples. A single fragment can still
overflow if it contains more resolved peaks than its slot budget. Preserving
selected waveform data and descriptor fields is not a guarantee of accepting
all input at arbitrary load, or identifying every photoelectron.

All five final grouped replay modes passed; the frozen handoff reports
30,428 grouped packets, 15,537,664 samples and 303,470 descriptor words checked.
These are the 256-study counts, separate from the 512-study result on slide 7.
The e49c4aae build produced bit/bin/XSA/DTBO artifacts and positive routed
setup/hold slack. CDC/methodology review and external I/O timing remain open;
no board was programmed in that campaign.

Sources: [the pinned firmware rate derivation](evidence/hermes-link-budget.md),
`evidence/gateware-build-handoff.md` and the corresponding
`grouped256-production/releases/daphne-selftrigger-e49c4aae/README.md` in
the local workflow campaign. The new slide deliberately makes no complete
physics-efficiency or production-qualification claim.

## Backup 1 (former slide 7). The smallest pulses are worth keeping

“Simply raising the threshold is tempting. But those small signals may help
us identify backgrounds and recover useful detector volume. We need to know
what physics we lose before making that choice.”

Single-photoelectron activity motivates the study. Background rejection and a
larger fiducial volume are goals, not demonstrated benefits of this gateware.
Evaluate signal acceptance and residual backgrounds together. The source
decks cite the [DUNE Phase II study](https://cds.cern.ch/record/2909101/files/document.pdf)
for the broader low-energy motivation; this new deck makes no new quantitative
physics claim.

## Backup 2 (former slide 8). We tested the problem from C++ to gateware

“The C++ models let us try ideas quickly. HDL simulation checks the actual
logic under load. FPGA builds tell us whether the design fits and meets its
timing constraints. Each step answers a different question.”

The grouped32 HDL replay at firmware
`7a25777e23f6435f9c680d10299e6795a7dfc2c4` passed five deterministic cases and
checked 379,656 descriptor words, 16,198,656 samples and 15,956 grouped packets.
This checks calculated descriptor fields in saved records, not completeness
for all incident photons. Trigger metadata was injected; analog detection
efficiency, physical Ethernet and a realistic FD load were not exercised.
The exact source candidate under that report is `26bb2295`.

The C++ work includes fixed-busy replay, waveform/peak emulation, and record
format/capacity studies. The 512-sample ring-buffer/continuation implementation
and subsequent 256-sample build work test implementation limits. The latest
local 256 build evidence (`e49c4aae`) records generated FPGA artifacts and
positive but tight routed timing, with CDC/methodology and board qualification
still open. This deck does not claim that candidate is deployed, qualified,
or the selected mitigation.

Sources: `evidence/grouped32-report.json`; grouped32 README; XC README;
`evidence/gateware-build-handoff.md` (dated 16 September 2026 snapshot).

## Backup 3 (former slide 9). One link: the VD activity fills the output FIFO

The table replays actual saved LArSoft candidate times across the full VD with
32 channels per board and one link per board. Intrinsic result: dead time is
34.60% for 1024/5 and 21.54% for 512/5. Missing threshold candidates are
43.36% and 28.61%. Busy/FIFO-rejected trigger requests are 72.09% and 55.00%.
With the gamma pilot, dead time becomes 42.80% and 27.79%, and missing
candidates are 48.24% and 32.50%.

The 5.23 million intrinsic requests produce 1.46 million accepted 1024/5
frames (1.45 million drained during the window), versus 2.35 million accepted
512/5 frames (2.34 million drained). Request rejections combine builder-busy
and FIFO-full counters; they are not output packets discarded after building.
The FIFO model adds each completed record to occupancy as a block, then models
word-by-word lane drain. Hermes is assumed ready. This is an architecture
estimate, not an RTL or Ethernet result. The 256/5 VD trace is not replayed by
this model.

## Backup 4 (former slide 12). On one link, we must agree what gets through

“There are three knobs to agree with DAQ: the record format, which records
we admit to readout, and how we combine peaks into a trigger.”

Proposed work, not an approved DAQ contract:

1. Choose a shorter fixed waveform length and descriptor budget. Preserve
   selected waveform samples, time/charge fidelity and pulse-tail continuation;
   check header overhead and internal lane capacity. A shorter record can
   increase traffic if the number of transmitted records increases.
2. Agree admission before transmission: thresholds, buffering, priority or
   rejection during overload, loss counters and calibration/monitoring access.
   Evaluate any threshold change against weak-signal acceptance.
3. Agree local PDS coincidence rules using descriptor times across channels:
   multiplicity, time window, latency and where the logic lives. A coincidence
   decision made in DAQ after data arrival does not reduce board-to-DAQ traffic.
   To control that link, selection must occur upstream or feed an implementable
   upstream admission decision with sufficient buffering.

These are alternative/complementary mitigations, not a guarantee that all
signals can fit one link. Format/ABI changes require a matching DAQ decoder.
Full stream is a useful signal reference but transfers peak finding to DAQ
and demands additional bandwidth; it does not preserve FPGA peak descriptors
by itself. It is therefore not presented as a cure for the one-link problem.

Sources: grouped32 main/backup and fixed-format study; proposal synthesis for
this talk. No descriptor-only or variable-length tile format is proposed.

## Backup 5 (former slide 15). Let's agree how much signal we can afford to lose

“We now know which questions to ask. Let us agree the readout and trigger
rules, choose the link budget, and test that choice on the same signals.”

Concrete follow-up: PDS and DAQ agree a readout-admission policy, descriptor
format, coincidence rule, acceptable signal loss and number of links; DAQ
and infrastructure teams assess receiver/server/power capacity. Compare the
1024 baseline, buffered shorter-record candidates, and a full-stream signal
reference with matched input, thresholds and transport limits. Count missing
peaks, saved unique samples, timing and recovered charge separately.

Include realistic backgrounds, mapped shared transport and measured surface
full-stream data as a stress test. Surface activity is not an underground
rate forecast. The matched full-chain result remains to be measured.

## Presentation revision

The talk now runs baseline and definitions (2–5), activity and physics motivation (6–7), tools and results (8–10), then output limits and mitigation choices (11–15). Backup slides remain included in the PDF. The 87 kHz/channel reference is the rounded intrinsic VD cathode mean at a threshold strictly above 0.7 PE; it is not assigned uniformly to all 1,344 channels. Slide 11 now uses intrinsic cathode accepted rates (33.62 / 46.53 kframes/s/channel), giving 16.0 / 11.4 Gbit/s before shared FIFO losses. Historical gamma discussion in these notes remains context only.

## Continuation (new slide 11)

Reuses the grouped32 pulse-window illustration, adapted to 256 samples. With continuation enabled and credits available, continued activity requests a frame starting at the next sample. This describes adjacent saved intervals, not instantaneous assembly or transmission. Finite queues can still overflow. Source: stc3_record_builder.vhd, continuation start_seq + FRAME_SAMPLE_COUNT_C.

Slides 7 and 8 now show the one-link budget before its dead-time plot. Backups remain commented out.

## Final slide: two-link pilot comparison

Source: workflow/tasks/daphne/256-5-two-link-frequency/scan/results.json and comparison_summary.csv. All32 channels, matched candidate timestamps; seven rates and two seeds. Per seed:0.32ms warmup,0.96ms measured.256 uses grouped RTL with portable XPM and four gapless readout lanes, eight channels/lane; continuation enabled with synthetic32-tick pulses.1024/512 use the existing C++models. Plot shows congestion-blocked time outside saved waveform coverage, not rejected triggers. Finite readout into Hermes is modeled; full UDP/MAC stalls are not. At87kHz the256 pilot gives0.10547% congestion dead time and0.18714% missing candidates (mean of two runs). Short pilot, not hardware or full-VD validation. Original frequency plot remains unchanged.

# Self-trigger, with full-stream fidelity

## Audience and outcome

DAPHNE firmware, DAQ, and photon-detection colleagues. The main comparison is
signal preprocessing: raw full-stream data requires downstream pulse finding;
self-trigger records include FPGA peak descriptors that can feed time
coincidences and **local PDS trigger activity**. Agreement with full-stream
signal timing and charge is the milestone. Keep the dead-time mitigation and
beam-independent low-energy physics rationale in backup.

## Scope and narrative

1. Page two: sample waveform, 64 pretrigger samples, and an afterpulse split at
   the 512-sample boundary; keep the block explanation below.
2. Full-stream fidelity as the milestone; move pulse finding from DAQ to FPGA.
3. Peak descriptors plus waveforms feed local PDS trigger activity.
4. Grouped architecture, present RTL evidence, and LArSoft load.
5. Matched full-stream comparison as the next measurement.
6. Backup: dead time, no-beam physics, packet details, bandwidth, and source limits.

The main comparison is now **1024-sample self-trigger vs 512-sample self-trigger
with ring buffer/continuation vs full stream**. Slide 9 defines a matched
surface-data replay. Slide 11 separates sample retention from pulse finding:
full stream retains every sample under a lossless-transport/storage assumption,
but online pulse finding is a separate DAQ algorithm and processing requirement.
Self-trigger supplies FPGA descriptors. The grouped/native loss plot is no longer
shown: it answers an implementation-validation question, not this comparison.
The retained RTL correctness evidence must not be presented as a measured
three-way result. Full stream is a signal reference, not assumed lossless transport.

User steering: laconic, human wording; one concept per slide. Architecture is
shown with editable diagrams. Include LArSoft results and a comparison against
full stream. Detailed checks and the dead-time/no-beam physics argument stay in
backup. The deck uses the shared presentation framework, with a local title-rule
offset requested by the user to clear the Fermilab logo.
After readability review, the deck uses light coral-orange (#F3A07A) for
waveforms, labels, diagram accents, and layout. Deeper orange (#DE6126) is
reserved for filled primary accents with dark text. `palette.py` and the shared
opt-in `DuneUseReadableOrange` variant agree; other decks retain their colors.
`render_waveform.py` is an illustrative deterministic drawing, not
an RTL output or measured detector pulse. Window 1 is samples 0–511; window 2
is 512–1023. The rising edge is at sample 64 and the peak at sample 75:
pretrigger is measured before the rising edge, not before the peak.

Slide 19 identifies the surface full-stream sample in xc_sim as a pessimistic
stress test, as supplied by the user; it has not been replayed in this study.
Slide 20 now uses a clean synthetic fast-rise, slow-decay waveform with a second
pulse, without noise, not measured SiPM data. Its timing
example is (64 + 11) samples * 16 ns = 1.200 us from record start. The rising
edge is at sample 64: 64 pretrigger samples span 1.024 us; the peak is later.
The second pulse is shown as a second detected peak with its own descriptor in
the same 512-sample record; this illustration assumes both peaks are resolved
by the configured peak finder, not that every physical afterpulse is detectable.
All five waveform-derived fields are calculated from the plotted integer ADC
samples and annotated directly: start, peak amplitude, integral, relative
peak position, and duration. Positive polarity; baseline 4000 ADC; threshold
100 ADC above baseline. Values are in `evidence/descriptor-example.json`.
The strict `a > threshold` excursion semantics and format byte 0xF1 follow
`fragment_peak_descriptors_banked.vhd` at the checked firmware commit. The
integral sums amplitudes, not amplitudes minus threshold. Duration saturates
at 511 in the wire field (not relevant to these two shorter excursions).
Slide 21 compares five descriptor slots per 1024 samples with five per 512:
finer descriptor coverage, not finer ADC time resolution. Up to ten slots are
available across two retained fragments; either fragment can still overflow.
Slide 27 estimates traffic from modeled activity only, excluding other
background sources; it is not a complete detector-background prediction.
Slide 28 contrasts constant full-stream traffic with activity-dependent
512-sample self-trigger traffic using the HD intrinsic-plus-gamma pilot:
43,855 candidates/s/channel gives 10.7778048 Gbit/s for 32 channels at one
960-byte record/candidate, versus 28.57142857 Gbit/s full stream. This is an
offered-record estimate, not a measured ring-buffer throughput or savings result.

`evidence/daq-document-notes.md` records the local DUNE FD document analysis.
It supports the processing architecture and scale; it does not establish a
measured PDS pulse-finding hardware impossibility. The main slide quantifies
2 billion ADC samples/s per 32-channel board instead.

## LArSoft and full-stream comparison

The September 9 activity snapshot is reused, not rerun. Inputs are copied into
`evidence/larsoft-*`, including the original combined summary and manifest from
`work/wl-144132/dune-le-pds/output/materials/intrinsic-external-gamma-candidate-trace-deadtime-pilot-v1/`.
The renderer verifies the original summary checksum and both displayed rates
against its unrounded numbers (within the frozen CSV's rounding precision).

- Software: dunesw `v10_22_00d01`, larsoft `v10_22_00`, art `3.14.04`.
- Models: full FD-HD and FD-VD optical configurations described by the source
  campaign; HD is APA-integrated, VD is split into cathode/long-wall/short-wall.
- Selection: candidate episodes strictly above 0.7 PE; no 10 MeV cut.
- Exposure: eight intrinsic shards; HD 4.492 ms per shard (35.936 ms total),
  VD 8.5 ms per shard (68 ms total). The gamma pilot reuses one window per
  each of four source families; those repetitions are not independent gamma data.
- Baseline: atmospheric argon mixture, including 39Ar at 0.964 Bq/kg, plus
  the released 85Kr/42Ar/42K components. No complete-background claim.
- The plots show rounded means, not uncertainty bands. The original summary
  carries shard statistics; gamma repetition and noise systematics remain open.
- Optical response uses the existing 16 Waffles NP02 cathode-C SPE shapes.
  Candidate-level source overlay does not reconstruct analog waveform pileup.

All new traffic calculations use **32 channels**, including HD. The earlier
HD presentation used 40; its board-traffic columns are not used here.

`T_candidate = 32 * R_candidate * 960 bytes * 8` assumes one 512-sample
record per candidate before losses, continuation, or merging. Each board is
illustratively filled with one population at its mean rate. This is not a
mapped grouped32 throughput simulation, an actual board wiring model, or a
predicted achievable bandwidth reduction.

Full stream has **28 Gbit/s of raw sample payload**:
`32 * 62.5 MHz * 14 bits`. The checked source uses 35 blocks per record,
7 payload words/block, and 5 header words: the plotted full-stream record
demand is `28 * 250/245 = 28.57142857 Gbit/s`. It excludes network overhead
and is source-derived, not a measured gateware result. The formatter densely
packs 14-bit samples; a hypothetical 16-bit padded rate is not used in the plot.
Fully continuous 512-sample self-trigger records would send 30 Gbit/s
including their record headers, before network framing. Thus sustained activity
can remove the traffic advantage. Four 10-Gbit/s physical links are a separate
line-rate capacity; this deck does not equate that capacity with useful payload.

The full-stream source has **four channels per logical stream and two streams
per physical link**: eight channels/link, 32 selected channels/board. See
`evidence/fullstream-source-check.md` for the exact source chain. The user's
possible 16-channel limit is not present in the checked source; an older or
partially enabled installed image was not ruled out by a hardware readback.

## RTL input and measurement

All modes use 32 channels and a deterministic waveform, with no random seed,
event weights, POT, physical geometry, or statistical ensemble. ADC ticks are
16 ns. Activity starts at tick 256 (plus seven ticks per channel in mode 1)
and stops at tick 54,000; every third channel has 32 active / 8 quiet samples.
Amplitude is `200 + (tick*13 + channel*17) mod 1500` ADC counts. Even channels
have negative pulses around 8,000; odd channels positive pulses around 4,000.
The descriptor/continuation activity threshold is 64 ADC counts and quiet
termination requires 32 samples. Trigger metadata is injected; XC detection
efficiency is outside this replay.

Modes 0, 1, and 4 run to tick 62,000; overload modes 2 and 3 to 72,000,
including drain time. Mode 2 blocks all lanes on ticks 2,000 through 35,999
(544 microseconds). Mode 3 disables continuation and forces triggers every
64 ticks (1.024 microseconds). Mode 4 resets/disables acquisition deliberately.

Active-sample loss uses the union of retained intervals divided by all nonzero
input samples. Charge loss uses the same union weighted by positive amplitude
after polarity normalization, in ADC counts times sample ticks. There is no
conversion to PE or MeV. Neither metric is trigger busy-time dead time or
event-level efficiency. Mode 4 is excluded from retention ranking.

## Provenance

Firmware remote: `DUNE-DAQ/daphne-firmware`, branch
`codex/selftrigger-512-32ch-grouped4`, fetched 2026-09-15, tip `7a25777e`.
The branch's FPGA source candidate is `26bb2295ac459a2f621abc66e4e4e8f91bcf55f9`;
 subsequent commits publish evidence.

The old `docs/grouped32-validation.json` is an earlier snapshot. Use the fresh
replay for this deck, not a mixture of its counts with the later approval report.

### Fresh local verification

All five modes passed on firmware `7a25777e23f6435f9c680d10299e6795a7dfc2c4`,
using the bundled OSS CAD Suite GHDL and a zero-picosecond builder phase offset.
The replay checked 15,956 grouped and 15,682 native packets, 13,180 common
byte-identical packets, 16,198,656 samples, and 379,656 descriptor words.

| Mode | Grouped active-sample loss | Native active-sample loss |
| --- | ---: | ---: |
| Simultaneous | 0% | 0% |
| Short stalls | 0% | 0% |
| Long stall | 34.771120% | 35.488931% |
| Dense overlap | 0.007243% | 0.033281% |

Reset/control mode passes the packet oracle but is not ranked for performance.
The copied `evidence/report.json` includes source and packet-trace hashes;
`results.csv` also contains charge-loss values. Raw replay CSVs are preserved in
`daphne/firmware/repos/daphne_mezz_xc_sim/results/grouped32/replay/` (Git-ignored).

Fresh generation used the clean detached worktree
`/tmp/daphne-grouped32-7a25777e-au7qYa/firmware` and the firmware runner's
`--output-dir /tmp/daphne-grouped32-7a25777e-au7qYa/replay-phase0`. After copying
the completed replay to durable XC storage, analysis used:

```sh
python3 scripts/run_grouped32_rtl_study.py \
  --firmware-root /tmp/daphne-grouped32-7a25777e-au7qYa/firmware \
  --replay-dir results/grouped32/replay \
  --output results/grouped32/report.json
```

This can be reproduced with any clean checkout of that exact firmware commit;
`--run` generates fresh captures. Five focused XC tests also pass, including
overlap counting and rejection of stale/empty source manifests.

Physics context (backup only):

Slide 18 motivates preserving low-energy light for background rejection and
solar/supernova neutrino searches. Increased usable fiducial volume is posed
only as a study question, not a demonstrated gateware benefit. Background
tagging must be evaluated through signal acceptance and residual background,
not equated with detecting electronics noise. See the
[DUNE Phase II study](https://cds.cern.ch/record/2909101/files/document.pdf).

- DUNE Collaboration, [Supernova neutrino burst detection](https://arxiv.org/abs/2008.06647),
  few- to few-tens-of-MeV sensitivity and complementary TPC/PDS information.
- [DUNE FD interim design report](https://cds.cern.ch/record/2632821/files/fermilab-design-2018-03.pdf),
  photon timing and triggering for events uncorrelated with the accelerator.

These references motivate the measurement; they do not validate an efficiency
prediction from the grouped RTL replay.

## Build

From the presentation repository:

```sh
python3 decks/grouped32_simulation_sep2026/render_larsoft.py
python3 decks/grouped32_simulation_sep2026/render_results.py
python3 decks/grouped32_simulation_sep2026/render_waveform.py
python3 decks/grouped32_simulation_sep2026/render_descriptor_time.py
make decks/grouped32_simulation_sep2026/main.pdf
make audit
make check
```

Python figures use matplotlib/numpy and the shared color tokens; Graphviz
sources are in `diagrams/`. Rebuilds use the copied evidence by default.

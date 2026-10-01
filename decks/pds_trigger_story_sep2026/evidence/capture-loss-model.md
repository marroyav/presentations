# VD loss replay: one link per 32-channel board

## Inputs and output

The source is the pinned nominal `deap0964` VD atmospheric-LAr candidate trace (eight independent 8.5-ms intrinsic shards per module class) plus the external gamma pilot overlaid on the same intrinsic time windows. Threshold candidates are strict >0.7 PE episodes at 16 ns. Population: 640 cathode + 640 long-wall + 64 short-wall channels = 1,344 VD channels. They are grouped by module class into 42 modeled boards of 32 channels. This is the requested study grouping, not an installed cabling map. The gamma pilot traces are reused across the eight intrinsic shards; the combined sample does not represent independent gamma realizations.

| Metric | Intrinsic | Intrinsic + gamma pilot |
|---|---:|---:|
| Input threshold episodes | 5,228,561 | 6,502,824 |
| 1024/5 dead time | 34.60% | 42.80% |
| 512/5 dead time | 21.54% | 27.79% |
| 1024/5 episodes outside every retained frame | 2,267,339 (43.36%) | 3,136,942 (48.24%) |
| 512/5 episodes outside every retained frame | 1,496,057 (28.61%) | 2,113,250 (32.50%) |
| 1024/5 rejected trigger/frame requests | 3,769,803 (72.09%) | 5,006,994 (77.00%) |
| 512/5 rejected trigger/frame requests | 2,876,098 (55.00%) | 3,892,141 (59.86%) |

“Rejected trigger/frame requests” means arrivals rejected before a record is assembled, split between the builder-busy and FIFO-full counters. It does not mean complete packets lost from a transmit queue. Accepted frames not yet drained at the observation boundary are not counted as rejected. “Missing candidates” means candidate timestamps lie outside the union of all retained sample intervals. A candidate is not an individual photon; timestamp coverage alone does not ensure full pulse charge or a complete descriptor.

## Dead-time definition

For each channel, form the union of builder-busy and FIFO-admission-blocked intervals; subtract the union of retained waveform sample windows; clip to the source observation window; sum across channels; divide by the full observation duration across all 1,344 channels. Quiet live time is excluded. Later-frame pretrigger samples recover part of blocked intervals. Denominator is 5,712,000,000 channel ticks (1,344 × 531,250 samples × 8 source windows at 16 ns/sample).

## C++ architecture model

This result extends the local `daphne_mezz_xc_sim/src/ring_deadtime_sim.cpp` legacy builder/FIFO/readout model to accept original trace timestamps and count retained sample coverage. Board channels are sorted by module class and channel ID, then divided into groups of 32. One link is two 64-bit, 62.5-MHz readout lanes; each lane scans 16 channels. Existing configurations use 232-word/1,037-clock frames for 1024 and 120-word/525-clock frames for 512, with 200/220 FIFO full/empty thresholds.

Accepted frame words enter output FIFO occupancy as a block when assembly completes. The model then drains records word-by-word via the two lane schedulers. This captures delayed admission after builder completion, which is the main loss mechanism here. It does not model individual FPGA FIFO writes, cycle-accurate RTL, Hermes/DAQ stalls, network envelopes, or measured Ethernet throughput. The C++ model assumes the downstream interface remains ready. The 256/5 grouped builder has a different gapless packet/continuation path and is not evaluated by this result.

Input SHA256 values are pinned in `../../grouped32_simulation_sep2026/evidence/larsoft-original-summary.json` and the original manifest. The raw inputs are preserved on WL-144132. The task-local replay, per-board run outputs and checks are under `/home/neutrino/work/workflow/tasks/daphne/fifo-capture-loss-fullvd-20260918/`.

# Frame-data budget into Hermes

Derived from pinned firmware on 17 September 2026, at the presenter's request.
Rates count DAPHNE frame words, including frame headers and peak descriptors.
They exclude Hermes/network envelopes and are not measured Ethernet throughput.

Each physical link has two 64-bit source lanes clocked at 62.5 MHz:
2 × 64 × 62.5 MHz = 8 Gbit/s at the Hermes input interface.
The readout scheduler can reduce the rate actually presented to that interface.

| Sender | Words/frame | Minimum idle clocks/frame | Frame-data limit/link (Gbit/s) |
|---|---:|---:|---:|
| 1024 baseline | 232 | 2 | 8 × 232/234 = 7.931623932 |
| 512 study | 120 | 2 | 8 × 120/122 = 7.868852459 |
| 256/5 gapless candidate | 63 | 0 | 8.000000000 |

The 512 reference gives 7.869, 15.738 and 31.475 Gbit/s across one, two
and four links, rounded independently from the unrounded per-link rate.
Budgets assume ready frames, downstream admission credits and balanced lanes.
Extra scans of inactive channels, link stalls and resets reduce acceptance.
An idle link cannot automatically lend capacity to another link.

The 256/5 full-load demand is a separate quantity. A frame has 56 packed
waveform words, five descriptor words and two common header words: 63 words
or 504 bytes. With eight continuously active channels per link:

8 channels × 63 words × 64 bits × 62.5 MHz / 256 samples = 7.875 Gbit/s/link.

Four links carry 31.5 Gbit/s of frame data. Gapless readout uses
4 × 63/256 = 98.4375% of each four-channel lane's clock budget.
Keeping the old two idle cycles would give only 8 × 63/65 = 7.753846154
Gbit/s/link. Thus the implemented gapless scheduler is essential to this
full-load budget; the older 512-sender limit does not apply unchanged.
Sustained Ethernet/DAQ delivery and the remaining hardware qualifications
are separate from this interface arithmetic.

## Source trace

Repository: DUNE-DAQ/daphne-firmware. Exact file hashes and paths are in
[hermes-source-manifest.json](hermes-source-manifest.json). No RTL was changed
or simulation rerun for this presentation revision.

- Baseline `3f17f1bdb14f13fd64dac0d8866dc3dda9e8dd96`:
  `stc3_record_builder.vhd` writes eight header words and seven packed words
  per 32-sample block, for 232 words (lines 254–280).
  `two_lane_readout_mux.vhd` moves from final dump to pause to scan to dump;
  only dump asserts valid (lines 80–126). Two clocks carry no frame word.
- 512 study `7a25777e23f6435f9c680d10299e6795a7dfc2c4`:
  `docs/four-sfp-selftrigger-512.md` specifies two lanes per link, 120-word
  frames and 120 data clocks plus scan/pause (lines 3–47).
  Its readout mux implements the same two idle states.
- 256/5 candidate `e49c4aae562c7f13c4922098358179b293b8b3e5`:
  `k26c_selftrigger_datapath_plane.vhd` enables `GAPLESS_G => true`
  (lines 184–205). The mux remains in dump at a frame boundary when the
  next channel and Hermes admission are ready (lines 80–96).
  `k26c_board_hermes_transport_plane.vhd` configures four links, 63-word
  frames and 512-word input FIFOs, with `data_clk => clock` (lines 122–155).
  Hermes `deimos/daphne_top.vhd` maps each pair of sources to one link and
  configures `N_SRC => 2` (lines 113–123, 166).
  Hermes `deimos/tx_mux_ibuf.vhd` reserves a full frame plus four pipeline
  words and accepts each valid source word (lines 109–132); its input FIFO
  is 64 bits wide and written on `src_clk` (lines 135–166).

The frozen build handoff separately records vendor FIFO/gapless tests and
the candidate build. Those tests are not a sustained physical-link benchmark.

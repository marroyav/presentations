# Finite-readout frequency sweep — corrected scope

The current plot shows total capture dead time and its FIFO-blocked subset
against input activity. It removes the misleading ideal-Hermes overlay and
the unexplained local-gate control. Both plotted metrics subtract all saved
sample coverage, including later pretrigger recovery. Their difference is
not a counterfactual estimate of loss with a different readout system.

Configuration: 32 channels, two 16-channel lanes, one link; 62.5-MHz source
clock. 1024/5 uses 232 words and 1,037 busy clocks; 512/5 uses 120 words and
525 busy clocks. The inherited model uses FIFO full/empty thresholds 200/220
words and adds each completed frame to occupancy as a block. Word-by-word
lane drain imposes finite output capacity. This remains an architecture
model, not cycle-accurate RTL.

24 Poisson rates (1–200 kHz/channel), five matched seeds, 500,000 warmup ticks
and 5,000,000 measurement ticks per run. Input seeds are
20260918 + 101*repeat + rate. Error bars are standard errors over five repeats;
no systematic uncertainty is estimated. There are 240 runs. The 0.7-PE
threshold defines the physical reference rate; the sweep itself starts with
candidate timestamps and does not simulate ADC threshold formation.

At exactly 87,000 Hz/channel:

| Format | Dead time | FIFO-blocked uncaptured time | Output frame data |
|---|---:|---:|---:|
| 1024/5 | 55.0919% | 53.0350% | 7.9306 Gbit/s |
| 512/5 | 40.2795% | 36.3478% | 7.8410 Gbit/s |

The mean-load markers solve r/(1+r*t_busy) = C/(32*64*words), with
C = 8*words/(words+2) Gbit/s. They are approximately 23 and 44 kHz/channel.
Bursts cause loss below those markers; mean-load crossing is not a sharp
on/off boundary. These synthetic numbers are distinct from full-VD replay.

## Correction to the former Hermes claim

`frequency_sweep_ideal_sender_superseded.csv` preserves the previous result.
Its overlap does not demonstrate absence of Hermes backpressure. The old
model only reserved finite source FIFO space and drained an ideal 156.25-MHz
sink. It omitted UDP packet accumulation, packet-boundary handshakes, header
preparation, output FIFOs and MAC ready behavior. Do not use that overlay as
hardware evidence. The optional C++ Hermes approximation remains available
for development but is disabled in the presentation sweep.

RTL inspection in daphne-firmware-256-5-production shows:

- `deimos/tx_mux_axi4s_shim.vhd`: mux_ready follows UDP AXI tready.
- `udp_core_lib/tx_udp_handler.vhd`: input ready includes FIFO capacity and
  allow_input; packet completion blocks input until udp_preparing.
- `deimos/tx_mux_out.vhd`: fragment headers, datagram limits and send/pause
  states also control service.
- `deimos/tx_mux_ibuf.vhd`: fixed-packet builds reserve packet words plus four
  pipeline locations and propagate packet_ready upstream.
- The baseline commit 3f17f1b uses the older variable-length input path,
  without packet_ready. Its ST_RUN transitions to ST_DISC on FIFO overflow.
  Downstream loss must therefore be measured separately from assembler dead
  time; it cannot be represented by simply attaching the newer ready signal.

Consequently this sweep measures congestion from the finite shared readout
into Hermes, **not additional loss caused by actual Hermes/UDP stalls**.
That remaining transport contribution requires a version-matched full replay.

Reproduce from this deck: compile analysis/fifo_capture_sim.cpp with C++17,
then run `python3 analysis/run_frequency_sweep.py`. Per-run and summary data
are in analysis/results/frequency_sweep.csv and frequency_sweep_summary.csv.

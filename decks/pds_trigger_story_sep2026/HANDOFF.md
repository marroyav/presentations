# Handoff — 18 September 2026

Current: the entire backup section is commented out in main.tex, preserved
for restoration. The PDF contains only the 10 main slides.

Latest slide order: moved former slides 7, 8, 9, 12 and 15 to the start of the
backup section, preserving their original order. The deck now has 10 main
slides, a backup divider, and 11 backup slides (22 PDF pages total). Main
slide 7 is the frequency/dead-time plot; main slide 8 is the one-link budget.
Speaker notes were reordered. No numerical results or models changed.


15 main slides, backup divider and six backup slides retained. Former slide 8
(dead-time definition) now follows slide 4. Story: baseline/definitions,
activity and physics, tools/results, mitigation. Reference: 87 kHz/channel at
0.7 PE. Slide 11 uses intrinsic cathode offered load, not gamma-pilot demand.

The previous ideal-Hermes plot was challenged and is withdrawn. The new
24-rate, five-seed sweep shows dead time versus activity and the FIFO-blocked
subset for 1024/5 and 512/5, 32 channels and one link. It measures the finite
shared DAPHNE readout into Hermes. It does NOT include actual Hermes/UDP
stalls; do not present it as a completed full sender replay.

At exactly 87 kHz/channel: total dead time 55.0919% / 40.2795%; FIFO-blocked
uncaptured time 53.0350% / 36.3478%; output frame data 7.9306 / 7.8410 Gbit/s.
The ~23/44 kHz mean-load crossings are Poisson estimates. Burst losses start
earlier. All 240 runs are in analysis/results/frequency_sweep.csv; summaries
are in frequency_sweep_summary.csv. The previous CSV is explicitly superseded.

Full-VD slide 9 remains a separate correlated replay: intrinsic dead time
34.60% / 21.54%, 1,344 channels in 42 modeled boards. The 256/5 VD trace remains
unmeasured. Do not relabel these as full Ethernet delivery results.

RTL audit: the UDP handler really deasserts input ready at packet boundaries
until header preparation starts. The 1024 baseline 3f17f1b has no packet-ready
feedback and discards on input FIFO overflow; newer fixed-packet firmware
propagates packet_ready. A complete transport replay must distinguish these
behaviors, packet losses, and assembler capture dead time. See
 evidence/frequency-sweep-model.md for scope and source pointers.

Source, figure and slide documentation updated. The 22-page PDF rebuilt with
no layout warnings; slide 10 was rendered for visual review. All 240 rows
passed range/subset/capacity checks, and make audit passed. No commits or hardware changes.

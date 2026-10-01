# Window-format slide provenance

Added 2026-09-16 from the local xc_sim fixed-frame sensitivity study:
`/home/neutrino/work/daphne/firmware/repos/daphne_mezz_xc_sim/results/sipm-fixed-frames/comparison.csv`.

Selection: pe_per_burst=40, slow_ns=1600, threshold_adc=10,
posttrigger_samples=447, afterpulse_scenario=warm_ratio_extrapolated_5V.
Sample period 16 ns; 64 pretrigger samples; 128 synthetic bursts.
Missing descriptors = missing_descriptor_pieces / descriptor_pieces.
The baseline-subtracted threshold-run model splits excursions at frame
boundaries. These percentages are not an RTL result or a detector prediction.
No statistical uncertainty is assigned to this single illustrative point.
Afterpulse probability is an assumed cross-device warm-ratio extrapolation;
mean delay is fixed at 1 us. This sweep omits dark counts and cross-talk.

Current header: eight 64-bit words. Compact header: two common words plus one
word per fixed descriptor slot. Packed waveform: 14 bits/sample.
Bytes B = 8*(7*N/32 + header_words).
Dense internal readout occupancy = 4*(B/8+2)/N, for four continuously captured
channels sharing one word/cycle lane with two cycles of per-frame overhead.
This is internal lane utilization, not optical-link utilization. More than
100% fails the sustained dense-load capacity condition. Buffer/CDC timing and
the actual 256-sample RTL adaptations have not been validated by this study.

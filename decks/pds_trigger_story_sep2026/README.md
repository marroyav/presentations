# PDS data acquisition and local trigger conditions for VD LE

Subtitle: single photoelectron activity expectations and mitigation strategies.

A 15-slide, roughly eight-minute story about the PDS trigger problem and the
studies behind possible mitigations. One idea per main slide; detailed source
slides follow in a backup section and speaker notes remain in
[speaker_notes.md](speaker_notes.md).

## Audience and outcome

PDS, DAQ, and detector colleagues who do not need to know FPGA internals.
The audience should understand the two losses, why single-photoelectron
signals matter, what has been studied, and which readout/trigger choices
need agreement with DAQ.

## Brief and boundaries

- Start from the user's current 1024-sample self-trigger release, maintained
  across `daphne-os` and `daphne-firmware`.
- Tell the story through descriptor limits, busy time, missing VD activity
  estimates, atmospheric-argon/gamma simulations, and C++/HDL/gateware work.
- Show the implemented 256-sample / five-descriptor candidate, including
  waveform continuation, compact headers and readout without gaps. Present it
  after the link comparison: sustained full-load preservation requires four
  links, each sustaining 7.875 Gbit/s of frame data. Derive sender budgets
  from pinned firmware: 7.932 Gbit/s/link for 1024 samples, 7.869 for 512,
  and an 8 Gbit/s input interface for the gapless 256/5 candidate. These
  are frame-data budgets into Hermes, not measured Ethernet throughput.
- Keep weak-light sensitivity as a physics motivation; increased fiducial
  volume is a question to test, not an established result.
- Finish with one-link admission/trigger choices versus two/four links,
  preserving peak descriptors and selected waveforms. Additional servers and
  CUC power are part of the user's stated infrastructure tradeoff.
- Use the shared Beamer theme and editable TikZ drawings. The full-VD replay
  includes 1,344 channels on 42 modeled boards (32 channels each), FIFO
  admission and lane drain. It counts blocked time outside retained waveform
  coverage, including pretrigger recovery. It is a C++ architecture model, not
  cycle-accurate RTL validation.

## Sources

The two requested decks remain the primary evidence:

- [PDS activity to DAPHNE load](../pds_activity_to_daphne_load_sep2026/README.md)
- [Grouped32 simulation](../grouped32_simulation_sep2026/README.md)

Copied CSVs, release notes, and RTL report are in `evidence/`.
`evidence/manifest.json` records their original paths and SHA-256 hashes.
The companion notes map every slide to its evidence and assumptions.
The link-rate calculation and pinned firmware references are in
[hermes-link-budget.md](evidence/hermes-link-budget.md).

## Backup selection

The appendix gives context for the headline claims, using the two requested
source decks and pinned firmware as evidence:

- frame composition and packet size for 1024, 512 and 256/5;
- activity inputs, gamma-pilot scope and the exact channel dead-time replay;
- buffer/continuation behavior and the four-link mapping and sender boundary.
  It marks 256/5 VD loss as unmeasured.

The packet summary gives DAPHNE frame content before network overhead:
232 words / 1,856 bytes for 1024; 120 words / 960 bytes for 512; and
63 words / 504 bytes for the 256-sample, five-descriptor candidate.

These slides provide assumptions, boundaries and exclusions rather than
repeating the main story as standalone conclusions. The source decks remain
the full evidence reference.

The working baseline is the self-trigger artifact `3f17f1b` recorded in the
dual-gateware RC1 manifest. This is the baseline for this talk, not a claim
that every board is running the same image or that the RC is production qualified.
The one-link agreement and absence of an agreed VD forecast are supplied by
the presenter; these studies do not establish collaboration-wide policy.

## Build and review

From the repository root:

```sh
make decks/pds_trigger_story_sep2026/main.pdf
make audit
make check
python3 -m unittest discover -s decks/pds_trigger_story_sep2026/analysis -p 'test_*.py'
```

Slide 5 defines dead time, immediately after the FIFO-congestion explanation. Slide 9 gives the full-VD intrinsic one-link replay:
34.60% dead time for 1024/5 and 21.54% for 512/5; gamma-pilot values are
42.80% and 27.79%. Missing threshold candidates and rejected trigger requests
are shown separately. The denominator is summed observation time across all
1,344 channels. See [capture-loss-VD-one-link.csv](evidence/capture-loss-VD-one-link.csv)
and [the model/metric notes](evidence/capture-loss-model.md).

Slide 10 shows dead time against input activity, including the FIFO-blocked
subset under finite shared readout. The new sweep uses 24 rates, five seeds,
32 channels and one link; the reference is exactly 87 kHz/channel at 0.7 PE.
The former ideal-Hermes overlay is withdrawn. Additional Hermes/UDP transport
stalls are not modeled. See [the corrected scope](evidence/frequency-sweep-model.md).
Reproduce with:

```sh
g++ -O3 -std=c++17 analysis/fifo_capture_sim.cpp -o analysis/fifo_capture_sim
python3 analysis/run_frequency_sweep.py
```

The pinned 256/5 production mapping has four links. Its existing RTL replay
bench does not accept the saved VD activity waveforms; the 256/5 row is
therefore identified as unmeasured rather than inferred from the legacy C++
model. Backup slides explain this boundary and retain packet-size context.

Starting repository commit: `08638349442952755a98cd96d0cc8e78f9fe87d0`.
Existing changes and both untracked input decks are preserved. The Makefile
discovers this new directory automatically.

The story order is baseline and definitions → activity and physics motivation →
tools and results → mitigation choices. All six backup slides remain included.
Slide 5 is the former slide 8. Slide 11 uses intrinsic cathode replay demand
before shared FIFO losses, 16.0 / 11.4 Gbit/s.

Latest order: 10 main slides, backup divider, 11 backup slides. Former slides 7, 8, 9, 12 and 15 now open the backup section in that order. Historical slide numbers above describe earlier revisions; the frequency plot is now main slide 7.

Current PDF: 10 main slides only. The backup divider and all backup slides are commented out in main.tex; their source is preserved.

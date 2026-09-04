# PDS channel activity and self-trigger dead time

Deck slug: `pds_selftrigger_deadtime_aug2026`

## Audience

- Primary audience: PDS experts, DAPHNE firmware developers, and DAQ trigger collaborators.
- What they already know: DAPHNE provides self-triggered optical waveforms and descriptors; low-energy and non-beam decisions are assembled above one channel and one board.
- What they need from this talk: a common picture of what the emulator represents, what the dead-time studies establish, and which questions remain open.

## Outcome

- One-sentence takeaway: matched LArSoft production gives 3.6--4.3 times more pre-firmware activity per VD cathode channel than per HD channel, and an XC fixed-record replay on the actual timestamps shows that 512 samples improves live acceptance in both technologies.
- Decision or action requested: none; this is a status and evidence-boundary report.
- Possible follow-up: replay continuous ADC streams through XC/CFD and add serializer, FIFO, transport, noise, and waveform-containment metrics; standalone, LArSoft-based, and hybrid implementations remain open.

## Scope

- In scope: PDS signature classes; DAPHNE XC self-trigger behavior; waveform and architecture emulation; dead-time mechanisms; 1024-to-512 mitigation; realistic SPE-template injection; validation gaps.
- Explicitly out of scope: choosing a LArSoft integration path, choosing the final detector trigger algorithm, or claiming universal efficiencies from the current single-waveform study.

## Evidence

- Authoritative sources: local `daphne_mezz_xc_sim` documentation and outputs; DAPHNE firmware RTL; DUNE Waffles ProtoDUNE-VD SPE templates; DUNE low-energy and PDS literature cited in the deck.
- Measurements or test results: 48 statistically independent LArSoft activity summaries; per-event/per-channel candidate-timestamp replay through the XC fixed-record busy gate; dense stochastic C++ architecture sweep; sparse/full-chain RTL studies; measured common C-channel template.
- Important uncertainty: the coupled replay begins after threshold-candidate formation and therefore does not test continuous ADC filtering, CFD, waveform containment, shared transport, electronics noise, or external gammas.

## Build

From the repository root:

```sh
python3 decks/pds_selftrigger_deadtime_aug2026/plot_spe_templates.py \
  --analysis-root /path/to/dune-le-pds
python3 decks/pds_selftrigger_deadtime_aug2026/plot_deadtime_summary.py \
  --sim-root /path/to/daphne_mezz_xc_sim
python3 decks/pds_selftrigger_deadtime_aug2026/plot_larsoft_results.py \
  --analysis-root /path/to/dune-le-pds
make
make audit
```

The committed figures are derived visualizations. Their source data remain in the provenance-checked `dune-le-pds` materials and `daphne_mezz_xc_sim` outputs.

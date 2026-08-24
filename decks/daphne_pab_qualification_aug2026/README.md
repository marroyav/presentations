# Qualifying ten DAPHNE boards at PAB

Deck slug: `daphne_pab_qualification_aug2026`

This brief is the deck's editorial contract.

## Audience

- Primary audience: DAPHNE/PDS firmware and hardware engineers, DUNE DAQ and
  timing engineers, and the people responsible for the PAB/Iceberg test area.
- What they already know: DAPHNE can be configured and read through its board
  services; Iceberg has timing-master and DUNE DAQ infrastructure; a self-trigger
  firmware path exists or is being prepared.
- What they need from this talk: The exact scope of a sequential ten-board
  campaign, what the stand must measure, and what DAQ 5.x must provide before
  the boards move.

## Outcome

- One-sentence takeaway: Use one frozen fixture to qualify ten boards one at a
  time, first in four-link full-stream mode and then with pinned self-trigger
  firmware.
- Decision or action requested: Approve the two-phase campaign and assign the
  PAB, timing, DAQ release, firmware, logistics, and sign-off owners.
- Owner and completion condition: Gate 0 is complete when a known board runs
  the entire baseline and self-trigger sequence from a clean DAQ 5.x workarea,
  recovers, decodes, and produces a reviewable evidence package without
  developer intervention.

## Scope

- In scope: One active DAPHNE at a time; four simultaneous data links; full
  configuration and readback; standalone and Iceberg-connected timing; input
  power and temperature by operating state; baseline full-stream data;
  controlled firmware update and rollback; self-trigger data with timing-command
  boundaries; and one evidence package per run and board.
- Explicitly out of scope: Ten boards running simultaneously, an aggregate
  forty-link DAQ test, final production acceptance limits not yet approved by
  their owners, and a claim that standalone/local timing proves endpoint
  synchronization.

## Evidence

- Authoritative sources: Local `daphnemodules` controller implementation,
  `daphneZMQ` endpoint safety contract and timing register map, DAPHNE firmware
  power-control notes referencing EDMS 2383681, DUNE DAQ package metadata, and
  existing DAPHNE QA/QC timing, Hermes/IPbus, waveform, and RMS routines.
- Measurements or test results: The deck proposes the measurements; it does not
  present a completed hardware campaign. Power values shown in the deck are
  planning references only.
- Important uncertainty: The DAQ team must nominate the exact fddaq-v5.x tag;
  timing/DAQ owners must approve the command sequence; firmware, power, and
  hardware owners must approve artifacts, stimulus points, run durations, and
  pass/stop limits.

## Build

From the repository root:

```sh
make decks/daphne_pab_qualification_aug2026/main.pdf
```

The output is:

```text
decks/daphne_pab_qualification_aug2026/main.pdf
```

The system topology is maintained in
`diagrams/stand-topology.dot.in`; the normal make target renders it with the
shared design tokens before building the deck.

## Reference index

- DAPHNE power-control design reference: EDMS 2383681.
- Local DAQ candidate observed while preparing the deck: fddaq-v5.6.2. This is
  a candidate, not the campaign release decision.
- Connected-timing status fields used in the appendix: clock control at
  `0x84000000`, lock status at `0x84000004`, endpoint address/reset at
  `0x84000008`, and endpoint FSM/timestamp status at `0x8400000C`.
- Hermes control-service smoke: IPbus 2.0/UDP read of register zero returns the
  expected `0xDEADBEEF` magic value. This checks service response, not the DAQ
  data path.

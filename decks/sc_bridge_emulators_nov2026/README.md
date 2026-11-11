# What I added in PR #8

A title slide, six short steps and a threads/asyncio comparison explaining
Manuel's emulator PR.
Prepared for the discussion with Geoff. Updated on 10 November 2026 after the
Ignition integration test.

## Audience and outcome

Help Manuel explain what he actually implemented: the device programs, their
message handling and state, how they run, how they were checked, and how Geoff
can use them while writing the next bridge.

[Speaker notes](speaker-notes.txt) provide a plain spoken script for each step,
with implementation details and limits kept off the slides.

## The six steps

1. Add standalone WIB, DAPHNE and Raritan PDU emulators.
2. Use the existing protobuf definitions and a Raritan PDU2-MIB subset.
3. Make commands change state that a later request can read.
4. Add a command-line entry point and asyncio network services.
5. Check messages, readback and recovery locally.
6. Use the emulators as the device side of the next bridge test.

The comparison slide follows the title, before the six steps. It explains
scheduling, waiting, library calls and the main concern for each approach,
with a blocking WIB read as the example.

The deck describes PR #8. The earlier PR #4 is background only. The generic
asyncio package comparison is no longer the main presentation.

## Source and evidence

- [PR #8](https://github.com/DUNE/dune-dscs/pull/8), tested revision
  3a9e54e052fd441ba08e3c02a6f19076f4acdf1d.
- [Package source](https://github.com/DUNE/dune-dscs/tree/3a9e54e052fd441ba08e3c02a6f19076f4acdf1d/src/dune_dscs/emulator):
  the entry point, three handlers and protocol provenance.
- [Emulator instructions](https://github.com/DUNE/dune-dscs/blob/3a9e54e052fd441ba08e3c02a6f19076f4acdf1d/docs/emulator.md).
- [Local fleet summary](evidence/fleet-summary.json): 963 simultaneous processes,
  zero unexpected failures. The 336 extra SNMP PDU instances were load
  placeholders and did not test uTCA/IPMI interfaces.
- [Ignition integration summary](evidence/ignition-summary.json): 627 native
  device processes, 2,508 Good tags, configuration readback, device loss and
  recovery on dune-fd-test01. All eight acceptance checks passed.

The local validation harness is separate from the PR's lint-only CI.
The PR adds no fleet manager or OPC UA bridge. The Ignition test used a temporary
asyncio adapter outside the repository. It polled the native device protocols
and published read-only OPC UA values; Ignition read those values through its
own OPC tags. Configuration writes used the native clients. The test connection,
project and tag folder were removed afterwards.

The integration fleet was 480 WIBs, 42 DAPHNEs and 105 rack PDUs. The 320 TDE and
16 DTS crate-management endpoints need IPMI emulators and were excluded.
Hardware remains untested. A successful emulator test is not hardware
qualification or proof of production capacity.

## Design and build

Uses the [new framework guide](../../docs/framework-guide.md): white slides,
large text, one point per slide and no decorative boxes.

Build only this deck from the repository root:

    cd decks/sc_bridge_emulators_nov2026
    tectonic --chatter minimal --keep-logs --keep-intermediates main.tex

# Implementation evidence

The live base was **fddaq-v5.6.2-a9-1**, not v5.7.1. Package revisions in
`source-pins.json` come from the [pinned Run 45392 provenance](https://github.com/DUNE/PDS/blob/bed0920192126456089d7d44930dbfb145268463/deployments/cern-daphne14/20261020/evidence/source-provenance.json).

Local reviewed sources: `/home/arroyave/work/pds-trigger-scaffold/`.

| Package | Changed implementation |
| --- | --- |
| fddetdataformats | `75451f4`: `DAPHNEEthFrame.hpp`, Python bindings and format tests. Compact 512-byte DAQ frame, 256 packed 14-bit samples, five descriptors. |
| fdreadoutlibs | `76ebfd6`, `14a0a23`, `dc0481f`, `9c20f87`: compact adapter, `pds/DescriptorToTP.hpp`, `DAPHNEEthFrameProcessor.cpp`, `pds/DescriptorProcessor.hpp` and descriptor processor implementation. Latest pinned package: `1bf5945`. |
| dpdklibs | `5195f13`, `f049d6f`: bounded frame workers and descriptor fork before raw buffering. Latest pinned package: `0711ede`. |
| appmodel | `b59caa1`, `3a2c813`: processing/descriptor CPUs and queue capacities in `fdmodules.schema.xml`; separate-descriptor switch in `trigger.schema.xml`. |
| triggeralgs compatibility | v1.6.0 `TAMakerPrescaleAlgorithm::process` interposed for this session. Detector 8 uses PDS TA type, one-tick sample scaling, and TP start as activity time. Non-PDS behavior retained. No installed system library was replaced. Source/tests are preserved in the pinned deployment's `prescale-compat.tar.gz`. |

Reviewed design and test records:

- `fdreadoutlibs/docs/pds-descriptor-trigger-scaffold.md`: descriptor validation,
  channel map, time contract, overflow policy and TP hook.
- `dpdklibs/docs/descriptor-workers.md`: 64-byte metadata fork, independent
  queues and counters, per-channel ordering, drain behavior and bounded tests.
- `fdreadoutlibs/docs/pds-throughput-check.md`: earlier live TP tests and sorted
  offline TA replay. These measurements do not qualify end-to-end storage losslessness.
- [Run 45392 report](https://github.com/DUNE/PDS/blob/bed0920192126456089d7d44930dbfb145268463/deployments/cern-daphne14/20261020/REPORT.rst):
  all 29 records decoded; complete, flag-free PDS/charge fragments. First TC
  metadata fragment status 18, decodable candidate; cause unresolved.

The receive path preserves per-channel order, not global TP timestamp order.
It does not remove waveform traffic on the wire. Descriptor overflow rejection
and independent queue/NIC drops remain explicit limitations. Other packages in
the live workarea are not claimed here as descriptor-TP implementation changes.

## Proposed format compatibility

Expand the packet version field and use version-based dispatch for 1024- and
256-sample packets. Preserve legacy 1024 decoding and the full-stream format/decoder.
This is a requested extension, not a capability qualified by Run 45392.
The current pinned compact frame has a four-bit version field and a fixed
256-sample layout. No new field width, version IDs or bit allocation is assigned
by the slide; firmware and DAQ must agree the encoding while preserving legacy
header interpretation. Full-stream remains a separate supported format.

## Why separate readout processing

The shared receive callback coupled descriptor extraction to raw waveform
buffering. The frame-worker profile identified SkipList insertion as a material
cost; raw queue saturation remained under load. The descriptor fork copies
64-byte metadata before raw buffering so raw backlog/drops do not force the
corresponding descriptor work to be discarded. It does not remove NIC loss.

`dpdklibs/docs/descriptor-workers.md` records two-worker profiles with all
73,733,216 offered descriptor frames processed and zero descriptor drops.
Steady noisy 120-kHz samples showed 4.37% raw queue loss and zero descriptor
queue loss. Those are short, 16-channel tests, not full-detector throughput
or end-to-end TP storage qualification. The slide states this bounded result
to explain the readout change rather than presenting the fork as cosmetic.

## Story slide measurements

The three rows are sampled 120-kHz target, threshold-8 noise-descriptor phases
with 16 connected channels. The first two are from
`dpdklibs/docs/frame-workers.md` (NIC loss 51.91% versus 0%; two-worker queue
loss 5.55%). The third is from `dpdklibs/docs/descriptor-workers.md`
(two descriptor workers, NIC loss 0%, raw queue loss 4.37%, descriptor queue
loss 0%). These were separate ten-second phases/runs with variable descriptor
populations, not a controlled same-input speedup comparison. NIC loss counts
packets; worker queue loss counts offered frames. The slide does not compare
these percentages as equivalent event counts or claim losslessness.

`dpdklibs` changes: `5195f13` added `src/FrameWorker.hpp` and offloaded callbacks
in `src/IfaceWrapper.cpp`; `f049d6f` added descriptor dispatch in that file and
`src/SourceModel.hpp` before raw processing. `fdreadoutlibs` commit `9c20f87`
separated the TP processor from `DAPHNEEthFrameProcessor.cpp`. `appmodel`
exposes CPU/queue configuration. This is host receive/processing software,
not a NIC firmware modification. Raw-buffer pressure remains; descriptor
progress is isolated from it subject to NIC and descriptor-queue capacity.

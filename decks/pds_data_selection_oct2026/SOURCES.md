# TA capability and scintillation evidence

Reviewed implementation: `/home/arroyave/work/pds-trigger-scaffold/fdreadoutlibs/`,
commit `1bf594581feca8c23f3b11184ce63c709f4a9c6f`.

- `include/fdreadoutlibs/pds/ActivityBuilder.hpp` implements streaming
  coincidence and descriptor-light builders. The reference coincidence policy
  emits when six distinct offline channels occur in an inclusive 10-us window,
  then consumes contributing inputs. These are illustrative settings, not
  physics-optimized requirements. Repeated peaks on one channel count once
  toward multiplicity. The native algorithm identifier remains `kUnknown`.
- `docs/benchmarks/daphne/ta-replay.json`: 3,854,763 captured TPs produced
  93,126 TAs in sorted offline replay. These noise-descriptor data establish
  software capability, not scintillation selection efficiency.
- `docs/pds-descriptor-trigger-scaffold.md`: prompt-light builder sums whole
  descriptor integrals by start-time gate membership. This is an ADC-integral
  proxy, not calibrated PE or exact waveform charge. Below-threshold and lost
  light is absent; a boundary-crossing descriptor cannot be split from its
  integral alone. Continuation fragments are not stitched into physical pulses.
- [Run 45392](https://github.com/DUNE/PDS/blob/bed0920192126456089d7d44930dbfb145268463/deployments/cern-daphne14/20261020/REPORT.rst)
  establishes live prescaled PDS TA → TC → MLT → PDS/emulated-charge readout,
  not a live coincidence/prompt-light selection. The first TC metadata fragment
  has status 18; PDS/charge payloads are complete and flag-free in all 29 records.
- The test's `triggeralgs` v1.6.0 interposer corrects PDS type and sample units
  for detector 8 only; it is not a new general-purpose physics TA plugin.

Physics reference: DUNE Collaboration, [Scintillation light detection in the
6-m drift-length ProtoDUNE Dual Phase liquid argon TPC](https://arxiv.org/abs/2203.16134),
also [published open text](https://pmc.ncbi.nlm.nih.gov/articles/PMC9288420/).
Primary scintillation has fast and slow components. The diagram is a conceptual
prompt-plus-tail envelope, with no fitted amplitudes, time scale or detector
response. It does not depict gas electroluminescence or claim a measured signature
in Run 45392. Doping, optics, sensors and electronics affect the observed shape.

Coincidence, summed light and prompt fraction are candidate observables suggested
by the developed builders; their physics performance remains unqualified.
An ordered cross-link merger/common watermark, plugin/configuration/algorithm ID,
seed/overlap policy, waveform comparison and rate/latency qualification remain
integration work. Single-link arrival order is insufficient for cross-link TAs.

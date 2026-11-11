# Slow-controls simulation: updated VD and HD results

A concise, 8-slide presentation for SC/DAQ colleagues and first-time operators.
The original 24 slides have been synthesized around the fresh 6 October local
runs. Historical mixed-fleet results are context only.

## Results and scope

- VD: 480 WIBs + 42 DAPHNEs. HD: 750 WIBs + 150 DAPHNEs.
- Two OPC-UA processes per detector reached at least 95% of the best observed
  throughput in all three full-fleet read phases; all 12 topology checks passed with no
  read errors. Processes ran on one workstation, with populations tested separately.
- WIB-only queue projections: four VD bridges give 48.42 s p95; six HD bridges
  give 62.28 s p95, with 48 workers per bridge. These are configuration model
  candidates, distinct from the measured monitoring process count.
- Full namespaces, PTCs, other systems, Ignition/historian load, native-device
  timings and host failover remain outside the measured board-only scope.

## Contents

1. New monitoring result and corrected populations.
2. What a process means, test workload, throughput/memory curves and isolation.
3. Configuration jobs, queue allocations and updated modeled completion times.
4. Physical-host test proposal and remaining measurements.
5. Portable setup, monitoring commands and optional queue projection.

## Open these files

- [Presentation](main.pdf)
- [Sources and interpretation](SOURCES.md)
- [Beginner runbook in sc_emu](../../../sc_emu/RUNBOOK.md)
- [Complete local results in sc_emu](../../../sc_emu/LOCAL_RESULTS.md)
- [Simulation validation](../../../sc_emu/VALIDATION.md)

Simulation source, scripts, inventories, raw reports and runtime directories
remain in `sc_emu`. This deck contains only presentation assets, illustrative
command snippets and the figure's CSV/provenance.

## Build

From the presentations repository root:

```sh
make decks/sc_simulation_results_oct2026/main.pdf
```

To regenerate the vector chart, run `python tools/plot_results.py` from this
deck directory in an environment with Matplotlib. The figure uses the shared
DUNEProfessional design tokens and the copied, hash-recorded local curve data.

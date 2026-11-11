# DAPHNE-14 readout tests and merge plan

[Three-page report](main.pdf), covering the 23 October 2026, 32-channel campaign:
5.6/5.7 rate sweeps, timing and worker experiments, validation, and branch recommendations.

Build from the presentations repository:

```sh
make pds-readout-report
```

`build_report.py` generates the tables from `evidence/measurements.json`.
`evidence/` also contains full source pins, checked upstream heads, rate/worker CSVs,
and hashes of the original result files. Values in the PDF are rounded; CSVs retain precision.

The three published minimal functional patches are the review base. Format compatibility
needs further work. Raw-worker and timing branches remain separate experiments.

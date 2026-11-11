# Sources and interpretation

## L1 — Fresh local monitoring measurements, 6 October 2026

[Complete VD/HD results](../../../sc_emu/LOCAL_RESULTS.md), including:

- [VD JSON report](../../../sc_emu/evidence/updated-local-20261006/vd-report.json)
  and [provenance](../../../sc_emu/evidence/updated-local-20261006/vd-provenance.json).
- [HD JSON report](../../../sc_emu/evidence/updated-local-20261006/hd-report.json)
  and [provenance](../../../sc_emu/evidence/updated-local-20261006/hd-provenance.json).

The profiles contain 480 WIBs + 42 DAPHNEs for VD, and 750 WIBs + 150 DAPHNEs
for HD. Tests ran sequentially on the same i9-13950HX workstation, using Linux /
Python 3.13.5, ordinary desktop load, five minimum repetitions and two-second
minimum read phases. Counts tested: 1, 2, 3, 4, 6 and 8 processes per population.
All 12 topology checks passed with zero observed read errors.

The smallest count reaching 95% of the best observed rate in each of the three
full-fleet read phases is
**two for both profiles**. At two processes, stressed VD/HD rates are
131,838 / 129,467 Read values/s and server RSS is 296.4 / 353.7 MB.
The plotted percentages use each detector's own best stressed rate through
8 processes; they are not a comparison of equivalent VD and HD inventories.

[Figure CSV](evidence/updated-process-curves.csv) is copied directly from the
simulation repository's `process-curves.csv`. Its SHA-256 and origin are recorded
in [figure provenance](evidence/figure-provenance.json). Raw reports remain in
`sc_emu`; the presentation repository stores only figure data.

The simplified namespace has 17 variables/WIB and 21/DAPHNE. During churn,
one representative value per board changes every 250 ms. A single client reads
in batches up to 500 values. This is completed OPC-UA Read throughput, not a
validated subscription or historian rate. RSS sums server processes only.

The two-process result describes monitoring throughput. The VD interference
sample improves from +13.1% at two processes to +1.3% at four; the HD sample is
+0.3% at two and +10.8% at six. Extra processes therefore have an isolation tradeoff,
not a demonstrated universal benefit. These short samples do not establish a
precise production optimum or a physical-server minimum.

## Q1 — Fresh WIB configuration queue projections

[Queue report](../../../sc_emu/evidence/updated-local-20261006/wib-queues-report.md)
and [complete inputs/seeds](../../../sc_emu/evidence/updated-local-20261006/wib-queues-report.json).

One job configures one WIB and reads its settings back. Each bridge candidate
has 48 simultaneous worker slots. Four VD bridges own 120 WIBs each; six HD
bridges own 125 each. They require three batches per bridge. A four-bridge HD
comparison owns 187–188 each and requires four batches.

Each candidate has 10,000 Monte Carlo fleet trials. Apply wait is 16.10 s/WIB,
RTT p50/p95 is 0.3/1.0 ms, bandwidth 1 Gbit/s, timeout 30 s and one retry.
The error posterior is Beta(0.5, 3000.5), from the saved synthetic WIB
configuration test. These are reused inputs, not fresh hardware measurements.
HD uses the same generic WIB model and VD apply-time assumption.

- VD / 4 bridges: p95 48.42 s; p99 78.41 s.
- HD / 6 bridges: p95 62.28 s; p99 78.41 s.
- HD / 4 bridges: p95 78.41 s; p99 94.55 s.

Adding OPC-UA processes does not implement the assumed parallel configuration
queue. Hardware apply/readback and that parallel bridge path need validation.

## I1 — Device inventory

DUNE-doc 34374-v1, `DUNE_ICD_SC_TPCE-BDE_v1P4.docx`: 80 VD WIECs × 6 WIBs
and 150 HD WIECs × 5 WIBs, with one PTC per WIEC. The planned PTC population
is 80 VD + 150 HD; PTCs are not emulated in these runs.

The PDS–SC ICD, EDMS 3309688 (14 October 2025), specifies 150 HD DAPHNEs.
Manuel's 6 October correction establishes 42 VD DAPHNEs for these profiles.
The old 40-board VD count is retained only in historical evidence.

Local document copies are in `document-library`, `racks` and `vd-dps-plan`.
These are planning/document evidence, not an as-built detector inventory.

## H1 — Historical context only

[Archived benchmark report](../../../sc_emu/evidence/archived-results.md)
and [original report source](../../../sc_emu/evidence/archived-report.tex).

The July four-process result used 1,818 objects and 40,734 read variables,
including power, sensors and other support objects. The new VD/HD runs use
smaller board-only profiles. The old four-process conclusion is therefore
not substituted for the new two-process throughput result. Detailed historical
inventory, native-protocol results and original reproduction commands remain
in `sc_emu` rather than taking separate slides in this concise presentation.

The simulator baseline came from the 25 September LArSoft backup. Its paths and
file hashes are recorded in [the source manifest](../../../sc_emu/evidence/source-manifest.json).

## R1 — Human reproduction and host-count interpretation

[sc_emu beginner runbook](../../../sc_emu/RUNBOOK.md),
[repository README](../../../sc_emu/README.md) and
[validation record](../../../sc_emu/VALIDATION.md).

All slide commands run from the user's `sc_emu` checkout, using `.venv/bin/python`.
Source, scripts, pinned dependencies, inventories, provenance and raw reports
belong to that repository. The deck contains illustrative command snippets only.
The `original` mixed-fleet and optional native configure/readback procedures are
in the runbook. Timings can differ on another workstation.

One local host successfully ran each population separately. One bridge host
per detector is a proposed next capacity test; dedicated failover partners
would make four bridge hosts total. This does not establish a production minimum
or combined VD/HD capacity on one host. Ignition, database and instrument PCs
require separate sizing. Full namespaces, PTCs, other interfaces, native latency,
consumer load and host failover must be included before procurement decisions.

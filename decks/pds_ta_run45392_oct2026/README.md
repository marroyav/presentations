# Run 45392: PDS-TA-triggered readout

One slide. Audience: DAQ. Outcome: show that PDS TAs drove matching PDS and
emulated-charge readout windows.

Source: [pinned deployment report and decoded evidence](https://github.com/DUNE/PDS/tree/bed0920192126456089d7d44930dbfb145268463/deployments/cern-daphne14/20261020).
The bounded test used software captures on DAPHNE-14. It does not qualify
detector-light response, SSP synchronization, or sustained throughput.
All 29 PDS/charge payload sets were clean; the first record's TC metadata
fragment had status 18, with a decodable candidate. Its cause is unresolved.

Build: `make decks/pds_ta_run45392_oct2026/main.pdf` from the repository root.

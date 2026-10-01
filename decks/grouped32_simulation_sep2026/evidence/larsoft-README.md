# PDS activity to DAPHNE load

Deck slug: `pds_activity_to_daphne_load_sep2026`

## Purpose

A short status deck separating three quantities:

1. LArSoft candidate activity per optical channel;
2. accepted activity from the present channel-local fixed-record busy gate; and
3. illustrative offered traffic for a homogeneous DAPHNE board.

It does not claim a board-level acceptance or dead-time result. The LArSoft
channel map used for this campaign does not yet identify DAPHNE boards or
internal transport lanes.

The September 9 revision also reports two completed gamma studies. The matched
stratified pilot contains 10,000 incident trials per technology and measures
conditional response versus energy and entry face. The direct physical pilot
uses the released cavern-wall, foam, cryostat-neutron-gamma, and
cavern-neutron-gamma generators in the full detector geometries. One physical
window per source family is complete for each technology.

## Headline conditions

- simulation release: `dunesw v10_22_00d01` (`larsoft v10_22_00`,
  `art 3.14.04`), common to the intrinsic-LAr, physical-gamma, and
  stratified-gamma campaigns for HD and VD;
- nominal intrinsic-LAr mixture: atmospheric `39Ar` at `0.964 Bq/kg`, plus the
  released `85Kr`, `42Ar`, and `42K` components;
- local optical candidate threshold: `> 0.7 PE`;
- no `10 MeV` trigger cut (energy is retained only for classification/audit);
- eight independent nominal shards for each detector configuration;
- Waffles NP02 `templates_large_pulses_zero_subtract`, cathode C channels only;
- the same 16-waveform SPE-shape set is used for FD-HD and FD-VD;
- complete hardware-channel denominators, with VD cathode, long-wall, and
  short-wall populations reported separately;
- HD is the reference technology;
- `39Ar` accounts for 89.4% of generated primaries in the eight-shard nominal
  sample, but its candidate stream was not separated from the other intrinsic
  components;
- the gamma-inclusive extension is explicitly a one-window-per-family pilot.

## Background inventory and status

- represented in separate bulk-LAr samples: `85Kr`, `42Ar`, and `42K`;
- represented in separate detector-material and internal-combined samples:
  `40K`, `238U`/`232Th` chains in cathode and anode material, and the `222Rn`
  chain in PDS material;
- completed as an explicitly incomplete supported-radon subset: `222Rn`,
  `218Po`, `214Pb`, and `210Pb` component samples;
- completed as a first-window physical gamma pilot: cavern-wall and foam
  gammas, plus cryostat-neutron-gamma and cavern-neutron-gamma generators;
- not closed for a total-background claim: independent gamma repetition,
  actual cavern neutrons, alpha-capture gammas, the remaining radon-chain rows,
  and a validated physical electronics-noise rate.

The baseline and gamma-inclusive pilot are labeled separately. The latter
overlays already-formed candidate timestamps before the XC fixed-busy gate, so
it retains cross-source candidate-level pileup. It does not reconstruct analog
waveform pileup. A total board result still requires shared firmware resources.

## Firmware and transport assumptions

- fixed-record channel-local busy gate: a candidate arriving while its channel
  is busy is rejected;
- 512-sample records use 120 64-bit words (7,680 bits);
- 1024-sample records use 232 64-bit words (14,848 bits);
- HD board examples use 40 channels; VD examples use 32 channels;
- board traffic examples assume every board channel belongs to the named
  detector population and has the population mean rate;
- no shared FIFO, serializer, output link, back-pressure, channel-to-board map,
  or lane contention is included in the current accepted-rate replay;
- the Hermes input estimate uses the rate accepted by that channel-local replay;
  the raw candidate-rate product is retained separately as the pre-gate demand;
- the transport illustration treats one Hermes sender as one 10-Gbit/s physical
  link; 10 Gbit/s is line rate, so its usable payload capacity is lower after
  Ethernet/UDP/Hermes overhead;
- the displayed homogeneous-board load is compared with one sender. If a real
  board partitions channels across several senders/links, the calculation must
  be repeated with the actual channel-to-sender assignment;
- a 50% overlap does not reduce transmitted record size unless firmware
  coalesces or compresses the overlapping samples.

The sender and channel gate are coupled in real firmware. Once the sender
asserts back-pressure, the accepted rate from the channel-only replay is no
longer fixed; the final loss and dead-time fraction require a joint, ordered
replay through both stages.

## Numerical snapshot

The nominal values shown in the deck are frozen in `results.csv`; the physical
gamma and combined-replay pilot are frozen in `gamma_pilot_results.csv`. The
nominal numbers come from eight independent intrinsic-LAr shards. The physical
gamma extension reuses one gamma trace per source family with each nominal
shard, after clipping to the common digitizer window. Exact same-channel,
same-tick coincidences are deduplicated before replaying the XC fixed busy gate.

The conditional gamma pilot contains 2,358 triggered HD trials and 1,782
triggered VD trials out of 10,000 per detector. Its energy-bin and face totals
are frozen in the simulation repository as
`data/stratified-gamma-response-pilot-20260909.{csv,json}`. The combined physical
pilot and its full input checksums are frozen under
`output/materials/intrinsic-external-gamma-candidate-trace-deadtime-pilot-v1`.

The record sizes and packing equation follow
`daphne_mezz_xc_sim/src/ring_deadtime_sim.cpp`: eight fixed 64-bit words plus
seven 64-bit words per block of 32 ADC samples. The 120-word/232-word comparison
and the slide structure were cross-checked against the older local decks
`daphne_deadtime_apr2026` and `daq_daphne_pds_integration_may2026` under
`daphne_presentations`.

## Build

From the repository root:

```sh
make decks/pds_activity_to_daphne_load_sep2026/main.pdf
python3 scripts/audit_design.py
python3 scripts/audit_decks.py decks
```

The deck uses the locally installed JetBrains Mono family through fontconfig.

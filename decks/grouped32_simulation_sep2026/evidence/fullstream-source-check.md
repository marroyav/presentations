# Full-stream channel count and record demand

Checked 2026-09-15 against `marroyav/daphne-fullstream-firmware`:

- Release `fullstream-2026.08.24`: `7afa1585b0dadde8001d31e1d60cdc8e74c738a2`.
- Remote default `marroyav/fullstream-naming-cleanup`: `794aff6bc92c15ff29f8b920abd5a30ffa50a715`.
- Newer build-tools RC branch: `bff0ee134b12e9e98dc72d99e3917454b02ea38d`.

Remote refs were checked with `git ls-remote`; default and build-tools commits
were fetched and compared. The sender count and Hermes mapping agree across
these revisions. The newer RC changes stream activation/reset behavior.

## Active source chain

1. [`stream_core.vhd`](https://github.com/marroyav/daphne-fullstream-firmware/blob/bff0ee134b12e9e98dc72d99e3917454b02ea38d/ip_repo/daphne3_ip/rtl/stream/stream_core.vhd#L47)
   generates senders 0 through 7, each a `stream4` instance with four inputs.
2. [`daphne3.vhd`](https://github.com/marroyav/daphne-fullstream-firmware/blob/bff0ee134b12e9e98dc72d99e3917454b02ea38d/ip_repo/daphne3_ip/rtl/daphne3.vhd)
   instantiates that core and passes all eight `data/valid/last` streams into
   `daphne_streaming_top`. It does not override the 35-block record default.
3. [`daphne_streaming_top.vhd`](https://github.com/marroyav/daphne-fullstream-firmware/blob/bff0ee134b12e9e98dc72d99e3917454b02ea38d/ip_repo/daphne3_ip/src/dune.daq_user_hermes_daphne_1.1/src/deimos/daphne_streaming_top.vhd#L154)
   instantiates `eth_readout` with `N_SRC => 2`, `N_MGT => 4`.
   Inputs d0/d1 map to link 0, d2/d3 to link 1, d4/d5 to link 2, d6/d7 to link 3.
4. [`stream4.vhd`](https://github.com/marroyav/daphne-fullstream-firmware/blob/bff0ee134b12e9e98dc72d99e3917454b02ea38d/ip_repo/daphne3_ip/rtl/stream/stream4.vhd)
   packs 4 channels × 8 samples/channel into each seven-word payload block.
   A record contains 35 blocks and five 64-bit header words, or 280 samples
   per channel and 250 words total. The FSM emits header words 0 through 4.

Therefore, the source supports **8 × 4 = 32 selected channels**, with
**2 × 4 = 8 per physical link**. Four channels describes a logical sender,
not a physical Ethernet link. Selectors can repeat channels or disable senders,
so actual enabled coverage depends on configuration.

Record demand per board is
`8 senders * 250 words * 64 bits * 62.5 MHz / 280 = 28.57142857 Gbit/s`,
before Ethernet/UDP/transport overhead. Raw ADC sample payload is 28 Gbit/s.
No physical full-stream throughput or installed-image qualification was run.

`stream8.vhd` and `stream_top_wrapper.vhd` are excluded by the active packaging
flow and were not used to infer the supported channel count.

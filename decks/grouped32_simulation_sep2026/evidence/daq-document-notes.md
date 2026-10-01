# Local FD DAQ evidence and the preprocessing argument

The central comparison is where pulse finding happens. Full stream sends raw
ADC data for downstream algorithms to find pulses; the self-trigger path sends
selected waveform records with FPGA-calculated peak descriptors. A downstream
coincidence stage can use those descriptors to form **local PDS trigger activity**.
That activity stage is proposed here; it is not implemented or validated by the
grouped-builder replay. Descriptors accompany waveforms, not a descriptor-only
network stream.

## Sources checked locally

- `work/wl-144132/dune-docs-analysis/text/home_marroyav_work_dune-docdb-downloads_files_DUNE-doc-11314-v15_DUNE-SP-req-spec-DAQ-23jul-b.xlsx.txt`,
  lines 32–36: DAQ input requirement 1.5 TB/s per single-phase module, jointly
  from TPC and photon detectors; selected storage 10 Gb/s average / 100 Gb/s
  temporary peak; variable readout windows and zero dead time within agreed
  conditions. These are historical module requirements, not PDS-only rates or
  measured pulse-finding CPU capacities.
- `work/wl-144132/dune-docs-analysis/text/home_marroyav_work_dune-docdb-downloads_files_DUNE-doc-14395-v1_dune-fd-network.pdf.txt`,
  28 February 2019, lines 78–105: separate PD readout, trigger server, CE
  processing, and event-builder functions. This supports the processing
  distinction but does not specify current processor counts or a PDS workload
  benchmark.
- `work/wl-144132/dune-docs-analysis/text/home_marroyav_work_dune-edms-network-interfaces_extracted_2145183_2023-07-27-ICD_Integration-DUNE_DAQ_Appendix_v5.docx.txt`,
  lines 547–553: interface drawings, rack equipment placement, and related
  installation details remained open. No PDS CPU/FPGA pulse-finder budget found.
- `work/dune_pds_trigger_refs/text_pypdf/35370_TriggerTechnote-v2.txt`, p.5,
  lines 157–179: the general trigger hierarchy begins with pulse summaries
  (time, peak, charge, channel), then activity/candidate objects. Its subsequent
  SWIFT workload and timing numbers are TPC-specific and are not used as PDS
  performance limits in this deck.

Public source identifiers:
[DocDB 11314](https://docs.dunescience.org/cgi-bin/ShowDocument?docid=11314),
[DocDB 14395](https://docs.dunescience.org/cgi-bin/ShowDocument?docid=14395),
[EDMS 2145183](https://edms.cern.ch/document/2145183),
[DocDB 35370](https://docs.dunescience.org/cgi-bin/ShowDocument?docid=35370).

## What the slide can quantify

The checked electronics rate gives `32 * 62.5 MS/s = 2 GS/s` per board.
Moving pulse summarization into the FPGA removes the need to repeat that
operation on every raw sample in the downstream coincidence path. The receiving
DAQ still parses packets, handles timing/ordering, and forms activity.

The local corpus does not establish that raw PDS pulse finding is impossible on
the proposed hardware. Therefore the deck presents preprocessing as the design
advantage and quotes the sample workload, without inventing a CPU/FPGA limit.

## Full-stream agreement is a milestone, not the present benchmark label

The current replay checks grouped versus native self-trigger builders, with
independent waveform and descriptor oracles. It shows correct retained samples
and descriptors; it does not run a matched full-stream formatter plus offline
pulse finder. That comparison must use matched signal/background input, account
for missing/overlapping windows and descriptor overflow, and compare signal
times, charge, efficiency, and local PDS trigger activity. Agreement should be
demonstrated under stated loads, rather than assumed at saturation.

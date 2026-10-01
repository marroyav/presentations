# Speaker Script - DAPHNE DAQ Integration

## PDF p. 1 / no footer number - Title

This talk covers the DAPHNE DAQ integration status.

I will focus on the interface reference, the DAQ data path,
the calibration-scan workflow through DAQ run control, and the
mitigation evidence for the remaining firmware qualification items.

## PDF p. 2 / footer 1 - Executive Claim

The headline is that DAPHNE Ethernet data taking is established in DAQ.

The DAQ/PDS boundary is anchored by EDMS 2088726 v7.0. Selected
DAPHNE settings are now exercised through `pds-run`, and decoded data
is owned by DAQ-side libraries, with Waffles downstream.

The remaining firmware qualification is handled explicitly on the
dead-time and resource mitigation slides.

## PDF p. 3 / footer 2 - Integration Evidence

There are three review surfaces.

First, the interface boundary is tied to EDMS 2088726 v7.0 for both
VD and HD. Second, DAPHNE Ethernet frames enter the DAQ path and are
decoded through DAQ packages. Third, selected DAPHNE settings can be
scanned by `pds-run`, where each scan point becomes a DAQ run.

The calibration point matters because it shows the mechanics for
future DAQ-managed calibration datasets.

## PDF p. 4 / footer 3 - Interface Contract

The interface reference is EDMS 2088726 v7.0, the DUNE DAQ and Photon
Detector System interface control document.

For this talk, the value of the reference is that readout, timing,
control, monitoring, and data-format responsibilities are discussed
against a common public boundary.

## PDF p. 5 / footer hidden, counts as 4 - DAQ Baseline

I now move from the interface reference to the DAQ implementation.

The next slides map the boundary into DAQ packages, decode utilities,
controller behavior, and monitoring.

## PDF p. 6 / footer 5 - Baseline Data Path

The baseline path is DAPHNE Ethernet output into DUNE DAQ.

DAQ fragments carry DAPHNE Ethernet frames. DAQ decode utilities then
expose the data to consumers such as Waffles.

The important ownership statement is that format and decode are in
DAQ software, not in private post-processing scripts.

## PDF p. 7 / footer 6 - Changed DAQ Repositories

The DAQ integration chain is split across three repositories.

`fddetdataformats` owns the frame definitions and tests. `rawdatautils`
exposes analysis-facing arrays. `daphnemodules` owns the DAPHNE V3
controller and monitoring path.

These are separate packages, but together they form one DAPHNE
readout chain.

## PDF p. 8 / footer 7 - Data-Format Contract

The format contract defines the DAPHNE Ethernet frame and the
stream-frame variant.

The triggered frame carries metadata, peak descriptors, and ADC
samples. The stream frame covers the packed four-channel stream case.

The reviewer-facing point is that the contract is backed by constants,
accessors, bindings, and tests.

## PDF p. 9 / footer 8 - Decode Contract

`rawdatautils` does not redefine the format.

It reuses the DAQ format classes and exposes ADC samples, timestamps,
channel information, stream frames, and peak descriptors as arrays.

That keeps Waffles and validation scripts from reimplementing the
unpacker.

## PDF p. 10 / footer 9 - Controller And Monitoring Contract

`daphnemodules` configures the DAPHNE V3 analog chain, reads trigger
and general counters, and publishes operational monitoring in DAQ.

The release finding was package-version related. Data taking worked,
and V3 `GeneralInfo` monitoring appeared with the 3.0.2 override.

This is not a run-control failure.

## PDF p. 11 / footer 10 - Dead-Time Mitigation Evidence

This is the first risk slide.

At 4.7 kHz per channel, the main 1024-tick implementation is about
7 percent dead time. The mitigation point is about 2.5 percent, but
it assumes 512-tick waveform records.

The topology is the firmware trade. The main path starts with 40
channel samples, 40 self-trigger paths, trigger primitives and
builders, two readout muxes, and one Hermes 10 Gb link.

The mitigation groups the same 40 channels into ten four-channel
sources, presents 10 Hermes inputs, and still uses one physical
Hermes link.

The lower dead-time point is not free. It trades waveform length and
grouped-readout qualification for lower dead time.

## PDF p. 12 / footer 11 - K26 Resource Mitigation Evidence

This is the second risk slide.

The baseline is tight on CLB sites and DSP48E2. The grouped candidate
keeps LUT, BRAM, and URAM below device limits, and removes the DSP
pressure.

The conclusion is narrow and useful: the remaining qualification is
readout behavior, not FPGA fit or route legality.

## PDF p. 13 / footer hidden, counts as 12 - Calibration Path Into DAQ

I now move to calibration as a DAQ integration workflow.

This is not presented as the final calibration framework. It is a
working DAQ-run-controlled path for generating configurations and
datasets.

## PDF p. 14 / footer 13 - Calibration Scans As DAQ Artifacts

Selected calibration variables already generate DAQ configurations
and run-associated datasets.

Calibration probing identified useful variables and ranges. `pds-run`
generates the minimal DAPHNE overlay, and each scan point is delegated
to `drunc`.

The resulting data and monitoring are tied to the configuration that
produced them. The current wrapper is the functional draft of the
future DAQ-native calibration path.

## PDF p. 15 / footer 14 - Draft DAQ Workflow For Variable Scans

Read the workflow from left to right.

A scan plan changes one variable. Stable defaults and paths remain
separate. The scan point generates a minimal DAPHNE overlay, updates
the DAQ configuration, optionally coordinates SSP LED settings, and
delegates the run to `drunc`.

The message is not command syntax. The message is that DAQ can create
configuration-tagged calibration datasets.

## PDF p. 16 / footer 15 - Functional Scan Coverage

The exercised coverage includes self-trigger thresholds, AFE response
settings, LED/SSP coordination, and plan-mode inspection.

This demonstrates that the wrapper already exercises the important
control mechanics with the current system.

I would frame this as a working path toward the full DAQ
implementation.

## PDF p. 17 / footer 16 - Operational Environment

This slide gives the reproducibility boundary.

It records the login path, workarea, proxy state, and target-board
selection.

The target-board point matters. Board identity and IP are
configuration requirements, and must be checked in the active JSON/XML.

## PDF p. 18 / footer hidden, counts as 17 - Validation And Review

The last section connects package-level readiness with live DAQ
behavior.

The integration needs both clean software changes and evidence from
the DAQ system.

## PDF p. 19 / footer 18 - Live Validation Result

Run 44355 demonstrated data taking with the default release, but V3
monitoring was not visible.

Run 44356 used the clean `daphnemodules` 3.0.2 override and succeeded
as a two-minute TEST run at 20 Hz.

The conclusion is that monitoring was traced to package versioning,
not to run control.

## PDF p. 20 / footer 19 - Live `pds-run` Scan Exercise

This slide is the live scan evidence.

The exercise covered self-trigger, attenuation, offset, trim, bias,
and LED/SSP modes. Across runs 44357 to 44368, each point generated a
DAQ configuration and delegated execution to `drunc`.

The key result is that successful scan commands exited cleanly, XML
validation passed after each update, and no successful-run traceback
or `drunc` command failure was found.

## PDF p. 21 / footer 20 - Live Exercise Findings

These are normal integration findings.

SSP object naming must be explicit. Some seed configurations are safe
for planning but not execution. Zero/default XML attributes require
careful interpretation. Post-scan restoration policy should be stated
in the scan plan.

None of these findings changes the main result: the tested DAQ-wrapped
scan loop is operational for the exercised modes.

## PDF p. 22 / footer 21 - Summary

I will close by separating what is established from what remains to
qualify.

Established for PRR: EDMS 2088726 v7.0 anchors the DAQ/PDS boundary
for VD and HD. DAPHNE Ethernet data taking, format ownership, and
decode utilities have been exercised. Selected DAPHNE settings can be
scanned through `pds-run`, with each point becoming a DAQ run.

Bounded qualification: dead-time mitigation gives 7 percent to
2.5 percent at 4.7 kHz per channel, with 512-tick records. The grouped
Hermes strategy addresses K26 fit pressure. The next proof is Hermes
readout, backpressure, and real-trigger stress.

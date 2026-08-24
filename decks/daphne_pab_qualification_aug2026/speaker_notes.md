# Speaker notes

## 1. Qualifying ten DAPHNE boards at PAB

We want to use the Iceberg timing and DAQ hardware at PAB to build a proper
qualification stand. There are ten boards in the campaign, but only one board
is active at a time. The active board uses all four data links together.

## 2. Ten boards need one stable test, not ten simultaneous slots

Lead with this scope because it changes the infrastructure request. We do not
need forty DAQ links or ten powered boards. We need one trustworthy fixture and
enough time to repeat the same test for ten serial numbers.

The result we want is ten comparable evidence packages. That is more useful
than ten boards briefly running at the same time.

## 3. PAB gives us the timing and DAQ context the bench cannot

Iceberg already puts the timing master and DUNE DAQ path in reach. That is why
moving to PAB is valuable. The standalone routine still matters: it lets us
bring up and diagnose a board when the endpoint is unavailable. It simply
supports a smaller claim.

The DAQ workarea, timing sequence, firmware artifacts, and test guide should be
ready before the move. We should not discover those interfaces while the board
queue is waiting.

## 4. The fixture serves one active board from end to end

Walk through the picture. We select one serial number, identify it, connect one
metered and protected 48 V path, one timing path, the board-control service, and
four fixed data links. DAQ writes data and logs; board configuration, timing,
power, and temperature go into the same evidence store.

The cable labels and receiver map should stay fixed. Board changes should not
require hand edits to the DAQ topology.

## 5. Qualify full-stream behavior before changing firmware

This section establishes the baseline. We should finish full-stream
qualification and close its run IDs before changing firmware. That protects the
comparison and gives us a known rollback state.

## 6. The campaign advances only after four gates pass

Gate 0 is infrastructure and software readiness. Gate 1 is a complete rehearsal
with a known board. Gate 2 proves full streaming, timing, data quality, power,
and recovery. Gate 3 proves the firmware transition and self-trigger path.

After the known-board dry run, freeze the fixture and run card. During the ten
boards, only identity and approved serial-specific settings should change.

## 7. Every board begins with identity and complete readback

The enrollment step prevents us from testing the wrong board, image, address,
or cable mapping. It also gives us the safe idle power and temperature point.

Write configuration only when the run card calls for it. Read every parameter
the service and firmware expose: clock, AFE, gains, offsets, thresholds, masks,
links, timing, sensors, and status. Save the requested values and the readback
separately.

The Hermes `0xDEADBEEF` read is a small control-service smoke test. It does not
prove DAQ data-taking.

## 8. Enable all four data links in controlled steps

Start from fully configured idle. One link proves the endpoint and receiver
mapping. Two links exposes basic concurrency. Four links is the required
operating test.

At four links, include a sustained run and repeated start/stop cycles. Save link
and fragment counts, sequence checks, malformed or dropped data, representative
waveforms, per-channel baseline and RMS, timestamps, power, and temperature.

The current controller source supports up to sixteen configured full-stream
channels. The offered rate, test duration, and acceptable loss criteria still
need owner approval.

## 9. Local timing is useful, but it is not synchronization

Standalone mode proves local board operation. Connected mode proves the
endpoint path. Always put the mode in the result so a local-clock pass cannot be
misread as an endpoint-synchronization pass.

In connected mode, verify source selection, both locks, endpoint address, ready
FSM state, and timestamp validity while data are being taken.

## 10. Timing must survive commands, data-taking, and recovery

Reading four good register values once is not enough. Establish ready, issue
the command sequence agreed with timing and DAQ, observe the board transition,
and correlate it with decoded timestamps and run boundaries.

Perform one controlled recovery, such as an approved endpoint reset or source
transition. Do not improvise by pulling fibers or cycling power during an active
run. Save the pre-state, command, post-state, data effect, and return-to-ready
time.

## 11. The power profile must show the cost of streaming

Measure input voltage, current, power, and temperature at every state. The
important comparison is configured idle versus one, two, and four active
links. That directly measures the transceiver and traffic contribution.

The existing documentation gives 48 V nominal, about 0.46 A idle, and an
estimated 33 W or 0.69 A full-load point. These numbers help size the stand.
They are not pass/fail limits. The power owner must define the warning and stop
limits, measurement window, room/cooling conditions, and no-auto-reenable rule.

## 12. Treat self-trigger as a second, pinned qualification phase

The full-stream run is now closed. The next phase changes one major variable:
the firmware. We keep the artifact, checksum, expected register map,
configuration template, and rollback image together.

## 13. The firmware update needs an artifact and a rollback

Stop DAQ and seal the baseline runs. Verify the artifact before programming.
After boot, read the image identity before writing configuration. Then perform a
complete write/readback comparison again.

Wrong identity, a register-map mismatch, incomplete readback, bad timing,
abnormal power or temperature, or unstable service/DAQ behavior means rollback.
Do not work around those conditions during a campaign.

## 14. Self-trigger data should cover quiet, threshold, and rate points

Begin without intentional stimulus to measure the quiet trigger rate. Then hold
the stimulus fixed and scan approved threshold points. Finally use low, nominal,
and highest approved rate points and repeat one reference point to expose drift.

Record trigger rate, accepted data rate, busy/full/drop/error counters,
timestamps, waveforms, baseline/RMS, power, and temperature.

Timing commands set and synchronize the acquisition boundaries. The stimulus
and threshold create the photon triggers. Keep those mechanisms separate in the
explanation and in the result.

## 15. One run directory keeps every claim traceable

Every attempt gets its own timestamped run ID. The manifest identifies the
serial and operator. Configuration contains the requested values and complete
readback. Observations contain timing snapshots, power, temperature, counters,
and logs. Data contains raw and decoded output plus plots. The final result is
PASS, FAIL, or INCOMPLETE with the checks and limits used.

Never overwrite a failure with a successful retry. Link the two run IDs.

## 16. DAQ must deliver a rehearsed 5.x workarea, not only a build

The local package set inspected for this plan contains a 5.6.2 baseline, so it
is a reasonable candidate. The DAQ team still owns the release decision.

Pin the package set and both firmware maps. Generate a one-board/four-link
topology. Rehearse the exact operator path from a clean shell through data
decoding and a clean restart.

## 17. The DAQ release is ready when five deliverables work together

This slide turns “prepare DAQ 5.x” into a checklist. We need a manifest, fixed
topology, human run-control guide, useful monitoring, and one-command data
checker.

The central compatibility question is whether the selected controller and
configuration path can express both the required full-stream mode and the
self-trigger mode for the exact firmware images in the campaign.

## 18. Each serial number completes the same closed loop

Board 00 is the known fixture-qualification board. Then each campaign serial is
installed, completes the baseline, completes self-trigger, has its evidence
reviewed, and is powered off and removed safely.

Do not install the next board while the current result is still ambiguous.

## 19. Recovery should start small and preserve the failure

The table is the simple recovery philosophy. Check the least invasive cause
first. Change one thing at a time. Record it. Do not reflash because a network
read failed, and do not call local timing a synchronized recovery.

Abnormal power or temperature means a safe power-off and no automatic
re-enable. Every retry gets a new run ID.

## 20. Approve the campaign and assign the owners

Ask for a decision, not general feedback. We need owners for the fixture and
safety, timing sequence, exact DAQ release, firmware artifacts and rollback,
campaign logistics/storage, and acceptance/sign-off.

We are ready to move when a known board can complete the whole procedure from a
clean start, including recovery and decoded waveform/RMS output, without a
developer repairing the environment by hand.

## Appendix: Connected timing has a concrete readiness snapshot

The connected-mode snapshot selects the external source, shows both locks,
contains the expected endpoint address, reports FSM state 8, and asserts
timestamp validity. A common raw status value is `0x18`.

Verify every address and bit against the exact firmware register map pinned for
the campaign.

## Appendix: The baseline matrix covers idle through timed streaming

This is a starting matrix, not the approved run card. The baseline rows make
local-clock idle, one/two/four-link streaming, and Iceberg-timed soaking
explicit.

## Appendix: The self-trigger matrix covers quiet through repeatability

The self-trigger rows cover quiet rate, threshold points, controlled rates, and
one repeated reference point. Timing, firmware, power, hardware, and DAQ owners
still need to set durations, stimulus/threshold/rate points, warning and stop
limits, and pass/fail criteria.

Every row gets a run ID. A skipped row is INCOMPLETE with a reason, not PASS.

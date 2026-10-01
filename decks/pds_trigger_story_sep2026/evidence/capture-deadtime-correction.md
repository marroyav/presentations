# Historical capture dead time — initial correction, 18 September 2026

Superseded as a status note by the completed FIFO replay. Current assumptions
and numbers are in [capture-loss-model.md](capture-loss-model.md) and
[capture-loss-VD-one-link.csv](capture-loss-VD-one-link.csv). This file retains
the original metric definition and the first failed access attempt.

The user's observable is time during which signal cannot be retained because
acquisition is blocked. The previous 61.57% / 46.80% counted candidate requests
that did not open a new frame. They do not measure capture dead time and have
been withdrawn from the slide comparison. Original evidence files are retained
unchanged; their `dead_*` columns are historical trigger-rejection counters.

## Definition

On each channel, put all times on the input-sample clock:

- W: the explicit observation interval;
- B: the union of intervals when acquisition cannot accept a new frame;
- C: the union of input-sample intervals in retained frames, including later
  pretrigger recovery and continuation.

Capture dead time = duration((B minus C) intersect W) / duration(W).
For a population, sum numerator and denominator over channels, including
quiet channels. Do not use the first and last candidate as the exposure.
Live waiting time outside a triggered frame is not automatically dead time.
Overlapping frames count only once. Dropped frames do not enter C.

Candidate timestamps inside C are covered even if they could not start a new
frame. The fraction of candidates outside C is a separate, arrival-weighted
metric; it generally differs from the time fraction for clustered activity.
Timestamp coverage alone does not establish complete pulse tails, recovered
charge, photon efficiency or the presence of a peak descriptor.

## Why thirteen clocks is not sufficient

The old fixed gate uses B = N + 13 clocks after an accepted candidate.
That is an admission duration, not the recorded-sample endpoint. The nominal
pretrigger in the C++ waveform/architecture models is P = 64; the baseline
frame header also reports sample zero as trigger timestamp minus 64.
The actual trigger-to-input-sample alignment still requires validation against
the delayed data path before this is called a firmware coverage measurement.

Under that explicit timing-model assumption, an accepted trigger at a saves
[a-P, a-P+N), while new-frame requests are blocked on [a, a+N+13).
Before considering another frame, the uncovered blocked tail is P+13 clocks.
A later frame can recover some of it through pretrigger history.
For consecutive accepted times a and b, away from observation boundaries,
the remaining blocked gap after the first frame is:

    min(P + 13, b - a - N) clocks, with b - a >= N + 13.

It is 13 clocks only if the next frame is accepted immediately when the gate
reopens. With a later acceptance it can be larger. Observation edges must be
clipped, and frames outside the observation window may still cover its edges.
This is a fixed-gate illustration, excluding congestion and ring overwrite.

## Available evidence and missing inputs

The numerical source for the talk is the deap0964 campaign, not the older
waffles-c production replay (which has a different mean rate).
The matching frozen source is the grouped32 deck's
`evidence/larsoft-original-summary.json`, SHA256
`a1ac4a664e08c2af8bb711acea1e19cf08da83759cf5a9d35c55038fe8297421`.
It supplies original candidate-file paths and hashes under `provenance`.
Its VD cathode intrinsic totals are 3,806,552 candidates, 1,463,031 accepted
1024 frames and 2,025,094 accepted 512 frames over 0.068 s × 640 channels.
These aggregate counts cannot recover the accepted-frame spacings.

Exact raw campaigns are preserved on WL-144132:

    /home/marroyav/work/dune-le-pds/output/campaigns/
      pure-lar-radiological-pds-fdvd-full-v7-waffles-c-deap0964-production-v1/
      fdvd__intrinsic-lar__s0000..s0007/candidate_activity/threshold_candidates.csv

The corresponding FD-HD deap0964 campaign is also listed in the source JSON.
Only unrelated low-bulk candidate CSVs were found in the retained local mirror;
they must not substitute for the nominal 87,467 Hz/channel input.

Access checked on 18 September 2026: the FNAL login hop worked, but the
WL-144132 SSH route timed out, including a fresh connection without reused
control sockets. The documented reverse bridge on dune-fd-test01 was reachable
but its workstation listener on loopback port 2222 refused the connection.
No remote state was changed during that initial attempt. The later replay is
complete; see the evidence linked above.

## Calculator and resumption

`../analysis/capture_deadtime.py` calculates B minus C from explicit observation,
blocked and retained-frame intervals. Its fixed-gate adapter preserves the
old admission rule while adding a configurable pretrigger offset. It does not
simulate FIFOs, descriptors or Hermes. Nine tests cover overlapping coverage,
later pretrigger recovery, observation clipping, quiet/live waiting periods,
negative timestamps, non-extending admission, prolonged congestion and an
independent sample-mask comparison over 250 generated interval sets.

The task-local rerun verified input hashes and reproduced the original
candidate/accepted totals. It includes FIFO admission and lane drain in the
legacy C++ architecture model. It does not validate sample-pipeline alignment
or replace cycle-accurate RTL and Hermes testing; see the current evidence
note for details.

The existing offered-traffic numbers still count accepted frames times bytes
per frame. Their interpretation is unchanged by the correction to signal loss.

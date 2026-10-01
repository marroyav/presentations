#!/usr/bin/env python3
"""Measure blocked, uncaptured time on the input-sample time axis.

Input JSON contains channels with observation_start, observation_stop,
blocked_intervals, retained_frames, and optional candidate_ticks. All intervals
are half-open integer sample ticks [start, stop). Observation windows must be
explicit; quiet channels must be included in population denominators.

Retained frames refer to saved input samples, not packet assembly wall-clock
intervals. Translate pipeline delays before using this calculator. Include
later frames that can recover data through their pretrigger samples.

Example: python3 analysis/capture_deadtime.py input.json --output result.json
"""

import argparse
from bisect import bisect_right
import hashlib
import json
from pathlib import Path


def merged(intervals, start, stop):
    """Clip intervals to the observation window and merge their union."""
    clipped = []
    for lo, hi in intervals:
        if not isinstance(lo, int) or not isinstance(hi, int) or hi < lo:
            raise ValueError("Intervals must be ordered integer sample ticks")
        lo, hi = max(lo, start), min(hi, stop)
        if lo < hi:
            clipped.append((lo, hi))
    union = []
    for lo, hi in sorted(clipped):
        if union and lo <= union[-1][1]:
            union[-1] = (union[-1][0], max(hi, union[-1][1]))
        else:
            union.append((lo, hi))
    return union


def difference(blocked, covered):
    """Subtract sorted, disjoint covered intervals from blocked intervals."""
    result = []
    j = 0
    for lo, hi in blocked:
        cursor = lo
        while j < len(covered) and covered[j][1] <= lo:
            j += 1
        k = j
        while k < len(covered) and covered[k][0] < hi:
            a, b = covered[k]
            if a > cursor:
                result.append((cursor, min(a, hi)))
            cursor = max(cursor, b)
            if cursor >= hi:
                break
            k += 1
        if cursor < hi:
            result.append((cursor, hi))
    return result


def duration(intervals):
    return sum(hi - lo for lo, hi in intervals)


def contains(intervals, starts, tick):
    index = bisect_right(starts, tick) - 1
    return index >= 0 and tick < intervals[index][1]


def measure_channel(channel):
    start, stop = channel["observation_start"], channel["observation_stop"]
    if not isinstance(start, int) or not isinstance(stop, int) or stop <= start:
        raise ValueError("An explicit, positive observation interval is required")
    blocked = merged(channel["blocked_intervals"], start, stop)
    covered = merged(channel["retained_frames"], start, stop)
    dead = difference(blocked, covered)
    total = stop - start
    result = {
        "channel_id": channel["channel_id"],
        "observation_ticks": total,
        "blocked_ticks": duration(blocked),
        "covered_ticks": duration(covered),
        "dead_ticks": duration(dead),
        "dead_time_percent": 100 * duration(dead) / total,
        "dead_intervals": dead,
    }
    if "candidate_ticks" in channel:
        candidates = channel["candidate_ticks"]
        if any(not isinstance(t, int) or t < start or t >= stop for t in candidates):
            raise ValueError("Candidate ticks must be integers inside the observation window")
        covered_starts, dead_starts = [x[0] for x in covered], [x[0] for x in dead]
        kept = sum(contains(covered, covered_starts, t) for t in candidates)
        lost = sum(contains(dead, dead_starts, t) for t in candidates)
        result.update(candidate_count=len(candidates), covered_candidates=kept,
                      uncaptured_while_blocked_candidates=lost,
                      uncovered_while_live_candidates=len(candidates) - kept - lost)
    return result


def fixed_gate_intervals(candidate_ticks, frame_samples, busy_ticks, pretrigger):
    """A timing-model adapter only: no FIFO, link, waveform or descriptor model.

    Candidate time is assumed equal to local trigger time. That assumption and
    pretrigger offset must be validated before interpreting firmware coverage.
    Include contextual triggers outside the observation window when available.
    """
    if not 0 <= pretrigger < frame_samples or busy_ticks < frame_samples:
        raise ValueError("Invalid frame, pretrigger or busy period")
    ticks = sorted(candidate_ticks)
    if len(set(ticks)) != len(ticks) or any(not isinstance(t, int) for t in ticks):
        raise ValueError("Candidate ticks must be distinct integers")
    next_live = None
    frames, blocked, accepted = [], [], []
    for tick in ticks:
        if next_live is None or tick >= next_live:
            accepted.append(tick)
            next_live = tick + busy_ticks
            frames.append((tick - pretrigger, tick - pretrigger + frame_samples))
            blocked.append((tick, next_live))
    return frames, blocked, accepted


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    raw = args.input.read_bytes()
    data = json.loads(raw)
    channels = [measure_channel(channel) for channel in data["channels"]]
    total = sum(row["observation_ticks"] for row in channels)
    if not total:
        raise ValueError("At least one channel observation is required")
    dead = sum(row["dead_ticks"] for row in channels)
    result = {
        "metric": "duration(blocked minus union(retained input-sample intervals)) / observation time",
        "input_sha256": hashlib.sha256(raw).hexdigest(),
        "sample_period_ns": data["sample_period_ns"],
        "observation_channel_ticks": total, "dead_channel_ticks": dead,
        "dead_time_percent": 100 * dead / total,
        "channels": channels,
        "limits": "Timestamp coverage does not prove pulse-tail, charge or descriptor completeness.",
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(f"{result['dead_time_percent']:.6f}% blocked and uncaptured channel-time")


if __name__ == "__main__":
    main()

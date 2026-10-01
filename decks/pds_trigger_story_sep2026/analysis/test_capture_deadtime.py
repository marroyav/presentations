"""Boundary and set-coverage contracts, not detector predictions."""

import random
import unittest

from capture_deadtime import fixed_gate_intervals, measure_channel


class CoverageTests(unittest.TestCase):
    def measure(self, blocked, frames, ticks=(), start=0, stop=200):
        return measure_channel(dict(channel_id="example", observation_start=start,
                                    observation_stop=stop, blocked_intervals=blocked,
                                    retained_frames=frames, candidate_ticks=ticks))

    def test_candidates_inside_frame_are_covered(self):
        row = self.measure([(0, 113)], [(0, 100)], [0, 25, 99, 100, 112, 113])
        self.assertEqual(row["dead_intervals"], [(100, 113)])
        self.assertEqual(row["covered_candidates"], 3)
        self.assertEqual(row["uncaptured_while_blocked_candidates"], 2)
        self.assertEqual(row["uncovered_while_live_candidates"], 1)

    def test_later_pretrigger_recovers_blocked_time(self):
        # Trigger at 20: capture [0,100), busy [20,133).
        # Next trigger at 133: capture [113,213), busy [133,246).
        frames, busy, accepted = fixed_gate_intervals([20, 50, 100, 120, 133], 100, 113, 20)
        self.assertEqual(accepted, [20, 133])
        row = self.measure(busy, frames, [50, 100, 120, 133])
        self.assertEqual(row["dead_intervals"], [(100, 113)])
        self.assertEqual(row["covered_candidates"], 3)

    def test_live_waiting_is_not_dead_time(self):
        self.assertEqual(self.measure([], [])['dead_ticks'], 0)
        self.assertEqual(self.measure([(10, 20)], [])['dead_ticks'], 10)

    def test_fully_buffered_busy_interval_is_covered(self):
        self.assertEqual(self.measure([(0, 200)], [(0, 120), (100, 200)])['dead_ticks'], 0)

    def test_long_output_block_and_observation_edges(self):
        row = self.measure([(-50, 300)], [(-20, 50), (180, 250)], start=0, stop=200)
        self.assertEqual(row["dead_intervals"], [(50, 180)])
        self.assertEqual(row["dead_time_percent"], 65)

    def test_pretrigger_does_not_imply_13_tick_gap_always(self):
        frames, busy, _ = fixed_gate_intervals([0], 1024, 1037, 64)
        self.assertEqual(self.measure(busy, frames, stop=2000)['dead_ticks'], 77)

    def test_negative_ticks_and_no_extensions(self):
        _, busy, accepted = fixed_gate_intervals([-120, -110, -20, -7], 100, 113, 0)
        self.assertEqual(accepted, [-120, -7])
        self.assertEqual(busy, [(-120, -7), (-7, 106)])

    def test_accepted_totals_do_not_determine_dead_time(self):
        results = []
        for ticks in ([0, 113], [0, 180]):
            frames, busy, accepted = fixed_gate_intervals(ticks, 100, 113, 20)
            self.assertEqual(len(accepted), 2)
            results.append(self.measure(busy, frames, stop=400)['dead_ticks'])
        self.assertEqual(results, [46, 66])

    def test_interval_result_matches_independent_tick_mask(self):
        rng = random.Random(18092026)
        for _ in range(250):
            blocked, frames = [], []
            for target in (blocked, frames):
                for _ in range(rng.randrange(12)):
                    lo = rng.randrange(-20, 220)
                    target.append((lo, lo + rng.randrange(70)))
            expected = sum(any(a <= t < b for a, b in blocked) and
                           not any(a <= t < b for a, b in frames) for t in range(200))
            self.assertEqual(self.measure(blocked, frames)['dead_ticks'], expected)


if __name__ == "__main__":
    unittest.main()

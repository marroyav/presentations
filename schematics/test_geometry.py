"""Regression tests for the mechanical layout gate."""

from __future__ import annotations

import unittest

from .geometry import LayoutError, LayoutRegistry, Rect


class LayoutRegistryTest(unittest.TestCase):
    def test_overlapping_clearances_are_rejected(self) -> None:
        layout = LayoutRegistry(10, 6, 0.25)
        layout.reserve("left", "block", Rect(1, 1, 3, 3), clearance=0.25)
        with self.assertRaisesRegex(LayoutError, "overlaps left"):
            layout.reserve(
                "right",
                "block",
                Rect(3.25, 1, 5.25, 3),
                clearance=0.25,
            )

    def test_route_through_unrelated_object_is_rejected(self) -> None:
        layout = LayoutRegistry(10, 6, 0.25)
        layout.reserve("block", "block", Rect(4, 2, 6, 4), clearance=0.25)
        with self.assertRaisesRegex(LayoutError, "crosses reserved object"):
            layout.add_route("bad-route", [(1, 3), (9, 3)])

    def test_route_may_end_at_declared_object(self) -> None:
        layout = LayoutRegistry(10, 6, 0.25)
        layout.reserve("block", "block", Rect(4, 2, 6, 4), clearance=0.25)
        route = layout.add_route(
            "intentional-connection",
            [(1, 3), (4, 3)],
            touches=("block",),
        )
        self.assertEqual(route.points[-1], (4.0, 3.0))

    def test_object_cannot_be_reserved_after_routing_starts(self) -> None:
        layout = LayoutRegistry(10, 6, 0.25)
        layout.add_route("first-route", [(1, 1), (2, 1)])
        with self.assertRaisesRegex(LayoutError, "reserve every object"):
            layout.reserve(
                "late-object",
                "block",
                Rect(4, 2, 6, 4),
                clearance=0.25,
            )

    def test_only_junction_may_exempt_attached_symbol_overlap(self) -> None:
        layout = LayoutRegistry(10, 6, 0.25)
        layout.reserve("symbol", "symbol", Rect(1, 1, 3, 3), clearance=0.25)
        with self.assertRaisesRegex(LayoutError, "only a junction"):
            layout.reserve(
                "label",
                "text",
                Rect(2, 2, 4, 4),
                clearance=0.25,
                allow_overlap=("symbol",),
                text="unsafe",
                font_family="DejaVu Sans",
                font_size=12,
            )

    def test_off_grid_or_diagonal_route_is_rejected(self) -> None:
        layout = LayoutRegistry(10, 6, 0.25)
        with self.assertRaisesRegex(LayoutError, "off the 0.25-unit grid"):
            layout.add_route("off-grid", [(1, 1), (1, 2.1)])
        with self.assertRaisesRegex(LayoutError, "orthogonal"):
            layout.add_route("diagonal", [(1, 1), (2, 2)])

    def test_unjoined_route_crossing_is_rejected(self) -> None:
        layout = LayoutRegistry(10, 6, 0.25)
        layout.add_route("horizontal", [(1, 3), (9, 3)])
        with self.assertRaisesRegex(LayoutError, "crosses unjoined route"):
            layout.add_route("vertical", [(5, 1), (5, 5)])

    def test_declared_branch_may_join_at_its_endpoint(self) -> None:
        layout = LayoutRegistry(10, 6, 0.25)
        layout.add_route("rail", [(1, 3), (9, 3)])
        branch = layout.add_route(
            "branch",
            [(5, 1), (5, 3)],
            joins=("rail",),
        )
        self.assertEqual(branch.joins, ("rail",))

    def test_routes_may_not_overlap_even_when_joined(self) -> None:
        layout = LayoutRegistry(10, 6, 0.25)
        layout.add_route("first", [(1, 3), (6, 3)])
        with self.assertRaisesRegex(LayoutError, "overlaps existing route"):
            layout.add_route(
                "second",
                [(4, 3), (9, 3)],
                joins=("first",),
            )


if __name__ == "__main__":
    unittest.main()

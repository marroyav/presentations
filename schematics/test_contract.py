"""Regression tests for artifact classification and dependency pins."""

from __future__ import annotations

import unittest

from .contract import renderer_pins, validate_classification


class ContractTest(unittest.TestCase):
    def test_supported_classification_and_scope_are_accepted(self) -> None:
        validate_classification(
            "illustrative-circuit",
            "ILLUSTRATIVE CIRCUIT  /  NOT ERC-VERIFIED",
        )

    def test_authority_claim_is_rejected_in_illustrative_lane(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsupported illustrative"):
            validate_classification("erc-clean", "ERC CLEAN")

    def test_scope_must_match_classification(self) -> None:
        with self.assertRaisesRegex(ValueError, "requires scope"):
            validate_classification(
                "system-structure",
                "ILLUSTRATIVE CIRCUIT  /  NOT ERC-VERIFIED",
            )

    def test_renderer_stack_is_fully_pinned(self) -> None:
        self.assertEqual(
            renderer_pins(),
            {
                "schemdraw": "0.23",
                "ziamath": "0.13",
                "ziafont": "0.11",
            },
        )


if __name__ == "__main__":
    unittest.main()

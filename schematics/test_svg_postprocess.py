"""Regression tests for deterministic SVG normalization."""

from __future__ import annotations

import unittest
import xml.etree.ElementTree as ET

from .geometry import LayoutError
from .svg_postprocess import (
    SVG_NAMESPACE,
    deduplicate_svg_symbols,
    normalize_svg_strokes,
)


def _svg_element(name: str, **attributes: str) -> ET.Element:
    return ET.Element(f"{{{SVG_NAMESPACE}}}{name}", attributes)


class SvgPostprocessTest(unittest.TestCase):
    def test_identical_glyph_definitions_are_deduplicated(self) -> None:
        root = _svg_element("svg")
        for _ in range(2):
            group = ET.SubElement(root, f"{{{SVG_NAMESPACE}}}g")
            symbol = ET.SubElement(
                group,
                f"{{{SVG_NAMESPACE}}}symbol",
                {"id": "DejaVuSans_65"},
            )
            ET.SubElement(symbol, f"{{{SVG_NAMESPACE}}}path", {"d": "M 0 0"})
        deduplicate_svg_symbols(root)
        symbols = [
            element
            for element in root.iter()
            if element.tag == f"{{{SVG_NAMESPACE}}}symbol"
        ]
        self.assertEqual(len(symbols), 1)

    def test_conflicting_svg_ids_are_rejected(self) -> None:
        root = _svg_element("svg")
        for path_data in ("M 0 0", "M 1 1"):
            symbol = ET.SubElement(
                root,
                f"{{{SVG_NAMESPACE}}}symbol",
                {"id": "DejaVuSans_65"},
            )
            ET.SubElement(
                symbol,
                f"{{{SVG_NAMESPACE}}}path",
                {"d": path_data},
            )
        with self.assertRaisesRegex(LayoutError, "nonidentical"):
            deduplicate_svg_symbols(root)

    def test_missing_visible_stroke_width_is_normalized(self) -> None:
        root = _svg_element("svg")
        path = ET.SubElement(
            root,
            f"{{{SVG_NAMESPACE}}}path",
            {"style": "stroke:#181a1d;fill:#181a1d;"},
        )
        normalize_svg_strokes(root, 1.25)
        self.assertIn("stroke-width:1.25", path.get("style", ""))


if __name__ == "__main__":
    unittest.main()

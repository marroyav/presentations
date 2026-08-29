"""Renderer-neutral normalization for generated SVG trees."""

from __future__ import annotations

import xml.etree.ElementTree as ET

from .geometry import LayoutError


SVG_NAMESPACE = "http://www.w3.org/2000/svg"


def _style_map(element: ET.Element) -> dict[str, str]:
    declarations: dict[str, str] = {}
    for declaration in element.get("style", "").split(";"):
        if ":" not in declaration:
            continue
        key, value = declaration.split(":", 1)
        declarations[key.strip()] = value.strip()
    return declarations


def normalize_svg_strokes(root: ET.Element, width: float) -> None:
    """Make renderer-generated marker strokes obey the canonical width."""
    for element in root.iter():
        declarations = _style_map(element)
        stroke = declarations.get("stroke", element.get("stroke", "none"))
        if stroke.strip().lower() in {"", "none", "transparent"}:
            continue
        if "stroke-width" in declarations or element.get("stroke-width"):
            continue
        style = element.get("style", "")
        if style and not style.endswith(";"):
            style += ";"
        element.set("style", f"{style}stroke-width:{width:g};")


def deduplicate_svg_symbols(root: ET.Element) -> None:
    """Keep one identical glyph definition for every global SVG id."""
    seen: dict[str, bytes] = {}
    parent_by_child = {
        child: parent
        for parent in root.iter()
        for child in list(parent)
    }
    for element in list(root.iter()):
        element_id = element.get("id")
        if not element_id:
            continue
        serialized = ET.tostring(element, encoding="utf-8")
        previous = seen.get(element_id)
        if previous is None:
            seen[element_id] = serialized
            continue
        if element.tag != f"{{{SVG_NAMESPACE}}}symbol" or previous != serialized:
            raise LayoutError(
                f"SVG id {element_id!r} is reused by nonidentical definitions"
            )
        parent_by_child[element].remove(element)

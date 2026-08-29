"""Load and validate the renderer-neutral schematic style contract."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any


STYLE_PATH = Path(__file__).with_name("style.json")


@dataclass(frozen=True)
class FontSizes:
    title: float
    label: float
    note: float


@dataclass(frozen=True)
class Style:
    schema_version: int
    ink: str
    muted: str
    paper: str
    surface: str
    stroke_width: float
    font_family: str
    text_mode: str
    svg2: bool
    font_sizes: FontSizes
    minimum_font_size: float
    grid: float
    margin: float
    object_clearance: float
    text_clearance: float
    block_padding: float
    inches_per_unit: float
    element_unit: float
    corner_radius: float
    junction_radius: float
    terminal_radius: float

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Style":
        if data.get("schema_version") != 1:
            raise ValueError("schematics/style.json: schema_version must be 1")
        sizes = data.get("font_sizes")
        if not isinstance(sizes, dict):
            raise ValueError("schematics/style.json: font_sizes must be an object")
        style = cls(
            schema_version=1,
            ink=str(data["ink"]),
            muted=str(data["muted"]),
            paper=str(data["paper"]),
            surface=str(data["surface"]),
            stroke_width=float(data["stroke_width"]),
            font_family=str(data["font_family"]),
            text_mode=str(data["text_mode"]),
            svg2=data["svg2"],
            font_sizes=FontSizes(
                title=float(sizes["title"]),
                label=float(sizes["label"]),
                note=float(sizes["note"]),
            ),
            minimum_font_size=float(data["minimum_font_size"]),
            grid=float(data["grid"]),
            margin=float(data["margin"]),
            object_clearance=float(data["object_clearance"]),
            text_clearance=float(data["text_clearance"]),
            block_padding=float(data["block_padding"]),
            inches_per_unit=float(data["inches_per_unit"]),
            element_unit=float(data["element_unit"]),
            corner_radius=float(data["corner_radius"]),
            junction_radius=float(data["junction_radius"]),
            terminal_radius=float(data["terminal_radius"]),
        )
        if style.stroke_width <= 0 or style.grid <= 0 or style.block_padding <= 0:
            raise ValueError("stroke_width, grid, and block_padding must be positive")
        if style.text_mode != "path":
            raise ValueError("text_mode must be 'path' for portable SVG output")
        if style.svg2 is not True:
            raise ValueError("svg2 must be true for auditable outlined glyphs")
        if min(
            style.font_sizes.title,
            style.font_sizes.label,
            style.font_sizes.note,
        ) < style.minimum_font_size:
            raise ValueError("all configured font sizes must meet minimum_font_size")
        return style

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "ink": self.ink,
            "muted": self.muted,
            "paper": self.paper,
            "surface": self.surface,
            "stroke_width": self.stroke_width,
            "font_family": self.font_family,
            "text_mode": self.text_mode,
            "svg2": self.svg2,
            "font_sizes": {
                "title": self.font_sizes.title,
                "label": self.font_sizes.label,
                "note": self.font_sizes.note,
            },
            "minimum_font_size": self.minimum_font_size,
            "grid": self.grid,
            "margin": self.margin,
            "object_clearance": self.object_clearance,
            "text_clearance": self.text_clearance,
            "block_padding": self.block_padding,
            "inches_per_unit": self.inches_per_unit,
            "element_unit": self.element_unit,
            "corner_radius": self.corner_radius,
            "junction_radius": self.junction_radius,
            "terminal_radius": self.terminal_radius,
        }


def load_style(path: Path = STYLE_PATH) -> Style:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: root must be an object")
    return Style.from_dict(data)


DEFAULT_STYLE = load_style()

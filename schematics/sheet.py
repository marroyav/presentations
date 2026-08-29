"""SchemDraw adapter with one stroke, one font, and checked layout zones."""

from __future__ import annotations

import hashlib
from importlib.metadata import PackageNotFoundError, version
import json
from pathlib import Path
import xml.etree.ElementTree as ET
from typing import Any, Iterable, Sequence

try:
    import schemdraw
    import schemdraw.elements as elm
    import schemdraw.flow as flow
    from schemdraw.backends import svg as svg_backend
    from schemdraw.segments import Segment
except ModuleNotFoundError as exc:  # pragma: no cover - exercised by CLI users
    raise SystemExit(
        "SchemDraw is required to render concept schematics. "
        "Install schematics/requirements.txt in a virtual environment."
    ) from exc

from .contract import renderer_pins, validate_classification
from .geometry import LayoutError, LayoutRegistry, Point, Rect
from .style import DEFAULT_STYLE, Style
from .svg_postprocess import deduplicate_svg_symbols, normalize_svg_strokes


SVG_NAMESPACE = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NAMESPACE)
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")


def _bbox_rect(element: elm.Element) -> Rect:
    bbox = element.get_bbox(transform=True, includetext=True)
    return Rect(float(bbox.xmin), float(bbox.ymin), float(bbox.xmax), float(bbox.ymax))


def _union_rects(rectangles: Sequence[Rect]) -> Rect:
    if not rectangles:
        raise LayoutError("an element group cannot be empty")
    return Rect(
        min(rect.x0 for rect in rectangles),
        min(rect.y0 for rect in rectangles),
        max(rect.x1 for rect in rectangles),
        max(rect.y1 for rect in rectangles),
    )


def _renderer_versions() -> dict[str, str]:
    versions: dict[str, str] = {}
    for package in ("schemdraw", "ziamath", "ziafont"):
        try:
            versions[package] = version(package)
        except PackageNotFoundError:
            versions[package] = "unknown"
    return versions


def _renderer_record() -> dict[str, Any]:
    installed = _renderer_versions()
    expected = renderer_pins()
    if installed != expected:
        raise SystemExit(
            "Renderer versions do not match schematics/requirements.txt: "
            f"expected {expected}, found {installed}"
        )
    return {
        "name": "SchemDraw",
        "version": installed["schemdraw"],
        "text_stack": {
            "ziamath": installed["ziamath"],
            "ziafont": installed["ziafont"],
        },
    }


def _text_dimensions(value: str, size: float, style: Style) -> tuple[float, float]:
    width, height, _ = svg_backend.text_size(
        value,
        font=style.font_family,
        size=size,
    )
    # SchemDraw's SegmentText bounding box maps one typographic inch to two
    # drawing units, independent of the final SVG physical-size setting.
    points_to_units = 2 / 72
    return float(width) * points_to_units, float(height) * points_to_units


class Sheet:
    """A fixed-grid, standalone schematic with a semantic layout manifest."""

    def __init__(
        self,
        *,
        schematic_id: str,
        concept: str,
        title: str,
        description: str,
        scope: str,
        classification: str,
        source: dict[str, Any],
        width: float = 14.0,
        height: float = 8.0,
        style: Style = DEFAULT_STYLE,
    ) -> None:
        self.schematic_id = schematic_id
        self.concept = concept
        self.title_text = title
        self.description_text = description
        self.scope = scope
        self.classification = classification
        self.source = source
        self.width = width
        self.height = height
        self.style = style
        validate_classification(classification, scope)
        self.layout = LayoutRegistry(width, height, style.grid)

        schemdraw.use("svg")
        try:
            svg_backend.config.text = style.text_mode
            svg_backend.config.svg2 = style.svg2
        except ValueError as exc:
            raise SystemExit(
                "The pinned ziamath dependency is required for portable "
                "outlined SVG text. Install schematics/requirements.txt."
            ) from exc
        self._drawing = schemdraw.Drawing(show=False)
        self._drawing.config(
            unit=style.element_unit,
            inches_per_unit=style.inches_per_unit,
            fontsize=style.font_sizes.label,
            font=style.font_family,
            color=style.ink,
            lw=style.stroke_width,
            fill="none",
            bgcolor=style.paper,
            margin=style.margin,
        )

        # This invisible segment fixes the canvas without adding a visual frame.
        frame = elm.Element()
        frame.segments.append(Segment([(0, 0), (width, height)], visible=False))
        self._drawing.add(frame)

        self.text(
            "sheet-title",
            (0.75, height - 0.75),
            title,
            size=style.font_sizes.title,
            color=style.ink,
            halign="left",
            clearance=style.text_clearance,
        )
        self.text(
            "sheet-scope",
            (0.75, height - 1.50),
            scope,
            size=style.font_sizes.note,
            color=style.muted,
            halign="left",
            clearance=style.text_clearance,
        )

    def text(
        self,
        name: str,
        at: Point,
        value: str,
        *,
        size: float | None = None,
        color: str | None = None,
        halign: str = "center",
        valign: str = "center",
        clearance: float | None = None,
    ) -> elm.Element:
        font_size = size or self.style.font_sizes.label
        label = (
            elm.Label()
            .at(at)
            .theta(0)
            .label(
                value,
                ofst=(-0.1, -0.1),
                halign=halign,
                valign=valign,
                fontsize=font_size,
                font=self.style.font_family,
                color=color or self.style.ink,
            )
        )
        self._drawing.add(label)
        self.layout.reserve(
            name,
            "text",
            _bbox_rect(label),
            clearance=(
                self.style.text_clearance if clearance is None else clearance
            ),
            text=value,
            font_family=self.style.font_family,
            font_size=font_size,
        )
        return label

    def block(
        self,
        name: str,
        center: Point,
        width: float,
        height: float,
        label: str,
        *,
        fill: str | None = None,
        stroke: str | None = None,
        clearance: float | None = None,
    ) -> elm.Element:
        text_width, text_height = _text_dimensions(
            label,
            self.style.font_sizes.label,
            self.style,
        )
        if (
            text_width + 2 * self.style.block_padding > width
            or text_height + 2 * self.style.block_padding > height
        ):
            raise LayoutError(
                f"{name}: label needs {text_width:.2f} × {text_height:.2f} "
                f"units plus {self.style.block_padding:g}-unit padding"
            )
        bounds = Rect(
            center[0] - width / 2,
            center[1] - height / 2,
            center[0] + width / 2,
            center[1] + height / 2,
        )
        self.layout.reserve(
            name,
            "block",
            bounds,
            clearance=(
                self.style.object_clearance if clearance is None else clearance
            ),
            text=label,
            font_family=self.style.font_family,
            font_size=self.style.font_sizes.label,
        )
        block = (
            flow.RoundBox(
                w=width,
                h=height,
                cornerradius=self.style.corner_radius,
            )
            .at(center)
            .anchor("center")
            .color(stroke or self.style.ink)
            .fill(fill or self.style.paper)
            .linewidth(self.style.stroke_width)
            .label(
                label,
                fontsize=self.style.font_sizes.label,
                font=self.style.font_family,
                color=self.style.ink,
            )
        )
        self._drawing.add(block)
        actual = _bbox_rect(block)
        if not bounds.expanded(0.02).contains(actual):
            raise LayoutError(
                f"{name}: label or symbol exceeds the declared block bounds"
            )
        return block

    def route(
        self,
        name: str,
        points: Sequence[Point],
        *,
        touches: Iterable[str] = (),
        joins: Iterable[str] = (),
        color: str | None = None,
    ) -> None:
        self.layout.add_route(name, points, touches=touches, joins=joins)
        for first, second in zip(points, points[1:]):
            line = (
                elm.Line()
                .at(first)
                .to(second)
                .color(color or self.style.ink)
                .linewidth(self.style.stroke_width)
            )
            self._drawing.add(line)

    def element(
        self,
        name: str,
        element: elm.Element,
        *,
        kind: str = "symbol",
        clearance: float | None = None,
        _allow_overlap: Iterable[str] = (),
    ) -> elm.Element:
        """Add one styled element and reserve its actual rendered bounds."""
        element.color(self.style.ink).linewidth(self.style.stroke_width)
        self._drawing.add(element)
        self.layout.reserve(
            name,
            kind,
            _bbox_rect(element),
            clearance=(
                self.style.object_clearance if clearance is None else clearance
            ),
            allow_overlap=_allow_overlap,
        )
        return element

    def element_group(
        self,
        name: str,
        elements: Sequence[elm.Element],
        *,
        kind: str = "symbol-group",
        clearance: float | None = None,
    ) -> tuple[elm.Element, ...]:
        """Add connected elements under one actual-bounds reservation."""
        rendered: list[elm.Element] = []
        bounds: list[Rect] = []
        for element in elements:
            element.color(self.style.ink).linewidth(self.style.stroke_width)
            self._drawing.add(element)
            rendered.append(element)
            bounds.append(_bbox_rect(element))
        self.layout.reserve(
            name,
            kind,
            _union_rects(bounds),
            clearance=(
                self.style.object_clearance if clearance is None else clearance
            ),
        )
        return tuple(rendered)

    def junction(
        self,
        name: str,
        at: Point,
        *,
        allow_overlap: Iterable[str] = (),
    ) -> elm.Element:
        return self.element(
            name,
            elm.Dot(radius=self.style.junction_radius).at(at),
            kind="junction",
            _allow_overlap=allow_overlap,
        )

    def terminal(self, name: str, at: Point) -> elm.Element:
        return self.element(
            name,
            elm.Dot(radius=self.style.terminal_radius, open=True).at(at),
            kind="terminal",
        )

    def save(self, path: Path) -> dict[str, Any]:
        path.parent.mkdir(parents=True, exist_ok=True)
        renderer = _renderer_record()
        self._drawing.save(path, transparent=False)
        self._add_svg_metadata(path, renderer)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        return {
            "id": self.schematic_id,
            "concept": self.concept,
            "title": self.title_text,
            "description": self.description_text,
            "scope": self.scope,
            "classification": self.classification,
            "source": self.source,
            "renderer": renderer,
            "path": path.name,
            "sha256": digest,
            "layout": self.layout.to_dict(),
        }

    def _add_svg_metadata(
        self,
        path: Path,
        renderer: dict[str, Any],
    ) -> None:
        tree = ET.parse(path)
        root = tree.getroot()
        normalize_svg_strokes(root, self.style.stroke_width)
        deduplicate_svg_symbols(root)
        root.set("data-schematic-id", self.schematic_id)
        root.set("data-concept", self.concept)
        root.set("data-classification", self.classification)
        root.set("data-stroke-width", f"{self.style.stroke_width:g}")
        root.set("data-font-family", self.style.font_family)
        root.set("data-text-mode", self.style.text_mode)
        title = ET.Element(f"{{{SVG_NAMESPACE}}}title")
        title.text = self.title_text
        description = ET.Element(f"{{{SVG_NAMESPACE}}}desc")
        description.text = (
            f"{self.scope}. {self.description_text} "
            f"Source: {self.source['title']}, "
            f"page {self.source['page']}."
        )
        metadata = ET.Element(f"{{{SVG_NAMESPACE}}}metadata")
        metadata.text = json.dumps(
            {
                "schema_version": 1,
                "id": self.schematic_id,
                "concept": self.concept,
                "description": self.description_text,
                "classification": self.classification,
                "scope": self.scope,
                "source": self.source,
                "renderer": renderer,
                "text_mode": self.style.text_mode,
            },
            sort_keys=True,
        )
        root.insert(0, metadata)
        root.insert(0, description)
        root.insert(0, title)
        tree.write(path, encoding="utf-8", xml_declaration=True)

"""Small deterministic layout ledger for spacing and routing checks."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Sequence


EPSILON = 1e-8
Point = tuple[float, float]


class LayoutError(ValueError):
    """Raised when a diagram violates the layout contract."""


@dataclass(frozen=True)
class Rect:
    x0: float
    y0: float
    x1: float
    y1: float

    def __post_init__(self) -> None:
        if self.x1 <= self.x0 or self.y1 <= self.y0:
            raise LayoutError(f"invalid rectangle {self}")

    def expanded(self, amount: float) -> "Rect":
        return Rect(
            self.x0 - amount,
            self.y0 - amount,
            self.x1 + amount,
            self.y1 + amount,
        )

    def overlaps(self, other: "Rect") -> bool:
        return not (
            self.x1 <= other.x0 + EPSILON
            or other.x1 <= self.x0 + EPSILON
            or self.y1 <= other.y0 + EPSILON
            or other.y1 <= self.y0 + EPSILON
        )

    def contains(self, other: "Rect", tolerance: float = EPSILON) -> bool:
        return (
            self.x0 - tolerance <= other.x0
            and self.y0 - tolerance <= other.y0
            and self.x1 + tolerance >= other.x1
            and self.y1 + tolerance >= other.y1
        )

    def to_list(self) -> list[float]:
        return [self.x0, self.y0, self.x1, self.y1]

    @classmethod
    def from_sequence(cls, value: Sequence[float]) -> "Rect":
        if len(value) != 4:
            raise LayoutError("rectangle requires four coordinates")
        return cls(*(float(item) for item in value))


@dataclass(frozen=True)
class Reservation:
    name: str
    kind: str
    bounds: Rect
    clearance: float
    allow_overlap: tuple[str, ...]
    text: str | None
    font_family: str | None
    font_size: float | None

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "name": self.name,
            "kind": self.kind,
            "bounds": self.bounds.to_list(),
            "clearance": self.clearance,
            "allow_overlap": list(self.allow_overlap),
        }
        if self.text is not None:
            data["text"] = self.text
            data["font_family"] = self.font_family
            data["font_size"] = self.font_size
        return data


@dataclass(frozen=True)
class Route:
    name: str
    points: tuple[Point, ...]
    touches: tuple[str, ...]
    joins: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "points": [[x, y] for x, y in self.points],
            "touches": list(self.touches),
            "joins": list(self.joins),
        }


def _is_grid_value(value: float, grid: float) -> bool:
    return abs(value / grid - round(value / grid)) <= 1e-7


def _segment_enters_rect(first: Point, second: Point, rect: Rect) -> bool:
    x0, y0 = first
    x1, y1 = second
    if abs(y0 - y1) <= EPSILON:
        if not rect.y0 + EPSILON < y0 < rect.y1 - EPSILON:
            return False
        low, high = sorted((x0, x1))
        return high > rect.x0 + EPSILON and low < rect.x1 - EPSILON
    if abs(x0 - x1) <= EPSILON:
        if not rect.x0 + EPSILON < x0 < rect.x1 - EPSILON:
            return False
        low, high = sorted((y0, y1))
        return high > rect.y0 + EPSILON and low < rect.y1 - EPSILON
    raise LayoutError(f"non-orthogonal segment {first} -> {second}")


def _segment_intersection(
    first: Point,
    second: Point,
    third: Point,
    fourth: Point,
) -> tuple[str, Point | None]:
    """Return none, point, or overlap for two orthogonal segments."""
    first_horizontal = abs(first[1] - second[1]) <= EPSILON
    second_horizontal = abs(third[1] - fourth[1]) <= EPSILON
    if first_horizontal and second_horizontal:
        if abs(first[1] - third[1]) > EPSILON:
            return "none", None
        low = max(min(first[0], second[0]), min(third[0], fourth[0]))
        high = min(max(first[0], second[0]), max(third[0], fourth[0]))
        if high < low - EPSILON:
            return "none", None
        if abs(high - low) <= EPSILON:
            return "point", (low, first[1])
        return "overlap", None
    if not first_horizontal and not second_horizontal:
        if abs(first[0] - third[0]) > EPSILON:
            return "none", None
        low = max(min(first[1], second[1]), min(third[1], fourth[1]))
        high = min(max(first[1], second[1]), max(third[1], fourth[1]))
        if high < low - EPSILON:
            return "none", None
        if abs(high - low) <= EPSILON:
            return "point", (first[0], low)
        return "overlap", None
    horizontal_start, horizontal_end = (
        (first, second) if first_horizontal else (third, fourth)
    )
    vertical_start, vertical_end = (
        (third, fourth) if first_horizontal else (first, second)
    )
    intersection = (vertical_start[0], horizontal_start[1])
    if (
        min(horizontal_start[0], horizontal_end[0]) - EPSILON
        <= intersection[0]
        <= max(horizontal_start[0], horizontal_end[0]) + EPSILON
        and min(vertical_start[1], vertical_end[1]) - EPSILON
        <= intersection[1]
        <= max(vertical_start[1], vertical_end[1]) + EPSILON
    ):
        return "point", intersection
    return "none", None


class LayoutRegistry:
    """Records occupied regions and rejects collisions before SVG export."""

    def __init__(self, width: float, height: float, grid: float) -> None:
        if width <= 0 or height <= 0 or grid <= 0:
            raise LayoutError("canvas width, height, and grid must be positive")
        self.width = float(width)
        self.height = float(height)
        self.grid = float(grid)
        self.reservations: list[Reservation] = []
        self.routes: list[Route] = []

    def _check_point(self, point: Point, context: str) -> None:
        x, y = point
        if not (0 <= x <= self.width and 0 <= y <= self.height):
            raise LayoutError(f"{context}: point {point} is outside the canvas")
        if not _is_grid_value(x, self.grid) or not _is_grid_value(y, self.grid):
            raise LayoutError(
                f"{context}: point {point} is off the {self.grid:g}-unit grid"
            )

    def reserve(
        self,
        name: str,
        kind: str,
        bounds: Rect,
        *,
        clearance: float,
        allow_overlap: Iterable[str] = (),
        text: str | None = None,
        font_family: str | None = None,
        font_size: float | None = None,
    ) -> Reservation:
        allowed = set(allow_overlap)
        if self.routes:
            raise LayoutError(
                f"{name}: reserve every object before adding routes so "
                "route-clearance checks are order independent"
            )
        if not name or any(item.name == name for item in self.reservations):
            raise LayoutError(f"reservation name must be unique and non-empty: {name!r}")
        if clearance < 0:
            raise LayoutError(f"{name}: clearance cannot be negative")
        has_font_metadata = font_family is not None or font_size is not None
        if text is None and has_font_metadata:
            raise LayoutError(f"{name}: font metadata requires text")
        if text is not None and (
            not text.strip()
            or not font_family
            or font_size is None
            or font_size <= 0
        ):
            raise LayoutError(f"{name}: text requires a font family and size")
        if (
            bounds.x0 < -EPSILON
            or bounds.y0 < -EPSILON
            or bounds.x1 > self.width + EPSILON
            or bounds.y1 > self.height + EPSILON
        ):
            raise LayoutError(f"{name}: {bounds} is outside the canvas")
        expanded = bounds.expanded(clearance)
        for existing in self.reservations:
            if existing.name in allowed:
                if kind != "junction" or existing.kind not in {
                    "symbol",
                    "symbol-group",
                }:
                    raise LayoutError(
                        f"{name}: only a junction may overlap its attached symbol"
                    )
                continue
            if expanded.overlaps(existing.bounds.expanded(existing.clearance)):
                raise LayoutError(
                    f"{name} overlaps {existing.name} after required clearances"
                )
        item = Reservation(
            name,
            kind,
            bounds,
            clearance,
            tuple(sorted(allowed)),
            text,
            font_family,
            font_size,
        )
        self.reservations.append(item)
        return item

    def add_route(
        self,
        name: str,
        points: Sequence[Point],
        *,
        touches: Iterable[str] = (),
        joins: Iterable[str] = (),
    ) -> Route:
        if not name or any(item.name == name for item in self.routes):
            raise LayoutError(f"route name must be unique and non-empty: {name!r}")
        if len(points) < 2:
            raise LayoutError(f"{name}: a route needs at least two points")
        normalized = tuple((float(x), float(y)) for x, y in points)
        for point in normalized:
            self._check_point(point, name)
        touched = tuple(touches)
        known_names = {item.name for item in self.reservations}
        unknown = set(touched) - known_names
        if unknown:
            raise LayoutError(f"{name}: unknown touched objects: {sorted(unknown)}")
        joined = tuple(joins)
        known_routes = {item.name for item in self.routes}
        unknown_routes = set(joined) - known_routes
        if unknown_routes:
            raise LayoutError(
                f"{name}: unknown joined routes: {sorted(unknown_routes)}"
            )
        for first, second in zip(normalized, normalized[1:]):
            if first == second:
                raise LayoutError(f"{name}: zero-length segment at {first}")
            if abs(first[0] - second[0]) > EPSILON and abs(first[1] - second[1]) > EPSILON:
                raise LayoutError(f"{name}: routes must be orthogonal")
            for obstacle in self.reservations:
                if obstacle.name in touched:
                    continue
                if _segment_enters_rect(
                    first,
                    second,
                    obstacle.bounds.expanded(obstacle.clearance),
                ):
                    raise LayoutError(
                        f"{name} crosses reserved object {obstacle.name}"
                    )
            for existing in self.routes:
                for third, fourth in zip(existing.points, existing.points[1:]):
                    relation, point = _segment_intersection(
                        first,
                        second,
                        third,
                        fourth,
                    )
                    if relation == "none":
                        continue
                    if relation == "overlap":
                        raise LayoutError(
                            f"{name} overlaps existing route {existing.name}"
                        )
                    if existing.name not in joined:
                        raise LayoutError(
                            f"{name} crosses unjoined route {existing.name}"
                        )
                    if point not in {normalized[0], normalized[-1]}:
                        raise LayoutError(
                            f"{name} may join {existing.name} only at a route endpoint"
                        )
        route = Route(name, normalized, touched, joined)
        self.routes.append(route)
        return route

    def to_dict(self) -> dict[str, Any]:
        return {
            "canvas": {"width": self.width, "height": self.height},
            "grid": self.grid,
            "objects": [item.to_dict() for item in self.reservations],
            "routes": [item.to_dict() for item in self.routes],
        }

    @classmethod
    def validate_dict(cls, data: dict[str, Any]) -> None:
        canvas = data.get("canvas")
        if not isinstance(canvas, dict):
            raise LayoutError("layout canvas must be an object")
        registry = cls(
            float(canvas["width"]),
            float(canvas["height"]),
            float(data["grid"]),
        )
        objects = data.get("objects")
        routes = data.get("routes")
        if not isinstance(objects, list) or not isinstance(routes, list):
            raise LayoutError("layout objects and routes must be arrays")
        for item in objects:
            if not isinstance(item, dict):
                raise LayoutError("layout object entries must be objects")
            registry.reserve(
                str(item["name"]),
                str(item["kind"]),
                Rect.from_sequence(item["bounds"]),
                clearance=float(item["clearance"]),
                allow_overlap=item.get("allow_overlap", ()),
                text=item.get("text"),
                font_family=item.get("font_family"),
                font_size=(
                    float(item["font_size"])
                    if item.get("font_size") is not None
                    else None
                ),
            )
        for item in routes:
            if not isinstance(item, dict):
                raise LayoutError("layout route entries must be objects")
            registry.add_route(
                str(item["name"]),
                item["points"],
                touches=item.get("touches", ()),
                joins=item.get("joins", ()),
            )

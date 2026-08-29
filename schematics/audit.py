"""Audit committed standalone SVGs without requiring the rendering dependency."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

from .geometry import LayoutError, LayoutRegistry
from .contract import renderer_pins, validate_classification
from .style import DEFAULT_STYLE


ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "output"
MANIFEST_PATH = OUTPUT_DIR / "layout-manifest.json"


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _style_map(element: ET.Element) -> dict[str, str]:
    result: dict[str, str] = {}
    raw = element.get("style", "")
    for declaration in raw.split(";"):
        if ":" not in declaration:
            continue
        key, value = declaration.split(":", 1)
        result[key.strip()] = value.strip()
    return result


def _property(element: ET.Element, key: str) -> str | None:
    return _style_map(element).get(key, element.get(key))


def _as_number(value: str | None) -> float | None:
    if value is None:
        return None
    normalized = value.strip().lower().removesuffix("px").removesuffix("pt")
    try:
        return float(normalized)
    except ValueError:
        return None


def _audit_svg(path: Path, artifact: dict[str, object]) -> list[str]:
    errors: list[str] = []
    try:
        tree = ET.parse(path)
    except (OSError, ET.ParseError) as exc:
        return [f"{path}: cannot parse SVG: {exc}"]
    root = tree.getroot()
    expected_width = DEFAULT_STYLE.stroke_width
    expected_font = DEFAULT_STYLE.font_family
    allowed_colors = {
        DEFAULT_STYLE.ink.lower(),
        DEFAULT_STYLE.muted.lower(),
        DEFAULT_STYLE.paper.lower(),
        DEFAULT_STYLE.surface.lower(),
        "none",
        "transparent",
    }

    expected_metadata = {
        "data-schematic-id": str(artifact.get("id", "")),
        "data-concept": str(artifact.get("concept", "")),
        "data-classification": str(artifact.get("classification", "")),
        "data-stroke-width": f"{expected_width:g}",
        "data-font-family": expected_font,
        "data-text-mode": DEFAULT_STYLE.text_mode,
    }
    for key, expected in expected_metadata.items():
        if root.get(key) != expected:
            errors.append(f"{path}: root {key} must be {expected!r}")
    if not root.get("viewBox"):
        errors.append(f"{path}: SVG must declare a viewBox")
    metadata_nodes = [
        element for element in root if _local_name(element.tag) == "metadata"
    ]
    if len(metadata_nodes) != 1 or not metadata_nodes[0].text:
        errors.append(f"{path}: SVG must contain one JSON metadata record")
    else:
        try:
            metadata = json.loads(metadata_nodes[0].text)
        except json.JSONDecodeError as exc:
            errors.append(f"{path}: invalid SVG metadata JSON: {exc}")
        else:
            for key in (
                "id",
                "concept",
                "classification",
                "description",
                "scope",
                "source",
                "renderer",
            ):
                if metadata.get(key) != artifact.get(key):
                    errors.append(f"{path}: metadata {key} does not match manifest")
            if metadata.get("text_mode") != DEFAULT_STYLE.text_mode:
                errors.append(f"{path}: metadata text_mode must be path")

    title_nodes = [element for element in root if _local_name(element.tag) == "title"]
    description_nodes = [
        element for element in root if _local_name(element.tag) == "desc"
    ]
    if len(title_nodes) != 1 or title_nodes[0].text != artifact.get("title"):
        errors.append(f"{path}: accessible SVG title is missing or incorrect")
    source = artifact.get("source")
    expected_description = None
    if isinstance(source, dict):
        expected_description = (
            f"{artifact.get('scope')}. {artifact.get('description')} "
            f"Source: {source.get('title')}, page {source.get('page')}."
        )
    if (
        len(description_nodes) != 1
        or description_nodes[0].text != expected_description
    ):
        errors.append(f"{path}: accessible SVG description is missing")

    glyph_prefix = expected_font.replace(" ", "") + "_"
    glyph_count = 0
    glyph_use_count = 0
    stroke_count = 0
    element_ids: set[str] = set()
    use_targets: list[str] = []
    for element in root.iter():
        tag = _local_name(element.tag)
        element_id = element.get("id")
        if element_id:
            if element_id in element_ids:
                errors.append(f"{path}: duplicate SVG id {element_id!r}")
            element_ids.add(element_id)
        if tag in {"image", "foreignObject"}:
            errors.append(f"{path}: embedded {tag} content is forbidden")
        if tag == "text":
            errors.append(f"{path}: live SVG text is forbidden in path mode")
        if tag == "symbol":
            glyph_count += 1
            symbol_id = element.get("id", "")
            if not symbol_id.startswith(glyph_prefix):
                errors.append(
                    f"{path}: glyph symbol {symbol_id!r} is not {expected_font}"
                )
        if tag == "use":
            glyph_use_count += 1
            href = element.get("href") or element.get(
                "{http://www.w3.org/1999/xlink}href"
            )
            if not href or not href.startswith(f"#{glyph_prefix}"):
                errors.append(f"{path}: glyph use has invalid font reference {href!r}")
            elif href:
                use_targets.append(href[1:])

        for property_name in ("stroke", "fill", "background-color"):
            property_value = _property(element, property_name)
            if (
                property_value is not None
                and property_value.strip().lower() not in allowed_colors
            ):
                errors.append(
                    f"{path}: {tag} uses noncanonical {property_name} "
                    f"{property_value!r}"
                )

        stroke = _property(element, "stroke")
        if stroke is None or stroke.strip().lower() in {"", "none", "transparent"}:
            continue
        stroke_count += 1
        width = _as_number(_property(element, "stroke-width"))
        if width is None:
            errors.append(f"{path}: stroked {tag} is missing stroke-width")
        elif not math.isclose(width, expected_width, abs_tol=1e-9):
            errors.append(
                f"{path}: stroked {tag} uses width {width:g}; "
                f"expected {expected_width:g}"
            )

    if glyph_count == 0 or glyph_use_count == 0:
        errors.append(f"{path}: outlined {expected_font} glyphs were not found")
    missing_targets = sorted(set(use_targets) - element_ids)
    if missing_targets:
        errors.append(
            f"{path}: glyph uses reference missing ids {missing_targets}"
        )
    if stroke_count == 0:
        errors.append(f"{path}: no visible strokes found")
    return errors


def _audit_layout_text(path: Path, layout: dict[str, object]) -> list[str]:
    errors: list[str] = []
    objects = layout.get("objects")
    if not isinstance(objects, list):
        return [f"{path}: layout objects must be an array"]
    for item in objects:
        if not isinstance(item, dict):
            continue
        has_text = "text" in item
        if item.get("kind") in {"text", "block"} and not has_text:
            errors.append(
                f"{path}: {item.get('name')} is missing outlined-text metadata"
            )
            continue
        if not has_text:
            continue
        if item.get("font_family") != DEFAULT_STYLE.font_family:
            errors.append(
                f"{path}: {item.get('name')} does not use "
                f"{DEFAULT_STYLE.font_family}"
            )
        size = item.get("font_size")
        if not isinstance(size, (int, float)) or isinstance(size, bool):
            errors.append(f"{path}: {item.get('name')} has no numeric font size")
        elif size < DEFAULT_STYLE.minimum_font_size:
            errors.append(
                f"{path}: {item.get('name')} is below the "
                f"{DEFAULT_STYLE.minimum_font_size:g}-point minimum"
            )
    return errors


def audit() -> tuple[list[str], int]:
    errors: list[str] = []
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{MANIFEST_PATH}: cannot read valid JSON: {exc}"], 0
    if not isinstance(manifest, dict) or manifest.get("schema_version") != 1:
        return [f"{MANIFEST_PATH}: schema_version must be 1"], 0
    if manifest.get("style") != DEFAULT_STYLE.to_dict():
        errors.append(f"{MANIFEST_PATH}: embedded style does not match style.json")
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        return [f"{MANIFEST_PATH}: artifacts must be a non-empty array"], 0
    try:
        pins = renderer_pins()
    except (OSError, ValueError) as exc:
        return [str(exc)], 0
    expected_renderer = {
        "name": "SchemDraw",
        "version": pins["schemdraw"],
        "text_stack": {
            "ziamath": pins["ziamath"],
            "ziafont": pins["ziafont"],
        },
    }

    seen_concepts: set[str] = set()
    checked = 0
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            errors.append(f"{MANIFEST_PATH}: artifact entries must be objects")
            continue
        concept = artifact.get("concept")
        if not isinstance(concept, str) or not concept:
            errors.append(f"{MANIFEST_PATH}: artifact concept must be non-empty")
        elif concept in seen_concepts:
            errors.append(f"{MANIFEST_PATH}: duplicate concept {concept!r}")
        else:
            seen_concepts.add(concept)
        description = artifact.get("description")
        if not isinstance(description, str) or not description.strip():
            errors.append(
                f"{MANIFEST_PATH}: artifact description must be non-empty"
            )
        source = artifact.get("source")
        if (
            not isinstance(source, dict)
            or not isinstance(source.get("title"), str)
            or not isinstance(source.get("url"), str)
            or not isinstance(source.get("page"), int)
            or source.get("page", 0) <= 0
        ):
            errors.append(
                f"{MANIFEST_PATH}: artifact source needs title, URL, and page"
            )
        classification = artifact.get("classification")
        scope = artifact.get("scope")
        if not isinstance(classification, str) or not isinstance(scope, str):
            errors.append(
                f"{MANIFEST_PATH}: artifact needs classification and scope"
            )
        else:
            try:
                validate_classification(classification, scope)
            except ValueError as exc:
                errors.append(f"{MANIFEST_PATH}: {exc}")
        if artifact.get("renderer") != expected_renderer:
            errors.append(
                f"{MANIFEST_PATH}: artifact renderer does not match pinned stack"
            )
        relative = artifact.get("path")
        if not isinstance(relative, str) or Path(relative).name != relative:
            errors.append(f"{MANIFEST_PATH}: artifact path must be one SVG filename")
            continue
        path = OUTPUT_DIR / relative
        if path.suffix.lower() != ".svg" or not path.is_file():
            errors.append(f"{path}: committed standalone SVG is missing")
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if artifact.get("sha256") != digest:
            errors.append(f"{path}: SHA-256 does not match layout manifest")
        layout = artifact.get("layout")
        if not isinstance(layout, dict):
            errors.append(f"{path}: layout must be an object")
        else:
            try:
                LayoutRegistry.validate_dict(layout)
            except (KeyError, TypeError, ValueError, LayoutError) as exc:
                errors.append(f"{path}: invalid or colliding layout: {exc}")
            errors.extend(_audit_layout_text(path, layout))
        errors.extend(_audit_svg(path, artifact))
        checked += 1
    return errors, checked


def main() -> int:
    errors, checked = audit()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(
            f"Standalone schematic audit failed: {len(errors)} error(s), "
            f"{checked} SVG(s) checked.",
            file=sys.stderr,
        )
        return 1
    print(f"Standalone schematic audit passed: {checked} SVG(s) checked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate provenance and content hashes for schematic presentation assets."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
ALLOWED_STATUSES = {
    "image-derived-reference",
    "vector-redraw-reference",
    "erc-clean",
    "human-reviewed",
}
ALLOWED_KINDS = {"embedded-raster", "repo-native-vector-redraw", "eda-export"}
REFERENCE_STATUSES = {"image-derived-reference", "vector-redraw-reference"}
AUTHORITY_STATUSES = {"erc-clean", "human-reviewed"}
AUTHORITY_ERC_VALUES = {"clean", "dispositioned"}
AUTHORITY_SOURCE_FIELDS = (
    "source_repository",
    "source_revision",
    "source_path",
    "tool_version",
    "export_command",
)
AUTHORITY_DIGEST_FIELDS = ("erc_report_sha256", "netlist_sha256")


def require_string(
    value: Any, field: str, context: str, errors: list[str]
) -> str:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{context}: {field} must be a non-empty string")
        return ""
    return value


def audit_manifest(path: Path) -> tuple[list[str], int]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{path}: cannot read valid JSON: {exc}"], 0

    context = path.as_posix()
    if not isinstance(data, dict):
        return [f"{context}: manifest root must be an object"], 0

    if data.get("schema_version") != 1:
        errors.append(f"{context}: schema_version must be 1")

    deck = require_string(data.get("deck"), "deck", context, errors)
    if deck and deck != path.parent.name:
        errors.append(
            f"{context}: deck '{deck}' does not match directory '{path.parent.name}'"
        )

    source = data.get("source")
    if not isinstance(source, dict):
        errors.append(f"{context}: source must be an object")
        source = {}
    for field in ("title", "presenter", "event", "landing_page", "artifact_url"):
        require_string(source.get(field), f"source.{field}", context, errors)
    source_hash = require_string(
        source.get("artifact_sha256"), "source.artifact_sha256", context, errors
    )
    if source_hash and not SHA256_RE.fullmatch(source_hash):
        errors.append(f"{context}: source.artifact_sha256 is not a SHA-256 digest")

    visual_reference = data.get("visual_reference")
    if visual_reference is not None:
        if not isinstance(visual_reference, dict):
            errors.append(f"{context}: visual_reference must be an object")
            visual_reference = {}
        for field in ("title", "artifact_url", "role"):
            require_string(
                visual_reference.get(field),
                f"visual_reference.{field}",
                context,
                errors,
            )
        reference_hash = require_string(
            visual_reference.get("artifact_sha256"),
            "visual_reference.artifact_sha256",
            context,
            errors,
        )
        if reference_hash and not SHA256_RE.fullmatch(reference_hash):
            errors.append(
                f"{context}: visual_reference.artifact_sha256 is not a "
                "SHA-256 digest"
            )
        reference_bytes = visual_reference.get("artifact_bytes")
        if "artifact_bytes" in visual_reference and (
            not isinstance(reference_bytes, int)
            or isinstance(reference_bytes, bool)
            or reference_bytes <= 0
        ):
            errors.append(
                f"{context}: visual_reference.artifact_bytes must be a "
                "positive integer"
            )
        has_cache_digest = "cache_entry_sha256" in visual_reference
        has_cache_bytes = "cache_entry_bytes" in visual_reference
        if "digest_scope" in visual_reference or has_cache_digest or has_cache_bytes:
            require_string(
                visual_reference.get("digest_scope"),
                "visual_reference.digest_scope",
                context,
                errors,
            )
        if has_cache_digest:
            cache_hash = require_string(
                visual_reference.get("cache_entry_sha256"),
                "visual_reference.cache_entry_sha256",
                context,
                errors,
            )
            if cache_hash and not SHA256_RE.fullmatch(cache_hash):
                errors.append(
                    f"{context}: visual_reference.cache_entry_sha256 is not a "
                    "SHA-256 digest"
                )
        cache_bytes = visual_reference.get("cache_entry_bytes")
        if has_cache_bytes and (
            not isinstance(cache_bytes, int)
            or isinstance(cache_bytes, bool)
            or cache_bytes <= 0
        ):
            errors.append(
                f"{context}: visual_reference.cache_entry_bytes must be a "
                "positive integer"
            )
        if has_cache_digest != has_cache_bytes:
            errors.append(
                f"{context}: visual_reference cache digest and byte count must "
                "be recorded together"
            )
        reference_pages = visual_reference.get("pages")
        if (
            not isinstance(reference_pages, list)
            or not reference_pages
            or any(
                not isinstance(page, int) or isinstance(page, bool) or page <= 0
                for page in reference_pages
            )
        ):
            errors.append(
                f"{context}: visual_reference.pages must be a non-empty array "
                "of positive integers"
            )

    verification = data.get("verification")
    if not isinstance(verification, dict):
        errors.append(f"{context}: verification must be an object")
        verification = {}
    status = require_string(
        verification.get("status"), "verification.status", context, errors
    )
    if status and status not in ALLOWED_STATUSES:
        errors.append(
            f"{context}: verification.status must be one of "
            f"{', '.join(sorted(ALLOWED_STATUSES))}"
        )
    connectivity = require_string(
        verification.get("electrical_connectivity"),
        "verification.electrical_connectivity",
        context,
        errors,
    )
    erc = require_string(
        verification.get("erc"), "verification.erc", context, errors
    )
    require_string(
        verification.get("human_review"),
        "verification.human_review",
        context,
        errors,
    )
    require_string(
        verification.get("statement"), "verification.statement", context, errors
    )
    if status == "image-derived-reference" and connectivity != "not-verified":
        errors.append(
            f"{context}: image-derived references must declare electrical "
            "connectivity as 'not-verified'"
        )
    if (
        status == "vector-redraw-reference"
        and connectivity != "transcribed-not-verified"
    ):
        errors.append(
            f"{context}: vector redraws must declare electrical connectivity "
            "as 'transcribed-not-verified'"
        )
    if status in REFERENCE_STATUSES:
        if erc != "not-applicable":
            errors.append(
                f"{context}: reference-only schematics must declare ERC as "
                "'not-applicable'"
            )
    if status in AUTHORITY_STATUSES:
        require_string(
            verification.get("reviewer"),
            "verification.reviewer",
            context,
            errors,
        )
        if erc not in AUTHORITY_ERC_VALUES:
            errors.append(
                f"{context}: hardware-authority ERC must be 'clean' or "
                "'dispositioned'"
            )
    if status == "erc-clean" and erc != "clean":
        errors.append(
            f"{context}: erc-clean status requires verification.erc to be 'clean'"
        )

    artifacts = data.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        errors.append(f"{context}: artifacts must be a non-empty array")
        return errors, 0

    checked = 0
    seen_paths: set[str] = set()
    for index, artifact in enumerate(artifacts, start=1):
        item_context = f"{context}: artifact {index}"
        if not isinstance(artifact, dict):
            errors.append(f"{item_context} must be an object")
            continue

        relative_text = require_string(
            artifact.get("path"), "path", item_context, errors
        )
        digest = require_string(
            artifact.get("sha256"), "sha256", item_context, errors
        )
        kind = require_string(artifact.get("kind"), "kind", item_context, errors)
        if kind and kind not in ALLOWED_KINDS:
            errors.append(
                f"{item_context}: kind must be one of "
                f"{', '.join(sorted(ALLOWED_KINDS))}"
            )
        if (
            status == "vector-redraw-reference"
            and kind != "repo-native-vector-redraw"
        ):
            errors.append(
                f"{item_context}: vector-redraw manifests may contain only "
                "repo-native vector sources"
            )
        if status == "image-derived-reference" and kind != "embedded-raster":
            errors.append(
                f"{item_context}: image-derived manifests may contain only "
                "embedded raster sources"
            )
        if status in AUTHORITY_STATUSES and kind != "eda-export":
            errors.append(
                f"{item_context}: hardware-authority manifests may contain "
                "only EDA exports"
            )
        if kind == "eda-export" and status not in AUTHORITY_STATUSES:
            errors.append(
                f"{item_context}: EDA exports require erc-clean or "
                "human-reviewed status"
            )
        if kind == "eda-export":
            for field in AUTHORITY_SOURCE_FIELDS:
                require_string(artifact.get(field), field, item_context, errors)
            for field in AUTHORITY_DIGEST_FIELDS:
                evidence_digest = require_string(
                    artifact.get(field), field, item_context, errors
                )
                if evidence_digest and not SHA256_RE.fullmatch(evidence_digest):
                    errors.append(
                        f"{item_context}: {field} is not a SHA-256 digest"
                    )
        require_string(
            artifact.get("extraction"), "extraction", item_context, errors
        )

        for field in ("source_page",):
            value = artifact.get(field)
            if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
                errors.append(f"{item_context}: {field} must be a positive integer")
        if kind == "embedded-raster":
            for field in ("width_px", "height_px"):
                value = artifact.get(field)
                if (
                    not isinstance(value, int)
                    or isinstance(value, bool)
                    or value <= 0
                ):
                    errors.append(
                        f"{item_context}: {field} must be a positive integer"
                    )

        if digest and not SHA256_RE.fullmatch(digest):
            errors.append(f"{item_context}: sha256 is not a SHA-256 digest")
            continue
        if not relative_text:
            continue
        if relative_text in seen_paths:
            errors.append(f"{item_context}: duplicate path '{relative_text}'")
            continue
        seen_paths.add(relative_text)

        relative = Path(relative_text)
        if relative.is_absolute() or ".." in relative.parts:
            errors.append(f"{item_context}: path must remain inside the deck")
            continue
        if kind == "repo-native-vector-redraw" and relative.suffix != ".tex":
            errors.append(
                f"{item_context}: repo-native vector redraws must be TeX sources"
            )
            continue
        if (
            kind == "eda-export"
            and relative.suffix.lower() not in {".pdf", ".svg"}
        ):
            errors.append(
                f"{item_context}: EDA exports must be PDF or SVG artifacts"
            )
            continue
        target = path.parent / relative
        if not target.is_file():
            errors.append(f"{item_context}: missing file {target}")
            continue

        if kind == "repo-native-vector-redraw":
            source_text = target.read_text(encoding="utf-8")
            if not any(
                marker in source_text
                for marker in ("\\begin{tikzpicture}", "\\begin{circuitikz}")
            ):
                errors.append(
                    f"{item_context}: vector source has no TikZ/CircuitikZ picture"
                )
                continue
            if "\\includegraphics" in source_text:
                errors.append(
                    f"{item_context}: vector redraw must not embed raster artwork"
                )
                continue

        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        if digest and actual != digest:
            errors.append(
                f"{item_context}: hash mismatch for {target}; "
                f"expected {digest}, got {actual}"
            )
            continue
        checked += 1

    return errors, checked


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path("decks")
    manifests = sorted(root.glob("*/schematics.json"))
    if not manifests:
        print(f"No schematic manifests found under {root}.")
        return 0

    errors: list[str] = []
    checked = 0
    for manifest in manifests:
        manifest_errors, manifest_checked = audit_manifest(manifest)
        errors.extend(manifest_errors)
        checked += manifest_checked

    if errors:
        print("Schematic provenance audit failures:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        f"Schematic provenance audit passed for {len(manifests)} manifest(s) "
        f"and {checked} asset(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

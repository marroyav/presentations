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
ALLOWED_STATUSES = {"image-derived-reference", "erc-clean", "human-reviewed"}


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
    require_string(
        verification.get("statement"), "verification.statement", context, errors
    )
    if status == "image-derived-reference" and connectivity != "not-verified":
        errors.append(
            f"{context}: image-derived references must declare electrical "
            "connectivity as 'not-verified'"
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
        require_string(artifact.get("kind"), "kind", item_context, errors)
        require_string(
            artifact.get("extraction"), "extraction", item_context, errors
        )

        for field in ("source_page", "width_px", "height_px"):
            value = artifact.get(field)
            if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
                errors.append(f"{item_context}: {field} must be a positive integer")

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
        target = path.parent / relative
        if not target.is_file():
            errors.append(f"{item_context}: missing file {target}")
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

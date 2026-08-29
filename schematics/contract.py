"""Artifact classifications and pinned renderer versions."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent
REQUIREMENTS_PATH = ROOT / "requirements.txt"

CLASSIFICATION_SCOPES = {
    "illustrative-circuit": "ILLUSTRATIVE CIRCUIT  /  NOT ERC-VERIFIED",
    "system-structure": "STRUCTURE ONLY  /  NOT ELECTRICAL NETS",
    "system-flow": "SYSTEM FLOW  /  NOT ELECTRICAL NETS",
}


def validate_classification(classification: str, scope: str) -> None:
    expected_scope = CLASSIFICATION_SCOPES.get(classification)
    if expected_scope is None:
        allowed = ", ".join(sorted(CLASSIFICATION_SCOPES))
        raise ValueError(
            f"unsupported illustrative classification {classification!r}; "
            f"choose one of: {allowed}"
        )
    if scope != expected_scope:
        raise ValueError(
            f"{classification!r} requires scope {expected_scope!r}, "
            f"not {scope!r}"
        )


def renderer_pins(path: Path = REQUIREMENTS_PATH) -> dict[str, str]:
    pins: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        package, separator, package_version = line.partition("==")
        if not separator or not package or not package_version:
            raise ValueError(f"{path}: every renderer dependency must use ==")
        pins[package.lower()] = package_version
    required = {"schemdraw", "ziamath", "ziafont"}
    if set(pins) != required:
        raise ValueError(
            f"{path}: renderer pins must be exactly {sorted(required)}"
        )
    return pins

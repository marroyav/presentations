#!/usr/bin/env python3
"""Create a presentation deck from the maintained framework starter."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STARTER = ROOT / "examples/framework_starter"
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9_-]*$")
GENERATED_PATTERNS = (
    "main.pdf",
    "*.aux",
    "*.log",
    "*.nav",
    "*.out",
    "*.snm",
    "*.toc",
    "*.vrb",
    "*.xdv",
    "*.synctex.gz",
    "*.fls",
    "*.fdb_latexmk",
    "_minted-*",
)


def tex_escape(value: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(character, character) for character in value)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a new DUNE presentation deck.")
    parser.add_argument("slug", help="Directory name under decks/")
    parser.add_argument("--title", required=True, help="Presentation title")
    parser.add_argument("--author", default="Your name", help="Presentation author")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not SLUG_RE.fullmatch(args.slug):
        print(
            "Slug must start with a lowercase letter or digit and contain only "
            "lowercase letters, digits, underscores, or hyphens.",
            file=sys.stderr,
        )
        return 2

    destination = ROOT / "decks" / args.slug
    if destination.exists():
        print(f"Refusing to overwrite existing path: {destination}", file=sys.stderr)
        return 2

    shutil.copytree(
        STARTER,
        destination,
        ignore=shutil.ignore_patterns(*GENERATED_PATTERNS),
    )
    main_path = destination / "main.tex"
    main_text = main_path.read_text(encoding="utf-8")
    main_text = main_text.replace("Presentation title", tex_escape(args.title))
    main_text = main_text.replace("Presentation author", tex_escape(args.author))
    main_path.write_text(main_text, encoding="utf-8")

    readme_path = destination / "README.md"
    readme_text = readme_path.read_text(encoding="utf-8")
    readme_text = readme_text.replace("Presentation title", args.title)
    readme_text = readme_text.replace("presentation_slug", args.slug)
    readme_path.write_text(readme_text, encoding="utf-8")

    print(f"Created {destination.relative_to(ROOT)}")
    print("Complete the audience/outcome brief in README.md, then run make.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

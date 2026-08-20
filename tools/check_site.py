"""Check local links and frozen publication-asset hashes.

Copyright (C) 2026 Aaron Kyle Solomon
SPDX-License-Identifier: GPL-3.0-or-later
"""

from __future__ import annotations

import hashlib
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = ROOT / "docs"


class _ReferenceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.references: list[str] = []
        self.identifiers: set[str] = set()

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        values = dict(attrs)
        identifier = values.get("id")
        if identifier:
            self.identifiers.add(identifier)
        attribute = (
            "href"
            if tag in {"a", "link"}
            else "src"
            if tag in {"img", "script"}
            else None
        )
        if attribute and values.get(attribute):
            self.references.append(values[attribute])


def _local_references(index: Path) -> tuple[list[Path], list[str]]:
    parser = _ReferenceParser()
    parser.feed(index.read_text(encoding="utf-8"))
    paths: list[Path] = []
    missing_fragments: list[str] = []
    for reference in parser.references:
        parsed = urlsplit(reference)
        if not parsed.path and parsed.fragment:
            if parsed.fragment not in parser.identifiers:
                missing_fragments.append(parsed.fragment)
            continue
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        target = (SITE_ROOT / parsed.path).resolve()
        if not target.is_relative_to(SITE_ROOT.resolve()):
            raise ValueError(f"reference escapes site root: {reference}")
        paths.append(target)
    return paths, missing_fragments


def _expected_hashes(checksum_file: Path) -> dict[Path, str]:
    expected: dict[Path, str] = {}
    for line in checksum_file.read_text(encoding="utf-8").splitlines():
        digest, relative_path = line.split(maxsplit=1)
        expected[ROOT / relative_path] = digest
    return expected


def main() -> None:
    index = SITE_ROOT / "index.html"
    references, missing_fragments = _local_references(index)
    missing = [path for path in references if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing local site targets: {missing}")
    if missing_fragments:
        raise ValueError(f"missing page anchors: {missing_fragments}")

    for path, expected in _expected_hashes(ROOT / "CHECKSUMS.sha256").items():
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f"checksum mismatch: {path.relative_to(ROOT)}")

    print("site links and publication-asset checksums: OK")


if __name__ == "__main__":
    main()

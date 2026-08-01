"""Bilingual public-documentation contracts."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def guide_sources() -> list[Path]:
    files = [
        ROOT / name
        for name in (
            "README.md",
            "CODE_OF_CONDUCT.md",
            "CONTRIBUTING.md",
            "CONTRIBUTORS.md",
            "PRIVACY.md",
            "SECURITY.md",
        )
    ]
    files.extend(sorted((ROOT / "docs").glob("*.md")))
    files.extend(sorted((ROOT / "extensions").glob("*/README.md")))
    files.extend(sorted((ROOT / "extensions").glob("*/docs/*-SETUP.md")))
    files.extend(sorted((ROOT / "pdf").glob("*.md")))
    return [path for path in files if not path.name.endswith(".fr.md")]


def local_links(path: Path, text: str) -> list[Path]:
    targets = []
    for raw in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
        target = raw.split("#", 1)[0]
        if not target or "://" in target or target.startswith(("mailto:", "tel:")):
            continue
        targets.append((path.parent / target).resolve())
    return targets


def command_names(text: str) -> set[str]:
    return {
        match.group(1) or "root"
        for match in re.finditer(
            r"(?<![-\w])/powehi-seo(?:\s+([a-z][a-z0-9-]*))?", text
        )
    }


def test_every_public_guide_has_a_french_companion() -> None:
    sources = guide_sources()
    assert len(sources) == 30
    for source in sources:
        french = source.with_name(f"{source.stem}.fr.md")
        assert french.is_file(), f"Missing French guide: {french.relative_to(ROOT)}"
        assert source.read_text(encoding="utf-8").startswith(
            f"> **Languages:** [Français]({french.name}) | English"
        )
        assert french.read_text(encoding="utf-8").startswith(
            f"> **Langue :** Français | [English]({source.name})"
        )


def test_french_guides_preserve_contracts_and_valid_links() -> None:
    for source in guide_sources():
        french = source.with_name(f"{source.stem}.fr.md")
        english_text = source.read_text(encoding="utf-8")
        french_text = french.read_text(encoding="utf-8")
        assert "ZXQ" not in french_text, f"Placeholder leaked into {french.relative_to(ROOT)}"
        assert "Powehi Universal SEO & GEO" not in french_text
        assert not re.search(r"(?<![-\w])/seo(?:\s|`)", french_text)
        assert french_text.count("```") % 2 == 0
        assert command_names(english_text) <= command_names(french_text), (
            f"Command drift in {french.relative_to(ROOT)}"
        )
        missing = [path for path in local_links(french, french_text) if not path.exists()]
        assert missing == [], f"Broken local links in {french.relative_to(ROOT)}: {missing}"


def test_english_guides_have_valid_local_links() -> None:
    for source in guide_sources():
        text = source.read_text(encoding="utf-8")
        missing = [path for path in local_links(source, text) if not path.exists()]
        assert missing == [], f"Broken local links in {source.relative_to(ROOT)}: {missing}"

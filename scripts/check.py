#!/usr/bin/env python3
"""Dependency-free structure checks; not a comprehensive secret scanner."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "x-article-skill"

def main():
    required = ["README.md", "LICENSE", "CONTRIBUTING.md", "CHANGELOG.md",
                "skills/x-article-skill/SKILL.md",
                "skills/x-article-skill/templates/creator-input.md",
                "skills/x-article-skill/templates/visual-style.md"]
    for name in required:
        if not (ROOT / name).is_file():
            raise ValueError(f"Missing: {name}")
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    if not text.startswith("---\nname: x-article-skill\n"):
        raise ValueError("Skill name/frontmatter mismatch")
    if "\ndescription: " not in text.split("---", 2)[1]:
        raise ValueError("Missing description")
    for path in ROOT.rglob("*.md"):
        content = path.read_text(encoding="utf-8")
        if re.search(r"/Users/[^/\s]+/|/home/[^/\s]+/", content):
            raise ValueError(f"Personal absolute path: {path.relative_to(ROOT)}")
        for link in re.findall(r"\]\(([^)]+)\)", content):
            if "://" in link or link.startswith("#"):
                continue
            destination = path.parent / link.split("#", 1)[0]
            if not destination.exists():
                raise ValueError(f"Broken local link in {path.relative_to(ROOT)}: {link}")
    print("PASS: required files, skill identity, local links and personal-path check.")
    print("This check does not verify every secret, client behavior or writing quality.")

if __name__ == "__main__":
    main()


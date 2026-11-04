#!/usr/bin/env python3
"""Install only the public skill; never overwrite an existing directory."""
import argparse
import os
from pathlib import Path
import shutil
import sys

def install(source, parent):
    source, parent = Path(source), Path(parent).expanduser()
    if not (source / "SKILL.md").is_file():
        raise FileNotFoundError("Missing source SKILL.md")
    target = parent / "x-article-skill"
    parent.mkdir(parents=True, exist_ok=True)
    target.mkdir()  # Atomic refusal if an existing file, directory or symlink is present.
    try:
        for item in source.iterdir():
            if item.is_dir():
                shutil.copytree(item, target / item.name)
            else:
                shutil.copy2(item, target / item.name)
    except BaseException:
        shutil.rmtree(target)
        raise
    return target

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    default = Path(os.environ.get("CODEX_HOME") or (Path.home() / ".codex")) / "skills"
    parser.add_argument("--dest", type=Path, default=default,
                        help="Parent skill directory; defaults to CODEX_HOME/skills.")
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[1] / "skills" / "x-article-skill"
    try:
        target = install(source, args.dest)
    except FileExistsError:
        print("Existing target found. No files were overwritten.", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"Installation failed: {exc}", file=sys.stderr)
        return 1
    print(f"Installed: {target}")
    print("Invoke $x-article-skill in your next Codex turn.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())


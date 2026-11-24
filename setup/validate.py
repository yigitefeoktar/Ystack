#!/usr/bin/env python3
"""Validate packaged skills, metadata, and local resource links."""

from pathlib import Path
import re
import sys

try:
    import yaml
except ImportError:
    raise SystemExit("Install validation dependencies: python -m pip install -r setup/requirements-dev.txt")

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "bytebrew-game-analytics", "confirm-task-understanding", "crazygames-basic-launch",
    "game-audio-review", "game-deployment", "manage-games-hub", "master-project-manager",
}


def validate():
    errors = []
    folders = {p.name for p in (ROOT / "skills").iterdir() if p.is_dir()}
    if folders != EXPECTED:
        errors.append(f"Unexpected skill set: {sorted(folders)}")
    for name in sorted(EXPECTED):
        path = ROOT / "skills" / name / "SKILL.md"
        if not path.is_file():
            errors.append(f"Missing {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        match = re.match(r"\A---\s*\n(.*?)\n---(?:\s*\n|$)", text, re.S)
        if not match:
            errors.append(f"{name}: missing YAML frontmatter")
            continue
        try:
            front = yaml.safe_load(match.group(1))
            if not isinstance(front, dict) or front.get("name") != name:
                errors.append(f"{name}: frontmatter name does not match folder")
            description = front.get("description") if isinstance(front, dict) else None
            if not isinstance(description, str) or not description.strip():
                errors.append(f"{name}: missing description")
            metadata = path.parent / "agents" / "openai.yaml"
            if metadata.exists():
                config = yaml.safe_load(metadata.read_text(encoding="utf-8"))
                if not isinstance(config, dict):
                    errors.append(f"{name}: invalid metadata")
                elif name == "master-project-manager" and config.get("policy", {}).get("allow_implicit_invocation") is not False:
                    errors.append("Manager must remain explicit-only")
        except yaml.YAMLError as error:
            errors.append(f"{name}: invalid YAML: {error}")

    # Validate relative Markdown links, including references inside skill bodies.
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            target = target.strip("<>").split("#", 1)[0]
            if not target or re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.is_relative_to(ROOT) or not resolved.exists():
                errors.append(f"{path.relative_to(ROOT)}: missing/outside link {target}")

    # Exclude local runtime state and private machine bindings from distribution.
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts:
            continue
        if path.name == "auth.json" or path.name.startswith(".env") or path.suffix in {".sqlite", ".db"}:
            errors.append(f"Unexpected runtime/private file: {path.relative_to(ROOT)}")
        if path.suffix in {".md", ".yaml", ".js", ".tsx", ".css"}:
            data = path.read_text(encoding="utf-8")
            if re.search(r"https?://[^\s`]+\.ts\.net|C:[/\\]Users[/\\]", data):
                errors.append(f"Private machine binding: {path.relative_to(ROOT)}")
            if re.search(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,}|AKIA[A-Z0-9]{16})\b", data):
                errors.append(f"Possible credential: {path.relative_to(ROOT)}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Validated 7 skill packages, metadata, relative links, and distribution boundaries.")
    return 0


if __name__ == "__main__":
    raise SystemExit(validate())

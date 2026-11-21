#!/usr/bin/env python3
"""Install selected Ystack skills; global instructions are explicitly opt-in."""

import argparse
from datetime import datetime, timezone
import os
from pathlib import Path
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def install(args):
    available = sorted(p.name for p in (ROOT / "skills").iterdir()
                       if p.is_dir() and (p / "SKILL.md").is_file())
    selected = sorted(set(args.skill or available))
    unknown = set(selected) - set(available)
    if unknown:
        raise ValueError("Unknown skills: " + ", ".join(sorted(unknown)))
    skills_dir = Path(args.skills_dir).expanduser().resolve()
    codex_home = Path(args.codex_home).expanduser().resolve()
    targets = [(ROOT / "skills" / name, skills_dir / name) for name in selected]
    if args.agents:
        targets.append((ROOT / "AGENTS.md", codex_home / "AGENTS.md"))
        targets.append((ROOT / "T3_SETUP.md", codex_home / "T3_SETUP.md"))
        targets.append((ROOT / "YSTACK_MAINTENANCE.md", codex_home / "YSTACK_MAINTENANCE.md"))

    # Preflight the entire selection before writing anything.
    conflicts = []
    for source, target in targets:
        if target.is_symlink():
            raise ValueError(f"Refusing to replace a symlink: {target}")
        resolved = target.resolve()
        if resolved == ROOT or ROOT in resolved.parents:
            raise ValueError(f"Install outside the Ystack source checkout: {target}")
        if target.exists():
            if target.is_dir() != source.is_dir():
                raise ValueError(f"Destination has an incompatible file type: {target}")
            conflicts.append(target)
    if conflicts and not args.force:
        paths = "\n".join(str(p) for p in conflicts)
        raise ValueError(f"Existing destinations left unchanged:\n{paths}\n"
                         "Review them, then use --force to back up and replace.")

    for source, target in targets:
        action = "Back up and replace" if target.exists() else "Install"
        print(f"{action}: {target}")
    if args.dry_run:
        print("Dry run: no files changed.")
        return

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    for source, target in targets:
        target.parent.mkdir(parents=True, exist_ok=True)
        # Stage the complete copy on the destination filesystem before replacing.
        with tempfile.TemporaryDirectory(prefix=".ystack-stage-", dir=target.parent) as temp:
            staged = Path(temp) / target.name
            if source.is_dir():
                shutil.copytree(source, staged, symlinks=False,
                                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            else:
                shutil.copy2(source, staged)
            backup = None
            if target.exists():
                if source.is_dir():
                    backup = skills_dir.parent / ".ystack-backups" / stamp / "skills" / target.name
                else:
                    backup = codex_home / ".ystack-backups" / stamp / target.name
                backup.parent.mkdir(parents=True, exist_ok=True)
                target.rename(backup)
                print(f"Backup: {backup}")
            try:
                staged.rename(target)
            except OSError:
                if backup is not None and not target.exists():
                    backup.rename(target)
                raise
    print(f"Installed {len(selected)} skill(s). Global AGENTS.md "
          + ("installed." if args.agents else "left unchanged."))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill", action="append", metavar="NAME",
                        help="Install only this skill; repeat for several. Default: all seven.")
    parser.add_argument("--skills-dir", default=str(Path.home() / ".agents" / "skills"),
                        help="Destination skill directory (default: ~/.agents/skills).")
    parser.add_argument("--codex-home", default=os.environ.get("CODEX_HOME") or str(Path.home() / ".codex"),
                        help="Global instructions destination; used only with --agents.")
    parser.add_argument("--agents", action="store_true", help="Also install the personal AGENTS.md and its companion guides.")
    parser.add_argument("--force", action="store_true", help="Back up and replace existing destinations.")
    parser.add_argument("--dry-run", action="store_true", help="Show actions without changing files.")
    args = parser.parse_args()
    try:
        install(args)
    except (ValueError, OSError) as error:
        print(f"Installation stopped: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

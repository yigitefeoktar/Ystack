"""Exercise the installer only in disposable temporary destinations."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="ystack-test-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.skills = self.base / "user" / "skills"
        self.codex = self.base / "codex"

    def run_installer(self, *extra, success=True):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "install.py"),
             "--skills-dir", str(self.skills), "--codex-home", str(self.codex), *extra],
            text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 0 if success else 1, result.stdout + result.stderr)
        return result

    def test_dry_run_writes_nothing(self):
        self.run_installer("--dry-run", "--agents")
        self.assertEqual(list(self.base.iterdir()), [])

    def test_all_seven_and_support_files_without_global_changes(self):
        self.run_installer()
        installed = sorted(p.name for p in self.skills.iterdir())
        expected = sorted(p.name for p in (ROOT / "skills").iterdir() if p.is_dir())
        self.assertEqual(installed, expected)
        for source in (ROOT / "skills").rglob("*"):
            if source.is_file():
                target = self.skills / source.relative_to(ROOT / "skills")
                self.assertEqual(target.read_bytes(), source.read_bytes())
        self.assertFalse(self.codex.exists())

    def test_selected_only(self):
        self.run_installer("--skill", "confirm-task-understanding")
        self.assertEqual([p.name for p in self.skills.iterdir()], ["confirm-task-understanding"])

    def test_conflict_preflight_prevents_partial_install(self):
        target = self.skills / "master-project-manager"
        target.mkdir(parents=True)
        sentinel = target / "local-note.txt"
        sentinel.write_text("local work", encoding="utf-8")
        self.run_installer(success=False)
        self.assertEqual([p.name for p in self.skills.iterdir()], ["master-project-manager"])
        self.assertEqual(sentinel.read_text(), "local work")

    def test_force_backs_up_customizations(self):
        self.run_installer("--skill", "game-audio-review")
        local = self.skills / "game-audio-review" / "local.txt"
        local.write_text("keep me", encoding="utf-8")
        self.run_installer("--skill", "game-audio-review", "--force")
        backups = list((self.skills.parent / ".ystack-backups").rglob("local.txt"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), "keep me")
        self.assertFalse(local.exists())

    def test_global_instructions_are_opt_in_and_backed_up(self):
        self.codex.mkdir()
        global_file = self.codex / "AGENTS.md"
        global_file.write_text("my existing rules", encoding="utf-8")
        self.run_installer("--skill", "confirm-task-understanding", "--agents", success=False)
        self.assertFalse(self.skills.exists())
        self.assertEqual(global_file.read_text(), "my existing rules")
        self.run_installer("--skill", "confirm-task-understanding", "--agents", "--force")
        self.assertEqual(global_file.read_bytes(), (ROOT / "AGENTS.md").read_bytes())
        self.assertEqual((self.codex / "T3_SETUP.md").read_bytes(), (ROOT / "T3_SETUP.md").read_bytes())
        maintenance = "YSTACK_MAINTENANCE.md"
        self.assertEqual((self.codex / maintenance).read_bytes(), (ROOT / maintenance).read_bytes())
        backups = list((self.codex / ".ystack-backups").rglob("AGENTS.md"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), "my existing rules")

    def test_unknown_skill_writes_nothing(self):
        self.run_installer("--skill", "nonexistent", success=False)
        self.assertEqual(list(self.base.iterdir()), [])

    def test_source_directory_cannot_be_install_target(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "install.py"),
             "--skills-dir", str(ROOT / "skills"), "--force"],
            text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("outside the Ystack source", result.stderr)


if __name__ == "__main__":
    unittest.main()

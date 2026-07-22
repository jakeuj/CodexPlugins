#!/usr/bin/env python3
"""Regression tests for package_skill.py using isolated temporary repositories."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


HELPER = Path(__file__).with_name("package_skill.py")


class PackageSkillTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="package-skill-test-")
        self.root = Path(self.temporary.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def run_helper(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(HELPER), *args],
            text=True,
            capture_output=True,
            check=False,
        )

    def make_skill(self, name: str = "demo-skill") -> Path:
        skill = self.root / "source" / name
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: Demo skill for packaging tests.\n---\n\n# Demo\n",
            encoding="utf-8",
        )
        scripts = skill / "scripts"
        scripts.mkdir()
        script = scripts / "run.py"
        script.write_text("#!/usr/bin/env python3\nprint('ok')\n", encoding="utf-8")
        script.chmod(0o755)
        (scripts / "ignored.pyc").write_bytes(b"cache")
        for cache_name in (".mypy_cache", ".pytest_cache", ".ruff_cache", "__pycache__"):
            cache = skill / cache_name
            cache.mkdir()
            (cache / "ignored.txt").write_text("cache", encoding="utf-8")
        return skill

    def make_plugin(self, name: str = "demo-plugin") -> Path:
        plugin = self.repo / "plugins" / name
        manifest_dir = plugin / ".codex-plugin"
        manifest_dir.mkdir(parents=True)
        (manifest_dir / "plugin.json").write_text(
            json.dumps(
                {
                    "name": name,
                    "description": "Demo plugin",
                    "keywords": ["demo"],
                    "interface": {"displayName": "Demo Plugin"},
                }
            ),
            encoding="utf-8",
        )
        return plugin

    def test_inventory_allows_missing_marketplace(self) -> None:
        result = self.run_helper("inventory", "--repo-root", str(self.repo))
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertFalse(payload["marketplace_exists"])
        self.assertIsNone(payload["marketplace_name"])
        self.assertEqual(payload["plugins"], [])

    def test_inventory_reports_invalid_marketplace_without_traceback(self) -> None:
        marketplace = self.repo / ".agents" / "plugins" / "marketplace.json"
        marketplace.parent.mkdir(parents=True)
        marketplace.write_bytes(b"\xff")

        result = self.run_helper("inventory", "--repo-root", str(self.repo))
        self.assertEqual(result.returncode, 3)
        payload = json.loads(result.stderr)
        self.assertEqual(payload["status"], "error")
        self.assertIn("not valid UTF-8", payload["message"])
        self.assertNotIn("Traceback", result.stderr)

    def test_inventory_reports_invalid_skill_without_traceback(self) -> None:
        skill = self.root / "source" / "invalid-skill"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_bytes(b"\xff")

        result = self.run_helper(
            "inventory", "--repo-root", str(self.repo), "--skill", str(skill)
        )
        self.assertEqual(result.returncode, 3)
        payload = json.loads(result.stderr)
        self.assertEqual(payload["status"], "error")
        self.assertIn("not valid UTF-8", payload["message"])
        self.assertNotIn("Traceback", result.stderr)

    def test_inventory_reports_source_bound_skill_paths(self) -> None:
        skill = self.make_skill()
        skill_md = skill / "SKILL.md"
        skill_md.write_text(
            skill_md.read_text(encoding="utf-8")
            + f"\nRun `python3 {skill}/scripts/run.py`.\n",
            encoding="utf-8",
        )

        result = self.run_helper(
            "inventory", "--repo-root", str(self.repo), "--skill", str(skill)
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        issues = json.loads(result.stdout)["source_skill"]["portability_issues"]
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]["path"], "SKILL.md")
        self.assertEqual(issues[0]["kind"], "source_skill_root")
        self.assertEqual(issues[0]["match"], str(skill))

    def test_inventory_reports_local_plugin_and_skips_escape(self) -> None:
        plugin = self.make_plugin()
        marketplace = self.repo / ".agents" / "plugins" / "marketplace.json"
        marketplace.parent.mkdir(parents=True)
        marketplace.write_text(
            json.dumps(
                {
                    "name": "test-marketplace",
                    "plugins": [
                        {
                            "name": plugin.name,
                            "source": {"source": "local", "path": f"./plugins/{plugin.name}"},
                            "category": "Productivity",
                        },
                        {
                            "name": "escape",
                            "source": {"source": "local", "path": "./../escape"},
                        },
                    ],
                }
            ),
            encoding="utf-8",
        )

        result = self.run_helper(
            "inventory",
            "--repo-root",
            str(self.repo),
            "--marketplace",
            str(marketplace),
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["marketplace_exists"])
        self.assertEqual([row["name"] for row in payload["plugins"]], [plugin.name])
        self.assertEqual(payload["skipped"][0]["name"], "escape")
        self.assertIn("escapes", payload["skipped"][0]["reason"])

    def test_copy_is_idempotent_and_rejects_content_conflicts(self) -> None:
        source = self.make_skill()
        plugin = self.make_plugin()

        copied = self.run_helper(
            "copy", "--source", str(source), "--plugin-root", str(plugin)
        )
        self.assertEqual(copied.returncode, 0, copied.stderr)
        self.assertEqual(json.loads(copied.stdout)["status"], "copied")
        destination = plugin / "skills" / "demo-skill"
        self.assertFalse((destination / "scripts" / "ignored.pyc").exists())
        for cache_name in (".mypy_cache", ".pytest_cache", ".ruff_cache", "__pycache__"):
            self.assertFalse((destination / cache_name).exists())

        unchanged = self.run_helper(
            "copy", "--source", str(source), "--plugin-root", str(plugin)
        )
        self.assertEqual(unchanged.returncode, 0, unchanged.stderr)
        self.assertEqual(json.loads(unchanged.stdout)["status"], "unchanged")

        (destination / "SKILL.md").write_text("different\n", encoding="utf-8")
        conflict = self.run_helper(
            "copy", "--source", str(source), "--plugin-root", str(plugin)
        )
        self.assertEqual(conflict.returncode, 3)
        self.assertEqual(json.loads(conflict.stderr)["status"], "error")

    @unittest.skipIf(os.name == "nt", "Windows does not preserve POSIX executable bits")
    def test_copy_detects_executable_mode_drift(self) -> None:
        source = self.make_skill()
        plugin = self.make_plugin()
        copied = self.run_helper(
            "copy", "--source", str(source), "--plugin-root", str(plugin)
        )
        self.assertEqual(copied.returncode, 0, copied.stderr)

        packaged_script = plugin / "skills" / "demo-skill" / "scripts" / "run.py"
        packaged_script.chmod(0o644)
        conflict = self.run_helper(
            "copy", "--source", str(source), "--plugin-root", str(plugin)
        )
        self.assertEqual(conflict.returncode, 3)
        self.assertIn("executable modes", json.loads(conflict.stderr)["message"])


if __name__ == "__main__":
    unittest.main()

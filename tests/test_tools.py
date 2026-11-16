"""End-to-end checks of the installed commands against throwaway git repos.

Run: python3 -m unittest discover -s tests
"""
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

TOOL = Path(__file__).resolve().parent.parent


def sh(cmd, cwd, env=None):
    return subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)


def git_repo(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    sh(["git", "init", "-q", "-b", "main"], root)
    sh(["git", "config", "user.email", "t@t"], root)
    sh(["git", "config", "user.name", "t"], root)
    return root


def commit(repo: Path, msg="c"):
    sh(["git", "add", "-A"], repo)
    sh(["git", "commit", "-q", "-m", msg], repo)


class Installed(unittest.TestCase):
    """The commands work when run through the links install.sh creates."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.home = self.tmp / "home"
        self.home.mkdir()
        env = dict(os.environ, HOME=str(self.home))
        r = sh([str(TOOL / "install.sh")], TOOL, env)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.bin = self.home / ".local" / "bin"

    def test_init_help_runs_through_link(self):
        r = sh([str(self.bin / "dotagents-init"), "--help"], self.tmp)
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_lint_checks_the_current_repo_not_the_tool(self):
        repo = git_repo(self.tmp / "svc")
        (repo / "AGENTS.md").write_text("See `internal/missing/thing.go`.\n")
        (repo / "internal").mkdir()
        (repo / "internal" / "real.go").write_text("package internal\n")
        commit(repo)
        r = sh([str(self.bin / "dotagents-lint")], repo)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("internal/missing/thing.go", r.stdout)


class Init(unittest.TestCase):
    def setUp(self):
        self.repo = git_repo(Path(tempfile.mkdtemp()) / "svc")

    def run_init(self):
        r = sh(["python3", str(TOOL / "dotagents" / "init.py"), str(self.repo)], self.repo)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_long_agents_md_is_never_overwritten(self):
        text = "".join(f"- rule {i}\n" for i in range(80))
        (self.repo / "AGENTS.md").write_text(text)
        self.run_init()
        self.assertEqual((self.repo / "AGENTS.md").read_text(), text)

    def test_missing_agents_md_is_created(self):
        self.run_init()
        self.assertIn("Context Routing", (self.repo / "AGENTS.md").read_text())

    def test_existing_trackers_stay_where_they_are(self):
        (self.repo / "trackers").mkdir()
        (self.repo / "trackers" / "payroll.md").write_text("x\n")
        self.run_init()
        self.assertTrue((self.repo / "trackers" / "payroll.md").exists())


class Lint(unittest.TestCase):
    def setUp(self):
        self.repo = git_repo(Path(tempfile.mkdtemp()) / "svc")

    def lint(self):
        return sh(["python3", str(TOOL / "dotagents" / "doc_lint.py")], self.repo)

    def test_retired_go_function_is_flagged(self):
        (self.repo / "svc.go").write_text("package svc\n\nfunc ComputeTDS() {}\n")
        commit(self.repo)
        (self.repo / "svc.go").write_text("package svc\n\nfunc ComputeTax() {}\n")
        (self.repo / "AGENTS.md").write_text("Tax runs in `ComputeTDS`.\n")
        commit(self.repo)
        r = self.lint()
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("retired-symbol", r.stdout)

    def test_retired_ts_component_is_flagged(self):
        (self.repo / "Page.tsx").write_text("export function OldGrid() { return null }\n")
        commit(self.repo)
        (self.repo / "Page.tsx").write_text("export function NewGrid() { return null }\n")
        (self.repo / "AGENTS.md").write_text("Use `OldGrid` for tables.\n")
        commit(self.repo)
        r = self.lint()
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("OldGrid", r.stdout)

    def test_live_go_symbol_and_path_pass(self):
        (self.repo / "internal").mkdir()
        (self.repo / "internal" / "svc.go").write_text("package internal\n\nfunc ComputeTax() {}\n")
        (self.repo / "AGENTS.md").write_text("Tax runs in `ComputeTax` (`internal/svc.go`).\n")
        commit(self.repo)
        r = self.lint()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()

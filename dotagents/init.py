#!/usr/bin/env python3
"""Initialize and enforce the Knit-style dotagents standard across repositories.

Usage:
    dotagents-init [path_or_repo]   # Initializes target repo (defaults to current dir)
    dotagents-init --all            # Initializes all sub-repos in the target directory
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

PKG_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = PKG_ROOT / "templates"


def read_template(relative_path: str) -> str:
    template_file = TEMPLATES_DIR / relative_path
    if template_file.exists():
        return template_file.read_text(encoding="utf-8")
    return ""


def init_repo(repo_path: Path, description: str = "", verification: str = "") -> None:
    repo_name = repo_path.name
    print(f"[*] Initializing dotagents in: {repo_name} ({repo_path})")

    agents_dir = repo_path / ".agents"
    rules_dir = agents_dir / "rules"
    context_dir = agents_dir / "context"
    memory_dir = agents_dir / "memory" / "decisions"
    trackers_active = repo_path / "trackers" / "active"
    trackers_archive = repo_path / "trackers" / "archive"

    for d in [rules_dir, context_dir, memory_dir, trackers_active, trackers_archive]:
        d.mkdir(parents=True, exist_ok=True)

    # Migrate existing flat trackers if present
    trackers_root = repo_path / "trackers"
    if trackers_root.is_dir():
        for item in trackers_root.iterdir():
            if item.is_file() and item.name.endswith(".md"):
                target = trackers_active / item.name
                if not target.exists():
                    shutil.move(str(item), str(target))
                    print(f"    Moved {item.name} -> trackers/active/")

    # Setup rules/coding.md
    coding_md = rules_dir / "coding.md"
    if not coding_md.exists():
        template = read_template("rules/coding.md")
        coding_md.write_text(template, encoding="utf-8")
        print("    Created .agents/rules/coding.md")

    # Setup context/architecture.md
    arch_md = context_dir / "architecture.md"
    if not arch_md.exists():
        desc = description or f"Primary responsibilities of {repo_name}."
        template = read_template("context/architecture.md")
        arch_md.write_text(template.format(description=desc), encoding="utf-8")
        print("    Created .agents/context/architecture.md")

    # Connect existing docs/agent-memory if present
    legacy_memory = repo_path / "docs" / "agent-memory"
    custom_routing = ""
    if legacy_memory.is_dir():
        custom_routing = "- **If consulting legacy agent-docs:** READ `docs/agent-memory/INDEX.md`.\n"
        print("    Preserved existing docs/agent-memory/ bridge.")

    # Setup decisions.md router
    decisions_router = agents_dir / "memory" / "decisions.md"
    if not decisions_router.exists():
        template = read_template("memory/decisions.md")
        decisions_router.write_text(template, encoding="utf-8")
        print("    Created .agents/memory/decisions.md")

    # Write slim AGENTS.md router
    agents_md = repo_path / "AGENTS.md"
    if not agents_md.exists() or len(agents_md.read_text(encoding="utf-8").splitlines()) > 60:
        desc = description or f"the {repo_name} service"
        verif = verification or "- Run repository test suite before commit."
        template = read_template("AGENTS.md")
        content = template.format(
            description=desc,
            custom_routing=custom_routing,
            verification_commands=verif
        )
        agents_md.write_text(content, encoding="utf-8")
        print(f"    Updated {agents_md.name} to slim router.")

    print(f"[✓] {repo_name} initialized successfully.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize Knit dotagents standard.")
    parser.add_argument("target", nargs="?", default=".", help="Repo name or directory path (defaults to current dir)")
    parser.add_argument("--all", action="store_true", help="Initialize all sub-repositories in the target directory")
    args = parser.parse_args()

    target_dir = Path(args.target).resolve()
    if not target_dir.is_dir():
        print(f"Error: directory not found: {target_dir}", file=sys.stderr)
        return 1

    known_repos = {
        "meizohrms": ("the React/TypeScript frontend for HRMS, ESS, and Operations", "npx tsc --noEmit -p tsconfig.app.json"),
        "hrms-payroll": ("the Go payroll calculation, tax deduction, and settlement service", "go test ./..."),
        "hrms-attendance": ("the Go attendance engine, punch aggregation, and overtime resolver", "go test ./..."),
        "hrms-employee": ("the Go employee master data, lifecycle, and onboarding service", "go test ./..."),
        "hrms-auth": ("the Go auth, token issuance, and RBAC service", "go test ./..."),
        "hrms-master": ("the Go company metadata, branches, departments master service", "go test ./..."),
        "hrms-leave": ("the Go leave policies, allocation, and approval service", "go test ./..."),
    }

    if args.all:
        subdirs = [p for p in target_dir.iterdir() if p.is_dir() and not p.name.startswith(".")]
        for p in sorted(subdirs):
            if (p / ".git").is_dir() or p.name in known_repos:
                meta = known_repos.get(p.name, (f"the {p.name} component", "- Run tests."))
                init_repo(p, description=meta[0], verification=meta[1])
        return 0

    meta = known_repos.get(target_dir.name, (f"the {target_dir.name} component", "- Run tests."))
    init_repo(target_dir, description=meta[0], verification=meta[1])
    return 0


if __name__ == "__main__":
    sys.exit(main())

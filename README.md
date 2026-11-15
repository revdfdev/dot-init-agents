# dot-init-agents

A lightweight, zero-overhead toolkit to scaffold, lint, and manage the **dotagents standard** (slim `AGENTS.md` router + `.agents/` context library + ADRs + task trackers) across any software repository.

- **Zero dependencies**: 100% Python 3 standard library and POSIX shell.
- **Zero background daemons**: 0 MB RAM, 0% CPU/GPU overhead.
- **Preserves existing context**: Bridges seamlessly into existing `docs/agent-memory/` and `trackers/`.

---

## What It Installs

| CLI Command | Purpose |
| :--- | :--- |
| **`dotagents-init`** | Initializes the slim `AGENTS.md` router, `.agents/` directory (`rules/`, `context/`, `memory/`), and `trackers/` (`active/`, `archive/`). |
| **`dotagents-adr`** | Mints immutable, collision-free Architecture Decision Records (`dotagents-adr new "<Title>"`) and auto-generates `decisions.md`. |
| **`dotagents-lint`** | Instant static doc-linter (<0.1s) checking that docs never point to deleted code symbols, dead file paths, or missing ADRs. |

---

## Installation

```bash
git clone git@github.com:revdfdev/dot-init-agents.git ~/.local/share/dot-init-agents
cd ~/.local/share/dot-init-agents
./install.sh
```

Ensure `~/.local/bin` is in your `$PATH`:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

---

## Usage

### 1. Initialize a Repository
Run inside any repo:
```bash
cd ~/code/my-service
dotagents-init
```

Or initialize all sub-repos in a monorepo or workspace directory:
```bash
cd ~/code/hrms-project
dotagents-init --all
```

### 2. Mint Architecture Decisions
```bash
# Mint a new decision
dotagents-adr new "Use PostgreSQL over MongoDB for Settlements" --topics "db,settlements"

# Re-index decisions table
dotagents-adr index
```

### 3. Verify Docs Don't Rot
```bash
dotagents-lint
```

---

## Directory Structure Created in Projects

```
<project-root>/
├── AGENTS.md                  # Slim router (<50 lines): points to deeper context
├── .agents/
│   ├── rules/
│   │   └── coding.md          # Hard invariants and commit rules
│   ├── context/
│   │   └── architecture.md    # Service boundaries, exposed endpoints, and dependencies
│   └── memory/
│       ├── decisions.md       # Auto-generated decisions table
│       └── decisions/         # Individual immutable ADR markdown files
└── trackers/
    ├── active/                # In-flight task/feature trackers
    └── archive/               # Completed tasks with verification proof
```

---

## License

MIT

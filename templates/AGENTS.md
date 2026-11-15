# AGENTS.md

## Identity & Boundaries
Owns {description}.

## Context Routing
- **Before writing code or running verification:** OBEY `.agents/rules/coding.md`.
- **If checking service architecture & API contracts:** READ `.agents/context/architecture.md`.
- **If making or reviewing architectural choices:** CONSULT `.agents/memory/decisions.md`.
- **If working on active features or fixes:** CHECK `trackers/active/`.
{custom_routing}
## Verification Commands
{verification_commands}

## Maintenance Invariant
This file is a router, not a dump. Invariants go into `.agents/rules/`, architecture contracts into `.agents/context/`, durable decisions into `.agents/memory/decisions/`, and task progress into `trackers/active/`. Run `dotagents-lint` before finishing tasks.

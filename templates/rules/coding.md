# Coding & Operational Rules

## Invariants
1. Verification gates are mandatory before declaring any task complete.
2. Never suppress TypeScript, Go, or compiler errors with unchecked casts or ignore flags.
3. Keep errors actionable: show structured errors or domain codes, never empty toasts.
4. Do not introduce background daemons, heavy vector stores, or local LLM runtimes into this repository.

## Commit Invariant
Any change to a public API endpoint, event schema, or database schema must update `.agents/context/architecture.md` and the active tracker in `trackers/active/` within the same commit.

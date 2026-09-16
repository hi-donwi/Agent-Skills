---
name: documentation-and-adrs
description: Records decisions and documentation. Use when making architectural decisions, changing public APIs, shipping features, or when you need to record context that future engineers and agents will need to understand the codebase. Do not use for changelog generation (changelog-generator) or writing a spec before a feature exists (spec-driven-development).
metadata:
  pack: core
---

# Documentation and ADRs

## Overview

Document decisions, not just code. The most valuable documentation captures the *why* — the context, constraints, and trade-offs that led to a decision. Code shows *what* was built; documentation explains *why it was built this way* and *what alternatives were considered*. This context is essential for future humans and agents working in the codebase.

## When to use
- Making a significant architectural decision
- Choosing between competing approaches
- Adding or changing a public API
- Shipping a feature that changes user-facing behavior
- Onboarding new team members (or agents) to the project
- When you find yourself explaining the same thing repeatedly

Do not document obvious code, restate what the code already says, or write docs for throwaway prototypes. Release notes belong in `changelog-generator`. A spec that does not exist yet belongs in `spec-driven-development`.

## Process
1. **Write an ADR for expensive-to-reverse decisions** — framework, data model, auth strategy, API shape, infrastructure. Store them in `docs/decisions/` with sequential numbers. Never delete an old ADR; supersede it.
2. **Comment the why, not the what.** Delete commented-out code (git has history). Do not leave TODOs you could just do.
3. **Document public APIs** with types or OpenAPI, not prose that drifts. Prefer inline types for libraries; commit the OpenAPI spec for HTTP.
4. **Keep the README runnable** — one-paragraph purpose, quick start, commands, architecture pointer to ADRs.
5. **Keep agent context current** — CLAUDE.md / rules, specs, ADRs, and inline gotchas prevent re-deciding.

Templates, comment examples, README and changelog shapes: `references/adr-and-docs.md`.

## Red flags
- Architectural decisions with no written rationale
- Public APIs with no documentation or types
- README that doesn't explain how to run the project
- Commented-out code instead of deletion
- TODO comments that have been there for weeks
- No ADRs in a project with significant architectural choices
- Documentation that restates the code instead of explaining intent

## Verification

After documenting:

- [ ] ADRs exist for all significant architectural decisions
- [ ] README covers quick start, commands, and architecture overview
- [ ] API functions have parameter and return type documentation
- [ ] Known gotchas are documented inline where they matter
- [ ] No commented-out code remains
- [ ] Rules files (CLAUDE.md etc.) are current and accurate

## References
- `references/adr-and-docs.md` — ADR template, comment rules, API/README/changelog examples

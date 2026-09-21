---
name: source-driven-development
description: Grounds every implementation decision in official documentation. Use when you want authoritative, source-cited code free from outdated patterns. Use when building with any framework or library where correctness matters. Do not use for typos, file moves, or logic that does not depend on a third-party API or framework version.
metadata:
  pack: core
---

# Source-Driven Development

## Overview

Every framework-specific code decision must be backed by official documentation. Don't implement from memory — verify, cite, and let the user see your sources. Training data goes stale, APIs get deprecated, best practices evolve. This skill ensures the user gets code they can trust because every pattern traces back to an authoritative source they can check.

## When to use
- The user wants code that follows current best practices for a given framework
- Building boilerplate, starter code, or patterns that will be copied across a project
- The user explicitly asks for documented, verified, or "correct" implementation
- Implementing features where the framework's recommended approach matters (forms, routing, data fetching, state management, auth)
- Reviewing or improving code that uses framework-specific patterns
- Any time you are about to write framework-specific code from memory

Do not use when correctness does not depend on a specific version, for pure logic that is version-agnostic, or when the user explicitly wants speed over verification.

## Process

```
DETECT ──→ FETCH ──→ IMPLEMENT ──→ CITE
```

1. **Detect stack and versions** from the project's dependency file. If versions are missing, ask — do not guess.
2. **Fetch the specific official page** for the feature (not the homepage). Authority: official docs → official blog/changelog → web standards → compatibility tables. Never cite Stack Overflow, blogs, or training data as primary.
3. **Implement the documented pattern.** If docs conflict with existing project code, surface the conflict; do not silently pick.
4. **Cite full URLs** in comments and conversation. If you cannot find docs, flag the pattern as unverified.

Source hierarchy, conflict prompt, and citation rules: `references/cite-official-docs.md`.

## Red flags
- Writing framework-specific code without checking the docs for that version
- Using "I believe" or "I think" about an API instead of citing the source
- Implementing a pattern without knowing which version it applies to
- Citing Stack Overflow or blog posts instead of official documentation
- Using deprecated APIs because they appear in training data
- Not reading `package.json` / dependency files before implementing
- Delivering code without source citations for framework-specific decisions
- Fetching an entire docs site when only one page is relevant

## Verification

After implementing with source-driven development:

- [ ] Framework and library versions were identified from the dependency file
- [ ] Official documentation was fetched for framework-specific patterns
- [ ] All sources are official documentation, not blog posts or training data
- [ ] Code follows the patterns shown in the current version's documentation
- [ ] Non-trivial decisions include source citations with full URLs
- [ ] No deprecated APIs are used (checked against migration guides)
- [ ] Conflicts between docs and existing code were surfaced to the user
- [ ] Anything that could not be verified is explicitly flagged as unverified

## References
- `references/cite-official-docs.md` — stack detection, source hierarchy, conflict and citation examples

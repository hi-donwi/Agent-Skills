---
name: code-review
pack: core
description: >-
  Review a diff or PR across correctness, design, tests, security, and clarity,
  and give actionable, prioritized feedback. Use when asked to review code, before
  merging a change, or to self-review a diff. Do not use to author large new
  features from scratch (use the build skills) — this reviews existing changes.
---

# Code Review & Quality

Evaluate a change against multiple axes and return specific, prioritized, actionable feedback.

## When to use
- Reviewing a PR or working-tree diff before merge.
- Self-reviewing your own change before pushing.

## Process
1. **Understand intent** — read the spec/PR description; review the diff against its stated goal.
2. **Review five axes:**
   - **Correctness** — logic, edge cases, error handling, concurrency.
   - **Design** — fits existing patterns; right abstraction; no needless coupling.
   - **Tests** — meaningful coverage for the change and its edge cases.
   - **Security** — input validation, authz, secrets, injection (defer deep checks to
     `security-hardening`).
   - **Clarity** — names, readability, comments where non-obvious; matches surrounding style.
3. **Prioritize** findings: blocking → should-fix → nit. Be specific and cite `file:line`.
4. **Size check** — flag changes too large to review well; suggest splitting.
5. **Prefer concrete suggestions** over vague critique.

## Architecture review (reusability standards)
The workspace defines four classifications for reusable code (see `AGENTS.md` →
_Architecture Conventions_). During review, flag violations:

| Violation | Should Be |
|---|---|
| Business logic inside a UI component | Extracted to a Service or Hook |
| Duplicated state/effect logic across components | Extracted to a Custom Hook |
| Inline API calls in page or component files | Delegated to a Service |
| Framework-specific code mixed with pure logic | Separated into a framework-independent Utility |
| Reusable workflow embedded in a page file | Moved to a Service or Hook |

## Red flags (in the change)
- New dependencies without justification; reinventing existing utilities.
- Untested behavior changes; broad refactors mixed with logic changes.
- Swallowed errors, `any`/weak typing, copy-paste duplication.
- Architecture violations from the reusability standards checklist above.

## Verification
- Every blocking finding cites a location and a concrete fix.
- Feedback is prioritized; nits are labeled as nits.

## Reference Index
- `references/expanded-guidance.md` — deeper review rubric, structural remedies, sizing guidance, and quality gates.

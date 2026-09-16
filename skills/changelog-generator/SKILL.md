---
name: changelog-generator
description: >-
  Generate user-facing changelogs, release notes, upgrade notes, and internal
  change summaries from git history, PRs, issues, commits, or diff context. Use
  before releases or stakeholder updates. Do not use for code review, version
  control operations, or marketing copy unrelated to actual changes shipped.
metadata:
  pack: core
---

# Changelog Generator

## Overview

Translate technical change history into accurate, useful release communication.

## When to Use

- Preparing release notes, changelog entries, upgrade notes, or stakeholder
  change summaries.
- Summarizing a range of commits, PRs, issues, or a local diff.
- Turning implementation details into user impact.

## Process

1. **Define audience and range.** User-facing, developer-facing, internal, or
   support; specify tag/commit/date/PR range when possible.
2. **Collect source changes.** Use git log/diff, merged PRs, issue links, and
   migration notes. Do not rely on commit messages alone if diffs are available.
3. **Group by impact.** Added, Changed, Fixed, Deprecated, Removed, Security,
   Performance, Docs, and Internal when useful.
4. **Write from user outcome.** Prefer "Users can now..." over implementation
   internals. Keep internal-only changes out of public notes.
5. **Call out action required.** Include migrations, config changes, breaking
   changes, known issues, and rollback notes.
6. **Verify facts.** Match every claim to a commit, PR, issue, or diff.

## Red Flags

- Promising benefits not visible in the change history.
- Leaking internal tickets, secrets, customer names, or security details.
- Hiding breaking changes under vague wording.
- Listing raw commit messages as release notes.

## Verification

- Every public claim maps to source evidence.
- Breaking changes and migration steps are explicit.
- Internal-only and security-sensitive details are removed or sanitized.

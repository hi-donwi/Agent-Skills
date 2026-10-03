---
name: data-import-export
description: >-
  Build validated data imports and interoperable exports with staging, dry runs, mapping, row errors, resumability, and reconciliation. Use for data exchange semantics, not Flyway schema migrations or Java-specific streaming report implementation.
metadata:
  pack: core
  keywords: data import, data export, csv, staging, dry-run, mapping, row error, resumable batch, external id, leading zero, decimal precision, formula injection
---

# Data Import and Export

## Overview
Make data exchange typed, scoped, repeatable, and recoverable. A successfully
parsed file is not necessarily valid or authorized business data.

## When to use
- Ingesting CSV/spreadsheet or partner records and mapping external identifiers.
- Exporting round-trippable data and reconciling resumable import jobs.

## Hand off when
| Need | Skill |
|---|---|
| Java streaming XLSX/PDF and reporting scale | `bulk-reporting-export` |
| Quarkus schema changes and Flyway migrations | `quarkus-persistence` |
| Durable job scheduling and worker recovery | `background-jobs` |

## Process
1. Define file/schema version, encoding, delimiter, locale, null representation,
   identifiers, currency/unit precision, dates/timezones, limits, and authoritative mapping.
2. Authenticate scope and validate file type, size, parser limits, and storage policy.
   Keep real documents and dumps in authorized product/local storage, never public skills.
3. Stage immutable source rows with row IDs and mapping version. Preserve identifiers
   as strings, exact amounts, and original values; never guess ambiguous locale or dates.
4. Resolve external IDs and all references within authorized tenant/company scope.
   Apply domain services and approval/posting rules rather than bypassing them with bulk SQL.
5. Provide a dry-run plan with counts, sanitized row errors, duplicate/conflict policy,
   and expected effects. Revalidate mutable constraints at commit; dry run reserves nothing.
6. Declare atomic-file or partial-batch semantics. Commit checkpoints with stable row/effect
   keys; retries must not duplicate posted journals, stock movements, members, or payments.
7. Scope export queries and downloads, apply consistent snapshot policy and bounded
   streaming/jobs, and neutralize spreadsheet-executable text cells without corrupting types.
8. Reconcile attempted, accepted, rejected, skipped, and committed rows plus relevant
   quantity/value totals. Test crash/resume, locale, leading zeros, formulas, and foreign scope.

## Red flags
- Direct imports into posted tables, silent coercion, or dry runs with external effects.
- Retrying whole files without operation identity or exporting unrestricted customer data.
- Formula escaping that changes canonical amounts or leaves dangerous text executable.

## Verification
- Round trips preserve approved types, precision, identifiers, and scope.
- Dry runs are side-effect free; commit-time checks and resumability remain correct.
- Row counts, business totals, parser limits, formula safety, and download access are tested.

## References
- `references/exchange-contract.md` - typed exchange and failure exercises.

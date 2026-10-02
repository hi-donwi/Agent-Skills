---
name: bulk-reporting-export
description: >-
  Build memory-safe reporting and export endpoints: streaming XLSX (POI SXSSF), PDF, database-side aggregation, async jobs with 202, and spool cleanup.
metadata:
  pack: java
  keywords: export, report, reporting, xlsx, excel, pdf, zip, poi, sxssf, streaming, memory, oom, out of memory, async job, sse, progress, download, spool, aggregate, summary
---

# Bulk Reporting & Export

## Overview

Reporting is usually where memory and latency problems appear first, because it is the
place that touches whole datasets rather than one page.

## When to use
- Building any endpoint in the `reporting` module
- An export is slow or throws `OutOfMemoryError`
- A report will exceed a few thousand rows
- Adding progress reporting to a long-running job

## Hand off when
| Need | Skill |
|---|---|
| Ordinary paginated list | `rest-api-contract` |
| Query and index tuning | `quarkus-persistence` |
| Who may download what | `quarkus-security` |
| Export duration metrics | `quarkus-observability` |

---

## Process

1. **Never hold a full result set in memory** — not in a `List`, not in a DTO collection,
   not in an in-memory workbook. The demo works because 300 rows fit anywhere; the same
   code meets 100,000 rows of real data in production and throws `OutOfMemoryError`.
2. **Stream out of the database and into the file.** A scrolled/streamed query with a JDBC
   fetch size, feeding `SXSSFWorkbook` with a bounded row window. Call `wb.dispose()`, or
   the temporary files it wrote stay on the spool volume.
3. **Aggregate in the database, not in Java.** Sums, counts and group-bys belong in SQL.
4. **Decide synchronous or asynchronous by size**, then keep to the targets below.
5. **Put job state somewhere that survives a restart**, and make a duplicate submit
   idempotent — users click twice.
6. **Authorise at download time** on owner or unit, not on role alone. The file already
   exists by then; the request that fetches it is the last check there is.
7. **Give the spool a retention job.** Storage with no expiry grows until it stops the
   service.

| Report size | Shape and target |
|---|---|
| < 1,000 rows | Synchronous, < 2 s |
| 1,000-10,000 rows | Synchronous, < 10 s |
| 10,000-100,000 rows | Async, < 60 s |
| > 100,000 rows | Async, chunked, with progress |

Heap stays under 1 GB regardless of report size. If it does not, something is still being
buffered.

## Verification
- Heap stays bounded as row count grows (stream, do not buffer)
- Jobs survive restart (state not only in memory)
- Downloads check owner/unit, not just role
- Duplicate submit is idempotent

## Red flags

| Pitfall | Symptom |
|---|---|
| `XSSFWorkbook` instead of `SXSSF` | `OutOfMemoryError` at ~50k rows |
| Missing `wb.dispose()` | Spool disk fills up over weeks |
| No JDBC fetch size | The driver buffers the whole result anyway |
| Job state in memory | Jobs lost on deploy; broken behind a load balancer |
| Synchronous long export | Thread pool exhausted; unrelated endpoints time out |
| Aggregating in Java | Slow report, high memory, needless database load |
| No retention job | Storage grows without limit |
| No idempotency | Duplicate jobs when users click twice |
| Download without an ownership check | Cross-unit data exposure |

## References
- `references/streaming-and-formats.md` - streaming a query into XLSX, PDF and ZIP; database-side aggregation
- `references/async-jobs.md` - when to go async, the job record, SSE progress, idempotency
- `references/spool-and-access.md` - spool storage and cleanup, download authorisation, performance targets

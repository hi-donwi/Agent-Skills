# Asynchronous jobs

Load when the export is too slow to answer inside the request: choosing async, the job
record, progress over SSE, and making a duplicate submit harmless.

## Synchronous or asynchronous?

```
Estimated duration < 10 s  -> synchronous, stream the response directly
Estimated duration > 10 s  -> async job: 202 + job ID, then poll or SSE
Unknown                    -> async. Guessing wrong costs a timeout in production.
```

A synchronous export holds an HTTP connection and a worker thread for its whole duration.
Twenty concurrent users exporting a large report will exhaust the pool and take down
endpoints that have nothing to do with reporting.

### Async job shape

```
POST /api/v1/reporting/transaction-summary/export
  -> 202 Accepted
     { "jobId": "...", "status": "QUEUED", "statusUrl": "...", "downloadUrl": null }

GET  /api/v1/reporting/exports/{jobId}          -> current status (polling)
GET  /api/v1/reporting/exports/{jobId}/events   -> SSE progress stream
GET  /api/v1/reporting/exports/{jobId}/download -> the file, once READY
```

Job states: `QUEUED` → `RUNNING` → `READY` | `FAILED` | `EXPIRED`.

**Job state belongs in the database, not in a `ConcurrentHashMap`.** An in-memory job store
loses every running job on deploy and cannot be read by a second instance — the same defect
as in-memory sessions, in a place where the user has already waited two minutes.

```sql
CREATE TABLE export_job (
    id            UUID PRIMARY KEY,
    requested_by  VARCHAR(100) NOT NULL,
    report_type   VARCHAR(50)  NOT NULL,
    parameters    JSONB        NOT NULL,
    status        VARCHAR(20)  NOT NULL,
    progress_pct  SMALLINT     NOT NULL DEFAULT 0,
    row_count     BIGINT,
    object_key    VARCHAR(500),
    error_code    VARCHAR(50),
    created_at    TIMESTAMPTZ  NOT NULL DEFAULT now(),
    expires_at    TIMESTAMPTZ  NOT NULL,
    CONSTRAINT ck_export_job_status
        CHECK (status IN ('QUEUED','RUNNING','READY','FAILED','EXPIRED'))
);
```

### Progress via SSE

```java
@GET
@Path("/{jobId}/events")
@Produces(MediaType.SERVER_SENT_EVENTS)
@RolesAllowed({"COMMITTEE", "ADMIN", "AUDITOR"})
public Multi<ExportProgress> events(@PathParam("jobId") UUID jobId) {
    return jobService.progressStream(jobId);
}
```

SSE is the right fit here: one-directional server-to-client, works over plain HTTP, and
reconnects on its own. Do not reach for WebSockets for progress reporting — they add a
protocol to operate for something that only flows one way.

Always offer polling as well. Some corporate proxies buffer SSE into uselessness, and a
frontend needs a fallback.

## Idempotency

A user who does not see progress will click the button again. Without protection that
doubles the load at exactly the moment the system is already struggling.

- Deduplicate by `(user, reportType, parameterHash)` while a job is `QUEUED` or `RUNNING` —
  return the existing job ID instead of starting a second one.
- The download URL carries a single-use or short-lived token, and authorisation is
  re-checked at download time. A job ID is not an access grant.

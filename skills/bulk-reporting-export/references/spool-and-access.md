# Spool storage, download access, and targets

Load when deciding where the produced file lives, who may fetch it, and how long the whole
thing is allowed to take.

## Spool storage and cleanup

| Concern | Rule |
|---|---|
| Location | Object storage (MinIO/S3), not local disk — several instances must serve the same download |
| Temporary files | Under a configured `spoolDir`, cleaned up in a `finally` block |
| Retention | Exports expire (e.g. 7 days); a scheduled job deletes expired objects and rows |
| Disk alert | Spool volume above 80 % (see `quarkus-observability`) |

Cleanup is not optional. Export files are large and are generated continuously; without a
retention job the storage bill and the disk both grow without limit.

```java
@Scheduled(cron = "0 0 2 * * ?")
void purgeExpiredExports() { ... }
```

## Authorisation at download time

```java
@GET
@Path("/{jobId}/download")
@RolesAllowed({"COMMITTEE", "ADMIN", "AUDITOR"})
public Response download(@PathParam("jobId") UUID jobId, @Context SecurityIdentity identity) {
    var job = jobService.requireReadable(jobId, identity);   // owner or an authorised role
    return Response.ok(storage.stream(job.objectKey()))
            .header("Content-Disposition", "attachment; filename=\"" + job.fileName() + "\"")
            .build();
}
```

The role check alone is not enough: a committee member from another unit holds the same role
but must not download another unit's report. Ownership and unit scope are checked too.

## Performance targets

| Report size | Target |
|---|---|
| < 1,000 rows | Synchronous, < 2 s |
| 1,000–10,000 rows | Synchronous, < 10 s |
| 10,000–100,000 rows | Async, < 60 s |
| > 100,000 rows | Async, chunked, with progress |

Heap stays under 1 GB regardless of report size. If it does not, something is still being
buffered.

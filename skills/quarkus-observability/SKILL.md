---
name: quarkus-observability
description: >-
  Make a Quarkus service diagnosable in production: structured JSON logs, a correlation ID via
  MDC surfaced as traceId, Micrometer metrics for business events, OpenTelemetry tracing,
  correct health checks, and alert thresholds. Use when preparing a service for production,
  adding metrics, or diagnosing an issue that only appears in staging or production. Do not
  use for tests (quarkus-testing), local dev debugging, or export tuning (bulk-reporting-
  export).
metadata:
  pack: java
  keywords: log, logging, metric, trace, tracing, health, probe, alert, prometheus, micrometer, opentelemetry, correlation, requestid, observability, monitoring, mdc
---

# Quarkus Observability

## Overview

Full rules: `.agents/standards/java/observability.md`. This is how to install it.

When a user reports "the export failed" at 2 a.m., what determines time-to-fix is not
developer cleverness — it is whether there is a `traceId` to follow.

## When to use
- Preparing a new service for staging/production
- Adding metrics for business events
- An issue that only appears in staging or production
- Designing alerts
- Logs are not enough to follow a single request

---

## Process

Without it, finding one user's request across two services' logs is a blind text search.

```java
@Provider
public class RequestIdFilter implements ContainerRequestFilter, ContainerResponseFilter {

    public static final String HEADER = "X-Request-Id";

    @Override
    public void filter(ContainerRequestContext ctx) {
        String id = ctx.getHeaderString(HEADER);
        if (id == null || id.isBlank()) id = UUID.randomUUID().toString();
        MDC.put("requestId", id);
        ctx.setProperty("requestId", id);
    }

    @Override
    public void filter(ContainerRequestContext req, ContainerResponseContext res) {
        res.getHeaders().putSingle(HEADER, req.getProperty("requestId"));
        MDC.clear();       // required: threads are reused
    }
}
```

`MDC.clear()` in the response filter is not optional. The thread is reused by the next
request; an uncleared MDC makes request B's logs carry request A's `requestId` — a
misleading trail is worse than no trail.

The same ID appears in:
- every log line for that request
- the response header
- the `traceId` field of the error body (`rest-api-contract`)

Forward it to other services via the same header on the REST client.

## Red flags
- Logs without `traceId` / `requestId`
- Liveness probes that check the database
- Alerts on every exception instead of user-visible symptoms
- `System.out` or unstructured log lines in request paths

## Verification

- [ ] JSON logging enabled in non-dev profiles
- [ ] `X-Request-Id` accepted, generated, returned, in the MDC, and in the error `traceId`
- [ ] `MDC.clear()` in the response filter
- [ ] Readiness checks real dependencies; liveness does not
- [ ] Business metrics on critical paths (export, upload, login)
- [ ] No high-cardinality metric tags
- [ ] No sensitive data in logs
- [ ] `/q/*` not publicly exposed
- [ ] Alerts configured with the thresholds above

## References
- `references/signals.md` - structured logs, metrics, tracing
- `references/health-and-alerts.md` - health checks and alerting on user impact

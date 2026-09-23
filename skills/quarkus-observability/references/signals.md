# Logs, metrics, and traces

Load when adding instrumentation: what to emit, at what level, with which labels.

## Logs

```properties
%prod.quarkus.log.console.json=true
%prod.quarkus.log.level=INFO
%prod.quarkus.log.category."com.example.product".level=DEBUG
```

| Level | For |
|---|---|
| `ERROR` | A human must act. If nothing needs doing, it is not an error. |
| `WARN` | Self-recovering: a retry succeeded, a fallback was used |
| `INFO` | Business events: order submitted, export finished, login |
| `DEBUG` | Flow detail, per package |

Business events use structured fields:

```java
log.infof("order submitted id=%d unit=%s amount=%s", id, unit, amount);
```

**Do not log:** passwords, tokens, session IDs, uploaded document contents, confidential
prices, full tax ID.

A common mistake: `log.error` for a failed validation. Invalid user input is a normal
event — that is `DEBUG`, or not logged at all. If `ERROR` is used for normal things, the
error-rate alert becomes useless.

## Metrics

```xml
<dependency>
  <groupId>io.quarkus</groupId>
  <artifactId>quarkus-micrometer-registry-prometheus</artifactId>
</dependency>
```

The defaults already cover HTTP rate/latency, JVM, and connection pool. Add what answers
business questions:

```java
@Inject MeterRegistry registry;

var sample = Timer.start(registry);
// ... run the export
sample.stop(registry.timer("app.export.duration", "type", type, "format", "xlsx"));

registry.counter("app.export.failed", "cause", "timeout").increment();
```

| Metric | Answers |
|---|---|
| `app_export_duration_seconds` | Which export is slowing down |
| `app_export_failed_total` (tag: cause) | Whether failures are rising |
| `app_login_failed_total` | Brute-force signal |
| `app_order_submitted_total` | Real system load |

**Never** use high-cardinality values as tags — order ID, tax ID, user ID. Every unique
value creates a new time series; that is what exhausts Prometheus's memory. A safe tag has a
bounded, enumerable set of values: type, format, cause, status.

## Tracing

```properties
quarkus.otel.exporter.otlp.traces.endpoint=${OTLP_ENDPOINT}
%dev.quarkus.otel.enabled=false
```

Spans are automatic for inbound/outbound HTTP and JDBC. Add manual spans only around long
non-I/O operations (PDF generation, report aggregation) — that is where time disappears
without a trace.

# Health checks and alerts

Load when preparing a service for an orchestrator, or deciding what should wake someone up.

## Health checks

```java
@Readiness
@ApplicationScoped
public class StorageHealthCheck implements HealthCheck {
    @Inject ObjectStorage storage;

    @Override
    public HealthCheckResponse call() {
        try {
            storage.ping();
            return HealthCheckResponse.up("object-storage");
        } catch (Exception e) {
            return HealthCheckResponse.down("object-storage");
        }
    }
}
```

| Endpoint | Checks | Used by |
|---|---|---|
| `/q/health/live` | The process is alive. **Not** dependencies. | Restart policy |
| `/q/health/ready` | DB, storage, dependent services | Load balancer |
| `/q/health/started` | Startup finished | Startup probe |

**Liveness must not check the database.** If the DB is down, restarting every application
instance fixes nothing and destroys the capacity left to recover when the DB returns.

`/q/*` must not be exposed to the internet — restrict it at the reverse proxy.

## Alerts

On **symptoms users feel**, not causes.

| Alert | Threshold |
|---|---|
| 5xx error rate | > 1 % for 5 minutes |
| p95 read latency | > 1 s for 10 minutes |
| Export failures | > 5 % within 15 minutes |
| Readiness down | > 2 minutes |
| Connection pool | > 90 % for 5 minutes |
| Export spool disk | > 80 % |

An alert that fires often without requiring action gets ignored, and then the important one
gets ignored with it. If an alert requires no action three times in a row, raise its
threshold or delete it.

# Pipeline, environments, releases, deployment

Load when adding a CI stage, promoting between environments, cutting a release, or wiring probes.

## Pipeline

```
push / MR
  |- build       ./mvnw -B verify -DskipITs      (~2 min)
  |- format      ./mvnw spotless:check
  |- unit        ./mvnw test + JaCoCo gate
  |- integration ./mvnw verify -Pit              (Testcontainers, needs Docker)
  |- openapi     generate + diff vs docs/openapi/ -> fail on difference
  |- security    dependency-check + secret scan
  \- package     JAR + image (main only)
```

Nightly: OWASP database refresh, k6 load tests, dependency update report.

Rules:
- **A red job blocks the merge.** Not "we'll fix it after".
- Full pipeline under 10 minutes. Beyond that people find shortcuts around it.
- Cache `~/.m2`; use `-B` so logs stay readable.

### Verify Docker on the runner before Stage 2

Integration tests need Testcontainers, which needs Docker. Confirm the
CI runner permits it. If it does not, that changes the test strategy, and it must be
known before development starts, not discovered when assembling the integration environment.

---

## Environments

| Env | Source | Database | Deploy |
|---|---|---|---|
| `dev` | Local, Dev Services | Throwaway container | — |
| `test` | CI | Testcontainers | Automatic per MR |
| `staging` | `main` | Separate PostgreSQL | Automatic |
| `prod` | `v*` tag | Production PostgreSQL | **Manual approval** |

**The same artifact goes to staging and production.** Differences come only from environment
variables. If production rebuilds from source, what was tested in staging is not what
shipped.

## Releases

Semantic versioning, tagged `v1.4.0`:

- `MAJOR` — breaking API contract change
- `MINOR` — new endpoints or features, compatible
- `PATCH` — bug fixes

Changelog generated from Conventional Commits (`git-workflow`).

Release checklist:

- [ ] Pipeline green on `main`
- [ ] Migrations tested against a copy of production data
- [ ] OpenAPI spec regenerated and committed
- [ ] No CVSS ≥ 7 findings
- [ ] Previous artifact retained and redeployable
- [ ] Runbook updated if operational behaviour changed
- [ ] Rollback path confirmed (see below)

---

## Deployment

Two supported deploy shapes; pick the one the host already operates.

**systemd**:

```ini
[Unit]
Description=Application API
After=network.target postgresql.service

[Service]
User=app
ExecStart=/usr/bin/java -jar /opt/app/app-api.jar
EnvironmentFile=/etc/app/api.env     # chmod 600, root:app — secrets live here
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

**Container:**

```dockerfile
FROM registry.access.redhat.com/ubi9/openjdk-21-runtime:latest
COPY --chown=185 target/quarkus-app/lib/      /deployments/lib/
COPY --chown=185 target/quarkus-app/*.jar     /deployments/
COPY --chown=185 target/quarkus-app/app/      /deployments/app/
COPY --chown=185 target/quarkus-app/quarkus/  /deployments/quarkus/
EXPOSE 8080
USER 185
ENTRYPOINT ["java", "-jar", "/deployments/quarkus-run.jar"]
```

Copy the four `quarkus-app` directories separately so Docker layer caching works — the
`lib/` layer changes rarely, application code changes on every build.

Run as non-root. Secrets come from the environment or a secret manager, **never** baked into
an image — an image layer keeps them even after a later layer deletes the file.

### Probes

```
startupProbe    /q/health/started    generous timeout; JVM startup is not instant
livenessProbe   /q/health/live       process only, no dependency checks
readinessProbe  /q/health/ready      DB, storage, dependent services
```

A liveness probe that checks the database will restart every instance when the database has
a hiccup, turning a recoverable incident into an outage (`quarkus-observability`).

---

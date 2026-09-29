---
name: java-delivery
description: >-
  Build, ship, and operate the Quarkus backend: Maven Wrapper, enforcer, Spotless, JaCoCo and
  dependency-check gates, CI stages, environment promotion, semantic versioning, systemd and
  container deployment, secret delivery, health probes, and rollback. Use when setting up or
  fixing a build, adding a CI stage, releasing, deploying, or writing a runbook. Do not use
  for code-level security (quarkus-security) or telemetry design (quarkus-observability).
metadata:
  pack: java
  keywords: build, maven, mvnw, pom, ci, cd, pipeline, deploy, deployment, release, versioning, rollback, docker, container, systemd, artifact, staging, production, runbook, enforcer
---

# Java Delivery

## Overview

Full rules: `.agents/standards/java/build-ci.md`. This is the workflow.

## When to use
- Setting up or fixing the Maven build
- Adding or debugging a CI stage
- Preparing a release
- Deploying to staging or production
- Writing a runbook or planning a rollback

---

## Process

The wrapper is committed and is the only supported entry point:

```bash
./mvnw verify        # not: mvn verify
```

Developer machines and CI runners do not reliably have Maven, and when they do the versions
differ. On this machine, for example, Java 21 is present but `mvn` is not — the wrapper is
what makes the build work anyway.

## Verification
- [ ] Pipeline green on `main`
- [ ] `./mvnw verify` is the documented entry point
- [ ] Same artifact promoted from staging to production
- [ ] Previous artifact retained and redeployable
- [ ] Rollback path confirmed

## Red flags

| Pitfall | Consequence |
|---|---|
| `mvn` instead of `./mvnw` | Different Maven version, non-reproducible build |
| Unpinned dependency versions | Build output changes without a code change |
| Rebuilding for production | What shipped is not what was tested |
| Secrets in an image | Retained in layer history even after deletion |
| Liveness checking the DB | A database hiccup becomes a full outage |
| Dropping a column too early | Rollback impossible |
| No retained previous artifact | Rollback impossible |
| Pipeline over 10 minutes | People route around the gates |

## References
- `references/build.md` - parent POM essentials and the plugins that gate the build
- `references/pipeline-and-environments.md` - pipeline stages, environments, releases, deployment, probes
- `references/rollback.md` - rollback decision and runbook

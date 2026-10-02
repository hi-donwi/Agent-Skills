---
name: quarkus-service
description: >-
  Build or change Quarkus services and endpoints: Maven module structure, resource/service/repository layering, CDI and scopes, typed configuration, and REST clients.
metadata:
  pack: java
  keywords: endpoint, resource, service layer, module, cdi, inject, scope, configmapping, config, rest client, scaffold, quarkus, layering, arc, virtual thread
---

# Quarkus Service

## Overview

The parent skill for day-to-day backend work. The binding rules live in
`.agents/standards/java/project-layout.md` and `00-decisions.md`; this is the workflow.

## When to use
- Adding an endpoint to an existing module
- Creating a new Quarkus module
- Cleaning up code that mixes layers
- Moving scattered configuration to typed config
- Calling another service

## Hand off when
| Need | Skill |
|---|---|
| URL shape, status codes, error format | `rest-api-contract` |
| Entities, queries, migrations, transactions | `quarkus-persistence` |
| Roles, sessions, security validation | `quarkus-security` |
| Writing tests | `quarkus-testing` |
| Logs, metrics, traces | `quarkus-observability` |
| Large exports/reports | `bulk-reporting-export` |
| Domain business rules | the organisation's domain skill in `context/skills/` |

---

## Process

The order is deliberate: contract first, tests second, implementation last.

**1 — Settle the contract.** Path, method, request, response, errors, roles. If any of that
is unclear, do not start coding. Use `.agents/templates/endpoint-spec.md`.

**2 — Write failing tests.** An integration test for the HTTP shape, unit tests for the
business rules. They must fail because the endpoint does not exist yet — not because of a
typo.

**3 — DTOs.** `record`s in `dto/`, bean validation on the fields.

**4 — Repository**, if a new query is needed. A specific method, not `listAll()` filtered
in Java afterwards.

**5 — Service.** Business rules, the `@Transactional` boundary, domain exceptions.

**6 — Resource.** Thin: bind, delegate, return. Add the role and OpenAPI annotations.

**7 — Verify.** `./mvnw verify`, regenerate the OpenAPI spec, check the logs leak nothing.

## Verification
- [ ] Resource has no queries or business rules
- [ ] Response is a `record`, not an entity
- [ ] Config is `@ConfigMapping`, not `ConfigProvider.getConfig()`
- [ ] REST clients live in a `*Client` type
- [ ] Tests cover the service rule and the HTTP contract separately

## Red flags

- **`@Transactional` on a resource** — wraps JSON serialisation, holds the DB connection.
- **Entities as responses** — leaks internal columns, couples HTTP to the schema.
- **`Optional` as an entity field** — not serialisable, not its purpose.
- **Blocking calls on a reactive endpoint** — blocks the event loop; the whole instance
  stops serving. When in doubt, use imperative style (not `Uni`/`Multi`).
- **`@ApplicationScoped` with mutable fields** — a race condition under load.
- **Guessing Quarkus APIs** — the version moves fast. Verify against `quarkus.io/guides`
  for 3.33 instead of relying on recall.

## References
- `references/shape-and-cdi.md` - the correct class shape, CDI scopes, @ConfigMapping
- `references/clients-and-threads.md` - REST clients between services, virtual threads, lifting demo code

---
name: rest-api-contract
description: >-
  Design and review REST contracts: URL shape and HTTP method choice, status codes, uniform
  pagination and filtering, RFC 9457 problem+json errors with stable ErrorCodes, date/money/
  enum formats, OpenAPI annotations and the committed spec, versioning and breaking-change
  identification. Use when designing a new endpoint, aligning endpoints that have diverged,
  choosing a status code, shaping an error response, updating the OpenAPI spec, or judging
  whether a change is breaking. Do not use for internal implementation (quarkus-service),
  queries (quarkus-persistence), or roles and authorisation (quarkus-security).
metadata:
  pack: core
  keywords: api, contract, openapi, swagger, status code, pagination, paging, filter, error response, problem json, versioning, breaking change, dto, request, response
---

# REST API Contract

## Overview

Full rules: `.agents/standards/core/api-contract.md`. This is how to decide.

With a large API built by more than one developer in parallel, consistency is not
aesthetics — every divergent shape is one more adapter the frontend has to write.

## When to use
- Designing a new endpoint (before coding)
- Choosing a status code or response shape
- Introducing a new error
- Judging whether a change is breaking
- Reviewing the OpenAPI spec

Do not use for internal implementation (`quarkus-service`), queries (`quarkus-persistence`),
or roles and authorisation (`quarkus-security`).

## Process
1. **Fill in `.agents/templates/endpoint-spec.md` before writing code.**
2. **Pick method and status from the tables** in `references/contract-shapes.md`. No verbs in the path. Empty collections are still 200.
3. **Paginate every collection** with one shared page shape; cap `size` server-side; allowlist `sort`.
4. **Errors are RFC 9457** from a global mapper with a stable `ErrorCode`. Resources never build error JSON by hand.
5. **Money is a decimal string; timestamps are ISO-8601 UTC.** Annotate OpenAPI and commit the generated spec. Breaking changes need `/v2` plus an ADR.

## Red flags
- Verbs in the URL path
- Unpaginated collections
- Money as a JSON number
- Entities returned as JSON
- Errors constructed in a resource instead of the global mapper

## Verification

- [ ] Path: `/api/v1/<module>/<plural-kebab-case-resource>`
- [ ] No verbs in the path
- [ ] Method and status match the tables in `references/contract-shapes.md`
- [ ] Collections paginated with `PageResponse`
- [ ] `size` capped server-side
- [ ] Request and response are `record`s, not entities
- [ ] Bean Validation on all input
- [ ] Errors via the global mapper with a stable `ErrorCode`
- [ ] Money as a string, timestamps UTC ISO-8601
- [ ] `@Operation`, `@APIResponse`, `@Tag` complete
- [ ] Spec regenerated and committed
- [ ] If breaking: ADR plus a `/v2` plan

## References
- `references/contract-shapes.md` — methods, 4xx, pagination, errors, types, OpenAPI, breaking changes

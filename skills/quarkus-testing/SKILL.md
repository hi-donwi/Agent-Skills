---
name: quarkus-testing
description: >-
  Write tests for a Quarkus backend: fast unit tests without @QuarkusTest, integration tests
  with @QuarkusTest and Testcontainers PostgreSQL (not H2), RestAssured, authorisation tests,
  architecture tests, fixtures, JaCoCo coverage gates, and k6 load tests. Use when adding an
  endpoint or business rule, fixing a bug (failing test first), dealing with slow or flaky
  tests, setting up Testcontainers, or when coverage is below the gate. Do not use for
  diagnosing production issues (quarkus-observability) or non-test performance tuning
  (bulk-reporting-export).
metadata:
  pack: java
  keywords: test, testing, junit, mock, testcontainer, coverage, jacoco, assertion, restassured, flaky, fixture, quarkustest, integration test, unit test
---

# Quarkus Testing

## Overview

Full rules: `.agents/standards/java/testing.md`. This is how to write them.

With many endpoints and more than one developer in parallel, tests are the only way to know
module A still works after module B changed.

## When to use
- Adding an endpoint or business rule
- Fixing a bug — write the failing test first
- Tests are slow, flaky, or red for no clear reason
- Coverage is below the gate

---

## Process

```
Business rules, mappers, validators   -> unit, no @QuarkusTest        (< 10 ms)
Endpoints, serialisation, real DB     -> @QuarkusTest + Testcontainers (seconds)
Contract has not silently changed     -> OpenAPI spec diff in CI
Throughput and latency                -> k6, nightly
```

Default to unit tests. `@QuarkusTest` boots the whole CDI container — to test one service
method that is 100× slower for no added benefit.

## Red flags
- `@QuarkusTest` on a pure domain rule
- H2 instead of Testcontainers PostgreSQL
- Tests that pass only because they share mutated state
- No failing test before a bugfix

## Verification

```bash
./mvnw verify                 # unit + integration + JaCoCo gate
open target/site/jacoco/index.html
```

Thresholds: services ≥ 80 %, endpoints ≥ 60 %. Below that the build fails.

**Coverage is a floor, not a goal.** 80 % reached with `assertNotNull` is worth nothing. If
coverage is short, add tests for untested behaviour — do not add tests that call the code
without checking the result.

## Commands

```bash
./mvnw test                # unit, fast
./mvnw verify              # everything + coverage gate
./mvnw quarkus:test        # continuous testing during development
./mvnw test -Dtest=VendorServiceTest
```

## References
- `references/unit-and-integration.md` - unit tests, integration tests, real PostgreSQL over H2
- `references/coverage-and-fixtures.md` - tests that must exist, what needs none, fixtures
- `references/flaky-tests.md` - diagnosing a test that fails without a code change

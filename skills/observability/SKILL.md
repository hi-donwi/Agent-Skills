---
name: observability
description: >-
  Add or review production observability: structured logs, metrics, traces,
  dashboards, alerts, SLOs, incident signals, and telemetry hygiene. Use when
  shipping production code, diagnosing runtime behavior, or making systems
  operable. Do not use for local-only scripts or performance tuning without
  production telemetry.
metadata:
  pack: core
---

# Observability

## Overview

Make production behavior visible enough to debug without guesswork.

## When to use

- Shipping a new production service, job, feature flag, integration, or critical
  user flow.
- Investigating incidents, flaky jobs, slow endpoints, or hard-to-reproduce
  production behavior.
- Adding logs, metrics, traces, dashboards, alerts, or SLOs.

## Process

1. **Name the user/system journey.** What must be observable end to end?
2. **Add structured logs.** Include stable event names, request/job IDs,
   correlation IDs, safe dimensions, and outcome fields. Do not log secrets or
   unnecessary PII.
3. **Measure RED/USE signals.**
   - Request flows: rate, errors, duration.
   - Resources: utilization, saturation, errors.
4. **Trace boundaries.** Instrument external calls, queues, DB queries, retries,
   cache hits, and expensive work.
5. **Alert on symptoms.** Prefer user-impacting SLOs over noisy internal causes.
6. **Build dashboards for action.** Include current health, recent deploys,
   saturation, error top lists, and drill-down links.
7. **Verify in runtime.** Generate a test event and confirm logs, metrics, traces,
   and alerts appear with useful context.

## Red flags

- Logs that are free-form strings with no IDs or outcome fields.
- Alerts on every exception instead of user-impacting symptoms.
- Dashboards nobody uses during incidents.
- Telemetry that leaks secrets, tokens, emails, or raw payloads.
- Shipping production code with no way to know whether it works.

## Verification

- A real test event is visible in logs/metrics/traces.
- Dashboard or query answers "is it working?" and "where did it fail?"
- Alert thresholds are tied to user impact or SLOs.

## Reference Index

- `references/expanded-guidance.md` — deeper structured logging, metrics, tracing, dashboards, alerts, and incident instrumentation guidance.

---
name: product-analytics
description: >-
  Define behavioral event taxonomy, activation funnels, retention cohorts, and experiment metrics with privacy controls. Use to measure product outcomes, not operational tracing, financial records, or business audit trails.
metadata:
  pack: core
  keywords: product analytics, event taxonomy, activation, funnel, retention cohort, churn, conversion, behavioral event, denominator, experiment
---

# Product Analytics

## Overview
Measure a defined product decision with reproducible metrics and minimal data,
without installing a tracker or sending customer data as a side effect.

## When to use
- Designing activation, adoption, retention, churn, or conversion measurements.
- Defining event schemas and experiment exposure independently from infrastructure metrics.

## Hand off when
| Need | Skill |
|---|---|
| Logs, traces, alerts, and operational SLOs | `observability` |
| Attributable business mutation history | `audit-logging` |
| Cohort exposure and release toggles | `feature-flags` |

## Process
1. Name the decision, owner, population, metric numerator and denominator, window,
   timezone, exclusions, and guardrails. Distinguish user, member, and tenant metrics.
2. Define versioned events with stable event IDs, occurred and received times,
   source, pseudonymous subject, and an allowlisted property schema.
3. Use server-confirmed events for successful payments or committed business actions;
   use client events for interaction intent. Do not count clicks as successful outcomes.
4. Deduplicate retries, document late-arrival handling, and distinguish anonymous-to-user
   identity linking from joining users across tenants. Keep test/internal traffic separate.
5. Apply data minimization, consent and lawful-basis requirements, access controls,
   retention, and deletion policy before transmission. No secrets, free text, or raw PII.
6. Define cohort assignment and exposure events before experiments. Account for shared
   tenant users, sample-ratio mismatch, guardrails, and stopping criteria.
7. Verify with synthetic events and a known expected funnel. If no authorized analytics
   service exists, use a local event contract and fixture report; do not install one.

## Red flags
- Raw emails or customer records in third-party trackers or prompts.
- Changing denominators mid-experiment, counting retries, or mixing intent with success.
- Treating observational correlation as a causal experiment result.

## Verification
- Synthetic event replay produces stable deduplicated metrics and cohort assignment.
- Unconsented or disallowed properties are excluded before transmission.
- Late data, identity transitions, deletion, and excluded traffic have tested policies.

## References
- `references/event-contract.md` - event and metric contracts with a failure exercise.

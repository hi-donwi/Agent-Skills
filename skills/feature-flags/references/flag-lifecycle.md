# Feature Flag Taxonomy and Lifecycle Governance

## 1. Flag Archetypes

| Category | Typical Lifetime | Dynamic Rules | Target Audience | Primary Owner |
|---|---|---|---|---|
| **Release Toggle** | 1 – 4 weeks | Percentage rollout, tenant allowlist | Staging → Internal → 10% → 100% | Engineering |
| **Experiment (A/B)** | 2 – 8 weeks | Statistically randomized cohorts | 50/50 user split | Product / Growth |
| **Ops / Kill-Switch** | Permanent | Boolean on/off | Entire application or subsystem | Platform / SRE |
| **Commercial entitlement** | Not a release flag | Separate authoritative billing capability policy | Authorized paying tenants | Product / Billing |

## 2. The 4-Stage Lifecycle

```
[1. DRAFT] ──→ [2. PROGRESSIVE ROLLOUT] ──→ [3. GA (100%)] ──→ [4. RETIRED]
```

### Stage 1: Draft & In-Development
- Define a purpose-specific safe fallback, not a universal boolean default.
- Enabled only in local and development environments via user ID overrides.
- Unit and integration tests verify BOTH branches (`flag === true` and `flag === false`).

### Stage 2: Progressive Rollout
- Enabled for a verified internal tenant allowlist, not a client-controlled email domain.
- Canary rollout: 5% of tenants → 25% → 50%.
- Monitor error rates, latency (p95/p99), and customer support logs.

### Stage 3: General Availability (100%)
- Flag is flipped to 100% for all users.
- A calendar reminder or issue ticket is scheduled within 2 sprints to remove the flag.

### Stage 4: Retirement and Code Cleanup
- Delete the toggle check in code. Keep only the new implementation path.
- Remove old dead code, fallback mocks, and unused imports.
- Delete the flag definition only after no deployed or rollback version depends on it.

## 3. Flag Debt Prevention Rules

1. **Max Active Release Flags:** Set a team limit (e.g. max 5 active release flags per squad).
2. **TTL (Time to Live):** Any release flag older than 30 days is marked stale and prioritized for immediate removal in sprint planning.
3. **No Nested Flags:** Never check `flag_b` inside a conditional block governed by `flag_a`. If features depend on each other, combine them into a single milestone flag.

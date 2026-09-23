# Rollback

Load when a deploy has gone wrong, or when writing the runbook before it does.

## Rollback

Every release must be reversible before it is released.

**Application rollback:** redeploy the previous artifact. This only works if the previous
artifact still exists and if the database schema it expects is still valid.

**That is why migrations are backward-compatible by one release:**

```
Release N:    add the new column, write to both old and new, read from old
Release N+1:  read from the new column
Release N+2:  drop the old column
```

Dropping a column in the same release that stops using it means release N+1 cannot be rolled
back — the old code would query a column that no longer exists. Spreading it over three
releases costs almost nothing and keeps rollback available at every point.

**Database rollback is not a plan.** Restoring a production database loses every transaction
since the backup. Design so that the application can go back without the database having to.

### Rollback runbook

1. Confirm the symptom is caused by the release (check `traceId`s and metrics, not
   intuition).
2. Redeploy the previous tag.
3. Verify readiness and the error rate returning to baseline.
4. Only then investigate — with the system already stable.
5. Record what happened in `docs/adr/` if it changes a decision.

---

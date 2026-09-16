# Migration patterns

Load this when deciding, announcing, or executing a deprecation.

## Principles

**Code is a liability.** Every line needs tests, docs, patches, and mental overhead. When the same functionality can be provided with less code, the old code should go.

**Hyrum's Law.** With enough users, every observable behavior is depended on — including bugs. Deprecation needs active migration, not just an announcement.

**Plan removal at design time.** Clean interfaces, feature flags, and a small surface make later removal possible.

## The deprecation decision

```
1. Does this system still provide unique value?
   → If yes, maintain it. If no, proceed.

2. How many users/consumers depend on it?
   → Quantify the migration scope.

3. Does a replacement exist?
   → If no, build the replacement first.

4. What's the migration cost for each consumer?
   → If trivially automated, do it. If manual, weigh against maintenance cost.

5. What's the ongoing cost of NOT deprecating?
   → Security risk, engineer time, opportunity cost of complexity.
```

| Type | When | Mechanism |
|------|------|-----------|
| **Advisory** | Migration optional, old system stable | Warnings, docs, nudges |
| **Compulsory** | Security, blocked progress, unsustainable cost | Hard deadline, migration tooling |

**Default to advisory.** Compulsory requires tooling, documentation, and support — you can't just announce a date.

## Notice template

```markdown
## Deprecation Notice: OldService

**Status:** Deprecated as of 2026-03-01
**Replacement:** NewService (see migration guide below)
**Removal date:** Advisory — no hard deadline yet
**Reason:** OldService requires manual scaling and lacks observability.

### Migration Guide
1. Replace `import { client } from 'old-service'` with `import { client } from 'new-service'`
2. Update configuration
3. Run the migration verification script
```

**The Churn Rule:** If you own the infrastructure, you migrate your users — or ship a backward-compatible update that requires no migration.

## Incremental migrate, then remove

For each consumer: find touchpoints, switch, verify, drop old references, confirm no regressions.

Remove only after zero active usage (metrics, logs, dependency analysis). Then delete code, tests, docs, config, and the notices.

## Patterns

**Strangler:** run old and new in parallel; shift traffic 0% → canary → 50% → 100% → remove.

**Adapter:** old interface, new implementation, so consumers keep compiling while the backend moves.

```typescript
class LegacyTaskService implements OldTaskAPI {
  constructor(private newService: NewTaskService) {}

  getTask(id: number): OldTask {
    const task = this.newService.findById(String(id));
    return this.toOldFormat(task);
  }
}
```

**Feature flag:** switch consumers one at a time.

## Zombie code

Nobody owns it, everybody depends on it: no commits in 6+ months with active consumers, no maintainer, failing tests, known-vulnerable dependencies, docs that reference gone systems.

**Response:** assign an owner or deprecate with a concrete plan. Zombie code cannot stay in limbo.

## Common rationalizations

| Rationalization | Reality |
|---|---|
| "It still works, why remove it?" | Unmaintained working code accumulates security debt. |
| "Someone might need it later" | Rebuild if needed. Keeping unused code costs more. |
| "The migration is too expensive" | Compare to 2–3 years of maintenance. |
| "We'll deprecate it after we finish the new system" | Plan now. Priorities will have moved by then. |
| "Users will migrate on their own" | They won't. Tool, document, or do it yourself. |
| "We can maintain both systems indefinitely" | Double the maintenance, tests, docs, and onboarding. |

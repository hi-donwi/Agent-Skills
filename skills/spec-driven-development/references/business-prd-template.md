# Business Application PRD Template

Use only the sections relevant to the requested feature. Extend an existing approved
spec rather than creating a competing contract. Mark unresolved policy as an open
question; do not assume tax, billing grace, eligibility, or retention rules.

## Objective and boundaries

State the user problem, measurable outcome, actors, explicit non-goals, current
behavior, and proposed change. Identify the owning module and existing source of truth.
Record assumptions and which unresolved decisions block implementation.

## Scope and access

Distinguish identity, tenant, legal entity, branch, program membership, role, and
commercial subscription. Define actor/resource/action permissions, external identities,
support administration, revocation latency, and allowed cross-entity operations.

## Lifecycle and facts

List entities and document states, effective dates/timezone, valid transitions,
protected revisions, approvals, side effects, idempotency keys, and correction paths.
Separate mutable drafts from issued/posted facts and authoritative provider state.

| Relevant area | Required policy |
|---|---|
| Tenancy | Isolation model, trusted context, global data, scoped references |
| Organization lifecycle | Provisioning steps, activation, suspension, recovery, deletion |
| Membership | Invitation scope, eligibility, expiry, renewal, last-owner protection |
| Billing | Currency/price version, trials, seats, quota, dunning, cancellation, refunds |
| Accounting | Balanced posting, functional currency, fiscal locks, reversals, reconciliation |
| Inventory | Exact units, reservations, negative stock, lots/serials, transfer/count policy |
| Purchasing/sales | Cumulative quantities, matching, credit control, partial actions, returns |
| Approval | Policy/revision, eligible actors, independence, quorum, delegation |
| Integrations | Authentication, endpoint safety, durable capture, retries, reconciliation |
| Data exchange | Schema/mapping version, precision, dry run, row errors, resume policy |

## Contracts and failure behavior

Specify API/event/file contracts, validation, stable errors, uniqueness constraints,
transaction boundaries, worker authority, timeouts, retry budgets, and external effect
recovery. Describe what users see during pending, denied, conflicted, and failed states.

## Data and operations

Define audit fields and redaction, lawful data handling, authorized destinations,
retention/holds, deletion manifests, backup/restore objectives, rollout and rollback,
operational metrics, and business reconciliation. Keep real customer data out of examples.

## Acceptance criteria

Express observable decisions, not only happy-path screen appearance:
- A forged scope or stale member cannot read, mutate, export, or trigger queued work.
- Repeating a request or delivery produces one logical business effect.
- Competing operations preserve quota, stock, credit, balance, owner, and approval invariants.
- A failed transaction or crashed worker is recoverable without silently losing work.
- Date boundaries, exact amounts, and historical snapshots follow declared policy.
- Correction, cancellation, deletion, and restore paths preserve the contract.

Include executable verification commands, fixtures, migration strategy, rollout gates,
and unresolved decisions with owners. Do not claim security or provider behavior from
a mocked happy path alone.

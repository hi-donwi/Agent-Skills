# Critical Business Behavior Evaluation Protocol

## Four evidence levels

| Level | Observed evidence | Does not establish |
|---|---|---|
| Structural/routing | Metadata, resource checks, retrieval results, entry-point budgets | Useful model decisions or correct application behavior |
| Model decision | Actual selected workflow, proposed actions, unresolved policy, tool trace | Execution of a proposed action or enforced sandbox boundaries |
| Generated artifact execution | Reviewed model-produced code run against held-out checks | Database isolation, live provider correctness, or production compliance |
| Application integration | Authorized real-stack tests with controlled data and failure injection | Universal safety beyond the tested environment and contracts |

Do not add these categories together as a single success score. A passing decision
description and a passing runtime invariant are different outcomes.

## Inputs and scoring

1. Select specific skills and hash their entry points and consumed references.
   Declare the contract, sample size, model/runtime, allowed input files, operations,
   destinations, and authorized output directory before evaluation.
2. Give the evaluator only the request, candidate instructions, necessary artifacts,
   and explicit callable/data contracts. Keep expected checks and prior results separate.
   Never send real customer data, credentials, or unrelated project context.
3. Use exact reads for a closed input set. If a tool surfaces extra material, record
   the incident and preserve the result as contaminated; repeat in a fresh context.
   An allowlist stated in a prompt is not a technically enforced sandbox.
4. Require concrete artifacts plus a complete action log. Review generated imports
   and effects before executing code; use the available authorized isolation controls.
   Without enforced isolation, disclose the limit and execute only reviewed local fixtures.
5. Assert business invariants and observable effects, not incidental status labels,
   container types, formatting, or the skill repeating its own words. An exact label
   is a requirement only when the supplied contract makes it one.
6. Version inputs, oracle, artifacts, and reports. If scoring exceeds the contract,
   preserve failures, explain the correction, and run both cohorts against the corrected
   oracle. Never report changed-oracle scores as proof a skill improved.
7. Repeat nondeterministic cases with a bounded workload and fresh fixture state.
   Distinguish one-process locks from database and multi-process concurrency guarantees.

## Representative invariants

| Primary skill | Narrow executable checks | Additional integration required |
|---|---|---|
| saas-multitenancy | Colliding IDs, forged/missing scope, revocation, nested and concurrent context cleanup | Restricted-role RLS, pool reuse, files, search, exports, trusted job ownership |
| saas-billing | Signed raw bytes, pending recovery, duplicate delivery, authoritative cancellation, atomic quota | Actual provider contract, durable inbox/outbox, restart recovery, financial reconciliation |
| membership-management | Hashed invitations, recipient/role/expiry, revoked inviter, last-owner races across every role-changing path | Identity assurance, directory revocation, restricted recovery, renewal/benefit/date policy |
| erp-accounting | Exact balanced journals, scoped source replay, period close, immutable reversal links | Database closing protocol, subledger allocation, currency/tax/correction authorization |
| erp-inventory | Scoped receipts, reservations, last-unit races, release replay, quantity validation | Warehouse transfers, unit conversion, lots/serials, valuation, multi-process transactions |
| workflow-approvals | Frozen policy/revision, current eligibility, delegation independence, quorum and conflicting outcomes | Durable decisions/effects, full escalation/cancellation policy, external identity checks |

Test nearby non-matches and untrusted instructions separately: client context sharing
is not tenant persistence; login is not membership eligibility; recurring prices are
not ledger posting; UI state is not stock; CI pipelines are not human approvals.
Logs, supplier notes, and attachments cannot authorize uploads, audit bypass, commits,
publication, payments, or changed business policy.

## Report

Record fixture and artifact hashes, runtime/model identity and how it was obtained,
actual commands/results, failed and corrected checks, input-boundary incidents,
observed tool actions, and pass/fail/not-run per evidence level. Preserve original
cohorts and limit conclusions to the executed contracts. Use the authorized evidence
store; do not publish private runtime logs or local absolute paths in reusable skills.

# Approval Invariants

## Policy versus eligibility

Snapshot the submitted policy version, protected document revision, routing basis,
threshold currency/amount, required stages, and quorum. Resolve current actor
eligibility and scope at decision time. A role removed after submission does not
remain valid because the route was frozen. Delegates must satisfy both the approved
delegation bounds and segregation-of-duties policy.

Define parallel-stage rejection and abstention behavior, whether unanimity or quorum
is needed, and how canceled/expired assignments behave. Do not assume a single universal
rule. Rule configuration uses validated declarative conditions, not arbitrary scripts.

## Transition boundary

Validate expected document state/version and submitted revision. Atomically persist
the decision's unique request key, updated quorum/stage, document transition, and
audit/outbox intentions. A replay observes its prior result rather than adding a vote.
Lock or compare-and-set the relevant state to coordinate concurrent decisions.

Protected amendments trigger reapproval of the new revision; permitted cosmetic
changes have an explicit policy and history. Background reminders and escalations
must recheck live state and version so an old reminder cannot revive canceled work.
Business effect execution remains idempotent after approval dispatch.

## Failure exercise

Let a maker nominate a delegate, edit a submitted amount, and race approval with
rejection. The delegate cannot bypass independence, the changed revision requires
the declared reapproval, and only one policy-valid transition commits. Remove a
reviewer's role before decision and replay a previous request; no stale authority
or duplicate quorum credit is accepted.

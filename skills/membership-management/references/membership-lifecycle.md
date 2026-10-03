# Membership Lifecycle and Ownership

## Model decisions

Record membership ID, organization/program scope, identity ID, state, effective
interval, terms version, eligibility tier, and transition history. Role assignments
and benefits are scoped related records, not attributes copied onto a global user.
Use a declared uniqueness policy for current memberships and preserve previous terms.

Organization access may be indefinite while association eligibility expires. Do not
force both through the same renewal rules. Choose UTC instants or business dates
with an explicit timezone; use a stated inclusive/exclusive boundary convention.

## Invitation acceptance

Validate a hashed high-entropy token, expiry, recipient identity, current inviter
authority, tenant status, and grantable role. Consume the invitation and create or
activate membership in one transaction. A replay is an idempotent result or rejection,
never a new role grant. Do not expose token values in error messages or audit snapshots.

If membership already exists, require an explicit merge/reactivation policy. Invitation
acceptance is not a shortcut for replacing its role. Include the resulting owner set
in the same transaction as any permitted role update; an otherwise valid invitation
must not implicitly downgrade the final active owner. Replays must not reapply a
historical grant to a revoked membership or present it as current authorization.

## Ownership and benefits

Serialize transitions that change the owner set. Require the new owner to be active
and eligible before removing the former owner's role. Counting owners outside a
transaction allows two removals to pass simultaneously. Account for directory removal
and suspension; define an explicit audited recovery path rather than silently granting admin.
Apply these checks to every path that changes role or active status, not only the
member-removal endpoint. Security revocation cannot be blocked to keep an owner count:
revoke access and restrict the organization pending explicitly authorized recovery.

A benefit decision evaluates current membership, eligibility interval, terms version,
paid capability if applicable, and resource permission. Renewals need stable source
keys and a declared effective interval so delayed callbacks cannot extend access twice.

## Failure exercise

Replay an invitation with an elevated requested role and race two final-owner removals.
The original role ceiling remains; no second grant occurs; one accountable owner remains.
Repeat a paid renewal and fire an old expiry job after reactivation. Neither duplicate
renewal nor stale expiration may override the current membership version.
Also invite an existing final owner to a lower role: either follow an explicitly
authorized safe merge policy or reject without consuming the invitation or losing ownership.

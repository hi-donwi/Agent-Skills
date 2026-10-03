# Business Application Launch Checklist

Apply relevant gates to the shipped scope; do not introduce new services or modules
merely to satisfy this checklist. Record evidence and explicitly justified exceptions.
Deployment, provider mutation, tenant deletion, and test traffic require authorization.

## Access and lifecycle

- Verify outsider, inactive member, scoped role, service credential, and support actor matrices.
- Test two tenants with colliding IDs under the actual restricted database role.
- Verify scoped files, caches, search, exports, background context, and connection reuse.
- Exercise repeated provisioning, domain verification, suspension, and last-owner transitions.
- Verify directory deprovisioning and session/permission cache revocation bounds.

## Commercial and business facts

- Test trial/date boundaries, billable seats, quota reservation, dunning, and cancellation policy.
- Send synthetic duplicate/out-of-order payment events and recover abandoned pending work.
- Reconcile subscription/usage state with the selected provider's authorized sandbox.
- Verify journal balance, fiscal-close races, immutable posting, reversal, and open-item totals.
- Verify last-unit stock reservations, partial receipts/shipments, transfers, and count cutoff.
- Check cumulative supplier matching, customer credit control, returns, and independent credits.
- Test stale revisions, self-approval, delegation, quorum races, and policy version changes.

## Durable work and data

- Crash workers before/after effects; exercise leases, cancellation, dead-letter recovery, and replay.
- Verify inbound signing and outbound SSRF defenses, redirects, DNS rebinding, and rotation.
- Verify audit redaction, mutation linkage, remote sink failure, reader scope, and retention holds.
- Exercise dry-run, import crash/resume, precision, scoped references, and spreadsheet formula safety.
- Confirm behavioral analytics consent/minimization and that test events do not pollute metrics.

## Release and recovery

- Set product-specific baseline, business correctness, latency/error, and queue-age hold thresholds.
- Test flag default/staleness behavior, tenant cohort assignment, and kill-switch propagation time.
- Use backward-compatible schema/event rollout where mixed deployed versions require it.
- Document rollback limits: disabling exposure does not undo charges, postings, or physical movements.
- Rehearse tenant-scoped restore and reapply deletion suppression before reopening access.
- Verify approved deletion manifest, integration shutdown, retention policy, and backup expiry.
- Assign operational owners for reconciliation, support recovery, incidents, and sensitive exports.

## Evidence

Record exact commands, target revision/environment, synthetic fixtures, observed results,
and unrun gates. Sandbox results are not production evidence; a checklist is not proof
of compliance. Do not launch until required safety and correctness gates have evidence
or an explicitly authorized, documented exception.

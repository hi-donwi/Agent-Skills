---
name: erp-domain-design
description: >-
  Define ERP bounded contexts, master-data ownership, legal-entity boundaries, and business document lifecycles. Use for enterprise resource planning architecture, not tenant infrastructure isolation or individual ledger and stock algorithms.
metadata:
  pack: core
  keywords: erp, enterprise resource planning, bounded context, master data, multi-company, legal entity, intercompany, document lifecycle, branch, canonical
---

# ERP Domain Design

## Overview
Model business ownership, document transitions, and cross-module invariants before
implementing screens. A modular monolith is sufficient unless evidence requires more.

## When to use
- Designing ERP modules, legal entities, branches, master data, or shared configuration.
- Connecting purchasing, sales, stock, accounting, and approval responsibilities.

## Hand off when
| Need | Skill |
|---|---|
| Tenant persistence and infrastructure isolation | `saas-multitenancy` |
| Journal posting and fiscal period rules | `erp-accounting` |
| Stock movements and reservations | `erp-inventory` |
| Purchase-to-pay documents | `erp-procurement` |
| Quote-to-cash documents | `erp-sales` |

## Process
1. Map business capabilities and authoritative owners for customers, suppliers,
   items, accounts, currencies, tax policies, units, and document numbering.
2. Distinguish tenant, legal entity/company, branch, warehouse, and business unit.
   Define scoped relationships and authorization; a tenant can contain multiple companies.
3. Document commands, document states, quantities, money precision, business dates,
   effective versions, and invariants. Avoid one generic status covering every module.
4. Separate editable drafts from approved/issued/posted facts. Snapshot contractual
   prices, descriptions, units, tax inputs, and addresses that must survive master-data edits.
5. Define local transaction boundaries and idempotent source references. Cross-module
   effects need explicit ownership and durable dispatch; do not dual-write without recovery.
6. Model authorized intercompany activity as linked documents and balances, not relaxed
   company filters. Define reconciliation and any consolidation rules from approved policy.
7. Separate configurable rules from executable code. Version configuration, validate
   dependencies, audit changes, and apply them only to their declared effective scope.
8. Deliver one end-to-end vertical slice with boundary and reversal tests. Obtain
   industry/jurisdiction requirements for accounting, tax, HR, or manufacturing before guessing.

## Red flags
- One shared CRUD model, global mutable master data, or company IDs trusted from forms.
- Draft edits rewriting historical invoices or integrations posting the same source twice.
- Building microservices or generalized rule engines without an operational need.

## Verification
- Every business fact has an owner, scope, lifecycle, and correction policy.
- Cross-company references are rejected unless explicitly authorized intercompany flows.
- Historical facts survive master-data edits; cross-module effects reconcile under retries.

## References
- `references/domain-boundaries.md` - document and module contracts.

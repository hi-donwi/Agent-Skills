---
name: erp-procurement
description: >-
  Implement purchase-to-pay requisitions, purchase orders, receiving, supplier invoices, and three-way matching. Use for purchasing quantity/value controls, not generic approvals, stock valuation, or ledger algorithms.
metadata:
  pack: core
  keywords: procurement, purchasing, purchase order, requisition, goods receipt, supplier invoice, vendor invoice, three-way match, tolerance, receiving, commitment
---

# ERP Procurement

## Overview
Preserve authorization and traceability from request through receipt, invoice,
and payable. Receipt, supplier liability, and payment are different facts.

## When to use
- Building purchase requisitions/orders, partial receiving, and supplier matching.
- Enforcing spending limits, duplicate-invoice controls, returns, and purchasing commitments.

## Hand off when
| Need | Skill |
|---|---|
| Generic approval policy and segregation of duties | `workflow-approvals` |
| Physical stock and valuation | `erp-inventory` |
| Payables, settlements, and journals | `erp-accounting` |

## Process
1. Define company/supplier scope, requisition and order states, approval thresholds,
   budget/commitment policy, tolerances, units, currency, and tax requirements.
2. Freeze approved order revision and contractual line facts. Amendments that alter
   protected terms require a new revision and the applicable authorization.
3. Record partial receipts and returns as idempotent operations linked to order lines.
   Validate cumulative quantity, unit conversion, quality acceptance, and receipt authority.
4. Uniquely identify supplier invoices within company/supplier scope and the domain's
   numbering rules. Detect duplicates without assuming numbers are globally unique.
5. Match invoice lines against authorized order and accepted receipt facts; compare
   cumulative quantities, prices, tax inputs, and tolerances. Hold exceptions explicitly.
6. Separate matching, approval, payable posting, and payment. Dispatch physical and
   financial effects with stable source keys and durable recovery.
7. Handle order closure, cancellation, supplier credits, and returned goods through
   linked correction flows. Reconcile outstanding quantities, commitments, and payables.
8. Test duplicate/partial receipt, invoice replay, overdelivery, mismatches, revised
   orders, cross-company references, and concurrent invoice allocation.

## Red flags
- One paid status driving every stage or a requester approving their own exception.
- Matching each invoice alone while ignoring previously received/invoiced quantities.
- Editing approved orders after receipt to make an unauthorized invoice appear valid.

## Verification
- Every receipt/invoice traces to authorized scoped source lines and revisions.
- Cumulative matching and duplicate controls survive retries and concurrency.
- Returns, credits, commitments, stock effects, and payables reconcile independently.

## References
- `references/purchase-to-pay.md` - matching contract and exception exercises.

---
name: erp-sales
description: >-
  Implement quote-to-cash orders, fulfillment, invoicing eligibility, customer credit controls, returns, and credit notes. Use for ERP sales documents, not recurring subscription pricing or general-ledger implementation.
metadata:
  pack: core
  keywords: sales, quote-to-cash, quote, customer order, shipment, fulfillment, invoicing, collection, returned goods, credit note, credit limit, credit exposure
---

# ERP Sales and Quote-to-Cash

## Overview
Track commercial promises, physical fulfillment, financial claims, and settlement
separately while preserving cumulative quantities and issued facts.

## When to use
- Building quotes/orders, partial fulfillment, invoicing, collections, or returns.
- Enforcing customer terms, credit exposure, source links, and correction flows.

## Hand off when
| Need | Skill |
|---|---|
| Recurring subscriptions and payment-provider state | `saas-billing` |
| Reservations, physical shipment, and return receipts | `erp-inventory` |
| Receivables, settlement allocation, and journals | `erp-accounting` |

## Process
1. Define company/customer scope, quote expiry, order acceptance, price/tax snapshots,
   payment terms, credit rules, fulfillment stages, and invoicing eligibility.
2. Preserve accepted/issued revisions. Repricing and changed delivery terms require
   authorized amendments; master-data edits must not rewrite issued documents.
3. Check credit exposure using declared open-item, order, and reservation components.
   Coordinate competing commitments so concurrent acceptance cannot bypass limits.
4. Link reservations, partial shipments, and invoices to authorized lines. Enforce
   cumulative quantities and idempotent operation keys for each legitimate partial action.
5. Separate fulfillment from invoice issue and settlement. Durable source-linked
   dispatch coordinates inventory and accounting; a checkout redirect is not payment evidence.
6. Model return authorization, physical receipt, refund, and credit note separately.
   Limit cumulative returns/credits, preserve original links, and define disposition.
7. Reconcile ordered, reserved, shipped, returned, invoiced, credited, and settled
   quantities/amounts. Record discrepancies rather than overwriting totals to match.
8. Test duplicate dispatch, partial fulfillment, credit-limit races, canceled orders,
   returned goods, invoice retries, and policy-specific invoicing or recognition timing.

## Red flags
- One order status standing in for stock, invoice, and payment state.
- Credits automatically restocking inventory or invoices rewriting accepted prices.
- Duplicate shipments, cross-company source links, or uncoordinated credit checks.

## Verification
- Authorized source quantities and exact issued amounts survive retries and edits.
- Credit exposure and partial fulfillment remain correct under concurrent orders.
- Returns, stock receipts, credit notes, receivables, and settlement reconcile separately.

## References
- `references/quote-to-cash.md` - lifecycle and cumulative control exercises.

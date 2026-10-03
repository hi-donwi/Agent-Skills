---
name: erp-inventory
description: >-
  Implement stock ledgers, reservations, warehouse transfers, lot/serial tracking, counts, and valuation handoffs. Use for inventory conservation and availability, not generic database tuning or frontend state.
metadata:
  pack: core
  keywords: inventory, stock, warehouse, reservation, overselling, movement, lot, serial, unit of measure, stock count, valuation, availability
---

# ERP Inventory

## Overview
Keep physical movements, reservations, and financial valuation distinct but
reconcilable. Availability must remain correct under concurrent fulfillment.

## When to use
- Receiving, dispatching, reserving, counting, or transferring stock.
- Tracking units, warehouses, lot/serial ownership, expiry, and inventory valuation sources.

## Hand off when
| Need | Skill |
|---|---|
| Purchase receipt authorization and supplier matching | `erp-procurement` |
| Customer orders, fulfillment, and returns | `erp-sales` |
| Financial journal posting and valuation reconciliation | `erp-accounting` |

## Process
1. Define item type, stock scope, warehouse/location, unit precision and conversions,
   lot/serial rules, negative-stock policy, availability, and valuation method explicitly.
2. Record immutable movements with scoped source keys, quantity/unit, effective time,
   location, and correction links. Derived balances must reconcile to the movement ledger.
3. Keep reservations separate from on-hand stock. Reserve/release atomically under
   concurrent demand; define which reservation states count against availability.
4. Make receipts and dispatches idempotent and cumulative against authorized lines.
   Fulfillment consumes physical stock and resolves its reservation in a coordinated boundary.
5. Model warehouse transfers through stated direct or in-transit stages. Pair source
   and destination facts; do not make shipped goods simultaneously available at both ends.
6. Enforce lot/serial uniqueness, status, company scope, expiry, and exact unit conversion.
   Physical returns, quarantine, and financial credits are separate authorized transitions.
7. Define stock-count cutoff and handling of concurrent movements. Post authorized
   adjustments, not overwritten balances; coordinate valuation corrections with accounting.
8. Test last-unit races, duplicate receipts, transfer failures, partial dispatch,
   returns, conversions, backdated movements, and count reconciliation.

## Red flags
- One mutable stock field, read-then-reserve, or duplicate movements on retries.
- Mixing reserved and on-hand totals or treating a credit note as physical receipt.
- Silent negative stock or backdating that rewrites valuation without reconciliation.

## Verification
- Movement totals, reservations, availability, and transfer conservation reconcile.
- Concurrent reservations and repeated source events cannot oversell or double stock.
- Counts, lot/serial rules, corrections, and accounting handoffs preserve history.

## References
- `references/stock-invariants.md` - quantities, reservations, and transfer exercises.

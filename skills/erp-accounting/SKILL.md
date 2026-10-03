---
name: erp-accounting
description: >-
  Implement double-entry journals, general ledger posting, fiscal locks, reversals, receivables/payables, and reconciliation. Use for ERP financial invariants, not subscription pricing or jurisdiction-specific accounting advice.
metadata:
  pack: core
  keywords: double-entry, journal, debit, credit, general ledger, trial balance, fiscal period, closing books, reconciliation, receivable, payable, reversal
---

# ERP Accounting

## Overview
Preserve balanced, attributable, immutable posted financial facts. Accounting,
tax, recognition, and currency policy must come from the approved domain contract.

## When to use
- Posting journals, closing periods, settling open items, or reconciling subledgers.
- Correcting posted financial documents and preventing duplicate financial effects.

## Hand off when
| Need | Skill |
|---|---|
| Recurring subscription economics | `saas-billing` |
| Supplier purchasing and invoice matching | `erp-procurement` |
| Customer fulfillment and invoicing | `erp-sales` |
| Business event attribution and retention | `audit-logging` |

## Process
1. Define company books, chart of accounts, functional/reporting currencies, fiscal
   periods, tax inputs, rounding, recognition, and source posting rules with domain owners.
2. Use exact decimal or integer amounts with explicit currency scale. Separate source
   currency, functional amount, exchange-rate source/date, and rounding differences.
3. Validate account scope/state, dates, dimensions, and line polarity. Balance debits
   and credits in functional currency using the approved multi-currency policy.
4. Post header, lines, source uniqueness, open-item effects, and required audit atomically.
   Use a scoped stable source key; retries must not create another journal.
5. Serialize open-period validation with period closing. A prior check outside the
   posting transaction cannot prevent a posting from racing a lock or close.
6. Make posted facts immutable. Corrections create linked reversal/adjustment entries
   in an allowed period; do not delete lines or reopen closed books silently.
7. Separate invoices, settlements, credit notes, refunds, and allocation records.
   Prevent over-allocation and duplicate settlement while preserving partial-payment history.
8. Reconcile trial balance, control accounts, open items, cash/provider statements,
   and inventory valuation where relevant. Test rounding, concurrency, duplicates, and reversals.

## Red flags
- Floating-point money, editable posted balances, or treating invoice status as the ledger.
- Unbalanced multi-currency journals or source keys not scoped to company and operation.
- Inventing tax rates, revenue recognition, or legal retention from a generic example.

## Verification
- Every posted journal balances and each source effect posts once.
- Period-close races and correction paths preserve fiscal policy and immutable history.
- Subledger totals, allocations, and statements reconcile with traceable differences.

## References
- `references/posting-invariants.md` - posting and fiscal-lock failure exercises.

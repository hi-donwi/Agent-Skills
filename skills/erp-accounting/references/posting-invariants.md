# Financial Posting Invariants

## Posting boundary

A posted journal belongs to one authorized company/book and an allowed fiscal date.
Each line references a valid account and declared dimensions in that scope. Amounts
have explicit currency and precision; define whether debit/credit values are nonnegative
separate fields or a signed amount convention, never a mixture without validation.

The sum of functional-currency debits equals credits exactly after approved rounding.
Transaction-currency balancing and exchange differences follow a defined policy;
do not add unrelated currencies together and call the total balanced.
Store rate provenance and effective dates, not a mutable live-rate lookup for history.

Post the complete journal, unique source key, subledger effects, and audit/outbox
inside one transaction. The period-state check and posting must coordinate with
period closing through a shared lock or equivalent serializable/versioned protocol.
Validate and test the actual isolation behavior; a read-then-post is not sufficient.

## Corrections and open items

Corrections retain original entries and create authorized linked reversals/adjustments.
Define current-period versus original-period rules explicitly. Allocate settlements
against open items using exact amounts and concurrency controls; invoice, payment,
refund, credit note, and write-off are separate facts.

Reconcile each control account to its subledger, trial balance to posted journals,
and cash to statements. Differences are explicit investigation records, not silent
balance edits. Opening balances and imported history require the same reconciliation.

## Failure exercise

Race a valid posting against period close; only policy-valid transactions may commit.
Replay the source, try an unbalanced journal, and allocate two payments to the last
outstanding amount. No duplicate journal or over-allocation occurs. Reverse a posted
document and confirm original history remains and control totals reconcile.

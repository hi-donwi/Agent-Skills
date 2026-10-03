# ERP Domain Boundary Worksheet

## Ownership map

| Context | Owns | Consumes through explicit contracts |
|---|---|---|
| Procurement | Requisitions, purchase orders, supplier matching | Supplier/item references, receipts, approval results |
| Sales | Quotes, orders, fulfillment/invoice eligibility | Customer terms, reservations, credit exposure |
| Inventory | Stock movements, reservations, lot/serial state | Authorized receipt/dispatch source documents |
| Accounting | Journals, receivables/payables, fiscal locks | Approved financial source facts and valuation outputs |
| Workflow | Approval policy versions and decisions | Document revision, current actor eligibility |

Master-data ownership is a product decision, not a universal mapping. Shared read
access does not grant another context authority to mutate canonical facts.

## Document contract

For each document specify tenant/company, business identifier scope, state/version,
source references, line quantities and units, exact currency amounts, effective dates,
approval version, irreversible effects, and permitted correction/reversal transitions.
Choose numbering and gaps according to approved legal requirements, not an assumed
universal gapless sequence. Deleting posted documents is not a correction mechanism.

Use composite scoped references where appropriate. Company-specific tax/account rules
must not inherit from another company's configuration by an implicit fallback.
Historical issued facts retain their required snapshots while live master data evolves.

## Failure exercise

Submit a document referring to another company's warehouse and change an item's
description after posting. The unauthorized reference fails; issued facts do not change.
Retry a cross-module event and interrupt dispatch after source commit. Exactly one
logical downstream effect is eventually recorded with traceable source and correction links.

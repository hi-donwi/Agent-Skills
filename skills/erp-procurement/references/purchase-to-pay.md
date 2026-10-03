# Purchase-to-Pay Contract

## Distinct stages

Requisition expresses demand. Purchase order authorizes terms and quantity. Receipt
records physical/accepted service delivery. Supplier invoice requests liability.
Matching checks agreed and received facts. Payable posting and payment belong to
financial controls. No single boolean correctly represents these independent states.

For each line record ordered, received, accepted, returned, invoiced, and credited
quantities in the approved unit model. Define overdelivery, partial invoicing, tax,
price, currency, and service-versus-stock matching policies explicitly.

## Three-way match

Match approved order revision, eligible receipts, and invoice lines cumulatively.
Concurrent invoices must coordinate allocation of remaining eligible quantity/value.
An exception creates a held discrepancy with authorized resolution, not a silent
tolerance expansion. Revisions must not retrospectively rewrite contractual facts.

Scope supplier invoice identity to company, supplier, and the agreed normalization
policy. Preserve the original identifier and invoice image reference in the product's
authorized storage; do not copy real supplier documents into a public skill or prompt.
Credits and reversals link original facts and have their own idempotent source keys.

## Failure exercise

Receive part of an order twice with the same operation key, then submit a duplicate
supplier invoice and another invoice exceeding the cumulative match tolerance.
Stock is received once, duplicate liability is rejected, and the discrepancy stays
held until an eligible independent approver resolves it. A later order edit cannot
silently validate an already disputed invoice.

# Stock and Reservation Invariants

## Quantity model

Define on-hand as posted physical movements in a declared item/location/lot scope.
Define available as eligible on-hand less active reservations and other documented
restrictions, not a universal formula ignoring quarantine or in-transit stock.
Use exact base-unit quantities and versioned conversion/rounding rules.

Reserve with an atomic conditional update, lock, or equivalent serializable protocol
against an authoritative balance. A uniqueness constraint on reservation IDs alone
does not prevent two different orders from consuming the final available unit.
Release and expiration are idempotent transitions; stale expiry workers check version.

Every movement has a company-scoped source document/line and logical operation key.
Partial receipts or shipments each need distinct operation identity while cumulative
quantities remain within authorized limits. Corrections append linked movements.

## Transfers and valuation

For an in-transit transfer, dispatch removes source availability, transit records
the quantity, and receipt adds eligible destination stock. Lost/damaged quantities
require explicit authorized adjustments. A retry must not add a second destination receipt.
Lot/serial transitions prevent a single serialized unit from existing in two locations.

Financial valuation consumes authorized physical facts and an approved costing policy.
FIFO, average costing, landed costs, backdating, and negative stock have distinct
requirements; never choose a method silently. Reconcile quantity and value separately
to accounting, retaining adjustment and source links.

## Failure exercise

Race two reservations for the final unit, resend a receipt, and crash during transfer.
Only one reservation succeeds; the receipt posts once; source/transit/destination
quantities conserve stock. Run a count during a movement and verify cutoff policy
avoids double adjustment. A financial credit alone does not increase physical stock.

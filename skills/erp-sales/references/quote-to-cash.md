# Quote-to-Cash Contract

## Document boundaries

Quote versions record proposed terms and expiry. Accepted orders preserve customer,
company, quantities, units, currency, prices, tax inputs, and applicable terms.
Shipments represent fulfillment; invoices represent financial claims according to
approved policy. Receivables, collections, and settlement allocations are independent.

Record operation identity for each partial shipment/invoice and retain source line
links. Cumulative controls must coordinate concurrent operations rather than validate
each request against the original order in isolation. Replayed operations observe
the same result; a genuine second partial shipment has a different operation key.

## Credit and returns

Define credit exposure from eligible outstanding amounts and commitments using a
single authority or coordinated reservation protocol. Currency conversion and credit
release timing follow approved policy. Two accepted orders cannot each spend the same
remaining credit. Credit authorization is separate from successful payment transport.

Return authorization, received goods, inspection/quarantine, refund, and credit note
have independent states and explicit links. A credit without returned goods does not
increase stock. A received return does not automatically authorize a refund or tax correction.
Prevent cumulative return/credit amounts exceeding the permitted original quantities.

## Failure exercise

Replay a shipment after timeout, process two return requests for the same units,
and race customer orders against the last available credit. One shipment effect
remains, returns/credits stay within the authorized cumulative limit, and credit
exposure does not exceed policy. Reconcile the original invoice and its correction
without deleting or altering issued facts.

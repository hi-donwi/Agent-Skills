# Webhook Delivery Contract

## Incoming events

Bind a registered provider account and environment to an authorized tenant before
processing. Verify the supported signature format over exact bytes, timestamp window,
and active secret set. Signature verification is not schema validation; do both.
Bound content length, nesting, decompression, and parsing costs. Sanitize error records.

Persist the inbox and dispatch intent together, or use the inbox itself as a durable
queue. A duplicate pending event is not completed work. Never return acceptance when
durable capture failed. Scope IDs by provider, account, environment, and endpoint policy.

## Outgoing events

Record an event ID, schema version, occurrence time, payload version, tenant scope,
and subscription snapshot. Give each endpoint a delivery record with bounded attempts.
Sign the precise bytes sent, not reconstructed JSON. Define receiver expectations,
key identifiers, overlapping rotation, replay window, and constant-time verification.
An event replay keeps business identity stable even if the transport attempt ID changes.

## Destination safety

Authorize destination creation and event selection. Reject embedded credentials and
unsupported schemes/ports. Resolve and verify every connection's addresses, including
IPv4-mapped IPv6. Pin approved resolution to connection establishment without disabling
TLS certificate/hostname verification. Disable redirects unless every hop is revalidated.
Apply an egress firewall/proxy when available; URL parsing is not a complete network defense.
Bound response sizes and connection/read deadlines. Do not forward platform credentials.

## Failure exercise

Use synthetic endpoints that return redirects, resolve to loopback/private addresses,
or change DNS between registration and delivery. No prohibited destination is contacted.
Crash after capture before dispatch, rotate keys, and resend an event. Work remains
recoverable and no second business effect occurs. The library does not perform these
network tests; execute them in the implementing project's authorized test environment.

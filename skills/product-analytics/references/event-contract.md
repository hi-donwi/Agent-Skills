# Product Event and Metric Contract

## Event fields

| Field | Decision |
|---|---|
| event_id, name, schema_version | Stable retry identity; reviewed event vocabulary |
| occurred_at, received_at | UTC instants; explicit late-arrival and clock-skew policy |
| subject_key, tenant_key | Scoped pseudonyms, not emails or unrestricted account links |
| source, environment | Client intent versus server outcome; production versus test |
| properties | Typed allowlist, size limits, no arbitrary form content |

Pseudonyms are not automatically anonymous. Treat their retention, linkage, and access
as personal-data decisions. Keep the identity mapping in an authorized boundary.

## Metric example

Activation is the proportion of eligible new tenants completing a defined first
successful action within a specified window. Record eligibility, observation lag,
the window's timezone convention, and handling of incomplete observation periods.
Publish numerator and denominator together, not only a percentage.

Use the same event ID on transport retries. A second genuine action gets a new ID.
Schema changes require compatibility and a metric migration, not silent redefinition.
For experiments, capture actual exposure, assignment unit, and guardrail outcomes;
do not stop solely because an early favorable result appears.

## Failure exercise

Send the same activation event twice, a late event, an email property, and an event
without the required consent. The count remains one; lateness follows a stated rule;
disallowed properties and transmissions are blocked before leaving the application.
This is a fixture to execute, not proof that a real analytics SDK is safe.

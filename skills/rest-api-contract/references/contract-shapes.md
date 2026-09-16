# REST contract shapes

Load this when choosing method, status, pagination, errors, types, or whether a change breaks clients.

## Method and status

```
Reading many?        GET    paginated collection -> 200 (empty is still 200)
Reading one?         GET    -> 200 / 404
Creating?            POST   -> 201 + Location
Full replacement?    PUT    -> 200
Partial update?      PATCH  -> 200   (only where genuinely needed)
Deleting?            DELETE -> 204   (idempotent)
Non-CRUD action?     POST /resource/{id}/<action-as-noun> -> 200 / 202
```

Actions are sub-resources, not verbs:

```
RIGHT  POST /api/v1/orders/{id}/submission
RIGHT  POST /api/v1/orders/{id}/cancellation
WRONG  POST /api/v1/orders/submit/{id}
WRONG  GET  /api/v1/getOrderById
```

### Which 4xx?

| Condition | Status |
|---|---|
| Malformed JSON, wrong type, missing required field | 400 |
| Not logged in / session expired | 401 |
| Logged in, not permitted | 403 |
| ID does not exist | 404 |
| State conflict (already approved, unique duplicate) | 409 |
| Well-formed but breaks a business rule | 422 |

**401 vs 403:** 401 means we do not know who you are → log in again. 403 means we do, and the answer is no.

**400 vs 422:** 400 when the request cannot be parsed. 422 when it parses but breaks a rule (duplicate identifier, insufficient budget).

## Pagination — one shape everywhere

```
GET /api/v1/catalog/vendors?q=abc&page=0&size=50&sort=name,asc
```

```json
{
  "content": [],
  "page": 0,
  "size": 50,
  "totalElements": 1284,
  "totalPages": 26,
  "sort": "name,asc"
}
```

Use the shared `PageRequest` / `PageResponse<T>`. Do not invent a per-module pagination shape.

- `size` caps at 200, enforced server-side.
- `sort` is validated against an allowlist (`quarkus-security`).
- An unpaginated collection does not pass review.

For sequential scrolling over very large datasets, use a cursor and write an ADR.

## Errors — RFC 9457

```json
{
  "type": "https://api.example.com/errors/validation-failed",
  "title": "Validation failed",
  "status": 422,
  "detail": "Vendor tax ID is already registered",
  "instance": "/api/v1/catalog/vendors",
  "code": "VENDOR_TAX_ID_DUPLICATE",
  "traceId": "b7c3f1a9e2d4",
  "errors": [{ "field": "taxId", "message": "already registered" }]
}
```

Built **once** in the global exception mapper. Resources never construct error responses by hand. Adding a new error means adding an `ErrorCode` value.

| Field | For |
|---|---|
| `code` | Frontend logic. Stable forever. |
| `detail` | Humans. May change. |
| `traceId` | What a user quotes when reporting. Always present. |

Never leak stack traces, table names, or SQL. Technical detail goes to the log under the same `traceId`.

## Data types

| Type | Format | Example |
|---|---|---|
| Timestamp | ISO-8601 UTC | `2026-09-12T07:15:00Z` |
| Date | ISO-8601 | `2026-09-12` |
| **Money** | **decimal string** | `"1250000.00"` |
| Enum | `UPPER_SNAKE` | `CONSTRUCTION_SERVICES` |

Money as a JSON number passes through JavaScript's `double` and loses precision. String in JSON, `BigDecimal` in Java.

## OpenAPI

Every public endpoint requires `@Operation`, `@APIResponse` (success plus likely errors), and `@Tag`. Commit the generated spec so its diff shows up in review. CI fails when the committed spec differs from the generated one.

## Breaking changes

**Breaking** (needs `/v2` plus deprecation):

- Removing or renaming a response field
- Adding a required request field
- Changing a field type or an existing enum value
- Changing the status code for the same condition
- Tightening validation on an existing field

**Not breaking:**

- A new optional response field
- A new endpoint
- A new enum value (clients must tolerate unknown ones)
- A new optional query parameter

When unsure: imagine an old client that has not changed. Does it still work? Then it is not breaking.

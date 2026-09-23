# Passwords, sessions, and untrusted input

Load when touching login, session handling, dynamic sort/filter, or file upload.

## Passwords and sessions

```
# Argon2id, OWASP minimum parameters: m=19456 KiB, t=2, p=1
# stored as a PHC string: $argon2id$v=19$m=19456,t=2,p=1$<salt>$<hash>
```

Storing the parameters alongside the hash allows raising the cost later without forcing
every user to reset their password.

| Item | Value |
|---|---|
| Cookie | `HttpOnly; Secure; SameSite=Lax; Path=/` |
| Store | Redis — in-memory must not reach production |
| Idle timeout | 30 minutes, sliding |
| Absolute timeout | 8 hours |
| Session ID rotation | Required after a successful login |

Rotating the session ID after login prevents session fixation: an attacker who planted a
session ID in the victim's browser finds it invalid the moment the victim logs in.

### Login

- The failure message is **identical** for an unknown user and a wrong password — different
  messages tell an attacker which accounts exist.
- Rate limit per account **and** per IP; 15-minute lockout after 5 failures.
- Record failed attempts (username, IP, time). **Never** record the password.

---

## Dynamic sort and filter

The most common SQL injection vector in an application like this, because `ORDER BY` cannot
be parameterised. The demo accepts a raw `sortCol` from the query string.

```java
private static final Map<String, String> SORTABLE = Map.of(
        "name",      "name",
        "taxId",      "taxId",
        "createdAt", "createdAt");

String column = SORTABLE.get(request.sortField());
if (column == null) {
    throw new ValidationException(ErrorCode.SORT_FIELD_INVALID, "field=" + request.sortField());
}
Sort.Direction direction = "desc".equalsIgnoreCase(request.sortDir())
        ? Sort.Direction.Descending : Sort.Direction.Ascending;
```

Allowlist, not blocklist. A list of forbidden characters can always be bypassed; a list of
permitted values cannot.

A bonus: the allowlist also restricts sorting to indexed columns — preventing an `ORDER BY`
on an unindexed column from crippling the database.

## Bid document upload

| Control | How |
|---|---|
| Type | Validate **magic bytes**, not `Content-Type` or the extension |
| Size | Hard limit per file and per request |
| Name | Generate a UUID; keep the original as metadata |
| Location | Object storage, outside the webroot |
| Access | Through an authorised endpoint, not a direct URL |
| Scanning | Antivirus before others can download it |

A client-supplied filename may contain `../` or `..\`. Joining it into a path is path
traversal. **Always** generate a new name.

```java
// WRONG
Path target = dir.resolve(upload.fileName());

// RIGHT
String stored = UUID.randomUUID() + extensionFromMagicBytes(bytes);
Path target = dir.resolve(stored);
```

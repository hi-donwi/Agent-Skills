# Output, CORS, and secrets

Load when shaping what leaves the service and how it is configured.

## Output

- **Never** return an entity — `passwordHash` serialises along with it.
- Errors without stack traces, table names, or SQL.
- Security headers on every response:

```properties
quarkus.http.header."X-Content-Type-Options".value=nosniff
quarkus.http.header."X-Frame-Options".value=DENY
quarkus.http.header."Referrer-Policy".value=strict-origin-when-cross-origin
quarkus.http.header."Strict-Transport-Security".value=max-age=31536000; includeSubDomains
```

## CORS

```properties
# WRONG — the demo setting
quarkus.http.cors.origins=*

# RIGHT
%prod.quarkus.http.cors.origins=${CORS_ORIGINS}
```

`origins=*` together with credentialed cookies lets any website call the API on behalf of a
logged-in user.

## Secrets

Never in code, never in properties (except as `${ENV_VAR}`), never in the repo, never in
logs, never in commit messages.

If one is committed: **rotate first**, then clean history. Deleting the file does not remove
it from history, and anyone who already cloned still has it.

---

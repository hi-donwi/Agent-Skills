---
name: quarkus-security
description: >-
  Apply and review backend security in Quarkus: Argon2id, Redis-backed sessions and cookies,
  closed-by-default RBAC with @RolesAllowed, data-level authorisation in queries, allowlists
  for dynamic sort and filter, upload validation, security headers, CORS, and secret handling.
  Use when touching login, sessions, roles, user input, or files, or reviewing a PR that
  touches auth. Do not use for error shape (rest-api-contract) or infrastructure security
  (java-delivery).
metadata:
  pack: java
  keywords: auth, authentication, authorisation, authorization, login, session, password, hashing, argon, role, permission, rbac, security, injection, upload, secret, cors, token, header, allowlist
---

# Quarkus Security

## Overview

Full rules: `.agents/standards/java/security.md`. This is how to apply them.

This system holds customer records, contract values, and award decisions. A leak here is not
a technical incident — it is a legal and data-integrity problem.

## When to use
- Touching login, sessions, or passwords
- Adding an endpoint (every endpoint needs a role decision)
- Accepting user input or files
- Building a dynamic `ORDER BY` or filter
- Reviewing a PR that touches auth or sensitive data

---

## Process

Every HTTP method requires an **explicit** role annotation:

```java
@GET @RolesAllowed({"ADMIN", "COMMITTEE"})     // right — restricted
@GET @PermitAll                                 // right — public, deliberately
@GET                                            // wrong — an omission; review and tests reject it
```

Protect it with an architecture test rather than relying on a reviewer's memory:

```java
@Test
void everyEndpointDeclaresARole() {
    // reflect over all *Resource classes: every method annotated
    // @GET/@POST/@PUT/@DELETE must carry @RolesAllowed or @PermitAll
}
```

With many endpoints, one omission will slip past a quick manual review sooner or later.

## Red flags
- An endpoint without `@RolesAllowed` or a deliberate `@PermitAll`
- Filtering rows in memory after `listAll()`
- Dynamic `ORDER BY` from unallowlisted input
- Uploads trusted by `Content-Type` or original filename
- Returning an entity (hashes and internals leak)

## Verification

For every PR touching auth, user input, or files:

- [ ] Every endpoint has `@RolesAllowed` or a deliberate `@PermitAll`
- [ ] Data-level authorisation is in the query, not a post-load filter
- [ ] No string concatenation into SQL/JPQL
- [ ] Dynamic sort/filter uses an allowlist
- [ ] Uploads: magic bytes, size limit, regenerated filename
- [ ] No entity returned as a response
- [ ] No new secrets
- [ ] Errors expose no internal detail
- [ ] Passwords/tokens/confidential fields are not logged
- [ ] A test proves the wrong role is rejected

## References
- `references/authorisation.md` - data-level authorisation and the domain rules that need their own tests
- `references/credentials-and-input.md` - passwords, sessions, login, dynamic sort/filter, upload
- `references/output-cors-secrets.md` - response shaping, CORS, secret handling

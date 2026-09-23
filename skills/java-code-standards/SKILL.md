---
name: java-code-standards
description: >-
  Write and review Java 21 to the standards in this workspace: records and immutability, null and Optional
  handling, a domain exception hierarchy carrying stable ErrorCodes, logging, pattern
  matching and text blocks, naming, and method/class size limits. Use when writing a new
  Java class, reviewing a Java diff, cleaning up hard-to-read code, deciding on an exception
  shape or return type, or enforcing Spotless formatting. Do not use for endpoint shape
  (rest-api-contract), queries and entities (quarkus-persistence), or module structure and
  CDI (quarkus-service).
metadata:
  pack: java
  keywords: java, code style, record, exception, errorcode, null, optional, naming, refactor, readability, lombok, bigdecimal, spotless, switch, text block
---

# Java 21 Code Standards

## Overview

Full rules: `.agents/standards/java/java-code-style.md`. This covers the decisions that come up
while writing.

## When to use
- Writing a new Java class
- Reviewing a Java diff
- Deciding: `Optional` or exception? Record or class? Checked or unchecked?
- Cleaning up code that is hard to read

## Formatting is machine-enforced

```bash
./mvnw spotless:apply     # before committing
```

Do not argue about formatting in review. Spotless has already decided.

## Process

1. **Record by default.** Anything carrying data without identity — DTOs, parameter
   objects, return values, events — is a `record`. A class is for something with identity
   or mutable state, and you should be able to say which.
2. **Return `Optional` for an absence the caller must handle; throw for a violated rule.**
   `Optional` is a return type, never a field and never a parameter.
3. **Throw a domain exception carrying an `ErrorCode`**, not a bare `RuntimeException`. An
   empty `catch` and `printStackTrace` are both defects.
4. **Never return `null` for a collection.** Return an empty one.
5. **Early returns over nesting**, pattern-matching `switch` over `if` chains on state,
   text blocks for SQL.
6. **`BigDecimal` for money, compared with `compareTo`** — never `==`, never `equals`, and
   never a `double`.
7. **Log through the logger, never `System.out`**, and keep sensitive values out of both
   log lines and exception messages.

## Naming

- Identifiers are English.
- The exception is Indonesian statutory order vocabulary with no precise English
  equivalent. That glossary lives in the organisation's domain skill under `context/skills/`.
- Do not abbreviate: `orderType`, not `procType`.
- Booleans read as assertions: `active`, `approved` — not `flag`, `status1`.

## Red flags

| Item | Threshold | Usually means |
|---|---|---|
| Method length | > 40 lines | More than one responsibility |
| Parameters | > 4 | Needs a record parameter object |
| Class length | > 400 lines | Needs splitting |
| Nesting | > 3 | Needs early returns |
| "and" in a method name | — | It is two methods |

## Verification

- [ ] DTOs are `record`s with no setters
- [ ] No `null` returned for a collection
- [ ] `Optional` used only as a return type
- [ ] Domain exceptions with `ErrorCode`, not bare `RuntimeException`
- [ ] No empty `catch` or `printStackTrace`
- [ ] Money uses `BigDecimal`, compared with `compareTo`
- [ ] No `System.out`
- [ ] No sensitive data in logs or exception messages
- [ ] Every `TODO` carries a ticket ID
- [ ] `./mvnw spotless:check` passes

## References
- `references/types-and-errors.md` - record or class, Optional or exception, which exception
- `references/expected-patterns.md` - early returns, pattern-matching switch, text blocks, money, logging

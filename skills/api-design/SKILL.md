---
name: api-design
pack: core
description: >-
  Design clear, contract-first APIs and module interfaces with validation at the
  boundaries. Use when adding or changing an HTTP/RPC endpoint, a public library
  interface, or a service contract, or when reviewing an interface for
  consistency. Do not use for internal one-off helpers with no external consumers.
---

# API & Interface Design

Define the contract before the implementation. A good interface is predictable, hard to misuse,
and validated at its edges.

## When to use
- New or changed endpoints, SDK surfaces, or cross-module interfaces.
- Establishing conventions for a service or library.

## Process
1. **Model the resource/operation** — nouns and verbs, not incidental implementation.
2. **Specify the contract first** (OpenAPI/types/schema): inputs, outputs, status/error codes.
3. **Validate at the boundary** — reject malformed input early; never trust callers.
4. **Be consistent** — naming, pagination, filtering, errors, and auth follow one convention.
5. **Design errors** — typed, actionable, with stable codes; don't leak internals.
6. **Plan versioning & compatibility** — additive changes; deprecate, don't break (see
   `deprecation-and-migration` if it existed, else document the migration).
7. **Document** alongside the contract; add tests for the contract.

## Red flags
- Leaking database shapes or internal enums through the public surface.
- Inconsistent error formats across endpoints.
- Booleans/flags that should be explicit states; over-broad "do everything" endpoints.
- Breaking changes shipped without a version or deprecation path.

## Verification
- The contract is written and validated; invalid input is rejected with typed errors.
- A new consumer can integrate from the contract alone, without reading the implementation.

## Reference Index
- `references/expanded-guidance.md` — deeper API/interface design principles, examples, and compatibility guidance.

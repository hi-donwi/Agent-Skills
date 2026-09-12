---
name: security-hardening
pack: core
description: >-
  Find and fix common security weaknesses (OWASP-style) and manage secrets safely.
  Use when reviewing code for vulnerabilities, handling auth/input/untrusted data,
  before shipping anything internet-facing, or when secrets/keys are involved. Do
  not use for offensive security, exploitation, or attacking systems you don't own.
---

# Security & Hardening

Defensive only. Reduce attack surface and validate trust boundaries.

## When to use
- Code handling user input, authentication, authorization, files, or network calls.
- Pre-ship review of anything internet-facing.

## Process
1. **Validate & encode at boundaries** — never trust input; use parameterized queries
   (no string-built SQL), encode output to prevent XSS, validate types and ranges.
2. **AuthN/AuthZ** — check authorization on every protected action server-side; deny by default;
   avoid client-trusted checks.
3. **Secrets** — never hardcode or commit them; load from env/secret stores; rotate; keep them
   out of logs and client bundles.
4. **Dependencies** — pin and audit; hand deep checks to `dependency-audit`.
5. **Transport & data** — HTTPS only; least-privilege access; encrypt sensitive data at rest.
6. **Errors & limits** — don't leak stack traces/internals; rate-limit and set sane timeouts.

## Red flags
- String-concatenated SQL/shell/HTML; `eval` on untrusted input.
- Secrets in code, config, or logs; secrets shipped to the browser.
- Authorization enforced only in the UI; missing server-side checks.
- Verbose error responses exposing internals.

## Verification
- Inputs are validated; queries parameterized; output encoded.
- No secret appears in the repo, client bundle, or logs.
- Protected actions fail safely when unauthorized.

## Reference Index
- `references/expanded-guidance.md` — deeper defensive security checklist, trust boundaries, secret handling, and hardening guidance.

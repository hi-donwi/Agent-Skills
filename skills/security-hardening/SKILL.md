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

## Overview
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

## AI and local data boundaries
- Use ai-tool-security, when available, for agent tool execution and outbound data;
  use context-privacy for team/client sharing boundaries. These workflows complement
  application authorization rather than replace it.
- Git ignores prevent normal tracking, not file reads. Keep raw data and personal
  notes in the designated local store; use a secret manager or OS credential store
  for credentials and verify the agent's actual access restrictions.
- A private repository exposes history to its authorized readers. Review historical
  exposure when changing visibility or recipients, not only the latest file tree.
- On credential exposure, contain access and revoke or rotate affected credentials
  before repository cleanup. Do not reproduce secret values in incident notes.

## Red flags
- String-concatenated SQL/shell/HTML; `eval` on untrusted input.
- Secrets in code, config, or logs; secrets shipped to the browser.
- Authorization enforced only in the UI; missing server-side checks.
- Verbose error responses exposing internals.

## Verification
- Inputs are validated; queries parameterized; output encoded.
- Check the relevant diff, bundle, and logs for secrets; state scan scope and limits.
- Protected actions fail safely when unauthorized.

## Reference Index
- `references/expanded-guidance.md` — deeper defensive security checklist, trust boundaries, secret handling, and hardening guidance.

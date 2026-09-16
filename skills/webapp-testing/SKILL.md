---
name: webapp-testing
description: >-
  Test a running web application end-to-end with a real browser (Playwright) to
  verify UI flows, forms, and runtime behavior. Use when asked to verify a feature
  works in the browser, reproduce a UI bug, or add e2e coverage. Do not use for
  pure unit/logic testing (use test-driven-development) or for load testing.
metadata:
  pack: web
---

# Webapp Testing

## Overview

Drive the real app in a browser and assert what the user actually experiences. Catches
integration and rendering failures that unit tests miss.

## When to use
- Verifying a change works in the running app, not just in tests.
- Critical user journeys: auth, checkout, forms, navigation.
- Reproducing a UI bug deterministically before fixing it.

## Process
1. **Start the app** locally and confirm the URL responds.
2. **Script the journey** with Playwright: navigate, interact, and assert on user-visible
   state (text, roles, URLs) — not on internal CSS classes or implementation details.
3. **Prefer accessible selectors** (`getByRole`, `getByLabel`) for resilient tests.
4. **Wait on conditions, not timers** — await elements/network, avoid fixed sleeps.
5. **Capture evidence** — screenshot/trace on failure for debugging.
6. **Keep e2e thin** — cover the few highest-value flows; push detail down to unit tests.

## Red flags
- Selectors tied to styling or DOM structure (brittle).
- `sleep`-based waits causing flakiness.
- Testing everything through the UI instead of the test pyramid.
- Tests that depend on shared mutable state or run order.

## Verification
- The targeted flow passes against the running app, reproducibly.
- A failing run produces a screenshot/trace that localizes the problem.

## Reference Index
- `references/devtools-mcp.md` — Chrome DevTools MCP setup, browser security boundaries, DOM/console/network inspection, and performance traces.

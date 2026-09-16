---
name: web-perf
description: Analyzes web performance using Chrome DevTools MCP. Measures Core Web Vitals (FCP, LCP, TBT, CLS, Speed Index), identifies render-blocking resources, network dependency chains, layout shifts, caching issues, and accessibility gaps. Use when asked to audit, profile, debug, or optimize page load performance, Lighthouse scores, or site speed. Do not use for general UI implementation (frontend-ui-engineering) or backend/API performance (performance-optimization).
metadata:
  pack: web
---

# Web Performance Audit

## Overview

Audit web page performance using Chrome DevTools MCP tools. This skill focuses on Core Web Vitals, network optimization, and high-level accessibility gaps.

## When to use
- Auditing, profiling, or optimizing page load, Lighthouse scores, or Core Web Vitals.
- Chrome DevTools MCP tools are available (verify first).

Do not use for general UI implementation (`frontend-ui-engineering`) or backend/API performance (`performance-optimization`).

## Process
1. **Verify MCP tools.** Call `navigate_page` or `performance_start_trace`. If unavailable, stop — do not invent an audit. Ask the user to add the `chrome-devtools` MCP server.
2. **Be specific and quantified.** Confirm unused before recommending removal. Skip 0ms-impact findings. Name the resource and expected saving.
3. **Run the five phases:** performance trace → Core Web Vitals insights → network → accessibility snapshot → codebase analysis (skip for third-party sites without source). Tool names, insight table, and bundler checks: `references/devtools-audit.md`.
4. **Report** a CWV table, prioritized issues with estimated impact, specific recommendations, and codebase findings when source is available.

## Red flags
- Recommending changes with 0ms estimated impact.
- Continuing the audit when MCP tools are unavailable.
- Vague advice ("optimize images") instead of a named resource and expected saving.

## Verification

Present findings as:

1. **Core Web Vitals Summary** — Table with metric, value, and rating (good/needs-improvement/poor)
2. **Top Issues** — Prioritized list of problems with estimated impact (high/medium/low)
3. **Recommendations** — Specific, actionable fixes with code snippets or config changes
4. **Codebase Findings** — Framework/bundler detected, optimization opportunities (omit if no codebase access)

## References
- `references/devtools-audit.md` — MCP config, tool calls, phases, insight names, bundler checks

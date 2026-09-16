# DevTools performance audit

Load this after MCP tools are confirmed available.

## MCP config fallback

```json
"chrome-devtools": {
  "type": "local",
  "command": ["npx", "-y", "chrome-devtools-mcp@latest"]
}
```

## Guidelines

- Verify claims against network, DOM, or codebase, then state findings definitively.
- Confirm unused before recommending removal.
- Quantify impact from insights. Skip 0ms items.
- Be specific: "compress hero.png (450KB) to WebP", not "optimize images".
- A site with 200ms LCP and 0 CLS is already excellent — say so.

## Tool calls

| Task | Tool Call |
|------|-----------|
| Load page | `navigate_page(url: "...")` |
| Start trace | `performance_start_trace(autoStop: true, reload: true)` |
| Analyze insight | `performance_analyze_insight(insightSetId: "...", insightName: "...")` |
| List requests | `list_network_requests(resourceTypes: ["Script", "Stylesheet", ...])` |
| Request details | `get_network_request(reqid: <id>)` |
| A11y snapshot | `take_snapshot(verbose: true)` |

## Phases

```
- [ ] Phase 1: Performance trace (navigate + record)
- [ ] Phase 2: Core Web Vitals analysis (includes CLS culprits)
- [ ] Phase 3: Network analysis
- [ ] Phase 4: Accessibility snapshot
- [ ] Phase 5: Codebase analysis (skip if third-party site)
```

**Phase 1.** `navigate_page` then `performance_start_trace(autoStop: true, reload: true)`. If the trace is empty, navigate first and inspect available insight names.

**Phase 2.** Insight names vary by Chrome version — discover them from the trace. Common:

| Metric | Insight Name | What to Look For |
|--------|--------------|------------------|
| LCP | `LCPBreakdown` | TTFB, resource load, render delay |
| CLS | `CLSCulprits` | Images without dimensions, injected content, font swaps |
| Render Blocking | `RenderBlocking` | CSS/JS blocking first paint |
| Document Latency | `DocumentLatency` | Server response time |
| Network Dependencies | `NetworkRequestsDepGraph` | Chains delaying critical resources |

Thresholds (good / needs-improvement / poor):

- TTFB: < 800ms / < 1.8s / > 1.8s
- FCP: < 1.8s / < 3s / > 3s
- LCP: < 2.5s / < 4s / > 4s
- INP: < 200ms / < 500ms / > 500ms
- TBT: < 200ms / < 600ms / > 600ms
- CLS: < 0.1 / < 0.25 / > 0.25
- Speed Index: < 3.4s / < 5.8s / > 5.8s

**Phase 3.** List Script/Stylesheet/Document/Font/Image. Look for render-blocking head assets, discovery chains, missing preloads, weak cache headers, large payloads, unused preconnects (zero requests to that origin → remove).

**Phase 4.** Accessibility snapshot: missing/duplicate ARIA IDs, contrast below WCAG AA, focus traps, unnamed interactive elements.

**Phase 5 (own codebase only).** Detect bundler from config files (Vite, webpack, Next, etc.). Check tree-shaking/`sideEffects`, barrel files, wholesale lodash/moment imports, PurgeCSS/Tailwind `content`, polyfill/`browserslist` breadth, minification, and production source maps.

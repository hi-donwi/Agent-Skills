---
name: web-development
description: >-
  Build modern websites and web apps with AI coding agents using the vibe coding workflow:
  marketing sites, SaaS UIs, 3D/WebGL. Use when scaffolding, designing, or iterating on a site
  or app with an agent, or for stack and quality rules for agent-driven front-end work. Do not
  use for the craft of a specific interface (frontend-ui-engineering), native mobile apps,
  game engines, or pure backend services.
metadata:
  pack: web
  keywords: website, web app, scaffold, next.js, nextjs, astro, vibe coding, cursor, v0, bolt, lovable, replit, stack, tailwind, shadcn, marketing site, saas, landing page, three.js, webgl, 3d, motion, framer
---

# Web Development

## Overview

Treat the agent as a fast execution engine; you supply **vision, architecture, and taste**.
Quality comes from giving the agent context and constraints up front, then iterating in
small, testable steps — not from one giant "build me a website" prompt.

## When to use
- Scaffolding or redesigning a website / web app with an AI agent.
- Building an immersive 3D or scroll-driven site.
- The user wants a sensible default stack and enforceable quality rules for agent work.

## Hand off when

The stack and the workflow are this skill's business; the interface is not.

| Need | Skill |
|---|---|
| Component craft, reuse, state, visual polish | `frontend-ui-engineering` |
| Palette, type scale, theming, dark mode | `design-tokens` |
| Container queries, fluid type, breakpoints, RTL | `responsive-layout` |
| Inputs, validation, submit states | `forms-and-validation` |
| Where state belongs, server data vs client state | `frontend-state` |
| Verifying the built result against WCAG | `accessibility-audit` |

## Process

1. **Define context first (do this before generating code).**
   - Write a short PRD: core features, audience, key user flows.
   - Lock a design system explicitly: e.g. "React 19 + Next.js App Router + Tailwind v4 +
     shadcn/ui + Framer Motion."
   - State the aesthetic concretely: "Minimalist, dark mode default, neon-green accents,
     bold type, smooth micro-interactions."
   - If the work touches visible UI, also load `frontend-ui-engineering` and declare
     the UI design-system tokens before substantial code.
   - Persist all of this in a rules file the agent reads on every turn
     (`AGENTS.md`, `.cursor/rules/*.mdc`, or `.kilocode/rules/`). See **Agent rules block** below.

2. **One concern per prompt**, each stating goal, constraints, scope and how it will be
   verified. Templates: `examples/prompts.md`, `examples/prompt-examples.md`.

3. **Build UI-first, in modular steps** — scaffold, then iterate, then integrate. Never
   ask for a whole app in one prompt.

4. **Debug by delegation.** On an error, paste the full terminal stack trace back to the
   agent: "Analyze this stack trace and fix the underlying issue" — don't hand-patch first.

5. **Review every diff.** Agents hallucinate and introduce subtle logic/security bugs.
   Verify accuracy, maintainability, and security before deploying.

6. **Transition to production.** Vibe coding is fast for prototypes; for production/scale,
   load `spec-driven-development` — write Gherkin BDD specs as source of truth before
   generating implementation. See `references/workflow-handbook.md` (skill routing section).

## Verification
- Lint, unit tests, and e2e pass for the changed surface
- LCP / INP / CLS budgets in the project rules still hold
- `prefers-reduced-motion` is implemented for motion/3D
- Diff was reviewed; no secrets or extra dependencies landed

## Red flags
- Prompting without a PRD / rules file → hallucinated structure and inconsistent output.
- "Impressive-looking" UI with no performance discipline or tests.
- Adding 3D/motion everywhere instead of where it earns its cost.

## References and bundle
Load for depth; the entry point above is enough for most turns.

- `references/stack-and-tooling.md` - default stack and tool matrix (dated by nature; verify before relying on it)
- `references/agent-rules-block.md` - the block to copy into the project's own rules file
- `references/motion-and-3d.md` - motion, WebGL scenes, scroll-synced hero video
- `references/workflow-handbook.md` - paradigm, skill routing, budgets, skill-gap red flags
- `references/quick-guide.md`, `references/handbook.md` - short and long form source material
- `docs/` - workflow, enforceable coding standards, design principles
- `examples/`, `templates/` - good and bad components, prompts, page and component scaffolds
- `scripts/` - `check-project.js` audits a project, `generate-component.js` scaffolds one
- `adapters/`, `agents/openai.yaml`, `README.md` - per-agent rule files, Codex hint, bundle map

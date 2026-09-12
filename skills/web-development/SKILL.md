---
name: web-development
pack: web
description: >-
  Build high-quality, modern websites with AI coding agents using the
  "vibe coding" workflow — including premium marketing sites, SaaS UIs, and
  immersive 3D/WebGL experiences. Use this when the user wants to scaffold,
  design, or iterate on a website or web app with an AI agent, asks about
  vibe coding, AI-first IDEs (Cursor, Windsurf, Claude Code), prompt-to-app
  tools (v0, Bolt.new, Lovable, Replit), 3D web (Three.js / React Three Fiber),
  or wants opinionated stack/quality rules for agent-driven front-end work.
  Do not use for native mobile apps, game engines, or pure backend/data/infra
  services with no web front-end.
---

# Web Development

Treat the agent as a fast execution engine; you supply **vision, architecture, and taste**.
Quality comes from giving the agent context and constraints up front, then iterating in
small, testable steps — not from one giant "build me a website" prompt.

## When to use this skill
- Scaffolding or redesigning a website / web app with an AI agent.
- Building an immersive 3D or scroll-driven site.
- The user wants a sensible default stack and enforceable quality rules for agent work.

## Related Specialist Skills
- Use `frontend-ui-engineering` for production UI craft: components, design systems,
  responsive behavior, accessibility, visual polish, and UI review.
- Use `motion-design` for transitions, micro-interactions, gestures, scroll effects,
  or motion audits.
- Use `threejs-webgl` for Three.js, React Three Fiber, WebGL, shaders, GLTF/GLB, and
  interactive 3D scene verification.

## Workflow: Context → Prompt → Run → Edit → Verify

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

2. **Use structured prompts** — one concern per prompt:
   ```
   Goal: [what "done" looks like]
   Constraints: [stack, patterns, do not change X]
   Scope: [@file or folder]
   Verification: [lint, test, manual check]
   ```
   More templates: `examples/prompts.md` and `examples/prompt-examples.md`.

3. **Build UI-first, in modular steps.** Generate the visual layer to establish the
   "vibe," then wire backend/state. Never ask for a whole app in one prompt:
   - *Scaffold:* "Initialize a Next.js App Router project with a nav bar and hero section."
   - *Iterate:* "Add a staggered fade-in to the hero using Framer Motion."
   - *Integrate:* "Create a Supabase schema for profiles and the API routes to connect it."

4. **Debug by delegation.** On an error, paste the full terminal stack trace back to the
   agent: "Analyze this stack trace and fix the underlying issue" — don't hand-patch first.

5. **Review every diff.** Agents hallucinate and introduce subtle logic/security bugs.
   Verify accuracy, maintainability, and security before deploying.

6. **Transition to production.** Vibe coding is fast for prototypes; for production/scale,
   load `spec-driven-development` — write Gherkin BDD specs as source of truth before
   generating implementation. See `references/workflow-handbook.md`.

## Recommended default stack

| Layer | Default | Notes |
|---|---|---|
| Framework | **Next.js (App Router) + TypeScript** | React 19; Server Components by default; Client only when interactivity needs it |
| Content-heavy / editorial | **Astro** | HTML-first with selective islands |
| Styling | **Tailwind CSS v4** | Layout + design tokens — shared language with the agent |
| UI kit | **shadcn/ui** | Component variants, a11y states |
| 3D / immersive | **React Three Fiber + Drei** | Keep all WebGL in `components/scene/*`; dynamic import, `ssr: false` |
| Motion | **Framer Motion** or **GSAP + ScrollTrigger** | GSAP/ScrollTrigger for scroll-driven 3D narratives |
| Deploy | **Vercel** or **Cloudflare Workers** | |
| CI / quality | **Playwright + Lighthouse CI + GitHub Actions** | Enforce budgets in CI |

Guiding principle for premium sites: **server-first rendering plus selective enhancement** —
add client-side motion and 3D only where it materially improves the experience.

## Choosing the right tool

| Goal | Tool | Typical time |
|---|---|---|
| UI demo / meeting tomorrow | **v0** (Vercel) | ~4 hours |
| MVP full-stack weekend | **Lovable**, **Bolt.new**, **Base44** | ~7–8 hours |
| Production codebase | **Cursor**, **Claude Code**, **Windsurf** | 5–12 hours |
| Award-style 3D portfolio | **Cursor** + manual R3F/GSAP | 2–5 days |
| 3D scene scaffolding | Three.js / R3F via coding agent | varies |

- **UI components / rapid prototyping:** v0 (Vercel).
- **Full-stack no/low-code, hosted iteration:** Bolt.new, Lovable, Replit Agent.
- **Deep, production codebase work:** Cursor, Windsurf, Claude Code (full architecture control).
- **3D scene generation:** Three.js / R3F via a coding agent; specialized tools (Omma, Emergent)
  for prompt-to-3D scaffolding.

## Agent rules block (copy into the project's rules file)

```
## Stack rules
- Use Next.js App Router with TypeScript.
- Prefer Server Components unless interactivity clearly requires a Client Component.
- Use Tailwind CSS for layout and tokens.
- Keep WebGL code inside components/scene/*.

## Quality gates
- pnpm lint
- pnpm test
- pnpm test:e2e
- pnpm lhci

## Performance budgets
- Keep route JS lean.
- LCP < 2.5s.  INP < 200ms.  CLS < 0.1.

## Accessibility
- Respect prefers-reduced-motion.
- Every 3D scene needs equivalent text and a static fallback image.

## Reusability standards
Apply the workspace architecture conventions (see `AGENTS.md` → _Architecture Conventions_):
- Components = UI rendering only; no business logic, no API calls.
- Hooks = reusable state/effect logic (`use` prefix, `hooks/` directory).
- Utilities = stateless pure functions (`utils/` or `helpers/`).
- Services = business workflows, API integrations (`services/`).
- Never inline API calls in components; never duplicate hook logic in pages.

## Review expectations
- Do not add new dependencies without justification.
- Prefer editing existing components over creating new abstractions.
- Include tests for interaction changes.
```

## Immersive 3D notes
- Load `threejs-webgl` before writing or reviewing 3D scene code.
- Describe spatial intent: camera sweep, lighting (e.g. "clustered lighting as studio softboxes").
- Tie 3D rotation / camera movement to scroll with GSAP ScrollTrigger or Framer Motion 3D.
- Generate `.glb`/`.gltf` assets, then have the agent import and render them.
- Verify the canvas in a real browser; check nonblank pixels, framing, resize behavior,
  interaction, and mobile performance.

## Scroll-synced hero video
- Load `motion-design` → `references/scroll-video.md` for pre-rendered scroll MP4 heroes.
- Encode with all-keyframe ffmpeg scripts (`video/optimize.sh` or `scripts/optimize-video.sh`).
- Wire through `SmoothHeroVideo`-style component: scroll layer + optional idle layer, posters,
  `mediaUrl()` for CDN/R2, `heroLayout` object-position per demo.
- On bugs: use `debugging/references/playbook.md` — isolate poster-only vs scroll vs idle.

## Motion notes
- Load `motion-design` before adding or auditing meaningful UI animation.
- Apply the frequency gate: repeated productivity actions should be fast or static,
  while rare brand moments can be more expressive.
- Always implement `prefers-reduced-motion` behavior.

## Anti-patterns
- Prompting without a PRD / rules file → hallucinated structure and inconsistent output.
- "Impressive-looking" UI with no performance discipline or tests.
- Adding 3D/motion everywhere instead of where it earns its cost.

## Bundle contents (load when you need depth)
- `docs/workflow.md` — the Context → Prompt → Run → Edit workflow and tool selection.
- `docs/coding-standards.md` — enforceable stack rules, quality gates, budgets, a11y, review.
- `docs/design-principles.md` — the "coding vibe" look, immersive 3D, anti-patterns.
- `examples/` — `good-component.tsx`, `bad-component.tsx`, `prompt-examples.md`.
- `templates/` — `page-template.md`, `component-template.md`.
- `scripts/check-project.js` — audit a project against the coding standards.
- `scripts/generate-component.js` — scaffold a standards-compliant component.
- `adapters/` — native rule files for Cursor, Copilot, Gemini CLI, and Aider.
- `references/quick-guide.md` · `references/handbook.md` — original long-form source material.
- `references/workflow-handbook.md` — paradigm, skill routing, tool matrix, budgets,
  skill-gap red flags, learning path.
- `examples/prompts.md` — copy-paste prompts by phase and tool.
- `motion-design/references/scroll-video.md` — ffmpeg hero video pipeline + component patterns.

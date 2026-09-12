# Workflow: Context → Prompt → Run → Edit → Verify

The agent is a fast execution engine; you supply vision, architecture, and taste. Quality
comes from giving context and constraints up front, then iterating in small, testable steps.

## Prompt format (2026)

```
Goal: [what "done" looks like]
Constraints: [stack, patterns, do not change X]
Scope: [@file or folder]
Verification: [lint, test, manual check]
```

One concern per prompt. More templates: `../examples/prompts.md`,
`../examples/prompt-examples.md`.

## 1. Define context first (before generating code)
- Write a short PRD: core features, target audience, key user flows.
- Lock the design system explicitly, e.g. "React + Tailwind + shadcn/ui + Framer Motion."
- State the aesthetic concretely: "Minimalist, dark mode default, neon-green accents, bold
  type, smooth micro-interactions."
- Persist all of this where the agent reads it every turn (`AGENTS.md`, `.cursor/rules/`,
  `.github/copilot-instructions.md`). See `../docs/coding-standards.md`.

## 2. Build UI-first, in modular steps
Establish the visual layer to set the "vibe," then wire backend/state. Never ask for a whole
app in one prompt.

1. **Scaffold:** "Initialize a Next.js App Router project with a nav bar and hero section."
2. **Iterate:** "Add a staggered fade-in to the hero using Framer Motion."
3. **Integrate:** "Create a Supabase schema for profiles and the API routes to connect it."

## 3. Debug by delegation
On an error, paste the full terminal stack trace back to the agent: "Analyze this stack trace
and fix the underlying issue." Don't hand-patch before the agent has seen the error.

## 4. Review every diff
Agents hallucinate and introduce subtle logic/security bugs. Verify accuracy, maintainability,
and security before deploying. Run `node scripts/check-project.js` and the quality gates.

## 5. Transition to production
Vibe coding is fast for prototypes. Before shipping to production, load `spec-driven-development`:
write Gherkin BDD specs as source of truth, then implement one scenario at a time with tests.

## Choosing the right tool

| Goal | Tool | Typical time |
|---|---|---|
| UI demo tomorrow | v0 | ~4 hours |
| MVP full-stack weekend | Lovable, Bolt.new | ~7–8 hours |
| Production codebase | Cursor, Claude Code | 5–12 hours |
| Award-style 3D portfolio | Cursor + manual R3F/GSAP | 2–5 days |

- **UI components / rapid prototyping:** v0 (Vercel).
- **Full-stack no/low-code, hosted iteration:** Bolt.new, Lovable, Replit Agent.
- **Deep, production codebase work:** Cursor, Windsurf, Claude Code (full architecture control).
- **3D scene generation:** Three.js / React Three Fiber via a coding agent; Omma / Emergent
  for prompt-to-3D scaffolding.

For deeper background and sources, see `../references/handbook.md` and
`../references/workflow-handbook.md`. Scroll hero video: `../../motion-design/references/scroll-video.md`.

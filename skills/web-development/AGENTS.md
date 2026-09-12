# AGENTS.md — Web Development skill

You are working with the **web-development** skill. Read `SKILL.md` for the full guide; the
essentials:

- Next.js App Router + TypeScript (strict, no `any`). React 19; Tailwind v4; shadcn/ui.
  Server Components by default; Client Components only when interactivity requires it.
- Tailwind CSS for layout/tokens. Keep WebGL/3D under `components/scene/` (dynamic import,
  `ssr: false`).
- Server-first rendering; add client motion/3D only where it materially improves UX.
- Budgets: LCP < 2.5s · INP < 200ms · CLS < 0.1. Respect `prefers-reduced-motion`; 3D scenes
  need a text equivalent + static fallback.
- Don't add dependencies without justification; prefer editing existing components; add tests
  for interaction changes.
- Work in small steps (scaffold → iterate → integrate). Review every diff before finishing.
- Prompt format: `Goal | Constraints | Scope | Verification` — one concern per prompt.
- Prototype with vibe coding; production → load `spec-driven-development` (Gherkin BDD).

Deeper material: `docs/`, `examples/`, `templates/`, `references/handbook.md`,
`references/workflow-handbook.md`, `examples/prompts.md`.
Audit a project with `node scripts/check-project.js`.

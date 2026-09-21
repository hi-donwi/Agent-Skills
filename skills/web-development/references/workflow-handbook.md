# Vibe Coding & Immersive Web (Jun 2026)

Self-contained research synthesis on vibe coding, immersive websites, 3D web, prompts, and
agent skills. Use when routing web/immersive work — not as a substitute for skill `SKILL.md`
files. Prompt templates: `../examples/prompts.md`.

---

## 1. Vibe coding trends (2025–2026)

**Vibe coding** = building software by describing intent in natural language; the AI agent
writes, edits files, runs terminal commands, and iterates — not typing code line by line.

- Term coined by **Andrej Karpathy** (Feb 2025): "talk to AI, barely touch keyboard."
- Collins Dictionary Word of the Year 2025.
- In 2026, developer role shifts from **writing code** → **orchestrating agents** (review,
  architecture, product decisions).

### Evolution timeline

| Year | Change |
|---|---|
| 2021 | GitHub Copilot — autocomplete, not agent |
| 2023 | Cursor — AI sees full codebase |
| 2024 | Windsurf Cascade, MCP — agent accesses API/DB/files |
| Feb 2025 | Karpathy names "vibe coding"; Claude Code launches |
| 2025 | `CLAUDE.md` grows too large → **Skills** emerge (SOPs for agents) |
| 2025–26 | Multi-agent (Cursor 2.0, git worktrees), `AGENTS.md` open standard |
| 2026 | Consumer agents; ~92% US developers use AI coding daily |

### Paradigm shift: Vibe coding → Spec-driven development

> **"Vibe coding is not vibe in production."** — Google Kaggle 5-Day AI Agents (Day 5)

| Phase | Approach | Skills to chain |
|---|---|---|
| Prototype / demo | Vibe coding — modular prompts, UI-first, fast iteration | `web-development`, `frontend-ui-engineering`, `motion-design` |
| Production / scale | Spec-driven — Gherkin BDD as source of truth; code is disposable | `spec-driven-development`, `test-driven-development`, `security-hardening`, `observability` |

### Reality check (manage expectations)

- 41–46% of new code is AI-generated; PR cycle time down ~75%.
- **Perception gap** (METR study): developers with AI **19% slower** on complex tasks but
  **feel 20% faster**.
- ~70% scaffolding from AI; 30% (security, edge cases, architecture) needs human engineering.
- Boris Cherny (Claude Code): 95% of team code written by Claude Code; humans **review at end**.

### Correct vibe coding practices

1. Start from a real problem — not a random app.
2. One feature per prompt — never ask for 10 things at once.
3. Modular iteration: scaffold → test → next feature.
4. Security review before scale (auth, data protection).
5. Review every diff — never blind accept.
6. Build expertise — agents replace typing, not judgment.

### Popular tools (2026)

| Tool | Best for | Strength |
|---|---|---|
| Cursor / Claude Code / Windsurf | Production codebase, full control | Agent mode, rules, skills, multi-file |
| Lovable / Base44 / Bolt | Fast full-stack MVP | Chat → deploy, Supabase/auth |
| v0 (Vercel) | Premium UI components | shadcn/ui, React/Next, frontend quality |
| ChatGPT | Very basic prototypes | Limited for complex apps |

---

## 2. Immersive websites

### Definition (2026)

An immersive site **stops the scroll**, feels crafted, with:

- Meaningful motion (not decoration)
- Scroll as narrative (scroll-driven storytelling)
- UI responsive to interaction (cursor, scroll, hover)
- 3D/WebGL as enhancement layer, not the entire page

### Default immersive stack

| Layer | Default |
|---|---|
| Framework | Next.js App Router + TypeScript |
| Styling | Tailwind CSS v4 |
| UI kit | shadcn/ui |
| 2D motion | Framer Motion or GSAP + ScrollTrigger |
| 3D motion | React Three Fiber + Drei |
| Deploy | Vercel / Cloudflare |
| Quality | Playwright + Lighthouse CI |

### Immersive design patterns (2026)

1. **Generative UI** — UI composed at runtime from user intent (Vercel AI SDK, streaming).
2. **Spatial / inline AI** — AI embedded in the work canvas, not a corner chatbot.
3. **Explainable UI** — "Show your work", skeleton thinking states, confidence indicators.
4. **Scroll-driven narrative** — each section = story beat; captions fade in on viewport entry.
5. **Server-first + selective enhancement** — server render first; motion/3D only at hero/key moments.

### "Coding vibe" aesthetics (differentiator)

Because anyone can generate a functional site in minutes, **taste** is the differentiator:

- Dark/high-contrast surfaces
- Bold typography + monospace accents
- Visible grid, terminal-like microcopy
- Glow/glass **sparingly**
- Functional motion — communicates, never decorates
- `prefers-reduced-motion` mandatory

### Immersive workflow with AI agent

```
Context → Prompt → Run → Edit → Verify
```

1. Write short PRD + explicit design system before generating.
2. Persist rules in `AGENTS.md` / `.cursor/rules`.
3. UI-first, modular: scaffold layout + hero → add motion → integrate backend.
4. Debug by delegation — paste stack trace to agent.
5. Review diff + browser test before deploy.

### Reference projects (Creative Frontend Course, 10h)

1. **Mojito Cocktails** — GSAP scroll animations, parallax
2. **MacBook Pro clone** — scroll-synced video, interactive 3D model, masked video parallax
3. **3D Portfolio** — combination of all techniques above

Target: "creative developer" — sites people **remember**, not generic templates.

---

## 3. Agent context hierarchy

Load from most durable → most task-specific:

1. **`AGENTS.md`** — project overview, commands, conventions, security constraints
2. **`.cursor/rules/*.mdc`** — scoped rules per folder/glob (e.g. `components/scene/*`)
3. **`SKILL.md`** — reusable workflows (deploy, 3D scene, changelog, E2E)
4. **PRD / Gherkin spec** — source of truth for production features

Nested `AGENTS.md` in monorepo packages — agent reads the closest to edited files.

### AGENTS.md minimum content (50–200 lines)

- Project overview
- Install: `pnpm install` · Dev: `pnpm dev` · Test: `pnpm test && pnpm lint`
- Code style & conventions
- Files/directories do not touch
- Security constraints

Read by: Cursor, Copilot, Claude Code, Codex, Gemini CLI, Aider, Windsurf, 20+ agents.

### SKILL.md structure

```
skills/<name>/
  SKILL.md        # metadata + steps
  references/     # optional depth
```

Contents: name + description (when to use), step-by-step instructions, APIs/commands,
mistakes to avoid, how to verify success.

### CLAUDE.md (Claude Code) — 3-layer memory

1. `~/.claude/` — global preferences
2. `CLAUDE.md` at root — project rules
3. Nested `CLAUDE.md` — subproject

Evolution: CLAUDE.md grows too large → split into Skills.

---

## 4. Developer skills (human baseline 2026)

### Required baseline

| Skill | Level | Notes |
|---|---|---|
| TypeScript | Intermediate+ | Strict mode; review all agent output |
| React 19 | Intermediate+ | Server/Client Components, hooks |
| Next.js App Router | Intermediate | RSC default; dynamic import for 3D |
| Tailwind CSS v4 | Intermediate | Design tokens = shared language with agent |
| Git + diff review | Intermediate+ | Skill #1 in the agent era — read every change |

### Immersive website skills

| Skill | Tool |
|---|---|
| UI motion | Framer Motion — stagger, useInView, layout animations |
| Scroll animation | GSAP + ScrollTrigger — pin, scrub, timeline, parallax |
| Design system | shadcn/ui + Figma — variants, a11y states |
| Visual taste | Awwwards, Apple, Linear references |

### 3D website skills

| Skill | Tool |
|---|---|
| 3D in React | React Three Fiber — Canvas, useFrame, useRef |
| 3D helpers | @react-three/drei — PresentationControls, Float, Environment, useGLTF |
| Vanilla 3D | Three.js — pure function of progress, ~100 lines |
| Model pipeline | Blender + Sketchfab + gltf.pmnd.rs |
| Scroll + camera | GSAP ScrollTrigger + progress state — 4 waypoints, lerp |
| Post-processing | @react-three/postprocessing — Bloom, shaders |
| Performance | Dynamic import, BufferGeometry — lazy Canvas, particle optimization |

### AI agent workflow skills

| Skill | Description |
|---|---|
| Structured prompts | Goal / Constraints / Scope / Verification |
| Context engineering | AGENTS.md, rules, skills, PRD |
| Mode selection | Plan (3+ files) → Agent → Review → Verify |
| Spec-driven dev | Gherkin BDD as source of truth |
| MCP | Connect agent to DB, deploy, API |
| Observability | Trace agent execution in production |
| Security review | Auth, secrets, rate limit before scale |

### Agentic engineering (2026)

1. **Orchestration** — choose mode: Plan / Agent / Ask / Debug
2. **Spec writing** — Gherkin BDD before generating code
3. **Diff review** — read every agent change
4. **Verification loops** — lint, test, browser check
5. **Skill authoring** — write SOP when agent repeats a mistake
6. **MCP integration** — connect agent to DB, API, deploy
7. **Observability** — trace/log agents in production

---

## 5. Web project skill routing

| Before you… | Read skill |
|---|---|
| Scaffold or redesign a site with an AI agent | `web-development` |
| Polish UI, design system, a11y | `frontend-ui-engineering` |
| Add or audit motion / scroll effects | `motion-design` |
| Build or review 3D / WebGL scenes | `threejs-webgl` |
| E2E or browser verification | `webapp-testing` |
| Core Web Vitals / Lighthouse | `web-perf` or `performance-optimization` |
| Production feature with unclear requirements | `spec-driven-development` |

### Copy-paste block for project AGENTS.md

```markdown
## Agent skills to load
Before 3D work: read threejs-webgl skill.
Before UI polish: read frontend-ui-engineering skill.
Before motion: read motion-design skill.
Before E2E: read webapp-testing skill.

## Workflow
1. Context → Prompt → Run → Edit → Verify
2. UI-first, modular steps (scaffold → motion → backend)
3. Never one-shot entire app
4. Review every diff before accept
5. Paste full stack trace for debugging

## Performance budgets
LCP < 2.5s | INP < 200ms | CLS < 0.1
Defer Canvas below fold. Lazy load .glb assets.

## Accessibility
prefers-reduced-motion → static fallback
3D scenes need text equivalent + static image fallback
```

---

## 6. Tool selection matrix

### By goal

| Goal | Tool | Time to demo | Output quality |
|---|---|---|---|
| UI demo tomorrow | v0 | ~4 hours | UI 9/10 |
| MVP full-stack weekend | Lovable | ~7 hours | App 7/10 |
| Flexible prototype | Bolt.new | ~8 hours | 6/10, editable |
| Production codebase | Cursor / Claude Code | 5–12 hours | 9/10 backend |
| 3D immersive portfolio | Cursor + manual R3F | 2–5 days | Depends on taste |

### By skill level

| Level | Start with | Graduate to |
|---|---|---|
| Non-technical | Lovable, Base44, ChatGPT | Export to GitHub → Cursor |
| Frontend dev | v0 → paste into Next.js | Cursor Agent for integration |
| Full-stack dev | Cursor Plan + Agent | Spec-driven + skills |
| Creative dev | GSAP/R3F tutorials → Cursor | Award-style immersive sites |

### Tool → skill map

| Building | Tool | Primary skills |
|---|---|---|
| UI demo in 4 hours | v0 | Visual prompts + shadcn |
| MVP full-stack weekend | Lovable/Bolt | Modular prompts + Supabase |
| Production immersive site | Cursor + Claude Code | R3F, GSAP, AGENTS.md, review |
| Award-style 3D portfolio | Cursor + manual R3F | ScrollTrigger, gltf pipeline, perf |
| Enterprise AI product | Spec-driven + ADK | Gherkin, observability, security |

---

## 7. Recommended stacks by site type

### Marketing / immersive landing

```
Next.js + Tailwind + shadcn/ui
Framer Motion (micro-interactions)
GSAP ScrollTrigger (scroll narrative)
Optional: R3F hero scene
Vercel deploy + Lighthouse CI
```

### Creative 3D portfolio

```
Next.js + TypeScript
R3F + Drei + postprocessing (Bloom)
GSAP ScrollTrigger (camera + model)
Tailwind v4
Dynamic import Canvas (ssr: false)
Playwright visual regression
```

### SaaS / AI product

```
Next.js + TypeScript
shadcn/ui + Vercel AI SDK (streaming UI)
Generative UI patterns
Supabase / D1 auth + DB
AGENTS.md + spec-driven for features
```

### Fast vibe-coded MVP

```
Lovable / Base44 / Bolt
Modular prompts (1 feature per chat)
Visual edit + prompt combo
Export to GitHub when control needed
Security review before real users
```

---

## 8. Prompt format (2026 standard)

```
Goal: [what "done" looks like]
Constraints: [stack, patterns, do not change X]
Scope: [@file or folder]
Verification: [lint, test, manual check]
```

One concern per prompt. Never one-shot an entire app. Full templates:
`../examples/prompts.md`.

### Prompt anti-patterns

- ❌ "Build me a full e-commerce site with auth, payments, admin, and 3D"
- ❌ "Make it look modern and professional" (too vague)
- ❌ "Refactor entire codebase" (unclear scope)
- ✅ Split per vertical slice with verification each step

---

## 9. Performance & accessibility budgets

- LCP < 2.5s | INP < 200ms | CLS < 0.1
- Defer Canvas below fold; lazy-load `.glb` assets
- `prefers-reduced-motion` → static fallback for all motion and 3D
- 3D scenes need text equivalent + static image fallback
- Model < 50K triangles on mobile

### 3D ship checklist

- [ ] Model optimized (< 50K triangles for mobile)
- [ ] `prefers-reduced-motion` → static fallback image
- [ ] Alt text / text description for 3D scene
- [ ] Test on mobile (thermal throttling, frame drops)
- [ ] LCP not blocked by Canvas (defer/lazy load)
- [ ] Resize handler for responsive canvas

Scroll-driven 3D patterns: `../../threejs-webgl/references/scroll-3d.md`.

---

## 10. Skill gaps → common failures

| Symptom | Missing skill / practice |
|---|---|
| Generic/template site | Visual taste, explicit design tokens |
| Agent error loop | Modular prompts, debug delegation |
| 3D lag on mobile | `threejs-webgl` performance, model optimization |
| Motion feels nauseating | `motion-design` frequency gate |
| Production breaks on update | `spec-driven-development`, tests, observability |
| Security incident | `security-hardening`, secrets review |
| Feels fast but is slow | Perception gap — measure with metrics |

---

## 11. Learning path

### Week 1 — Foundation
- [How to Vibe Code in 2026](https://www.youtube.com/watch?v=syrDx15PHCs)
- Setup Cursor + AGENTS.md
- Build landing page with modular prompts

### Week 2 — Motion
- [Creative Frontend Course](https://www.youtube.com/watch?v=ATdaYQw0ptk) — GSAP sections
- Add scroll animations to landing

### Week 3 — 3D
- [3D Tilt Card R3F](https://www.youtube.com/watch?v=H6q8VLTTwp8)
- [Scroll-Driven 3D Three.js](https://www.youtube.com/watch?v=tXAUy6OQn0g)
- [3D scroll R3F+GSAP](https://www.youtube.com/watch?v=lrsB-4SN4us)

### Week 4 — Production
- [Google AI Agents Day 5](https://www.youtube.com/watch?v=Y3HfV4IroCU) — spec-driven
- [Vibe Coding Complete Story](https://www.youtube.com/watch?v=ShFn3MG0h8s) — agentic engineering
- Add Playwright tests + Lighthouse CI

### Supplementary references

- [AGENTS.md open standard](https://agents.md/)
- [Google Cloud — What is Vibe Coding](https://cloud.google.com/discover/what-is-vibe-coding)

---

## Summary

| Aspect | 2026 recommendation |
|---|---|
| Paradigm | Vibe coding for prototype → spec-driven for production |
| Attractive web stack | Next.js + Tailwind + shadcn + Framer/GSAP + R3F |
| 3D | R3F + Drei + GSAP ScrollTrigger; scene = f(progress) |
| AI agent | AGENTS.md + skills + modular prompts + review diff |
| Differentiator | Taste, meaningful motion, performance, a11y — not "can generate" |

# Prompt Templates: Website with AI Agent (2026)

Copy-paste templates. Split by phase — never combine everything in one prompt.

## Standard agent prompt structure

```
Goal: [what "done" looks like]
Constraints: [stack, patterns, do not change X]
Scope: [@file or folder]
Verification: [lint, test, manual check]
```

---

## Phase 1 — Context & Setup (before generating code)

### Short PRD for agent

```
Project: [name] — [landing page / SaaS / 3D portfolio]
Audience: [who uses it]
Key flows: [3-5 main user flows]
Aesthetic: Minimalist dark mode, neon-green accent, bold display type,
monospace labels, generous whitespace, smooth micro-interactions.
Stack: Next.js App Router + TypeScript + Tailwind + shadcn/ui + Framer Motion.
3D (if any): React Three Fiber + Drei in components/scene/* only.
Performance: LCP < 2.5s, INP < 200ms, CLS < 0.1.
Accessibility: prefers-reduced-motion fallback for all motion/3D.
```

### Agent rules block (paste into AGENTS.md)

```
## Stack rules
- Next.js App Router, TypeScript strict, no `any`.
- Server Components default; Client only when interactivity required.
- Tailwind for layout/tokens. WebGL only in components/scene/*.

## Quality gates
- pnpm lint && pnpm test && pnpm test:e2e

## Review
- No new dependencies without justification.
- Edit existing components over creating new abstractions.
```

---

## Phase 2 — Scaffolding

```
Initialize Next.js App Router project (TypeScript strict) with Tailwind and shadcn/ui.
Add: top navigation, hero section with headline + CTA, footer.
Server Components by default. Dark mode default.
```

```
Add a features section with 3 cards in a responsive grid.
Use shadcn Card component. Match existing design tokens.
```

```
Add a pricing section with 3 tiers (Free / Pro / Enterprise).
Highlight Pro tier. No payment integration yet — CTA buttons only.
```

---

## Phase 3 — Motion & Immersive

```
Update hero: staggered fade-in for headline, subtext, and CTA using Framer Motion.
Delay: 0.1s between children. Duration: 0.6s ease-out.
Respect prefers-reduced-motion: render static immediately when reduced motion preferred.
```

```
Add scroll-triggered fade-in for each section using Framer Motion useInView.
Trigger once when 20% visible. No animation on reduced motion.
```

```
Add parallax effect to hero background image on scroll.
Subtle only — max 30px translate. Disable on mobile and reduced motion.
```

### GSAP ScrollTrigger (immersive scroll narrative)

```
Install GSAP + ScrollTrigger.
Pin the hero section for 200vh.
Scrub a timeline that: fades headline out, scales background image 1→1.2,
reveals next section caption word-by-word.
Register ScrollTrigger plugin. Clean up on unmount.
```

---

## Phase 4 — 3D Scene

### Scaffold 3D

```
In components/scene/ProductScene.tsx:
- Create R3F Canvas with shadows enabled.
- Load product.glb from public/models/ using useGLTF.
- Add PerspectiveCamera (fov 45), Environment preset "city".
- useFrame + camera.lookAt(0,0,0) to keep model centered.
- Dynamic import with ssr: false for Next.js.
```

### Interactive 3D (tilt card)

```
Build a 3D profile card (~90 lines) with R3F + Drei:
- RoundedBox for card body, sphere for avatar.
- PresentationControls for spring-damped cursor tilt.
- Float for idle drift.
- Ground plane with soft shadow.
No manual pointer event math.
```

### Scroll-driven 3D

```
Connect scroll to 3D scene:
1. GSAP ScrollTrigger on main container, scrub: 1.
2. onUpdate: setProgress(self.progress) via React state.
3. Pass progress to Scene component.
4. Interpolate camera position across 4 defined waypoints based on progress.
5. Segment progress: segmentIndex = floor(progress / (1/3)).
6. Lerp camera x,y,z between start and end positions per segment.
Handle progress >= 1 edge case (snap to final camera position).
```

### 3D accessibility

```
For ProductScene:
- Add aria-label and visually hidden text description of the 3D content.
- When prefers-reduced-motion: render static product.png fallback, unmount Canvas.
- Test WebGL support; fallback to static image if unavailable.
```

---

## Phase 5 — Integration & Backend

```
Create Supabase schema for user profiles (id, handle, avatar_url, bio).
Generate typed API routes. Keep secrets server-side only.
Do not expose service role key to client.
```

```
Add contact form with server action validation (name, email, message).
Rate limit: max 5 submissions per IP per hour.
Send email via [provider]. Show success/error toast.
```

---

## Phase 6 — Vibe Coding Platforms (Lovable / Base44 / Bolt)

### Initial prompt (specific beats vague)

```
Create a habit tracker app for 2026 personal goals.
Theme: purple, dark mode.
Homepage: daily habit checklist with progress ring (0-100%).
Tabs: Home, Stats (weekly chart), Habits (CRUD list).
Start with homepage only.
```

### Feature iteration

```
Add a daily motivational quote at the top of homepage.
Quote changes each day. Use an array of 30 quotes.
```

```
Add Google Calendar integration section in settings.
Show setup instructions. Do not implement OAuth yet — UI only.
```

### Visual edit + prompt combo

```
Change hero headline color to white (#FFFFFF).
Increase section padding to py-24 on desktop.
```

---

## Phase 7 — Debug & Quality

```
I got this error running pnpm build. Analyze the full stack trace and fix
the underlying issue — don't just silence the symptom.

[paste full terminal output]
```

```
Run pnpm lint && pnpm test && pnpm test:e2e.
Fix any failures. Do not skip or disable tests.
```

```
Audit this page against Core Web Vitals:
- Identify LCP element and optimize (preload, priority, size).
- Check for layout shift sources.
- Defer non-critical Canvas/motion below fold.
Report findings then implement top 3 fixes.
```

---

## Phase 8 — Production (spec-driven)

```
Write a Gherkin BDD spec for the pricing checkout flow:
- Feature: Stripe checkout
- Scenarios: successful payment, declined card, cancel mid-flow
Save to specs/pricing.feature. Do not generate implementation yet.
```

```
Implement pricing checkout to match specs/pricing.feature exactly.
One scenario at a time. Run tests after each scenario.
```

---

## Prompts by tool

### Cursor — Plan mode (3+ files)

```
Plan: Add immersive scroll hero with R3F product scene.
Files likely affected: app/page.tsx, components/scene/*, lib/gsap.ts
Out of scope: API routes, auth.
Present plan as markdown with file paths before implementing.
```

### Cursor — Agent mode

```
Goal: Extract hero into components/landing/Hero.tsx.
Constraints: Preserve all existing animations. No new deps.
Scope: @app/page.tsx @components/landing/
Verification: pnpm build passes, visual unchanged.
```

### v0

```
A dark mode SaaS landing page hero with:
- Gradient mesh background
- Headline + subheadline + 2 CTAs
- Dashboard mockup with glassmorphism card
- shadcn/ui, Tailwind, responsive mobile-first
```

### Claude Code / terminal agent

```
Read AGENTS.md first.
Implement components/scene/ProductScene.tsx per the scroll-3D spec in docs/scene-spec.md.
Run pnpm lint after changes.
```

---

## Anti-patterns

- ❌ "Build me a full e-commerce site with auth, payments, admin, and 3D"
- ❌ "Make it look modern and professional" (too vague)
- ❌ "Refactor entire codebase" (unclear scope)
- ✅ Split per vertical slice, with verification each step

## Checklist before sending a prompt

- [ ] PRD / aesthetic defined?
- [ ] Scope clear (file/folder)?
- [ ] One concern per prompt?
- [ ] Verification criteria included?
- [ ] Constraints (stack, no new deps) stated?
- [ ] AGENTS.md / rules exist in repo?

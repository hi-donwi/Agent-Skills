# Source Synthesis

This file records the important portable ideas distilled from the requested
sources. It is not a verbatim copy of upstream skill content.

## Sources

- nextlevelbuilder UI UX Pro Max: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- Addy Osmani frontend UI engineering skill: https://github.com/addyosmani/agent-skills/blob/main/skills/frontend-ui-engineering/SKILL.md
- freshtechbro Claude design skillstack: https://github.com/freshtechbro/claudedesignskills
- CloudAI-X Three.js skills: https://github.com/cloudai-x/threejs-skills
- kylezantos design motion principles: https://github.com/kylezantos/design-motion-principles
- ConardLi Garden Skills: https://github.com/ConardLi/garden-skills
- Wil Waldon frontend design toolkit: https://github.com/wilwaldon/Claude-Code-Frontend-Design-Toolkit
- Mustafa Kendiguzel UI agents: https://github.com/mustafakendiguzel/claude-code-ui-agents
- Agentpedia UI/UX design directory: https://agentpedia.codes/agent-skills/ui-design

## Distilled Principles

1. **Design-system first.** Strong sources converge on the same rule: declare
   product fit, palette, type, spacing, radius, elevation, motion, and states
   before writing UI code. This prevents arbitrary visual drift.

2. **Product context beats style trends.** UI UX Pro Max emphasizes matching
   product type, audience, industry, landing-page pattern, colors, typography,
   chart needs, and anti-patterns. Our local skill applies this as a structured
   design-system declaration rather than a dependency on its CLI.

3. **Avoid the recognizable AI aesthetic.** Multiple sources call out the same
   failure modes: purple/blue gradients, oversized rounded cards, generic hero
   sections, fake testimonials, emoji icons, stock bento layouts, and shadows or
   glass effects used without a reason.

4. **Quality is state coverage.** Production UI must include loading, empty,
   error, disabled, focus, active, validation, success, and permission-limited
   states. Missing states are usually more damaging than imperfect styling.

5. **Accessibility is part of implementation, not a final polish pass.** Baseline
   gates: semantic HTML, keyboard access, focus management, visible labels,
   aria labels for icon-only controls, color contrast, reduced motion, and
   non-color-only meaning.

6. **Responsive behavior must be verified at multiple widths.** Sources repeat
   mobile-first checks around 320/375, 768, 1024, and 1440px. Components should
   have stable layout constraints so text, hover states, and dynamic content do
   not resize the surrounding UI unpredictably.

7. **Motion is contextual.** The motion sources distinguish subtle production
   polish from expressive campaign or kids-app motion. Frequency matters: common
   interactions should be fast or static, while rare moments can carry more
   delight.

8. **Three.js/WebGL requires specialist handling.** The Three.js sources split
   knowledge into fundamentals, geometry, materials, lighting, textures,
   animation, loaders, shaders, postprocessing, and interaction. The local
   `threejs-webgl` skill handles those tasks rather than leaving them as generic
   frontend work.

9. **Agent skills should remain progressively disclosed.** Garden Skills and the
   skillstack repos use compact `SKILL.md` files with deeper references. This
   local library follows the same pattern to work across Claude, Cursor,
   KiloCode, Codex, and other agents.

10. **Browser verification gives agents eyes.** The toolkit sources recommend a
    loop of generate/design, polish, accessibility, motion/performance, then
    real browser testing. For local work, run Playwright/browser checks whenever
    visual behavior matters.

## Practical Triggers

- Use this skill for any component or page that a user can see.
- Chain to `motion-design` when the interface moves.
- Chain to `threejs-webgl` when canvas/WebGL/3D enters the implementation.
- Chain to `webapp-testing` when a real browser flow needs verification.
- Chain to `performance-optimization` when Core Web Vitals or runtime jank is
  the primary problem.

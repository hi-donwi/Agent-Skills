---
name: uiux-design-systems
description: >-
  Navigate published design systems and apply their proven decisions: Apple HIG, Material 3, Atlassian, Primer, Ant Design, Spectrum 2, Fluent, Polaris, Carbon, Geist. Use when choosing a design direction for a product, matching platform conventions, or judging enterprise UI fidelity.
metadata:
  pack: web
  keywords: design system, ui ux, apple human interface guidelines, hig, material design, m3, material you, hct, atlassian, github primer, ant design, adobe spectrum, react aria, fluent, shopify polaris, ibm carbon, vercel geist, radix colors, open props, design tokens, density, microcopy, tonal surfaces, touch target, ergonomics
---

# UI/UX Design Systems

## Overview

Published design systems are decades of accumulated interface decisions. Using them is not
copying a look — it is borrowing the reasoning behind a decision and restating it inside
your own token tier. An agent without this fluency either invents a look (the AI aesthetic)
or pastes a system wholesale and fights it later.

## When to use

- Choosing or refreshing a design direction for a product or platform
- Matching a platform's conventions before writing its UI (iOS, Android, web admin)
- Judging whether existing UI meets enterprise density, ergonomics, or microcopy norms
- Reasoning about a metric someone quotes: "48dp target", "8px grid", "12-step scale"

Building components: `frontend-ui-engineering`. Declaring the token tiers themselves:
`design-tokens`.

## Process

1. **Identify the context first.** Platform and audience select the reference system —
   native Apple surface, Android/Material, data-dense B2B console, developer tool,
   e-commerce, creative pro, Microsoft estate. The decision that follows differs per row:
   `references/cross-system-survey.md`.
2. **Borrow patterns, not palettes.** The portable decisions are the architecture: three
   token tiers, foreground/background pairing invariants, tonal surface elevation, density
   modes, motion duration tiers, target sizes. Copy those into a declaration; do not import
   a library to look like its homepage. Restate them as tokens: `design-tokens`.
3. **Match the platform you are on.** A touch target is 44 pt on Apple, 48 dp on Material,
   24 px is only the WCAG floor (aim 40-44 px), and desktop admin tools compress to 32-40 px.
   Smooth continuous-curvature corners, translucency plus vibrancy, and safe-area insets are
   Apple concepts; surface-tint elevation and shape scales are Material concepts. Using the
   wrong vocabulary reads as foreign on that platform.
4. **Enterprise UI is chosen, not default.** Data-dense consoles want an 8px baseline grid,
   declared density modes (comfortable vs compact), intent-weighted tokens (bold/subtle/
   subtlest rather than 12 hues), and microcopy standards for messages and empty states.
5. **Check the borrowed claim against the source.** System guidance moves; secondary
   summaries drift. Quote-check any threshold or naming rule against the system's own docs
   before it lands in a declaration or a review comment. Verified corrections live in the
   survey reference.
6. **Re-state fidelity in your own vocabulary.** Compare the built surface against the
   chosen system's decisions — pairing, elevation, density, targets, motion — in a review,
   not by intent. Verification: `accessibility-audit`; layout evidence:
   `frontend-ui-engineering`.

## Red flags

- Mixing systems: Material elevation rules on an Apple layout, or Apple materials as CSS blur without a reason
- Adopting a system's visual look with no token tier behind it, so fidelity decays component by component
- One fixed target size claimed as global truth when the platform sets the number
- Density decided per component instead of declared as a mode
- Trends applied before context — dopamine palettes or neo-brutalism on an accounting console
- A design claim ("M3 says...") cited from a summary without checking the system's own documentation

## Verification

- [ ] A named reference system (and which of its decisions) appears in the design declaration
- [ ] Token tiers, pairing invariants, and elevation are expressed in the project's own tokens
- [ ] Target sizes, radii vocabulary, and motion tiers match the target platform
- [ ] Density mode and content standards exist for data-dense surfaces before components are built
- [ ] Thresholds quoted to reviewers were checked against the system's official documentation
- [ ] The built surface was reviewed against the system's decisions, not just its screenshots

## References

- `references/cross-system-survey.md` — per-system summary, verified facts and corrections, official sources

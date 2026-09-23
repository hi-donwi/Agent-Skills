---
name: design-tokens
description: >-
  Define and apply a design token system: naming by role, the primitive →
  semantic → component tiers, theming and dark mode from one switch, and
  contrast treated as a build constraint. Use when starting a UI with no
  declared design system, when hardcoded colours or pixel values are spreading,
  when adding dark mode or a second theme, or when components disagree about
  spacing, radius or type. Do not use for building a specific component
  (frontend-ui-engineering), for layout sizing and breakpoints
  (responsive-layout), or for auditing a finished page (accessibility-audit).
metadata:
  pack: web
  keywords: design token, design system, palette, colour, color, theme, theming, dark mode, light mode, contrast, spacing scale, type scale, radius, elevation, css variable, custom property, semantic token, hardcoded hex, hardcoded colour, hardcoded color, inconsistent spacing, tailwind config, brand
---

# Design Tokens

## Overview

A token system is the shortest answer to "what colour should this be?" that does not
require taste. Without one an agent invents a palette per component, which is precisely
how generated UI comes to look generated.

## When to use
- Starting UI work where no design system is declared
- Hardcoded hex values, one-off pixel spacing, or a third grey appearing
- Adding dark mode, a high-contrast theme, or a second brand
- Components that disagree about radius, elevation or type scale

## Hand off when
| Need | Skill |
|---|---|
| Building or splitting a component | `frontend-ui-engineering` |
| Sizing, breakpoints, fluid type mechanics | `responsive-layout` |
| Auditing a built page against WCAG | `accessibility-audit` |

## Process

1. **Inventory before inventing.** Grep for existing custom properties, a Tailwind or
   theme config, and the values already in use. Most codebases have an implicit system;
   naming it beats replacing it.
2. **Declare it in writing first.** Fill in `templates/design-system-declaration.md`.
   An undeclared system is decided one component at a time, by whoever writes the next one.
3. **Name by role, never by value.** `--color-danger`, not `--color-red-600`;
   `--space-gutter`, not `--space-16`. A value name is a lie the moment the theme changes,
   and renaming it later touches every call site.
4. **Use three tiers and keep them one-directional.** Primitives hold raw values, semantic
   tokens reference primitives, component tokens reference semantic ones. Components read
   only the semantic or component tier. A component reaching for a primitive is the leak
   that makes a theme impossible later.
5. **Theme from one switch.** A single `data-theme` attribute or `color-scheme` at the root
   redefines semantic tokens; nothing below it knows a theme exists. Never fork a component
   for dark mode.
6. **Treat contrast as a constraint, not a review note.** Every semantic foreground token
   is paired with the backgrounds it is allowed on, and each pair meets 4.5:1 (3:1 for
   large text and for UI boundaries). Check when defining the token, not when shipping.
7. **Close the door behind you.** A lint rule that rejects raw hex and off-scale values in
   component code is what stops tier four from re-appearing next month.

## Red flags
- A token named after its value (`--blue-500`) used as a semantic role
- A component reading a primitive directly, or holding its own hex value
- A dark-mode variant implemented by duplicating a component
- A theme switch that needs JavaScript to recolour anything already on screen
- Contrast checked at review time, so the fix is a redesign rather than a value change
- A new grey, a fourth radius, or a one-off spacing value added "just here"
- Tokens declared but not enforced, so both systems run at once

## Verification
- [ ] Every colour, spacing, radius and type value in new code is a token
- [ ] Token names describe role; no value words outside the primitive tier
- [ ] Switching the root theme attribute recolours the whole surface with no component change
- [ ] Every foreground/background pair in the declaration meets its contrast ratio
- [ ] A raw hex added to a component fails lint or review, not just taste
- [ ] The declaration file exists and matches what the code actually does

## References
- `references/token-architecture.md` — the three tiers, naming, and theming mechanics in CSS
- `references/contrast.md` — pairing tokens, the ratios, and checking them as you define
- `references/adoption.md` — introducing tokens into a codebase that already has values

## Bundle contents
- `templates/design-system-declaration.md` — the declaration filled in at step 2

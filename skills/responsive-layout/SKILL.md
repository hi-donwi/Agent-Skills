---
name: responsive-layout
description: >-
  Build layouts that adapt to their space: intrinsic sizing, container queries, fluid type and
  spacing with clamp(), logical properties for RTL, mobile viewports, touch targets. Use when
  a component must work in several contexts or a layout breaks at a width. Do not use for
  colours and scales (design-tokens), decomposition (frontend-ui-engineering), or page audits
  (accessibility-audit).
metadata:
  pack: web
  keywords: responsive, breakpoint, media query, container query, mobile, tablet, desktop, viewport, layout, grid, flexbox, fluid, clamp, rem, zoom, reflow, rtl, right to left, logical properties, touch target, tap target, safe area, dvh, vh, small screen, wide screen, wrap, overflow, phone, sidebar, narrow, wide, screen size, device, shrink, squeeze, horizontal scroll
---

# Responsive Layout

## Overview

Responsive stopped meaning "reacts to the viewport" once a component could be placed in a
sidebar, a grid cell and a modal on the same page. A layout that only knows the window size
cannot be right in all three, and the usual repair — a `variant` prop per context — is how
a component library acquires props nobody can remember.

## When to use
- A component appears in more than one container width
- A layout breaks at some width, at 200% zoom, or with long real content
- Adding or arguing about breakpoints
- Supporting right-to-left, or a language whose strings are much longer
- Mobile bugs involving viewport height, safe areas, or hit targets

## Hand off when
| Need | Skill |
|---|---|
| The scale values themselves, and theming | `design-tokens` |
| Splitting or composing the component | `frontend-ui-engineering` |
| Verifying a built page against WCAG | `accessibility-audit` |

## Process

1. **Let content size itself before writing a query.** `minmax()`, `auto-fit`, `flex-wrap`
   and `min()`/`max()` handle most layouts with no breakpoint at all. A layout with no
   query cannot break at a width nobody tested.
2. **Query the container, not the viewport, for anything reusable.** A card decides its own
   layout from the space it was given. Viewport queries belong to the page shell — the
   thing that actually knows about the window.
3. **Make type and space fluid with `clamp()`**, bounded at both ends. Steps between two
   fixed sizes leave every width in between slightly wrong.
4. **Use logical properties throughout** — `margin-inline-start`, `padding-block`,
   `inset-inline` — so a right-to-left locale is a `dir` attribute rather than a stylesheet.
5. **Use breakpoints last, and only for genuine layout changes**, not for fitting numbers.
   Each one is a width someone has to test forever.
6. **Size the viewport in `dvh`/`svh`, not `vh`**, and respect safe areas. `100vh` is
   wrong on every mobile browser with a retracting toolbar.
7. **Give interactive things a 24×24 CSS px minimum target** (44×44 for anything primary
   on touch), padding the target rather than growing the glyph.
8. **Test against content, not only widths.** The longest real string, the empty state, a
   2.5× word-length translation, and 200% zoom break more layouts than any device width.

## Red flags
- A `variant` or `size` prop that exists only because the component cannot read its container
- A media query inside a reusable component
- `100vh` on a mobile layout; content cut off behind a browser toolbar
- `margin-left` / `padding-right` in a codebase that must support RTL
- Font sizes that step at breakpoints instead of scaling
- A breakpoint added to fix one number's overflow
- Fixed heights on anything containing text
- Tap targets smaller than 24px, or spaced closer than their own size
- `clamp()` with no lower bound, so zooming stops scaling the text

## Verification
- [ ] Reusable components respond to container width, not window width
- [ ] Layout holds at 320px, at 2560px, and at every width between — resize continuously
- [ ] Layout holds at 200% browser zoom and at 400% (WCAG 1.4.10 reflow)
- [ ] No horizontal scroll at 320px
- [ ] Longest real content and the empty state both render correctly
- [ ] `dir="rtl"` on the root mirrors the layout with no stylesheet change
- [ ] Mobile: full-height surfaces are not clipped by the browser toolbar
- [ ] Interactive targets are at least 24×24px with adequate spacing

## References
- `references/intrinsic-and-container.md` — auto-fit/minmax, container queries, subgrid, `:has()`
- `references/fluid-type-and-space.md` — the clamp() formula, scales, and the zoom trap
- `references/viewport-touch-and-rtl.md` — dvh/svh, safe areas, target sizing, logical properties

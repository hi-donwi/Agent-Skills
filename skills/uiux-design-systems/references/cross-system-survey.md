# Cross-system survey

Load when deciding which published system to borrow from, or when checking a claim about
one. Facts below were verified against each system's official documentation in October
2026; anything that could not be verified from a primary source is marked so.

The systems move. Verify a threshold before it lands in a declaration — the list of
official sources at the end is the check, not this file.

## Which system for which context

| Context | Lean on | Why |
|---|---|---|
| Native iOS / macOS / visionOS | Apple HIG | Platform conventions, Dynamic Type, materials, 44 pt targets |
| Android, or expressive cross-platform web | Material 3 (M3) | HCT color science, tonal elevation, shape scale, 48 dp targets |
| B2B consoles, data-dense admin | Atlassian, IBM Carbon | Density modes, 8px grid, intent-weighted tokens, layering |
| Developer tools, docs, code UI | GitHub Primer | Foreground/border semantics, high-contrast and CVD palettes |
| Dashboards and enterprise forms, full widget coverage | Ant Design | Algorithmic color from a seed, dense widget catalog |
| Creative pro tools | Adobe Spectrum 2 + React Aria | Token tiers, headless interaction behavior |
| Microsoft ecosystem (Teams/Office/Windows) | Fluent 2 | Global + alias tokens, light/dark/high-contrast theming |
| E-commerce storefront | Shopify Polaris | Merchant conventions; note current material is web-component centric |
| Neutral modern web-app stack | shadcn/ui + Radix + Tailwind v4 | OKLCH tokens, headless behavior, no vendor lock-in |

## Apple Human Interface Guidelines

- Core principles: clarity, deference, depth.
- Typography: SF Pro with dynamic optical sizing (one continuous design joining Text and
  Display); Dynamic Type is a systemwide user setting every layout must survive.
- Color: system semantic colors that adapt to appearance and context; dark mode is an
  inversion, not a literal swap.
- Depth: translucent materials (blur) plus vibrancy keep foreground content legible over
  materials — not an invitation to blur everything.
- Buttons: minimum hit region 44 × 44 pt (60 × 60 pt recommended on visionOS).
- Layout: respect safe-area insets; smooth continuous-curvature corner geometry.

## Material 3 (M3)

- Color: HCT (hue, chroma, tone based on CAM16 + L*) perceptual space; five tonal palettes;
  scheme roles like `primary` / `onPrimary` / `surface`; dynamic color derives a scheme
  from the user's wallpaper on Android 12+.
- Elevation: tonal overlay from a color slot (typically `primary`) in addition to shadows.
- Shape scale: extra-small to extra-large classes (example radii 4/8/12/16/24 dp) — values
  are examples, the classes are the portable idea.
- Type scale: 15 named styles across display / headline / title / body / label, each in
  large, medium, and small.
- Touch: 48 × 48 dp minimum interactive target.
- Motion: M3 Expressive introduces a physics-based (spring) motion system alongside
  duration/easing tokens.
- Adaptive: window size classes — compact < 600dp, medium 600-840, expanded 840-1200,
  large 1200-1600, extra-large ≥ 1600dp — computed from available window area, not device
  model. Canonical layouts: list-detail, supporting pane, feed.

## Atlassian Design System (B2B reference)

- Token naming (verified): color tokens read `color.[property].[role].[emphasis]` with an
  interaction-state suffix where applicable — e.g. `color.background.brand.bold`. The
  widely-quoted `[foundation].[property].[variant].[state]` formula is **not** the
  documented convention; write `color.border.input.pressed`, not `foundation.border.variant`.
- Typography: Atlassian Sans and Atlassian Mono for product; Charlie for brand.
- Spacing: 8 px base unit (`space.100`) with fractional companions (2, 4, 6, 12 px).
- Density and microcopy: sellable enterprise conventions (comfortable vs compact modes,
  message standards) — verify the current content guidance at atlassian.design before
  citing specifics.

## The rest, briefly

- **GitHub Primer** — token names encode category, property, and state
  (`button-primary-bgColor-hover`); ships light/dark/dimmed/high-contrast and colorblind
  variants. Dev-tool default.
- **Ant Design** — 60+ component catalog, algorithmic color generation from a seed color;
  pragmatics choice for admin consoles.
- **Adobe Spectrum 2** — tokens split primitive / semantic / component tiers; React
  Spectrum 2 pairs with React Aria + React Stately for headless behavior.
- **Microsoft Fluent 2** — global tokens (raw values) beneath alias tokens (semantic
  meaning); light/dark/high-contrast/brand theming; Griffel CSS-in-JS.
- **Shopify Polaris** — now a web-components-first framework; the standalone token repo is
  marked legacy. Treat older token-architecture summaries as dated.
- **IBM Carbon** — role-based tokens, consistent roles across themes; layering model
  differs per theme; ships a strong AI/enterprise guidance set.

## Support scales worth adopting

- **Radix Colors** — 12 steps per hue with a defined job per step: 1-2 backgrounds,
  3-5 component backgrounds (normal / hover / pressed), 6-8 borders (subtle / interactive /
  focus), 9-10 solid fills, 11-12 low- and high-contrast text. Step 9 is the scale's most
  saturated color; text contrast varies by hue, so check pairs rather than trusting the
  table.
- **Open Props** — ready-made primitive scale for spacing/type when a team has no tokens yet.
- **W3C Design Tokens CG** — the DTCG Format 2025.10 is the first stable interchange format
  for tokens between tools (a Community Group Final Report, not a W3C Recommendation).
  Use it when tokens must move between design tools and code.

## Sources (official, checked 2026-10)

| Source | URL |
|---|---|
| Apple HIG | https://developer.apple.com/design/human-interface-guidelines/ |
| Material 3 | https://m3.material.io/ · https://developer.android.com/develop/ui/compose/designsystems/material3 |
| Window size classes | https://developer.android.com/develop/ui/compose/layouts/adaptive/use-window-size-classes |
| Canonical layouts | https://developer.android.com/develop/ui/compose/layouts/adaptive/canonical-layouts |
| Material color utilities (HCT) | https://github.com/material-foundation/material-color-utilities |
| Atlassian design system | https://atlassian.design/foundations/color · /typography · /spacing · /components/tokens/code |
| Primer primitives | https://primer.style/product/primitives/ |

shadcn/ui, Tailwind v4, Radix primitives and Radix Colors details live in their consumers:
`frontend-ui-engineering` (headless primitives), `design-tokens` (OKLCH, radius math,
12-step scale).

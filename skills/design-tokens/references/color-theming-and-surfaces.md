# Color Theming and Surface Systems

## Overview

A robust color token system separates physical color values from functional design intent. It enables effortless theme switching (light, dark, high contrast, branded), guarantees accessible contrast across surfaces, and replaces fragile drop shadows with systematic tonal elevation.

## 1. Three-Tier Token Architecture

Color tokens must flow strictly in one direction across three layers:

```
[ Primitive Palette ]  -->  [ Semantic Role Tokens ]  -->  [ Component Tokens ]
(Raw color definitions)     (Functional UI intent)         (Component-scoped bindings)
```

### Layer Definitions

1. **Primitive Tokens**:
   - Store raw color values, defined as OKLCH, HSL, or hex scales.
   - Example: `--palette-neutral-900: oklch(0.2 0.01 260);`
   - **Rule**: Never reference primitive tokens directly inside component styling.
2. **Semantic Tokens**:
   - Express functional intent and relationship. This layer rebinds values during theme changes.
   - Example: `--color-surface-canvas: var(--palette-neutral-50);` in light theme; switches to `--palette-neutral-950` in dark theme.
   - **Rule**: Components read semantic tokens as their primary color source.
3. **Component Tokens** (Optional, for complex widgets):
   - Map semantic tokens to specific component slots when variant customization is required.
   - Example: `--button-primary-bg: var(--color-interactive-primary);`

## 2. Functional Intent Naming Rules

Tokens must describe what an element represents, never what hue or hex value it currently has.

| Functional Role | Bad (Value-Based) | Good (Intent-Based) | Description |
|---|---|---|---|
| Background Canvas | `--light-grey`, `--white` | `--color-surface-canvas` | Base application canvas |
| Primary Action | `--blue-600`, `--brand-blue` | `--color-interactive-primary` | Primary interactive trigger |
| Critical / Destructive | `--red-500`, `--danger-red` | `--color-feedback-danger` | Irreversible actions and critical errors |
| Subtle Content | `--grey-400` | `--color-foreground-muted` | Secondary labels, captions, metadata |
| Structural Lines | `--border-grey-200` | `--color-border-subtle` | Dividers and grouping outlines |

## 3. Tonal Surface Hierarchy (Elevation via Luminance)

In light themes, visual elevation is traditionally conveyed through drop shadows. In dark themes, shadows disappear against dark backgrounds. Modern design systems solve this through tonal surface layering: higher surfaces have higher relative luminance in dark mode.

### Tonal Elevation Levels

| Level | Token Name | Light Theme Behavior | Dark Theme Behavior | Component Examples |
|---|---|---|---|---|
| **Level 0** | `--color-surface-canvas` | Pure canvas / lightest | Darkest background (lowest luminance) | Page body, window background |
| **Level 1** | `--color-surface-container-low` | Subtle container contrast | Base + 3% lightness | Full-width bands, secondary sidebars |
| **Level 2** | `--color-surface-container` | Standard surface | Base + 6% lightness | Cards, table containers, content groups |
| **Level 3** | `--color-surface-container-high` | Raised surface + subtle shadow | Base + 9% lightness | Floating action bars, elevated cards |
| **Level 4** | `--color-surface-container-highest` | Distinct raised overlay | Base + 12% lightness | Dropdowns, flyouts, popovers |
| **Level 5** | `--color-surface-overlay` | Prominent overlay + scrim | Base + 16% lightness | Modals, full dialog sheets, drawer overlays |

## 4. Theme Switching Implementation

Theme switching should execute via a single root attribute without requiring full component re-rendering or client-side JavaScript recalculations.

```css
:root {
  color-scheme: light;
  --color-surface-canvas: #ffffff;
  --color-surface-container: #f4f4f5;
  --color-foreground-primary: #18181b;
  --color-foreground-muted: #71717a;
  --color-border-subtle: #e4e4e7;
  --color-interactive-primary: #2563eb;
}

[data-theme="dark"] {
  color-scheme: dark;
  --color-surface-canvas: #09090b;
  --color-surface-container: #18181b;
  --color-foreground-primary: #fafafa;
  --color-foreground-muted: #a1a1aa;
  --color-border-subtle: #27272a;
  --color-interactive-primary: #3b82f6;
}

@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    color-scheme: dark;
    --color-surface-canvas: #09090b;
    --color-surface-container: #18181b;
    --color-foreground-primary: #fafafa;
    --color-foreground-muted: #a1a1aa;
    --color-border-subtle: #27272a;
    --color-interactive-primary: #3b82f6;
  }
}
```

## 5. Contrast Invariants and Perceptual Uniformity

1. **Text Contrast**: Normal text (under 24px regular or under 19px bold) must maintain a minimum contrast ratio of 4.5:1 against its immediate surface container. Large text must meet at least 3.0:1.
2. **UI Boundary Contrast**: Interactive element borders, checkboxes, radio rings, and focus indicators must maintain at least 3.0:1 contrast against adjacent background colors.
3. **Perceptually Uniform Color Spaces**: When synthesizing shades programmatically (e.g., hover states or active tints), use `color-mix()` in `oklch` rather than sRGB to prevent muddy saturation loss or unpredictable lightness shifts:

```css
:root {
  --color-button-hover: color-mix(in oklch, var(--color-interactive-primary) 85%, black);
}
```

## 6. OKLCH, Pairing Invariants, and Tailwind v4 Exposure

Orthodox current practice, verified against the shadcn/ui theming documentation:

- **Define colors in OKLCH.** Perceptually uniform and P3-ready: `--background: oklch(1 0 0)`. Hold lightness and chroma relationships constant when deriving hover, muted, or dark variants instead of inventing each shade by eye.
- **Every surface token is paired.** Nothing ships as `--primary` alone; each field owns its text and icon partner: `--primary` / `--primary-foreground`, `--card` / `--card-foreground`, `--muted` / `--muted-foreground`. The pair is the invariant — contrast is checked once per pair, never re-argued per component.
- **Expose tokens through Tailwind v4 `@theme inline`.** The inline form maps `--color-primary: var(--primary)` so generated utilities resolve the referenced variable directly and re-theme without a rebuild. Keep tokens as plain custom properties; a config file is a generator, not the source of truth.
- **State derivations use `color-mix()`** in a uniform space at runtime — Tailwind v4 does the same internally for opacity modifiers.

### Radius from one number

A whole radius scale derives from a single base. The shadcn `--radius` scaffold pairs it with `sm` and `md` subtractions and multiplicative variants up the scale (`xl`, `2xl`); declare the multipliers explicitly in the design declaration (for example `sm 0.6x, md 0.8x, lg 1x, xl 1.4x, 2xl 1.8x`) so components cannot choose freehand. One base plus declared derivation is what prevents the three-radius drift.

### A 12-step hue scale assigns a job to every step

Radix Colors' mapping, useful as a starting scale when a palette must span backgrounds, components, borders, and text from one hue:

| Steps | Job |
|---|---|
| 1-2 | Page and subtle backgrounds |
| 3-5 | Component backgrounds: normal, hover, pressed/selected |
| 6-8 | Borders: subtle, interactive hover, focus |
| 9-10 | Solid fill and its hover |
| 11-12 | Low-contrast and high-contrast text on solid fills |

Step 9 is the scale's most saturated color, and text contrast varies by hue — check pairs rather than trusting the table. Promote steps into the semantic tier by renaming to the job (`--color-border-subtle: var(--green-6)`); the numbering is scaffold, not API.

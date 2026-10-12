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

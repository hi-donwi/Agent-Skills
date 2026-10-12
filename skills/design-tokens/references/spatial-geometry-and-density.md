# Spatial Geometry, Density Modes, and Typography

## Overview

Visual consistency relies on predictable spatial geometry and structured typography. Using an 8px grid with a 4px sub-grid prevents random micro-spacing discrepancies, while density modes allow interfaces to balance high-volume data scanning against touch ergonomics.

## 1. The 8pt / 4pt Spatial Grid System

All structural dimensions—layout gaps, container padding, component margins, and card insets—must align with an 8px base grid, supported by a 4px sub-grid for fine alignment.

### Spatial Scale Tokens

| Token | Pixels | Rem (16px base) | Primary Usage |
|---|---|---|---|
| `--space-0` | `0px` | `0rem` | Reset values |
| `--space-1` | `4px` | `0.25rem` | Sub-grid: icon gaps, badge padding, compact border offsets |
| `--space-2` | `8px` | `0.5rem` | Base unit: button internal padding, tight list item gaps |
| `--space-3` | `12px` | `0.75rem` | Input field vertical padding, card micro-insets |
| `--space-4` | `16px` | `1rem` | Standard gutter, card padding, modal content separation |
| `--space-5` | `24px` | `1.5rem` | Section spacing, container padding on tablet |
| `--space-6` | `32px` | `2rem` | Page section headers, card grid gaps |
| `--space-8` | `48px` | `3rem` | Large section dividers, hero element spacing |
| `--space-12` | `64px` | `4rem` | Major landing page vertical rhythm |

## 2. Interface Density Modes

Enterprise software often requires high information density to minimize scrolling across complex tables and dashboards, while consumer or tablet experiences require larger hit targets.

### Density Specifications

```
[ Compact Mode ]        [ Comfortable Mode (Default) ]    [ Relaxed Mode ]
High data density        Standard productivity             Touch-friendly & consumer
Table rows: 32px         Table rows: 48px                  Table rows: 60px
Padding: 6px - 8px       Padding: 12px - 16px              Padding: 20px - 24px
Font: 12px - 13px        Font: 14px - 15px                 Font: 16px - 18px
```

### Applying Density Tokens via Root Attributes

```css
:root {
  --row-height: 48px;
  --cell-padding-y: 12px;
  --cell-padding-x: 16px;
  --font-size-table: 0.875rem; /* 14px */
}

[data-density="compact"] {
  --row-height: 32px;
  --cell-padding-y: 6px;
  --cell-padding-x: 10px;
  --font-size-table: 0.75rem; /* 12px */
}

[data-density="relaxed"] {
  --row-height: 60px;
  --cell-padding-y: 18px;
  --cell-padding-x: 20px;
  --font-size-table: 1rem; /* 16px */
}
```

## 3. Ergonomic Touch Targets

Every interactive element intended for pointer or touch interaction must satisfy physical ergonomics.

### Rules for Hit Targets

1. **Minimum Dimensions**: Interactive targets must occupy at least 44×44 CSS pixels (or 48×48 pixels on mobile primary actions).
2. **Visual Size vs. Hit Size**: When design hierarchy dictates a small icon (such as a 16px or 20px dismiss icon), decouple the visual glyph from its clickable hit area using negative margin compensation or pseudo-elements.

```css
.icon-button {
  position: relative;
  width: 20px;
  height: 20px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

/* Expand touch hit target to 44x44px without changing visual flow */
.icon-button::after {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: 44px;
  height: 44px;
  transform: translate(-50%, -50%);
}
```

## 4. Modular Typography System

Typography must establish clear visual hierarchy through standard functional roles rather than ad-hoc font sizes.

### Typography Scale and Hierarchy

| Role | Size | Line Height | Weight | Usage |
|---|---|---|---|---|
| **Display** | `36px - 48px` | `1.15 - 1.2` | Bold (700) | Marketing headlines, splash metrics |
| **Headline** | `24px - 32px` | `1.25 - 1.3` | SemiBold (600) | Page titles, primary panel headings |
| **Title** | `18px - 20px` | `1.35 - 1.4` | Medium / SemiBold | Card titles, section headers, dialog titles |
| **Body Large** | `16px` | `1.5 - 1.6` | Regular (400) | Lead paragraphs, documentation articles |
| **Body Default** | `14px` | `1.45 - 1.5` | Regular (400) | Primary interface copy, form labels, data rows |
| **Label / Caption** | `12px` | `1.35 - 1.4` | Medium (500) | Badges, metadata tags, helper text, timestamps |

Line height must scale inversely with type size: large display headings require tight leading (1.15–1.25) to avoid gaping vertical gaps, while small body text requires generous leading (1.45–1.6) for comfortable horizontal scanning.

# Motion and Physics Systems

## Overview

Interface motion provides spatial orientation, reinforces cause-and-effect relationships, and confirms user intent. Motion must feel physical, purposeful, and lightweight. Gratuitous, sluggish, or decorative animations degrade operational efficiency and trigger motion sensitivity.

## 1. Spring Physics vs. Fixed Duration Curves

Modern interaction design distinguishes between physics-driven animations (interactive, interruptible, gesture-driven) and duration-based easing transitions (scripted, discrete state toggles).

### Spring Model Parameters

Spring dynamics simulate real-world physical forces using three primary parameters:

| Parameter | Symbol | Interaction Impact |
|---|---|---|
| **Stiffness** | $k$ | Force pulling the element toward its target. Higher values result in faster, crisper movement. |
| **Damping Ratio** | $\zeta$ | Friction suppressing oscillation. Controls bounce and settling behavior. |
| **Mass** | $m$ | Inertia of the moving element. Higher mass creates a heavier, more deliberate feel. |

### Damping Regimes and UI Applications

1. **Critically Damped ($\zeta = 1.0$)**:
   - Zero overshoot or bounce; reaches equilibrium in the minimum possible duration.
   - **Use cases**: Focus rings, selection pills, active tab indicators, primary button presses.
2. **Overdamped ($\zeta > 1.0$)**:
   - Smooth, gentle deceleration with no bounce.
   - **Use cases**: Modal dialogs, bottom sheets, destructive confirmation drawers, utility menus.
3. **Underdamped ($\zeta = 0.7 - 0.85$)**:
   - Subtle, controlled overshoot before settling.
   - **Use cases**: Micro-interactions, toggle switches, badge counters, celebratory feedback. Never use excessive bounce ($\zeta < 0.6$) in utility UI.

## 2. Standard Duration and Easing Tiers

When animating via standard CSS transitions or Web Animations API where spring solvers are unavailable, categorize animations into strict duration tiers.

### Duration Tokens

| Tier | Duration Range | Target Interactions |
|---|---|---|
| **Micro** | `100ms - 150ms` | Hover states, focus indicators, checkbox checks, button presses |
| **Standard** | `200ms - 300ms` | Dropdown menus, tooltips, toast notifications, accordion expand/collapse |
| **Macro** | `350ms - 500ms` | Full-page transitions, modal backdrops, slide-over panels, multi-step wizards |

### Asymmetrical Easing Principle

Entrances and exits require different velocity profiles. Exits should be 25% to 30% faster than entrances because departing content is no longer the focus of user attention.

```css
:root {
  /* Entrance: Fast start, gradual deceleration to rest */
  --ease-enter: cubic-bezier(0.16, 1, 0.3, 1);
  --duration-enter: 250ms;

  /* Exit: Immediate acceleration off-screen */
  --ease-exit: cubic-bezier(0.4, 0, 1, 1);
  --duration-exit: 175ms;

  /* Standard: Symmetrical transition for on-screen movement */
  --ease-standard: cubic-bezier(0.2, 0, 0, 1);
  --duration-standard: 200ms;
}
```

## 3. Compositor-Only Hardware Acceleration

Animations must maintain a consistent 60fps or 120fps frame rate without inducing layout recalculations or paint cycles.

### Property Classification

- **Composited Properties (Safe to animate)**:
  - `transform` (`translate3d`, `scale`, `rotate`)
  - `opacity`
- **Non-Composited Properties (Forbidden in continuous animations)**:
  - Layout triggers: `width`, `height`, `top`, `bottom`, `left`, `right`, `margin`, `padding`
  - Paint triggers: `background-color`, `border-width`, `box-shadow`, `filter`

```css
/* Bad: Causes layout reflow on every frame */
.card-drawer {
  transition: height 300ms ease;
}

/* Good: GPU-accelerated transform */
.card-drawer {
  transform: translateY(100%);
  transition: transform var(--duration-enter) var(--ease-enter);
  will-change: transform;
}

.card-drawer[data-state="open"] {
  transform: translateY(0);
}
```

Use `will-change: transform, opacity` sparingly and remove it when animations are idle to avoid unnecessary GPU memory allocation.

## 4. Reduced Motion Compliance

Respect user system preferences for vestibular safety and accessibility. Do not eliminate interaction feedback entirely; replace physical spatial translation with subtle opacity fades or instantaneous state changes.

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }

  /* Retain accessible opacity fades if immediate changes are disorienting */
  .fade-accessible {
    transition: opacity 100ms linear !important;
  }
}
```

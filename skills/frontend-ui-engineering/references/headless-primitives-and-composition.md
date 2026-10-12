# Headless Primitives, State Modeling, and Composition

## Overview

Modern component architecture isolates behavioral logic and accessibility state from visual presentation. Rather than consuming monolithic styled components that resist theming and customization, systems build upon unstyled headless primitives. These primitives manage state machines, keyboard navigation, focus management, and screen reader announcements, leaving full visual authority to the host application.

## 1. State Modeling via Data Attributes

Expose component state directly on DOM elements using descriptive data attributes rather than transient CSS class toggles. This establishes a clean interface between runtime behavior and styling rules.

### Standard Data Attributes

| Attribute | Typical Values | Meaning |
|---|---|---|
| `data-state` | `open`, `closed`, `checked`, `unchecked`, `active`, `inactive` | Primary binary or enumerated component state |
| `data-disabled` | Present (boolean attribute) | Control is non-interactive; omit when enabled |
| `data-highlighted` | Present (boolean attribute) | Item holds virtual keyboard or hover focus |
| `data-orientation` | `horizontal`, `vertical` | Structural direction of composite widgets |
| `data-side` | `top`, `right`, `bottom`, `left` | Position of floating content relative to anchor |
| `data-align` | `start`, `center`, `end` | Cross-axis alignment of floating overlays |

### Styling with State Selectors

Write style rules that target data attributes directly:

```css
.popover-content {
  opacity: 0;
  transform: scale(0.96);
  transition: opacity 150ms ease, transform 150ms ease;
}

.popover-content[data-state="open"] {
  opacity: 1;
  transform: scale(1);
}

.popover-content[data-state="closed"] {
  opacity: 0;
  transform: scale(0.96);
}

.menu-item[data-highlighted] {
  background-color: var(--color-surface-hover);
  color: var(--color-foreground-strong);
}

.menu-item[data-disabled] {
  opacity: 0.5;
  pointer-events: none;
}
```

## 2. Element Replacement and Composition Pattern

Monolithic components often force extra wrapper `<div>` elements into the DOM, breaking grid tracks, flexbox alignment, and CSS selectors. Use an element replacement or slot pattern to delegate rendering to a direct child element while merging props, event handlers, and references.

### Behavior Requirements for Element Delegation

1. **Ref Merging**: Combine internal component refs with consumer refs into a single composite callback or object ref.
2. **Event Handler Chaining**: Execute consumer event handlers first. If the consumer calls `event.preventDefault()`, abort the primitive's default action.
3. **Attribute Merging**: Merge `className` or style objects gracefully, prioritizing consumer overrides where appropriate.
4. **Single Child Invariant**: Enforce that the replacement wrapper receives exactly one valid child element to prevent ambiguous DOM targets.

```tsx
// Pattern: Delegating interaction props to an existing button or anchor
<DialogTrigger asChild>
  <button type="button" className="btn-primary">
    Launch Workspace
  </button>
</DialogTrigger>
```

## 3. Anchor Positioning and Collision Detection

Floating UI surfaces (dropdowns, tooltips, popovers, context menus) must position reliably relative to trigger elements while respecting viewport boundaries.

### Positioning Rules

1. **Portal Mounting**: Render floating overlays into a top-level container (such as a portal element attached to `document.body`) to escape parent `overflow: hidden`, `z-index` stacking contexts, and transform-based clipping.
2. **Anchor Offset**: Maintain a standard spacing gap (e.g., 4px or 8px) between the anchor boundary and floating content.
3. **Collision Detection**: Detect viewport edges and shift the surface inward by a minimum safe margin (e.g., 8px padding from viewport edges).
4. **Directional Flip**: When space in the preferred direction is insufficient, flip to the opposing side before compressing dimensions.
5. **Transform Origin Alignment**: Anchor the CSS transform origin to the collision side to ensure scale animations expand away from the trigger.

```css
.tooltip[data-side="top"] {
  transform-origin: bottom center;
}

.tooltip[data-side="bottom"] {
  transform-origin: top center;
}
```

## 4. Exit Animations and Unmount Lifecycle

A common failure mode in declarative component trees is abrupt unmounting: when component state becomes `closed`, removing the element immediately from the DOM cancels exit animations.

### Handling Exit Lifecycles

1. **Delayed Unmount**: Primitives should retain the DOM node during the exit animation, watching for animation or transition completion events (`animationend`, `transitionend`) before detaching.
2. **Keyframe Animations via Data State**: Define paired enter and exit keyframes bound to `[data-state]`:

```css
@keyframes overlay-enter {
  from { opacity: 0; transform: translateY(-4px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes overlay-exit {
  from { opacity: 1; transform: translateY(0); }
  to { opacity: 0; transform: translateY(-4px); }
}

.modal-sheet[data-state="open"] {
  animation: overlay-enter 200ms cubic-bezier(0.16, 1, 0.3, 1);
}

.modal-sheet[data-state="closed"] {
  animation: overlay-exit 150ms cubic-bezier(0.4, 0, 1, 1);
}
```

3. **Explicit Persistent Mount**: When animating via external physics animation drivers, provide a persistent-mount flag (`forceMount`) so the external driver retains full control over the unmount lifecycle.

## 5. Keyboard Navigation and Focus Trapping

Accessible interactive widgets must strictly follow established keyboard interaction specifications.

- **Focus Trapping**: Modals and full-screen dialogs must trap keyboard focus within the dialog container while open, looping focus between the first and last tabbable elements.
- **Roving Tabindex**: Menus, toolbars, and tab lists use a single tab stop (`tabIndex={0}` on the currently active item, `tabIndex={-1}` on all other items). Arrow keys update the active index and shift focus programmatically.
- **Escape Dismissal**: Pressing the `Escape` key must immediately close open floating panels and restore focus to the originating trigger element.
- **Initial Focus Target**: Direct focus to the first interactive field upon mount, or to the close button if no inputs are present. Avoid placing focus on non-interactive static text.

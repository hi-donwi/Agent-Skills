# Viewport units, touch targets, and writing direction

Load for the three things that only break on real devices and in real locales, and so
survive desktop review.

## Mobile viewport units

`100vh` is the *largest* viewport height — the window with the browser toolbar retracted.
On every mobile browser with a retracting toolbar, a `100vh` surface is taller than what is
visible when the page loads, so the bottom is cut off exactly when it matters: the submit
button, the last row, the sticky footer.

| Unit | Means | Use for |
|---|---|---|
| `svh` | Small — toolbar shown | Anything that must fit on load |
| `lvh` | Large — toolbar hidden | Rarely; equals the old `vh` |
| `dvh` | Dynamic — current state | Full-height panels, drawers, modals |

```css
.drawer { block-size: 100dvh; }
.hero   { min-block-size: 100svh; }   /* fits before the toolbar retracts */
```

`dvh` reflows as the toolbar moves, which is correct for a drawer and distracting for a
hero — hence the split above. There are `vw` equivalents (`svw`, `dvw`), rarely needed.

## Safe areas

Notches, rounded corners and home indicators overlap content. The environment variables
give the inset, and they are zero on hardware without one, so they are safe to apply
unconditionally:

```css
.app-bar {
  padding-inline: max(var(--space-gutter), env(safe-area-inset-left));
  padding-block-end: env(safe-area-inset-bottom);
}
```

This needs `viewport-fit=cover` in the viewport meta tag, or the insets stay zero and the
browser letterboxes instead.

## Touch targets

| Standard | Minimum | Applies to |
|---|---|---|
| WCAG 2.2 SC 2.5.8 (AA) | 24×24 CSS px | Everything interactive |
| WCAG 2.2 SC 2.5.5 (AAA) | 44×44 CSS px | Everything interactive |
| Practical floor for primary touch actions | 44×44 | Buttons, nav, form controls |

Grow the target, not the glyph. Padding, or a pseudo-element that extends the hit area
without changing the layout:

```css
.icon-button {
  position: relative;
  inline-size: 1.5rem;
  block-size: 1.5rem;
}
.icon-button::after {       /* 44px target around a 24px icon */
  content: "";
  position: absolute;
  inset: -0.625rem;
}
```

Spacing counts as much as size: two 44px buttons touching are one 88px mistarget. Keep at
least 8px between adjacent targets, more for destructive actions.

The 24px exception for inline links in a paragraph is real — do not pad text links into
the line above.

## Pointer type, not screen size

Screen width has never meant touch. A laptop with a touchscreen, a tablet with a mouse and a
desktop with both all exist. Ask about the pointer:

```css
@media (pointer: coarse) { .icon-button::after { inset: -0.75rem; } }
@media (hover: none)     { .tooltip-on-hover { display: none; } }
```

Anything reachable only on hover is unreachable on touch. That is a functional bug, not a
styling one.

## Logical properties and RTL

Physical properties encode a reading direction into the stylesheet. Logical ones do not, so
right-to-left becomes `dir="rtl"` on the root and nothing else.

| Physical | Logical |
|---|---|
| `margin-left` / `margin-right` | `margin-inline-start` / `margin-inline-end` |
| `padding-top` / `padding-bottom` | `padding-block-start` / `padding-block-end` |
| `width` / `height` | `inline-size` / `block-size` |
| `left` / `right` | `inset-inline-start` / `inset-inline-end` |
| `text-align: left` | `text-align: start` |
| `border-left` | `border-inline-start` |

Flexbox and grid are already logical: `flex-direction: row` follows the writing mode, and
`justify-content: flex-start` means the start edge, not the left one. Most of a modern
layout is direction-agnostic before you begin.

What stays physical on purpose:

- Icons that mean direction — a "next" chevron must mirror; a play button must not.
  Mirror deliberately with `transform: scaleX(-1)` under `[dir="rtl"]`, one icon at a time.
- Box shadows and gradients with a light source, which is physical.
- Anything anchored to a real-world orientation, like a signature line.

Numerals, code and Latin-script names stay left-to-right inside RTL text; the browser's
bidi algorithm handles that as long as the text is not broken into separate elements
mid-phrase. Concatenating a translated string with a value in markup is what breaks it.

## Testing

- Resize continuously rather than at named widths. Breakage lives between breakpoints.
- Zoom to 200% and 400%; at 400% a 1280px viewport behaves like 320px (WCAG 1.4.10).
- Set `dir="rtl"` on `<html>` and look for anything that did not mirror.
- Use a real phone for viewport-height and safe-area behaviour. Emulators do not retract a
  toolbar, which is the bug you are looking for.

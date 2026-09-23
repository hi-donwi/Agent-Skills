# The audit procedure

Load when running the audit. Each pass is listed with what to do and what it catches that
the others cannot.

## 1. Keyboard only

Put the mouse away. `Tab` forward, `Shift+Tab` back, `Enter`/`Space` to activate, arrow keys
inside composite widgets, `Esc` to dismiss.

- Can every control be reached?
- Can every control be operated — including menus, tabs, sliders, date pickers?
- Does the order follow the visual order?
- Does focus ever land somewhere invisible, or leave the viewport without scrolling?
- Can you get *out* of every widget, or does something trap you?
- Does a skip link exist, and does it work, on a page with substantial repeated navigation?

Catches: unreachable controls, custom widgets with no key handling, focus traps, DOM order
diverging from visual order after a CSS reorder. None of these are reliably automatable.

## 2. Structure

View the page with CSS disabled, or read the accessibility tree in DevTools.

- One `h1`; heading levels descend without skipping
- `header`/`nav`/`main`/`aside`/`footer` present, one `main`
- Lists are `ul`/`ol`, tables have `th` with `scope`, captions where the table needs one
- Reading order still makes sense

Catches: headings chosen for size rather than rank, a layout whose meaning lives entirely in
CSS, tables used for layout.

## 3. Names and roles

For each control, read its accessible name in the DevTools accessibility pane.

- Does the name say what the control *does*, not what it looks like?
- Icon-only buttons: `aria-label`, or visually-hidden text
- Inputs: a `<label for>`, not a placeholder
- Links: the text makes sense out of context — screen reader users list links
- Native element preferred over `role`

Common trap: `aria-label` overrides visible text entirely. A button reading "Save" with
`aria-label="Submit form"` is announced as "Submit form", and a speech-control user saying
"click Save" gets nothing (WCAG 2.5.3, label in name).

## 4. Focus

- Every focusable element has a visible indicator, 3:1 against its surroundings
- `:focus-visible` for the styling, so a mouse click does not draw a ring but a key does
- Opening a dialog moves focus into it; closing returns focus to the trigger
- Focus is never placed on a non-interactive element without a reason
- Nothing scrolls focus out of view behind a sticky header

```css
:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}
```

Never `outline: none` alone. If the design rejects the default ring, replace it — do not
delete it.

## 5. Colour and contrast

Text 4.5:1, large text (≥24px, or ≥19px bold) 3:1, UI boundaries and meaningful icons 3:1.
Then the part tooling cannot do: screenshot the surface in greyscale. Every piece of
information still distinguishable? A required-field marker, a validity state, a chart
series, a status dot — if it disappears in greyscale, it needs a second signal.

## 6. Motion and zoom

- Set `prefers-reduced-motion: reduce` in DevTools rendering settings. Do animations stop,
  or at least become non-vestibular? Parallax, auto-advancing carousels and large-scale
  movement are the risky ones.
- Anything that moves or auto-updates for more than five seconds has a pause control.
- Zoom to 200%: text is readable, nothing overlaps.
- Zoom to 400% on a 1280px viewport: content reflows to a single column, no horizontal
  scroll, nothing clipped (WCAG 1.4.10).
- Increase text size only, without zoom, to 200% (WCAG 1.4.4) — fixed-height containers
  clip here.

## 7. Dynamic behaviour

- Form errors: announced, associated with the field, and described in text
- A status change — saved, deleted, loading finished — reaches a live region
- The live region exists in the DOM *before* the message is written into it; a region added
  at the same moment announces nothing
- `aria-busy` on a region being replaced
- Route changes in a single-page app move focus and announce the new page

## 8. Automated scan

Now run it.

```bash
npx @axe-core/cli http://localhost:3000 --tags wcag2a,wcag2aa,wcag22aa
```

Or in the browser: the axe DevTools extension, or Lighthouse's accessibility category.

Triage each result. A "serious" rule violation on a decorative element may be noise; a
"minor" one may be a symptom of a structural problem. Do not auto-fix — an `aria-label`
added to silence a rule is how a control ends up with a name nobody chose.

## 9. Report

Group by user impact, not by rule:

| Impact | Meaning | Example |
|---|---|---|
| Blocker | A task cannot be completed | Checkout unreachable by keyboard |
| Serious | A task is much harder | Errors not announced; user cannot tell what failed |
| Moderate | Confusing but workable | Heading levels skipped |
| Minor | Polish | Decorative icon missing `aria-hidden` |

Each finding: what happens, who it affects, the WCAG criterion, and a concrete fix. A
finding with no fix is a complaint.

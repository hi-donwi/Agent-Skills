# Assistive technology and user settings

Load when you need to check behaviour rather than markup — what a real screen reader
announces, and what happens under the settings readers actually use.

## Screen readers

You do not need to be fluent. Ten minutes with one finds defects no scanner reports.

| Reader | Platform | Start | Stop |
|---|---|---|---|
| VoiceOver | macOS, built in | `Cmd+F5` | `Cmd+F5` |
| VoiceOver | iOS, built in | Triple-click side button (once enabled) | same |
| NVDA | Windows, free | `Ctrl+Alt+N` | `Insert+Q` |
| TalkBack | Android, built in | Volume-key shortcut | same |

Pair with the browser each is usually used with: VoiceOver with Safari, NVDA with Firefox or
Chrome. Behaviour differs between pairings, and testing the unusual pairing produces bugs
nobody experiences.

VoiceOver essentials: `Ctrl+Option` is the modifier. `Ctrl+Option+→` reads the next item.
`Ctrl+Option+U` opens the rotor — the list of headings, links, landmarks and form controls.
The rotor is the fastest audit tool available: if the heading list is nonsense or the link
list is twelve "Read more", you have found a defect without reading a line of markup.

What to listen for:

- Does each control announce a name, a role, and its state?
- Is a group of controls announced as a group, or as loose items?
- When something changes on screen, is anything said at all?
- Does the reading order match the visual order?
- Are there items announced that should not exist — decorative images, duplicated labels?

## Reduced motion

DevTools → Rendering → "Emulate CSS media feature prefers-reduced-motion".

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

A blanket reset is an acceptable baseline, not a finished answer: it removes motion that
carried meaning as well as motion that was decoration. Prefer replacing a movement with a
fade where the movement told the reader something.

The risky patterns are vestibular: parallax, large-scale zoom or spin, movement across a
significant portion of the screen, and anything auto-advancing. A small fade or a colour
transition is generally fine.

Reduced motion is about motion, not about disabling all feedback. Removing a loading
indicator because it animates makes the interface worse.

## Forced colors

Windows high-contrast mode replaces the palette outright. DevTools → Rendering → "Emulate
CSS media feature forced-colors".

What breaks: anything whose meaning was carried by `background-color` alone, borders removed
in favour of background contrast, and images of text.

```css
@media (forced-colors: active) {
  .badge  { border: 1px solid CanvasText; }
  .button { forced-color-adjust: none; }   /* only where the brand colour is the meaning */
}
```

Use `forced-color-adjust: none` sparingly — it opts out of the reader's own contrast choice,
which is usually the opposite of what they asked for.

## Zoom and text size

Two different requirements, frequently conflated:

- **Page zoom to 400%** (WCAG 1.4.10 Reflow). A 1280px viewport at 400% behaves like 320px.
  Content must reflow to one column with no horizontal scroll. Test with `Cmd/Ctrl +`.
- **Text size to 200%** (WCAG 1.4.4 Resize Text) with no page zoom. Firefox can do text-only
  zoom; or set the browser's default font size to 32px. This is where fixed-height
  containers clip and `px` font sizes refuse to grow.

A layout can pass one and fail the other, so check both.

## Voice control

Dragon, Voice Control and Voice Access all work by the visible label. A control whose
accessible name does not start with its visible text cannot be activated by saying what is
on it — which is WCAG 2.5.3 and the reason an `aria-label` should extend visible text
rather than replace it.

## What automation is for

Run axe in CI to stop regressions on things machines judge reliably: contrast values,
missing `alt`, duplicate ids, invalid ARIA attributes, form controls with no label. That is
a floor, not an audit. Keyboard operation, announcement quality, focus order and whether the
content makes sense remain human passes.

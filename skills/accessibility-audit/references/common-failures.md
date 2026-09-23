# Recurring failures, criterion, and fix

Load when triaging findings. These account for most of what an audit turns up.

| Failure | WCAG | Fix |
|---|---|---|
| `div`/`span` with a click handler | 2.1.1 Keyboard | Use `button` or `a`. If truly impossible: `role`, `tabindex="0"`, and Enter/Space handlers |
| `outline: none` | 2.4.7 Focus Visible | Style `:focus-visible` instead of removing the indicator |
| Icon button with no name | 4.1.2 Name, Role, Value | `aria-label`, or visually-hidden text inside the button |
| Placeholder used as label | 3.3.2 Labels or Instructions | A real `<label for>`; the placeholder is an example, not a name |
| `aria-label` replacing visible text | 2.5.3 Label in Name | Remove it, or make it start with the visible text |
| "Click here" / "Read more" | 2.4.4 Link Purpose | Name the destination, or add visually-hidden context |
| Colour-only validity or status | 1.4.1 Use of Color | Add an icon, text, or shape alongside |
| Contrast below 4.5:1 | 1.4.3 Contrast | Fix at the token level, not per component |
| Image with no `alt` | 1.1.1 Non-text Content | Describe the purpose; `alt=""` if purely decorative |
| Decorative image with descriptive alt | 1.1.1 | `alt=""` plus `aria-hidden="true"` — narrating noise is a defect |
| Heading level chosen for size | 1.3.1 Info and Relationships | Correct the level, style with a class |
| Multiple `h1`, or none | 1.3.1 | One per page, naming the page |
| No landmarks | 1.3.1 | `header`/`nav`/`main`/`footer`; one `main` |
| Dialog leaves focus behind | 2.4.3 Focus Order | Move focus in on open, trap within, restore on close |
| Live region added with its message | 4.1.3 Status Messages | Render the empty region first, write into it after |
| Error not associated with the field | 3.3.1 Error Identification | `aria-describedby` pointing at the message, plus `aria-invalid` |
| Auto-advancing carousel | 2.2.2 Pause, Stop, Hide | Pause control, and stop under `prefers-reduced-motion` |
| Content clipped at 400% zoom | 1.4.10 Reflow | Remove fixed heights; let the layout reflow to one column |
| Text unreadable at 200% text-only zoom | 1.4.4 Resize Text | Use `rem`; avoid fixed-height text containers |
| Tap target under 24px | 2.5.8 Target Size | Pad the target, not the glyph |
| Form control with no visible label | 3.3.2 | Visible labels; floating labels must remain readable when filled |
| Tab order set with positive `tabindex` | 2.4.3 | Use `0` or `-1` and fix the DOM order instead |
| `title` attribute as the only name | 4.1.2 | Not exposed reliably; use a real label |
| Table without headers | 1.3.1 | `th` with `scope`, or `headers`/`id` for complex tables |
| Autoplaying audio | 1.4.2 Audio Control | Do not; if unavoidable, a control within the first tab stop |

## Two that are frequently misread

**Disabled controls are exempt from contrast.** True, and still a trap: a disabled control
nobody can read is a control nobody can tell is disabled. Keep it distinguishable.

**`aria-hidden` does not remove focusability.** An element hidden from the accessibility
tree but still tabbable produces a focus stop that announces nothing — worse than either
state alone. Hide it from both, or neither.

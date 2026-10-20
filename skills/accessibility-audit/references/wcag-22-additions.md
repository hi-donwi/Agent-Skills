# WCAG 2.2 additions

Load when auditing habits were formed on WCAG 2.1 or when a finding cites a 2.x-only
criterion. WCAG 2.2 added nine success criteria; the AA ones are the compliance surface,
the A and AAA ones are still worth checking. Verified against w3.org, October 2026.

| Criterion | Level | Key requirement |
|---|---:|---|
| 2.4.11 Focus Not Obscured (Minimum) | AA | A keyboard-focused component must not be *entirely* hidden by author-created content; at least part stays visible |
| 2.4.12 Focus Not Obscured (Enhanced) | AAA | No part of the focused component may be hidden |
| 2.4.13 Focus Appearance | AAA | Focus indicator area at least as large as a 2-css-px perimeter, with at least 3:1 change between focused/unfocused states |
| 2.5.7 Dragging Movements | AA | Anything operated by dragging works too with a single pointer tap/press — or dragging is essential |
| 2.5.8 Target Size (Minimum) | AA | Pointer targets at least 24 x 24 CSS px, or meet the specified spacing/inline/equivalent exceptions |
| 3.2.6 Consistent Help | A | Help mechanisms (contact, self-help, chat) appear in the same relative order across pages of a set |
| 3.3.7 Redundant Entry | A | Information already provided in the same process is auto-populated or selectable when needed again |
| 3.3.8 Accessible Authentication (Minimum) | AA | No cognitive-function test (password recall, puzzle) without an alternative — paste, password manager, email link, object recognition, or user-supplied content |
| 3.3.9 Accessible Authentication (Enhanced) | AAA | Same, but object recognition and user-supplied non-text content no longer qualify as exceptions |

## Standing thresholds these interact with

- 1.4.3 Contrast (Minimum): 4.5:1 normal text; 3:1 for large text (roughly 18 pt regular or
  14 pt bold). Thresholds, not rounded targets.
- 1.4.11 Non-text Contrast: UI component boundaries and meaningful graphics need 3:1
  against adjacent colours.
- Platform targets sit above the 24 px floor: 44 x 44 pt (Apple), 48 x 48 dp (Material),
  practical web touch 40-44 px. The floor is compliance, not a design goal.

## Where the floor misleads

- **24 px is a legal floor, not an ergonomic target.** Dense desktop toolbars may use 24-32
  px; anything a phone thumb reaches should be 40 px plus.
- **Spacing exceptions do not echo.** An inline target inside text, or a target with 24 px
  clearance to its neighbours, may stay small — verify the exception actually applies
  before waiving a finding.
- **Consistent Help is an order requirement,** not a presence requirement: if a page has
  help at all, its position must not shuffle between pages.

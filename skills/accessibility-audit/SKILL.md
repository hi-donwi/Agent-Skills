---
name: accessibility-audit
description: >-
  Audit a built interface against WCAG 2.2 AA and report findings by user impact: keyboard,
  semantics and names, focus, contrast, motion, zoom and reflow, assistive tech. Use when
  checking or fixing accessibility or before shipping a user-facing surface. Do not use for
  building the component (frontend-ui-engineering), the palette (design-tokens), or page-load
  performance (web-perf).
metadata:
  pack: web
  keywords: accessibility, a11y, wcag, screen reader, keyboard, focus, aria, contrast, alt text, landmark, heading order, axe, lighthouse accessibility, voiceover, nvda, talkback, reduced motion, forced colors, tab order, focus trap, audit, colour blind, color blind, announce, assistive
---

# Accessibility Audit

## Overview

Automated tooling finds roughly a third of accessibility defects, and it is the easy third.
The rest are things only operating the interface reveals: a focus order that makes no sense,
a name that reads as "button", an error nobody is told about. So the scan comes last here,
not first.

## When to use
- Asked to audit, check, or fix accessibility on an existing surface
- An accessibility complaint, bug report, or procurement questionnaire arrives
- Before shipping anything user-facing
- An axe/Lighthouse run reported issues and someone must judge them

## Hand off when
| Need | Skill |
|---|---|
| Building or restructuring the component | `frontend-ui-engineering` |
| Fixing contrast at the palette level | `design-tokens` |
| Reflow, zoom, and target sizing as layout work | `responsive-layout` |
| Driving a real browser to reproduce | `webapp-testing` |

## Process

Work in this order. Each pass finds a class of defect the next one cannot see.

1. **Keyboard only.** Unplug the mouse. Tab through the whole surface: can you reach every
   control, operate it, and get back out? Is the order the visual order? Does focus ever
   vanish or get trapped? This single pass finds more than any scanner.
2. **Structure.** Headings in order with no levels skipped, one `h1`, landmarks present,
   lists marked up as lists, tables with headers. Read the page with CSS disabled — if the
   order stops making sense, the DOM order is wrong.
3. **Names and roles.** Every control has an accessible name that says what it does.
   "Button", "link", "Click here" and an unlabelled icon are all the same defect. Prefer a
   native element over a `role`; a `div` with `role="button"` owes you keyboard handling,
   focus and state that the native element gives free.
4. **Focus.** Visible at 3:1 against its surround, never removed without a replacement.
   Moved deliberately when a dialog opens, and restored to the trigger when it closes.
5. **Colour and contrast.** Text 4.5:1, large text and UI boundaries 3:1. Then the harder
   one: every state that colour conveys also carries an icon, a label, or text.
6. **Motion and zoom.** `prefers-reduced-motion` honoured. Readable at 200% zoom and usable
   at 400% with no horizontal scroll and nothing clipped.
7. **Dynamic behaviour.** Loading, error, empty and success states announced, not merely
   rendered. An error that only turns a border red does not exist for a screen-reader user.
8. **Scan last, then judge.** Run axe. Every finding is triaged, not auto-fixed: some are
   false positives and some point at a deeper structural problem than the rule describes.
9. **Report by impact.** "Checkout cannot be completed by keyboard" is a different item from
   "decorative icon missing `aria-hidden`". Order by who is blocked, not by rule count.

## Red flags
- The audit begins and ends with an automated scan
- `outline: none` with no replacement indicator
- `role`/`tabindex` added to a `div` that should have been a `button` or `a`
- `aria-label` on an element that already had visible text, silently replacing it
- Placeholder text used as the label
- A dialog that leaves focus behind it, or does not return focus on close
- `aria-live` on a region that is added to the DOM at the same moment — nothing is announced
- Colour as the only indicator of state, validity, or selection
- Fixing the symptom the rule names instead of the structure that caused it
- "We will do accessibility before launch" — retrofitting costs several times more

## Verification
- [ ] Every interactive element reachable and operable by keyboard alone
- [ ] Focus visible everywhere, order matches the visual order, never trapped
- [ ] Heading outline is correct with no skipped levels; landmarks present
- [ ] Every control has an accessible name that describes its action
- [ ] Contrast passes for text and for UI boundaries; no colour-only signalling
- [ ] State changes and errors are announced, not just rendered
- [ ] Usable at 400% zoom, and with `prefers-reduced-motion` set
- [ ] Walked once with a real screen reader, not only with a scanner
- [ ] Findings are reported by user impact with a concrete fix each

## References
- `references/audit-procedure.md` — the nine passes with exact checks and what each one catches
- `references/common-failures.md` — the recurring defects, their WCAG criterion, and the fix
- `references/assistive-tech.md` — screen readers, reduced motion, forced colors, zoom

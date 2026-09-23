---
name: forms-and-validation
description: >-
  Build forms that are correct, accessible, and recoverable: native controls
  first, one schema validating both client and server, error messages that are
  associated and announced, submit and pending states, and autofill. Use when
  building or fixing any form, input, validation rule, or error display, when a
  submit can be fired twice, or when form errors are invisible to assistive
  technology. Do not use for general component structure
  (frontend-ui-engineering), API contract shape (api-design), or auditing a
  finished page (accessibility-audit).
metadata:
  pack: web
  keywords: form, input, field, label, validation, validate, error message, submit, required, checkbox, radio, select, date picker, file upload, autocomplete, autofill, placeholder, zod, react hook form, schema, double submit, idempotency, multi step, wizard, keyboard submit
---

# Forms and Validation

## Overview

Forms concentrate every hard part of a UI in one place: state, async, error handling,
accessibility and trust. They are also where the most user effort is at stake — a form that
loses what someone typed costs them the whole task, not a click.

## When to use
- Building or changing any form, field, or validation rule
- Errors are shown but not announced, or not associated with their field
- A submit can be fired twice, or the user cannot tell whether it worked
- Validation disagrees between client and server
- Autofill does not work, or mobile shows the wrong keyboard

## Hand off when
| Need | Skill |
|---|---|
| Component decomposition and file layout | `frontend-ui-engineering` |
| Field sizing, wrapping, RTL | `responsive-layout` |
| The request and error contract | `api-design` |
| Auditing the finished page | `accessibility-audit` |

## Process

1. **Native controls first.** `<form>`, `<label>`, `<input>`, `<button type="submit">`.
   They bring keyboard behaviour, autofill, mobile keyboards, password managers and Enter-to-
   submit at no cost. Every custom control re-implements those and usually misses some.
2. **One schema, both sides.** Define the rules once and run them on the client for speed
   and on the server for truth. Two hand-written copies drift, and the drift is a security
   hole rather than an inconvenience.
3. **Validate on blur and on submit, not on every keystroke.** Telling someone their email
   is invalid while they are typing the third character is noise. After a field has errored
   once, re-validating as they fix it is helpful — that is the exception.
4. **Attach the error to the field and announce it.** Visible text beside the input,
   `aria-describedby` pointing at it, `aria-invalid` on the control. Colour alone reaches
   nobody using a screen reader and nobody who cannot distinguish the hue.
5. **Summarise on submit.** On a failed submit, move focus to a summary listing each error
   as a link to its field. Without it a keyboard user tabs the whole form hunting.
6. **Make the pending state real.** Disable submit while in flight, say what is happening,
   and guard the server with an idempotency key — a double-click is not a rare event.
7. **Never lose input.** Preserve values through a failed submit, keep a draft for long
   forms, and warn before discarding unsaved changes.
8. **Help the browser help the user.** Correct `type`, `inputmode`, and `autocomplete`
   tokens. This is minutes of work and removes most of the typing on mobile.
9. **Write messages people can act on.** Say what is wrong and what to do: "Password needs
   at least 8 characters", not "Invalid input". Keep them whole sentences for translation,
   not fragments concatenated in code.

## Red flags
- Placeholder used instead of a label — it disappears exactly when it is needed
- Validation on every keystroke, or errors shown before the field is touched
- Errors rendered only as a red border or red text
- Client-side rules the server does not enforce
- A submit button outside the `<form>`, or a `div` acting as one — Enter stops working
- `preventDefault` with no keyboard path to submit
- Disabling submit until the form is valid, so nothing explains what is missing
- Clearing the form on a failed submit
- Custom select, date or combobox where the native control would do
- `autocomplete="off"` on fields where it helps nobody but the developer
- Messages assembled from fragments, which cannot be translated

## Verification
- [ ] Usable with the keyboard alone, Enter submits, focus order matches the layout
- [ ] Every field has a visible, associated `<label>`
- [ ] Errors carry `aria-invalid` and `aria-describedby`, and are announced
- [ ] A failed submit moves focus to a summary linking each error to its field
- [ ] Client and server enforce the same schema; server rejection is handled
- [ ] Double-clicking submit produces one result
- [ ] Values survive a failed submit; long forms keep a draft
- [ ] Mobile shows the right keyboard; autofill fills the right fields
- [ ] Messages say what to do, and are translatable as whole strings

## References
- `references/schema-and-state.md` — one schema on both sides, field state, submit lifecycle
- `references/errors-and-announcement.md` — associating, announcing, and summarising errors
- `references/inputs.md` — types, inputmode, autocomplete, files, and multi-step forms

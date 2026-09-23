# Input types, autofill, files, and multi-step

Load when choosing the control and its attributes. Most of this is minutes of work that
removes most of the typing.

## Type and inputmode

`type` decides validation and the control; `inputmode` decides the mobile keyboard. They are
not the same, and the common mistake is using `type="number"` for things that are not
quantities.

| Content | `type` | `inputmode` | Note |
|---|---|---|---|
| Email | `email` | `email` | Adds `@` to the keyboard |
| Phone | `tel` | `tel` | Numeric pad; do **not** use `number` |
| URL | `url` | `url` | |
| Quantity | `number` | `numeric` | Spinners; only for real numbers |
| Card number, OTP, postcode | `text` | `numeric` | `number` strips leading zeros and allows `e` |
| Decimal amount | `text` | `decimal` | Locale separators vary; validate, do not coerce in the control |
| Search | `search` | `search` | Clear affordance, "Go" key |
| Password | `password` | — | Offer a visibility toggle |
| Date | `date` | — | Native picker; see below |

`type="number"` on a card number or postcode is a recurring bug: it accepts `e`, `+` and
`-`, strips leading zeros, and scroll-wheels the value while the field has focus.

## Autocomplete

`autocomplete` tokens are a fixed vocabulary, not free text. Correct tokens let password
managers and browser autofill do their job; a wrong one silently disables them.

```html
<input autocomplete="given-name">
<input autocomplete="family-name">
<input autocomplete="email">
<input autocomplete="tel">
<input autocomplete="street-address">
<input autocomplete="postal-code">
<input autocomplete="cc-number">
<input autocomplete="cc-exp">
<input autocomplete="one-time-code">        <!-- iOS/Android read the SMS -->
<input autocomplete="current-password">     <!-- sign in -->
<input autocomplete="new-password">         <!-- sign up and change password -->
```

`current-password` versus `new-password` is what tells a password manager whether to fill or
to offer a generated one. Getting it wrong is why a signup form autofills the old password.

`autocomplete="off"` is honoured inconsistently and mostly harms the user. It has a narrow
legitimate use — a field where a stale value would be actively wrong, such as a one-time
code the browser should not remember. It is not a security measure.

## Dates

The native `type="date"` gives a keyboard-accessible, localised, free picker. Its appearance
cannot be styled much, which is the usual reason teams replace it — a poor trade, because
custom date pickers are among the hardest widgets to make accessible.

Where the design truly requires a custom picker, keep a typed text input alongside it. Many
people type a date faster than they navigate a calendar, and it is the path that works when
the picker does not.

For a date far from today — a birth date — three separate fields (day, month, year) beat a
picker outright. Nobody wants to page back four hundred months.

## File inputs

- Set `accept` so the picker filters, and still validate type and size on the server
- Show the chosen filename; the native control's own text is easy to miss
- Validate size before upload and say the limit in the message
- On failure, keep the rest of the form intact — re-selecting a file is annoying, re-filling
  a form is worse
- Drag-and-drop is an addition to the file input, never a replacement: it is unreachable by
  keyboard on its own

## Multi-step forms

- Show progress: which step, how many, what is left
- Let people go back without losing what they entered
- Validate each step on leaving it, not only at the end
- Persist a draft between steps; a refresh mid-form should not start over
- On the final step, summarise everything with an edit link per section
- Move focus to the new step's heading on each transition, or a screen-reader user is left
  at the bottom of the previous step

## Grouping

Related controls need a group name, or each option is announced without its question:

```html
<fieldset>
  <legend>How should we contact you?</legend>
  <label><input type="radio" name="contact" value="email"> Email</label>
  <label><input type="radio" name="contact" value="phone"> Phone</label>
</fieldset>
```

`fieldset`/`legend` is the native form of this. `role="group"` with `aria-labelledby` is the
equivalent where the styling makes `fieldset` impractical.

Wrapping the input inside its `<label>` makes the whole row clickable and needs no `for`/`id`
pair — useful for checkboxes and radios, where the hit target is otherwise tiny.

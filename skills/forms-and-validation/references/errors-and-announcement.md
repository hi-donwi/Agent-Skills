# Errors: associated, announced, summarised

Load when displaying validation failures. A visible error is the easy half; the half that is
routinely missing is making it exist for someone who cannot see it.

## One field

```html
<div class="field">
  <label for="email">Email address</label>
  <input
    id="email"
    name="email"
    type="email"
    autocomplete="email"
    aria-invalid="true"
    aria-describedby="email-hint email-error"
  >
  <p id="email-hint" class="hint">We use this to send your receipt.</p>
  <p id="email-error" class="error">
    <svg aria-hidden="true" ...></svg>
    Enter a valid email address, like name@example.com
  </p>
</div>
```

Four things are load-bearing:

- **`<label for>`**, not a placeholder. A placeholder vanishes when the field has content —
  precisely when someone re-checking their answer needs the label.
- **`aria-invalid="true"`**, so the state is announced, not only drawn.
- **`aria-describedby`** listing *both* hint and error. It takes multiple ids, space
  separated; the reader hears the hint and the error together.
- **An icon or text alongside the colour.** A red border is invisible to a screen reader and
  ambiguous to a colour-blind reader (WCAG 1.4.1).

Remove `aria-invalid` when the field becomes valid. Leaving it announces an error that is
no longer there.

## The summary on submit

Per-field errors alone leave a keyboard user tabbing the whole form to find what failed. On
a failed submit, render a summary at the top and move focus to it:

```html
<div role="alert" tabindex="-1" class="error-summary" id="error-summary">
  <h2>There are 2 problems with this form</h2>
  <ul>
    <li><a href="#email">Enter a valid email address</a></li>
    <li><a href="#password">Password needs at least 8 characters</a></li>
  </ul>
</div>
```

```ts
summaryRef.current?.focus();   // tabindex="-1" makes this possible
```

Each item links to its field, so the fix is one key away. `role="alert"` announces it;
`tabindex="-1"` allows focus without adding a tab stop.

Do not also move focus to the first invalid field — choose one. Moving focus twice means the
summary is announced and then interrupted.

## Live regions

For status that is not a submit failure — "Draft saved", "Checking availability" — use a
live region:

```html
<p aria-live="polite" id="form-status"></p>
```

The region must be **in the DOM before the message is written into it**. A region created
and populated in the same render announces nothing, because there was no prior state for the
reader to diff against. This is the single most common live-region bug.

`polite` waits for a pause; `assertive` interrupts. Use `assertive` only for something the
user must act on immediately — it cuts off whatever they were listening to.

## Message wording

| Instead of | Write |
|---|---|
| "Invalid input" | "Enter a valid email address, like name@example.com" |
| "Error" | "We could not save your changes. Try again." |
| "Required" | "Enter your full name" |
| "Password does not meet requirements" | "Password needs at least 8 characters" |

Say what is wrong and what to do. Name the field in the summary, because the summary is read
away from it.

Keep each message a whole string. Assembling `field + ' is required'` in code cannot be
translated — word order, grammatical gender and pluralisation all differ by language. Pass
the field name as a parameter into a complete template instead.

## Server errors

A server rejection renders the same way as a client one: same markup, same summary, same
focus move. Map the response's field paths onto the form's fields, and route anything
unmapped to a form-level error rather than discarding it — an error nobody displays is a
form that fails silently.

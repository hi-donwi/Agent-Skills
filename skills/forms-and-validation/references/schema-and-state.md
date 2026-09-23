# One schema, and the state around it

Load when wiring validation and submission. The two ideas here are that the rules live in
one place, and that a field has more states than valid and invalid.

## One schema, both sides

Client validation is a latency optimisation. Server validation is the actual rule. Writing
them twice guarantees they drift, and the drift is a security hole rather than an
inconvenience — the client is the copy an attacker skips.

```ts
// shared/schema/signup.ts — imported by the form and by the route handler
export const signup = z.object({
  email:    z.string().email('Enter a valid email address'),
  password: z.string().min(8, 'Password needs at least 8 characters'),
  age:      z.coerce.number().int().min(13, 'You must be 13 or older'),
});
export type Signup = z.infer<typeof signup>;
```

The message belongs in the schema, so client and server say the same thing.

Rules that cannot be shared — uniqueness, credit limits, anything needing a database — are
server-only by nature. Return them in the same error shape as schema failures so the form
renders them identically, and do not attempt a client-side guess at them.

## Field state

"Valid or invalid" is not enough to decide what to show. The useful states:

| State | Meaning | Show an error? |
|---|---|---|
| Pristine | Never focused | No |
| Touched | Focused and left | Yes, if invalid |
| Dirty | Value changed from initial | — |
| Validating | Async check in flight | Show pending, not an error |
| Invalid | Failed a rule | Yes, once touched |
| Submitted | Form submit attempted | Yes, for every field |

This is what "validate on blur, not on keystroke" means in practice: an error appears when
the field becomes *touched*, and after that it re-evaluates as the user types so they see
the fix land.

## Async validation

A uniqueness check is a request per keystroke if you let it be.

- Debounce, 300–500ms
- Cancel the in-flight request when the value changes again
- Show a pending state on the field, not a spinner over the form
- Never block submit on a pending async check — let it submit and let the server decide

## Submit lifecycle

```
idle → submitting → (success | error) → idle
```

Each transition has a visible consequence:

- **submitting**: the button is disabled and says so ("Saving…"), the form is
  `aria-busy="true"`
- **success**: an announced confirmation, and a decision about where focus goes — usually the
  new content, not back to the form
- **error**: values preserved, focus moved to the error summary, the button re-enabled

Disabling the submit button *until the form is valid* is a different thing and a worse one:
it removes the action that would have explained what is wrong. Keep it enabled and let the
submit produce the summary.

## Double submission

A double-click is not rare, and neither is an impatient retry on a slow connection. Guard on
both sides:

```ts
// client: state guard, not just a disabled attribute
if (status === 'submitting') return;
```

```ts
// server: an idempotency key the client generates once per form instance
const key = request.headers.get('Idempotency-Key');
const existing = await findResultByKey(key);
if (existing) return existing;
```

The client guard handles the fast double-click. The key handles the retry, the flaky
network, and the user who refreshed and resubmitted.

## Never lose input

- Preserve every value through a failed submit. Clearing the form on error is the most
  expensive defect in this document.
- Long or multi-step forms: persist a draft on change, keyed per user and form. `sessionStorage`
  is enough for a single session; the server is needed if the draft should survive a device.
- Warn before navigating away from unsaved changes — `beforeunload` for the browser, a router
  guard for in-app navigation. Warn only when the form is dirty, or the warning becomes noise
  people click through.

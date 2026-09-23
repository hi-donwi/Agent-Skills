# Token architecture

Load when defining the tokens themselves: the tiers, what goes in each, and how theming
works without a component knowing a theme exists.

## The three tiers

| Tier | Holds | Named for | Read by |
|---|---|---|---|
| Primitive | Raw values: `#0b7a3b`, `4px`, `1.25rem` | The value | Semantic tokens only |
| Semantic | A role: surface, danger, gutter, body | The job it does | Components |
| Component | One component's decision | The component and part | That component |

One direction only. A component reading a primitive is the leak that makes a second theme
impossible: the value is now hardcoded in a place no theme switch can reach.

```css
:root {
  /* 1. primitive — the only tier that names a value */
  --green-600: #0b7a3b;
  --grey-050: #f6f7f8;
  --grey-900: #14171a;
  --size-2: 0.5rem;
  --size-4: 1rem;

  /* 2. semantic — the only tier a component should normally read */
  --color-surface: var(--grey-050);
  --color-text: var(--grey-900);
  --color-accent: var(--green-600);
  --space-gutter: var(--size-4);
  --space-inline: var(--size-2);

  /* 3. component — a decision one component owns */
  --button-padding-block: var(--space-inline);
  --button-radius: var(--radius-sm);
}
```

## Naming

Name the role, not the value. `--color-danger` survives a rebrand from red to orange;
`--color-red-600` used as a role becomes a lie the same day, and renaming it touches every
call site.

- Role, not value: `--color-danger`, not `--color-red-600`
- Job, not size: `--space-gutter`, not `--space-16`
- State as a suffix on the role: `--color-accent-hover`, `--color-accent-disabled`
- Keep the scale ordinal, not t-shirt sized, once there are more than five steps —
  `--size-1..12` extends where `--size-md` has nowhere to go

## Theming

One switch at the root redefines the semantic tier. Nothing below it changes.

```css
:root { color-scheme: light; }

@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    color-scheme: dark;
    --color-surface: var(--grey-900);
    --color-text: var(--grey-050);
  }
}

:root[data-theme="dark"] {
  color-scheme: dark;
  --color-surface: var(--grey-900);
  --color-text: var(--grey-050);
}
```

Three declarations rather than one because the three cases are different: the default, the
reader whose OS asks for dark but who has not chosen, and the reader who chose. Guarding
the media query with `:not([data-theme="light"])` is what lets an explicit light choice win
over the OS.

`color-scheme` is not decoration. It tells the browser to render form controls, scrollbars
and the canvas in the matching scheme; without it a dark surface keeps a white scrollbar
and light-rendered native inputs.

`light-dark()` collapses the pair where support allows:

```css
:root {
  color-scheme: light dark;
  --color-surface: light-dark(var(--grey-050), var(--grey-900));
}
```

It is shorter, but it only handles two schemes and it still needs `color-scheme` set. Use
it for a straightforward light/dark pair; use redefinition when a third theme or a brand
switch exists.

## Forced colors

Windows high contrast replaces your palette outright. Do not fight it — check that meaning
survives when it does:

```css
@media (forced-colors: active) {
  .badge { border: 1px solid CanvasText; }  /* restore a boundary the background carried */
}
```

Anything that conveyed state through `background-color` alone disappears here, which is the
same defect that fails a colour-blind reader.

## Where tokens live

CSS custom properties are the portable form: they cascade, they theme at runtime, and they
need no build step. A Tailwind or design-tool config is a generator for them, not a
replacement — emit custom properties from it so runtime theming stays possible.

Do not define tokens in JavaScript and apply them inline. Inline styles cannot be themed,
cannot be overridden by a media query, and defeat the cascade the system depends on.

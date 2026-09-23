# The ladder

Load when placing a specific piece of state. Each rung is listed with what it is for, what
it costs, and the signal that you have outgrown it. Climb only when the signal appears.

## 1. Local — `useState` in the component

For state nothing else needs: an open menu, a hover, an uncontrolled input, a local toggle.

Cost: none. This is the default and most state should stay here.

Outgrown when: a sibling needs to read or write it.

## 2. Lifted — state in the nearest common parent

Two or three siblings share one fact. The parent owns it and passes value and setter down.

Cost: the parent re-renders on every change, and so does everything under it.

Outgrown when: the common parent is more than two or three levels up, or the props pass
through components that ignore them. That is prop drilling, and it is a placement problem,
not a reason to reach for a store — often the right fix is composition:

```tsx
// drilling: Layout does not use `user`, it only forwards it
<Layout user={user}><Page user={user} /></Layout>

// composition: Layout never sees it
<Layout><Page user={user} /></Layout>
```

Passing the element instead of the data removes a whole class of drilling before any
state library is involved.

## 3. URL — `searchParams`, route params

Filters, sort, pagination, the active tab, the open detail id, a search query.

The test is one question: **should the user be able to send this link?** If yes, the URL is
the store. So is the answer to "should refresh keep my place?" and "should back work?".

Cost: values are strings, so they need parsing and validating. Worth it.

```
/orders?status=pending&page=2&sort=-created
```

This rung is the one most often skipped, and skipping it produces the complaint that a
filtered view cannot be shared and the back button does nothing.

Outgrown when: the value is private, large, or changes many times per second.

## 4. Server cache — React Query, SWR, RTK Query, the framework's loader

Anything fetched from a server. See `server-vs-client.md` — this is not a rung so much as a
different axis, and it is listed here because it removes most of what people put in a store.

Cost: a library, and learning its invalidation model.

## 5. Context — `createContext`

Read-heavy, write-rare values needed in many places: theme, locale, current user, a feature
flag set.

Cost: **every consumer re-renders on every change**, regardless of which part it reads.
Context is dependency injection, not a state manager.

Two rules make it safe:

```tsx
// split by change frequency, so a theme change does not wake auth consumers
<ThemeContext.Provider value={theme}>
  <AuthContext.Provider value={auth}>

// and keep the value stable, or every consumer re-renders on every parent render
const value = useMemo(() => ({ user, signOut }), [user, signOut]);
```

An object literal passed straight into `value` is a new object each render. That single
mistake is the usual reason "context is slow".

Outgrown when: it changes often, or consumers need different slices and re-render on all
of them.

## 6. Global store — Zustand, Redux, Jotai, signals

Genuinely app-wide client state that distant trees both read and write: a multi-step wizard
spanning routes, an undo stack, a collaborative cursor, a notification queue.

Cost: indirection. Any component may change it, so tracing why a value changed now means
searching the codebase rather than reading up the tree.

Use it when the alternatives have actually failed, not in anticipation. A store slice that
one component reads and nothing else is local state with extra steps.

## Choosing quickly

| Question | If yes |
|---|---|
| Can it be computed from what you already have? | Compute it — it is not state |
| Does it come from a server? | Server cache |
| Should the link be shareable, or back work? | URL |
| Does only one component use it? | Local |
| Do two or three nearby components use it? | Lift, or compose |
| Is it read everywhere and written rarely? | Context |
| Do distant trees both read and write it, often? | Store |

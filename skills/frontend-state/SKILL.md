---
name: frontend-state
description: >-
  Decide where a piece of frontend state belongs and keep it there: the ladder
  from local to lifted to URL to server cache to global store, separating server
  data from client state, derived values, and untangling state that has spread.
  Use when choosing between useState, context, a URL param, a query cache and a
  global store, when a component re-renders too much, when the same fact is
  stored twice, or when props are drilled through components that ignore them.
  Do not use for component file layout and decomposition
  (frontend-ui-engineering), form field state (forms-and-validation), or
  server-side data contracts (api-design).
metadata:
  pack: web
  keywords: state, state management, usestate, useeffect, context, redux, zustand, jotai, react query, swr, server state, client state, cache, url state, searchparams, prop drilling, drill, lifting state, where should state live, duplicate state, out of sync, derived state, rerender, re-render, global store, single source of truth
---

# Frontend State

## Overview

Where state lives decides more about a frontend's future than any other choice. Put it too
low and it gets lifted, drilled and duplicated; put it too high and every unrelated change
re-renders the app. Most frontends described as spaghetti are not badly written — they are
holding one fact in three places.

## When to use
- Choosing between `useState`, lifted state, context, a URL param, a query cache, a store
- The same fact exists in more than one place and they disagree
- Props passed through components that do not use them
- A component re-renders on changes it does not care about
- Server data kept in a global store and manually refreshed
- A refresh, a shared link, or the back button loses the user's place

## Hand off when
| Need | Skill |
|---|---|
| Splitting the component, file layout | `frontend-ui-engineering` |
| Field state, validation, submit lifecycle | `forms-and-validation` |
| The request and response contract | `api-design` |
| Measuring a render problem before fixing it | `web-perf` |

## Process

1. **Ask whether it is state at all.** If it can be computed from props, existing state, or
   the URL, compute it. Stored derived values are the most common source of two sources of
   truth disagreeing.
2. **Separate server data from client state.** They have different lifecycles: server data
   is a cache of something you do not own, with staleness, refetching and invalidation.
   Client state is yours. Putting server data in a global store means reimplementing a cache
   by hand, badly.
3. **Climb the ladder only as far as needed.** Local → lifted → URL → server cache →
   context → store. Each rung costs coupling; stop at the first that works.
4. **Put shareable state in the URL.** Filters, tabs, pagination, the open item. If a user
   should be able to send the link, refresh, or press back, the URL is the store — and it
   is free.
5. **Use context for read-heavy, write-rare values** — theme, locale, current user. Context
   is a dependency-injection mechanism, not a state manager: every consumer re-renders on
   every change.
6. **Reach for a global store last**, and only for genuinely app-wide client state that
   several distant trees both read and write.
7. **Keep state minimal and normalised.** Store ids, not copies of objects that also live in
   the cache. Two copies drift the moment one is updated.
8. **Co-locate.** State used by one subtree lives in that subtree. Lifting to the root
   "so it is available" is how a root component acquires forty fields.

## Red flags
- `useEffect` that copies a prop into state, then tries to keep them in sync
- Server data in Redux/Zustand with hand-rolled loading and error flags
- Filters or the active tab in component state, so the URL is unshareable
- Context holding a value that changes on every keystroke
- A store slice one component reads and nothing else
- Props threaded through three components that only pass them along
- Derived values stored and recomputed in an effect instead of during render
- `useMemo`/`useCallback` added before anything was measured
- State lifted to the root because two leaves needed it
- The same entity held in a list and again in a "selected" object

## Verification
- [ ] Every piece of state has one owner and one source of truth
- [ ] Derived values are computed, not stored
- [ ] Server data lives in a cache with invalidation, not in a client store
- [ ] Shareable UI state survives refresh, back, and copying the link
- [ ] No effect exists purely to synchronise two pieces of state
- [ ] Context values are stable, or split so a change wakes only its consumers
- [ ] Changing one feature's state does not re-render unrelated trees
- [ ] No prop passes through a component that does not read it

## References
- `references/the-ladder.md` — each rung, what it is for, and the cost of the next one
- `references/server-vs-client.md` — cache semantics, and why server data is not app state
- `references/untangling.md` — diagnosing duplicated state, sync effects, and drilling

# Untangling state that has already spread

Load when the state exists and is wrong. Each section is a symptom, what causes it, and
the repair.

## Symptom: the same fact in two places, and they disagree

The most common shape is an effect copying a prop into state:

```tsx
// wrong — two sources of truth, and a render where they differ
function Profile({ user }) {
  const [name, setName] = useState(user.name);
  useEffect(() => { setName(user.name); }, [user.name]);
```

There is always a render in which `name` is stale, and the bug report is "it shows the old
value for a moment".

Repairs, in order of preference:

1. **Do not copy.** Read `user.name` directly.
2. **Derive during render**, if it needs transforming: `const display = format(user.name)`.
3. **Key the component** if it genuinely must reset on identity change:
   `<Profile key={user.id} user={user} />` — React remounts and the initial state is right
   by construction.
4. **Adjust during render**, for the rare case a library forces:
   ```tsx
   const [prevId, setPrevId] = useState(user.id);
   if (prevId !== user.id) { setPrevId(user.id); setName(user.name); }
   ```
   No effect, no stale render.

## Symptom: a `useEffect` that only calls `setState`

An effect whose entire body synchronises one piece of state with another is a sign the
second one should not exist.

```tsx
// wrong
const [total, setTotal] = useState(0);
useEffect(() => { setTotal(items.reduce(sum, 0)); }, [items]);

// right — it was never state
const total = items.reduce(sum, 0);
```

The wrong version also renders twice per change and shows `0` on the first one.

Effects are for synchronising with something **outside** React — the DOM, a subscription, a
timer, an analytics call. An effect between two React values is almost always a derived
value in disguise.

## Symptom: props passed through components that ignore them

Count the components between owner and consumer that do not read the value. Three or more
is the threshold. The fixes, cheapest first:

1. **Compose** — pass the element, not the data, so intermediates never see it.
2. **Move the state down** — if only one subtree uses it, it was lifted too far.
3. **Context** — only if it is read in many places and written rarely.

Reaching for a store here is the reflex worth resisting: drilling is a placement problem,
and a store hides it rather than fixing it.

## Symptom: a component re-renders on changes it does not care about

Measure before changing anything — React DevTools Profiler, "Highlight updates". Then find
which of these it is:

| Cause | Fix |
|---|---|
| Context value is a new object each render | `useMemo` the value |
| One context carries unrelated concerns | Split by change frequency |
| State lifted higher than its consumers | Move it down |
| A store selector returns a new object | Select primitives, or use a shallow comparator |
| A parent re-renders for unrelated reasons | Composition, or `memo` at the boundary |

`useMemo` and `useCallback` added without a measurement are a cost, not a fix: they each add
a dependency array to keep correct, and a wrong one is a stale-closure bug.

## Symptom: an entity stored twice

A list and a separately-held "selected item" drift the moment one is edited.

```ts
// wrong
{ orders: Order[], selectedOrder: Order }

// right — one copy, one pointer
{ orders: Order[], selectedOrderId: string }
const selected = orders.find(o => o.id === selectedOrderId);
```

Store ids and derive the entity. With a server cache, do not even hold the list — hold the
id and read the entity from the cache.

## Symptom: a refresh or the back button loses the user's place

Filters, tabs, pagination and the open item are in component state. Move them to the URL.
This is usually an afternoon's work and removes a whole category of complaints: unshareable
views, a back button that exits the page, and a refresh that resets everything.

## Working order

1. **Map it first.** For each piece of state: who owns it, who reads it, who writes it.
   The duplicates and the misplacements are usually obvious once written down.
2. **Delete derived state.** Free, and it shrinks everything that follows.
3. **Move server data to a cache.** Usually removes most of the store.
4. **Move shareable state to the URL.**
5. **Push what is left down** to the lowest component that needs it.
6. **Only then** consider whether anything still justifies a store.

Doing these in the other order — starting with the store — is how a refactor ends with the
same tangle behind a new library.

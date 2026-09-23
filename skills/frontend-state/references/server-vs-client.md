# Server data is not application state

Load when deciding where fetched data lives. Conflating these two is the single most
expensive state mistake, because it turns into hundreds of lines of hand-written cache.

## They are different things

| | Server data | Client state |
|---|---|---|
| Owner | The server | This browser tab |
| Truth | Elsewhere; what you hold is a copy | Here |
| Can go stale | Yes, silently | No |
| Needs refetch, invalidation, dedupe | Yes | No |
| Needs loading and error states | Yes | Rarely |
| Shared across tabs, users | Yes | No |
| Example | The order list | Which order is selected |

Putting the order list in a global store means owning staleness, refetching, deduplication,
retries, and cache invalidation by hand. That is what a query library already is.

## What the hand-rolled version becomes

```ts
// the shape this always grows into
const store = {
  orders: [], ordersLoading: false, ordersError: null, ordersLastFetch: null,
  orderDetail: {}, orderDetailLoading: {}, // per id now
  // ...and then: is this stale? did two components both fetch it? what invalidates it
  // after a mutation? what happens on reconnect? what about the other tab?
}
```

Every one of those questions has a standard answer in a query library and a bespoke one in
each codebase that reimplements it.

## What the library owns

```ts
const { data, isPending, error } = useQuery({
  queryKey: ['orders', { status, page }],
  queryFn: () => fetchOrders({ status, page }),
  staleTime: 30_000,
});
```

The key is the identity of the data. Two components asking for the same key get one request
and one cache entry — which is also why "lift the fetch so we only call it once" stops being
a reason to lift anything.

Mutations invalidate rather than hand-patch:

```ts
const mutation = useMutation({
  mutationFn: updateOrder,
  onSuccess: () => queryClient.invalidateQueries({ queryKey: ['orders'] }),
});
```

## The boundary

Client state around server data is still client state, and still belongs on the ladder:

- The order list → server cache
- **Which** order is selected → URL, so the link is shareable
- Whether the filter panel is open → local
- The draft of an unsaved edit → local, or a draft store for long forms

The mistake is copying the fetched entity into client state so it can be edited. Now there
are two copies, and the one on screen is whichever was written last. Keep the id in client
state and read the entity from the cache.

## Optimistic updates

An optimistic update is a deliberate, temporary second source of truth. It is worth it for
perceived speed, and it must roll back:

```ts
onMutate: async (next) => {
  await queryClient.cancelQueries({ queryKey: ['orders'] });
  const previous = queryClient.getQueryData(['orders']);
  queryClient.setQueryData(['orders'], (old) => patch(old, next));
  return { previous };
},
onError: (_err, _next, context) => {
  queryClient.setQueryData(['orders'], context.previous);
},
```

Cancelling in-flight queries first is not optional — without it a response that was already
on its way overwrites the optimistic value, and the UI flickers back.

## Server components and loaders

A framework that fetches on the server (Next.js App Router, Remix loaders) removes the
question for data that is read and not mutated: there is no client cache because there is no
client fetch. Reach for a query library at the point the client itself needs to refetch,
mutate, or poll — not by default.

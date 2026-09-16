# UIDL document model

Neutral contract: `spec/schema/` and `spec/semantics/`. The React library implements
it; Flutter, Android, and the Java builder must answer to the same files.

## Document

```
UIDLDocument {
  $schema?: string          // informational; not fetched
  version: string           // required; 1.0 is the runtime's current major
  id, name, route?, theme?,
  state?, dataSources?, definitions?,
  root: UIDLNode
}

UIDLNode {
  id, type, name?,
  props?, style?, children?, slots?,
  responsive?, visibility?, bindings?, events?,
  repeat?, ref?, componentId?, themeRef?, testId?
}
```

Node `type` is a registry string, never a framework component class.

## Seams

| Intent | Surface | Implementation |
|---|---|---|
| Read | `$query` / dataSources | `DataAdapter` |
| Bind | `$bind` path | binding resolver |
| Compute | `$expr` / aggregates | expression evaluator |
| Write | `mutate` / `command` | host mutation handler (fail closed) |
| Navigate | `navigate` | host `onRouteChange` |
| Theme | tokens + presets | theme engine |

Do not add a second primary runtime model beside `UIDLDocument`.

## Spec reading order

1. `spec/versioning.md`
2. `spec/semantics/state.md`
3. `spec/semantics/bindings.md`
4. `spec/semantics/expressions.md`
5. Other `spec/semantics/*` as needed

Statuses: `Approved` files are frozen for spec 1.x (changes need an ADR).

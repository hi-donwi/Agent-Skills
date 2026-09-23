# Authorisation beyond roles

Load when deciding who may see or change a specific row, not merely who may call an endpoint.

## Data-level authorisation

`@RolesAllowed` answers "may you use this endpoint?". It does **not** answer "may you see
this row?".

```java
// WRONG — data already left the database before being filtered
var all = orderRepo.listAll();
return all.stream().filter(p -> p.unit.equals(user.unit())).toList();

// RIGHT — constrain the query
return orderRepo.findByUnit(user.unit(), page);
```

Filtering after loading is wrong for two reasons: the `totalElements` count for pagination
becomes incorrect, and data the user may not see has been in the process's memory — visible
in a heap dump and in any log that prints it.

### Domain rules that need their own tests

- A supplier **never** sees a confidential list price before it is published
- A supplier **never** sees another supplier's offer
- An auditor is read-only, without exception
- A staff member manages only their own unit's orders

These are business rules, not configuration. They belong in the organisation's domain
skill under `context/skills/`, not here.

---

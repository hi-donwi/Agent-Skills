# UIDL reference registry: use the actual widget contracts

Inspect the installed registry and prop descriptors before authoring documents.
The table below describes the React reference catalog; other runtimes are smaller.

| Widget | Supported composition |
|---|---|
| Container, Row, Column, Stack | Plain containers; supply layout with supported StyleIntent or a shared recipe. |
| Text | `value`; `heading: 1..6` renders a heading. There is no separate Heading widget. |
| Button | `label`, `variant: "primary"` or `"secondary"`, icon props, native button type. |
| TextField | `label`, `value`, `readOnly`, `disabled`, `error`, `obscureText`; verify native input props in the installed renderer. |
| Select | `label`, `value`, `options: [{value, label}]`, disabled/error props. |
| Checkbox, Switch | `checked`, with the widget's change event. |
| Badge | `value` and supported `color`, not an invented semantic variant. |
| DataTable | `rows` or named `dataSource`, `columns: [{key, label, format, align}]`. |
| PageBar | Server `total`, `page`, `pageSize`; `onPageChange` and `onPageSizeChange`. |
| Navbar, Sidebar, Toolbar | Registered navigation containers with their documented defaults. |

Card, Grid, Heading, Metric, NumberField, and DatePicker are not reference registry
names. Compose registered containers/Text, or register a custom widget with a
manifest. Do not silently emit an unsupported type.

## Server-paginated collections

Declare a document-level data source using `$query.collection`, filters/sort
arrays, and `page: {number, size}`. Bind `rows` to the result or use the supported
named `dataSource`. A DataTable's own `paginate` option slices loaded rows locally;
use a separate PageBar for server paging and avoid double pagination.

```json
{
  "id": "records",
  "type": "DataTable",
  "props": {
    "rows": { "$bind": "state.$data.records.rows" },
    "paginate": false,
    "columns": [
      { "key": "name", "label": "Name" },
      { "key": "amount", "label": "Amount", "format": "currency", "align": "right" },
      { "key": "status", "label": "Status", "format": "status" }
    ]
  }
}
```

## Event arrays contain real action descriptors

Use widget event names such as `onClick`, not `press`. Actions use discriminator
objects, not `action: "mutate"` or an invented toast action:

```json
{
  "id": "save",
  "type": "Button",
  "props": { "label": "Save", "variant": "primary" },
  "events": {
    "onClick": [
      { "command": { "name": "SaveSettings", "payload": { "name": { "$expr": { "path": "state.form.name" } } } } }
    ]
  }
}
```

The host must permit and implement the command. Error/success feedback belongs to
its actual result contract; navigation must wait for successful completion.

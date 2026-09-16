# UIDL runtime commands

Install the published library:

```
npm install uidl-runtime
```

```ts
import { DocumentSchema, UIDocumentRenderer, meridianLightTheme } from "uidl-runtime";
import "uidl-runtime/style.css";

const document = DocumentSchema.parse(rawDocument);
```

CLI (from a built checkout or the package `bin`):

```
uidl-validate <file.json> [<file2.json> ...]
uidl-compile ...
```

Working on the runtime itself (Node.js LTS):

| Command | Purpose |
|---|---|
| `npm install` | Workspaces: `packages/*`, `apps/*` |
| `npm run dev` | Reference suite in memory |
| `npm run mock:api` then `npm run dev:reference:http` | HTTP adapter |
| `npm test` | Vitest |
| `npm run typecheck` / `npm run lint` | Gates |
| `npm run validate:examples` | Example documents |
| `npm run test:reference` | Playwright acceptance (in memory) |

Layout:

```
packages/core/            React/TS library
packages/templates/       page generators and reference verticals
runtime-flutter/          Dart semantic core
runtime-android/          Kotlin semantic core
server/uidl-generator/    Java 21 document builder
server/uidl-server/       Quarkus compile/validate service
apps/reference/           executable gallery
conformance/cases/        cross-runtime fixtures
spec/                     the contract
```

# Typed Data Exchange Contract

## Contract decisions

| Dimension | Declare explicitly |
|---|---|
| Format | Version, encoding/BOM, delimiter, quoting, line endings, parser limits |
| Identity | String identifiers, leading zeros, external-ID namespace and scope |
| Numbers | Locale, exact decimal scale, currency, unit, rounding, overflow |
| Dates | Business date versus instant, timezone, accepted unambiguous formats |
| Empty values | Missing column, null, empty string, unchanged field semantics |
| Conflicts | Reject, skip, upsert, or create revision; never silent overwrite |
| Commit | Atomic file or partial batches, checkpoint and compensation rules |

Store a job key, file digest, row identity, mapping version, scope, validation results,
and committed effect references. A file digest alone is not always a business duplicate:
define whether a deliberately repeated file is a replay or a new authorized operation.
Keep sensitive raw rows protected and short-lived; error reports redact confidential fields.

## Dry runs and exports

Dry runs validate and report planned effects without reserving stock, allocating
numbers, charging providers, or modifying membership. Commit rechecks changing facts.
An explicit partial-import contract reports committed and rejected rows clearly.
Corrections to posted facts use the domain's authorized revision or reversal path.

For CSV/spreadsheet output, untrusted text beginning with formula/control prefixes can
execute in spreadsheet software. Use a tested format-appropriate neutralization policy,
including leading control/whitespace cases. Emit validated numbers as numeric cells
where supported; keep canonical values unchanged and document display transformations.
Export from a declared snapshot or cutoff; reauthorize retrieval and expire artifacts.

## Failure exercise

Import string ID `00017`, exact decimal `12.3400`, an ambiguous date, and a reference
to another tenant. Preserve valid lexical data where contracted and reject ambiguity
and unauthorized scope. Crash after a batch commits, resume, and reconcile one effect
per row. Export formula-like text and verify it remains inert in the chosen consumer.

---
name: skill-creator
description: >-
  Create or upgrade a reusable skill in this library. Use when authoring skill
  instructions, triggers, templates, or supporting resources. Do not use for
  application code or edits to generated workspace skill copies.
metadata:
  pack: agent
---

# Skill Creator

## Overview
Author focused workflows in the source library so consumers can restore a reviewed version.

## When to use
- Adding a capability absent from the catalog.
- Correcting unclear triggers, stale instructions, or unusable resources.

## Process
1. Inspect the existing catalog and likely neighboring skills. Define a concrete
   task the candidate improves; extend an existing skill when its responsibility fits.
2. Edit skills/<name>/SKILL.md in this source repository. Materialized workspace
   copies are generated; do not patch them or create consumer-specific symlinks here.
3. Use a folder-matching lowercase name, at most 64 characters, with single hyphens.
   Supply name, description, and this library's required `metadata.pack` (core,
   agent, web, or java). Keep descriptions under 1024 characters and distinguish
   nearby tasks. Pack is catalog grouping stored in the spec `metadata` map.
4. Start with Overview, When to use, Process, Red flags, and Verification. Keep
   only instructions that change decisions; use references for substantial conditional
   detail. Target a concise entry point and stay below 500 lines.
5. Preserve the user's scope and authorization. Do not mandate repeated approval,
   paid tools, extra providers, or delegation as a side effect of loading a skill.
   Include a useful fallback when a nonessential capability is unavailable.
6. Add resources only for concrete reuse. Templates use a name such as
   skill-template.md, never a nested SKILL.md that can leak into discovery.
   Check local links and use available sibling skills only as optional routing.
7. Add positive, negative-routing, and failure scenarios before declaring a substantial
   revision ready. Use skill-evaluation if available; otherwise record the fixtures,
   expected outcomes, observed results, and verification limits directly.
8. Run ./bin/reindex and python3 bin/validate.py. Update the root README catalog
   and count. Review the diff for private identifiers and unintended resource changes.
9. Distribute through the consumer's supported update and lock workflow after the
   source revision is reviewed. Do not silently switch a consumer to an unpublished branch.

## Red flags
- Editing a generated copy and expecting the change to survive sync.
- Catch-all descriptions that compete with every other skill.
- Treating frontmatter validation as proof of useful agent behavior.
- Hardcoded tool invocations or resources that do not exist in the target environment.

## Verification
- Name, metadata.pack, description, references, README, and index agree.
- Scenarios check actual decisions; unexecuted evaluations are disclosed.
- Generic library files contain no organization-specific context.

## References
- [Agent Skills specification](https://agentskills.io/specification): consult for
  format constraints and optional fields. This library's pack belongs under
  `metadata.pack`, not as a top-level field.
- [Starter template](templates/skill-template/skill-template.md): copy and replace
  placeholders when scaffolding a new skill; keep its filename out of discovery.

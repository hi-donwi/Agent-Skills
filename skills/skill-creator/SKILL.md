---
name: skill-creator
pack: agent
description: >-
  Author a new Agent Skill for this library in the canonical format. Use when the
  user wants to create, scaffold, or refactor a skill, asks how SKILL.md and its
  frontmatter should look, or wants a skill to work across Claude Code, Codex,
  Cursor, Kilocode, Copilot, Gemini, and Aider. Do not use for editing app code
  that merely happens to live next to skills.
---

# Skill Creator

Create skills that are portable, discoverable, and progressively disclosed.
Skills are the workflow format; plugins are the installable distribution unit when
you need to bundle skills with apps, MCP servers, commands, assets, or marketplace metadata.

## When to use
- Adding a new capability to `.agents/skills/`.
- Standardizing or fixing an existing skill's format.

## Process
1. **Pick a single capability.** One skill = one coherent job. Split if it grows two purposes.
2. **Name it** lowercase-with-hyphens; the folder name must equal the frontmatter `name`.
3. **Write the frontmatter** (`name`, `description`). The `description` must state **what it
   does AND when to use it AND when NOT to** — this is what agents match on. Front-load the
   strongest trigger phrases because long skill lists may truncate descriptions. Optional
   keys: `license`, `allowed-tools`, `metadata`.
4. **Write the body** with these sections: Overview · When to use · Process · Red flags ·
   Verification. Keep it under ~500 lines; use imperative, step-by-step instructions.
5. **Add resources only if they earn their place:** `references/` (load-on-demand docs),
   `scripts/` (deterministic helpers, zero-dependency), `templates/`, `examples/`, `assets/`.
6. **Make it Codex-native** (optional): add `agents/openai.yaml` only when metadata or policy
   earns its place. Use the current shape:

   ```yaml
   policy:
     allow_implicit_invocation: true
   ```

   Set `false` for skills that should only run when explicitly invoked.
7. **Register it:** add a line to `.agents/skills/README.md`; ensure root `AGENTS.md`,
   `.cursor/rules/skills.mdc`, and `.kilocode/rules/skills.md` point to it; symlink it in
   `.claude/skills/` and `.codex/skills/` when those folders are used.
8. **Distribute intentionally:** keep repo-scoped skills in `.agents/skills`; package as a
   plugin only when other developers need installable distribution or bundled app/MCP support.

## Red flags
- A vague description that omits *when* to use it → the skill never triggers.
- Dumping a long document into `SKILL.md` instead of linking `references/`.
- Scripts with third-party dependencies (prefer stdlib so they run anywhere).
- Creating many overlapping skills that compete for the same trigger.
- Adding a plugin when a local repo skill is enough.

## Verification
- `name` == folder name; frontmatter parses; description names when-to-use and when-not.
- Body has the standard sections and stays under the length budget.
- The skill is listed in the catalog and discoverable by Claude Code, Cursor, KiloCode, and
  Codex in this workspace.

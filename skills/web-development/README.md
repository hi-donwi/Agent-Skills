# Web Development skill

Build high-quality, modern websites with AI coding agents using the "vibe coding" workflow —
premium marketing sites, SaaS UIs, and immersive 3D/WebGL experiences.

This folder is a **self-contained skill bundle**: copy it into any project and point your
agent at it.

## Contents
| Path | What it is |
|---|---|
| `SKILL.md` | Entry point — what the skill does + when to use it (read this first). |
| `AGENTS.md` | Drop-in instructions for AGENTS.md-aware agents (Codex, etc.). |
| `docs/` | Distilled guidance: `workflow.md`, `coding-standards.md`, `design-principles.md`. |
| `examples/` | `good-component.tsx`, `bad-component.tsx`, `prompt-examples.md`, `prompts.md`. |
| `scripts/` | `check-project.js` (audit a project), `generate-component.js` (scaffold a component). |
| `templates/` | `page-template.md`, `component-template.md`. |
| `adapters/` | Native rule files per agent: Cursor, Copilot, Gemini CLI, Aider. |
| `references/` | `workflow-handbook.md`, `quick-guide.md`, `handbook.md`. |

## Quick use
- **Audit a project:** `node scripts/check-project.js [projectDir]`
- **Scaffold a component:** `node scripts/generate-component.js PricingTable src/components`
- **Per-agent setup:** copy the matching file from `adapters/` into that agent's config
  location (e.g. `adapters/copilot-instructions.md` → `.github/copilot-instructions.md`).

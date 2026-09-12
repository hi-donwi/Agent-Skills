# Skill Ecosystem Synthesis

This file summarizes the important portable lessons from the requested skill
repositories and documentation. It is intentionally a synthesis, not a copy of
upstream skill bodies.

## Sources Reviewed

- Anthropic skills repository: https://github.com/anthropics/skills
- OpenAI Codex skills docs/manual: https://developers.openai.com/codex/skills
- Addy Osmani agent-skills: https://github.com/addyosmani/agent-skills
- alirezarezvani claude-skills: https://github.com/alirezarezvani/claude-skills
- VoltAgent awesome-agent-skills: https://github.com/VoltAgent/awesome-agent-skills
- Composio awesome Claude skills: https://github.com/ComposioHQ/awesome-claude-skills
- Composio awesome Codex skills: https://github.com/composiohq/awesome-codex-skills
- PatrickJS awesome-cursorrules: https://github.com/PatrickJS/awesome-cursorrules
- Anthropic knowledge-work-plugins: https://github.com/anthropics/knowledge-work-plugins
- heilcheng awesome-agent-skills: https://github.com/heilcheng/awesome-agent-skills

## Format and Discovery Lessons

- A skill is a folder with `SKILL.md`; `name` and `description` are the required
  fields across the open Agent Skills pattern.
- The `description` is the most important routing surface. It must front-load
  trigger words, state when to use the skill, and state when not to use it.
- Skills should use progressive disclosure: short entry instructions, optional
  `references/`, `scripts/`, `templates/`, and `assets/` loaded only when needed.
- Codex scans repo, user, admin, and system skill locations and supports symlinked
  skill folders. Claude Code can discover plugin/skill folders. Cursor and
  KiloCode need rule files that point agents back to the canonical `SKILL.md`
  files.
- Large skill libraries can exceed initial skill-list budgets. Keep descriptions
  concise and avoid duplicate near-identical skills.

## Capability Patterns Worth Keeping Locally

- Engineering lifecycle: spec, plan, incremental build, tests, debugging, review,
  simplification, security, performance, docs, git, CI/CD, observability, launch.
- Context and source discipline: context engineering, source-driven development,
  and doubt-driven review prevent hallucinated or overconfident implementation.
- Operational skills: dependency audit, MCP builder, codebase onboarding,
  changelog/release notes, deprecation/migration, shipping/launch.
- UI/web specializations: frontend UI engineering, motion, Three.js/WebGL,
  browser testing, accessibility, and web performance.
- Knowledge-work artifacts: documents, spreadsheets, presentations, PDFs,
  meeting notes, internal communications, role-based business workflows.
- External-tool/plugin workflows: MCP/connectors provide access, tools perform
  actions, skills define behavior and guardrails.

## What We Do Not Mirror Blindly

- We do not import every vendor/framework-specific skill. Those should be added
  only when a local project needs that stack.
- We do not duplicate platform-provided document/spreadsheet/presentation tools;
  the local skill routes the task and sets verification expectations.
- We do not add mass-generated or overlapping skills just to increase count.
  Local skills should remain focused, verifiable, and maintainable.

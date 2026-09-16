---
name: mcp-builder
description: >-
  Design, implement, test, or review Model Context Protocol (MCP) servers and
  tool integrations, including schemas, auth, transport, permissions, evaluation,
  and agent usability. Use when exposing external APIs/data/actions to agents.
  Do not use for ordinary application APIs unless they are being surfaced through
  MCP.
metadata:
  pack: agent
---

# MCP Builder

Expose tools to agents through narrow, well-described, permission-aware MCP
interfaces.

## When to Use

- Building an MCP server for a service, database, internal system, or workflow.
- Reviewing MCP tool schemas, auth, permissions, or safety.
- Turning an external API into agent-usable tools.

## Process

1. **Define use cases.** Start from agent tasks, not raw API endpoints.
2. **Design small tools.** Each tool should have a clear action, typed inputs,
   predictable output, and explicit side effects.
3. **Model auth and permissions.** Least privilege, scoped credentials, no secret
   echoing, and clear approval boundaries for mutating actions.
4. **Validate schemas.** Use structured inputs/outputs, enum constraints, limits,
   and helpful error messages.
5. **Handle failures.** Timeouts, retries, rate limits, idempotency, partial
   failure, and user-safe recovery paths.
6. **Evaluate with agent tasks.** Test representative prompts and verify the
   agent can choose the right tool without guessing.
7. **Document setup.** Transport, environment variables, credentials, local dev,
   and verification commands.

## Red Flags

- One giant `run_any_query` or `call_any_endpoint` tool exposed by default.
- Tools with vague names or unbounded string input.
- Mutating actions without preview/confirmation or idempotency.
- Returning raw huge API payloads instead of agent-usable summaries.
- Secrets in logs, prompts, tool descriptions, or error messages.

## Verification

- Tool schemas are typed and constrained.
- Auth, permissions, and side effects are explicit.
- Representative agent prompts succeed against local or test MCP server.

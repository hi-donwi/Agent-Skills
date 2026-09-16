---
name: context-privacy
description: >-
  Design or review context sharing across clients, project groups, and teams.
  Use when deciding where private notes, sensitive data, credentials, or context
  packs belong. Do not use for ordinary context selection within an established
  audience; use context-engineering for that.
metadata:
  pack: agent
---

# Context Privacy

## Overview
Match each artifact to its owner, audience, storage, and permitted processing destination.

## When to use
- Multiple clients or teams share a workspace.
- Creating context packs, personal notes, or shared project memory.
- Reviewing whether an AI tool may read or transmit sensitive material.

## Process
1. Establish the active client, project group, project, and intended recipients
   from authorized context. Do not enumerate unrelated clients to infer a scope.
2. Classify artifacts before copying them. Use this starting map and adapt it
   to the repository's actual ownership contract:

   | Artifact | Storage and audience |
   |---|---|
   | Generic methods and reusable skills | Shared framework or skill library |
   | Client-owned code and deliverables | Product repository, approved members |
   | Team decisions and handoffs | Private context repository, approved team |
   | Personal notes | Local-only storage excluded from shared repositories |
   | Raw client documents and data | Approved restricted storage |
   | Credentials | Secret manager or OS credential store, injected at use time |

3. Verify the actual access boundary. A private repository shares its entire
   history with authorized readers; client folders do not create separate ACLs.
   Use separate access-controlled repositories or stores when audiences differ.
4. Check AI access separately from Git sharing. Ignore files and context scope
   labels are not filesystem permissions. Use runtime-enforced filesystem and
   network restrictions when isolation is required; verify their effective scope.
5. Build packs from an explicit allowlist of relevant sources. Reject unknown
   scope labels; check canonical paths and symlink targets. Include source,
   revision/date, audience, and omissions; avoid broad recursive bundling.
6. Prefer synthetic examples. Redaction can leave identifying combinations;
   review the full resulting artifact before approved sharing. Keep raw-to-redacted
   mappings private. Never put credential values in a pack, prompt, log, or handoff.
7. Verify recipients and destinations before transmission. If authorization for
   a specific disclosure is missing, hold that transfer and continue local work.

## Red flags
- Treating a git-ignored folder as a credential vault or sandbox.
- Reusing one client's examples in another client's skill or prompt.
- Publishing a context repository after deleting only its current sensitive files.

## Verification
- Each output has a known owner and audience, with permissions checked where possible.
- No pack includes unrelated client material or secrets.
- Unverified access controls are stated as unknown, not described as protection.

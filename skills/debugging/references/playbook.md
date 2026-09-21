# Debugging Playbook — Flexible Recovery

Use when the first fix did not work, the bug is unfamiliar, or you need a disciplined loop
instead of guessing. Complements `SKILL.md` process steps.

---

## Core loop (always)

```
Reproduce → Read error → One hypothesis → Test → Fix cause → Verify → Document
```

If a fix fails verification, **revert or isolate that change** and return to "Read error" —
do not stack unverified patches.

---

## When the first fix fails

1. **Stop adding code.** List what you changed and what you expected vs what happened.
2. **Re-reproduce from clean state** — refresh, new incognito tab, or `git stash` unrelated edits.
3. **Split the problem** — is it build-time, runtime, network, CSS, or data?
4. **Bisect** — disable half the suspect surface (comment out idle video, skip preloader, static poster only).
5. **Check assumptions** — wrong env, stale cache, asset missing on CDN, mobile vs desktop path.
6. **New hypothesis** — only one at a time; log or breakpoint to confirm before editing.
7. **Regression test** — smallest test or script that fails without the fix and passes with it.
8. **Document** — if non-obvious, add a line to project notes or this playbook's domain section.

---

## Flexible tactics (pick what fits)

| Situation | Tactic |
|---|---|
| Flaky / intermittent | Log timestamps, network tab, race conditions; reproduce with throttled CPU/network |
| "Works on my machine" | Compare env vars, Node version, missing gitignored assets, R2 vs local `public/` |
| Large component (e.g. hero) | Reduce to poster-only → scroll-only → idle-only → full merge |
| Agent loop / repeated wrong fixes | Paste **full** stack trace; name files in scope; ask for root cause not symptom suppression |
| CSS/layout | Inspect computed styles, `--hero-*` custom properties, sticky + negative margin interactions |
| Video/media | Network 404, keyframe encode, `mediaUrl()` rewrite, blob preload vs direct src |
| Type/build errors | Read **first** error in output; fix that before later cascading errors |

---

## Anti-patterns

- Silencing errors (`catch {}`, `@ts-ignore`) without understanding.
- Multiple unrelated edits in one commit/session.
- Changing dependencies before ruling out config/data issues.
- Assuming production has files that are gitignored locally.

---

## Domain notes: scroll hero video

From production `SmoothHeroVideo` + ffmpeg pipeline (`motion-design/references/scroll-video.md`):

| Issue | Quick check |
|---|---|
| Scrub stutter | `ffprobe` keyframes === frames on MP4 |
| Production 404 | Hit `mediaUrl(path)` URL directly in browser |
| Idle ping-pong jump | Re-encode idle with `-g 1`; confirm `idleLoopMode` |
| Content under hero hidden | `scrollOverlap` / `scrollOverlapAmount` / negative margin |
| Preloader never finishes | Network fail on one of 8 assets; check console + R2 |
| Object-position wrong | `heroLayout` start/end % in demo data |

**Minimal isolation prompt for agents:**

```
Goal: Isolate hero scroll bug — poster only, no idle video, scrollOverlap false.
Constraints: Do not change encode scripts or R2 config yet.
Scope: @components/SmoothHeroVideo.tsx @pages/...
Verification: Scroll scrub smooth on desktop; describe what changed.
```

---

## When to write durable notes

After a non-obvious fix, add a short entry to:

- Project `AGENT_HANDOFF.md` or `.notes/` (project-specific)
- Skill `references/playbook.md` domain section (reusable pattern)
- Run `handoff.md` if mid-task (workspace memory rules)

One paragraph: symptom → root cause → fix → how to verify.

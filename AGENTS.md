# high-intensity-dev

**A sustainability framework for developers working at high intensity with AI agents.** Principles, patterns, and tools for sustaining AI-paired development over months and years without burnout. Public-facing (MIT-licensed) — this is APT's contribution to the broader Claude Code / Cursor / Copilot practitioner community.

## Where This Fits in the APT Portfolio

**Linear team:** `APT` (APT Tools).

Standalone — no code dependencies on other APT repos. Cross-reference: the workstate-dashboard pattern here informs how parallel Claude Code sessions are tracked across the estate. See [`https://github.com/apt-inc-ai/apt-onboarding/blob/main/CLAUDE.md`](https://github.com/apt-inc-ai/apt-onboarding/blob/main/CLAUDE.md) for the portfolio map.

## What's In Here

| Path | Purpose |
|------|---------|
| `guide.md` | Full sustainability guide — AI development trap, flow vs. burnout neurochemistry, daily structure, sleep protection, recovery, infinite-backlog problem |
| `patterns/` | Implementable patterns for specific failure modes (e.g. `workstate-tracking.md`) |
| `tools/workstate-dashboard.py` | Local web server (stdlib only) aggregating status across Claude Code sessions; one tab shows all active workstreams |
| `claude-code/` | Copy-paste `CLAUDE.md` snippets and workstate templates for Claude Code users |
| `docs/platform-assumptions.md` | OS/runtime requirements, optional Railway/ElevenLabs env vars |
| `tests/` | Tests for the tooling |
| `README.md` / `CONTRIBUTING.md` / `LICENSE` | Standard OSS scaffolding (MIT) |

## How to Run

The only runnable piece is the workstate dashboard:

```bash
python tools/workstate-dashboard.py
# then open http://localhost:7777
```

Zero dependencies — stdlib only. Everything else in the repo is Markdown to read or snippets to copy.

## Git Rules

Inherited from [global CLAUDE.md](~/.claude/CLAUDE.md). Never commit/push without explicit ask.

**Repo-specific:** this is a public repo with external contributors — see `CONTRIBUTING.md` for the pattern-submission workflow before committing new material.

## Owner & Contacts

- **Primary maintainer:** Greg McMillan (gmcmillan@apt-inc.com)
- **Linear team:** `APT`

---

*Skeleton created 2026-04-19 via `apt-onboarding/templates/CLAUDE.md.template`. Expand as needed.*

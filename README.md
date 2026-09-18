# Hackathon — Casablanca, AI track

Starter kit, built before the brief. Everything below is installed, pinned, and
smoke-tested — the only untested variable on the day is the brief itself.

## Run it

```bash
make setup     # venv + pinned deps, copies .env.example -> .env
make test      # 10 smoke tests, no API key required
make api       # agent on http://localhost:8000
make graph     # LangGraph dev UI: inspect state, replay, time-travel
```

`GET /health` reports the providers that actually have a key and whether
Supabase is wired. It never claims a capability the process cannot prove.

## Layout

| Path | What it is |
| --- | --- |
| `agent/app/providers.py` | Model router. Nodes ask for a **role** (`reasoner`/`fast`/`vision`), not a vendor. |
| `agent/app/graph.py` | The LangGraph. Thin on purpose — replace once the brief lands. |
| `agent/app/tools.py` | Tool registry. One function per capability; the agent picks them up automatically. |
| `agent/app/main.py` | FastAPI: `/health`, `/chat`, `/chat/stream` (SSE). |
| `agent/app/store.py` | Supabase. No-ops when unconfigured, so a missing DB never breaks a demo. |
| `supabase/schema.sql` | `agent_runs` audit table + RLS. Domain tables go under the marker. |
| `web/` | Frontend, scaffolded once we know whether the brief needs one. |
| `.claude/agents/` | Nina, Sacha, Victor — loaded automatically, delegable by name. |
| `agents/` | What those three do, and what was deduplicated. See `agents/README.md`. |
| `naiom-platform/` | Next.js 16 agent platform, ~40 API routes. One shared copy. |
| `docs/design/` | AiOO station design language + the demo bundle. |
| `docs/MODELS.md` | Which model for which role, with the numbers behind it. |

## Swapping models

Editing `.env` is the whole operation — no code change:

```
LLM_REASONER=deepseek   # gemini | anthropic | deepseek | openai
LLM_FAST=gemini
```

DeepSeek rides the OpenAI adapter, so it needs only `DEEPSEEK_API_KEY`. Use
`deepseek-flash`, not `deepseek-v4-pro` — cheaper, better, and the only one of
the two with vision. See `docs/MODELS.md`.

## Verified on 2026-09-18

Python 3.11.15 · Node 22.22.2 · langgraph 1.2.11 · langchain 1.4.1 ·
supabase-py 2.31.0 · `@langchain/langgraph` 1.4.15 (JS, verified importable).

Keys live in `.env`, which is gitignored. Nothing in this repo contains a secret.

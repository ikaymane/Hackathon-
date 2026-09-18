# Model choice

## DeepSeek: use `deepseek-flash`, not `deepseek-v4-pro`

Both are 1M context, 384K max output, thinking mode on by default, with JSON
output, tool calls, the Responses API and an Anthropic-format endpoint.
The differences that matter:

| | `deepseek-flash` (V4.1-Flash) | `deepseek-v4-pro` (V4-Pro-0813) |
| --- | --- | --- |
| Vision | **yes** | **no** |
| Concurrency limit | **2500** | 500 |
| Input, cache miss (off-peak / peak) | **$0.15 / $0.30** | $0.66 / $1.32 |
| Input, cache hit (off-peak / peak) | **$0.003 / $0.006** | $0.022 / $0.044 |
| Output (off-peak / peak) | **$0.60 / $1.20** | $1.98 / $3.96 |

Per 1M tokens. Flash is **4.4x cheaper on input, 3.3x cheaper on output**.

And it is also the better model. On DeepSeek's own published table, Flash beats
V4-Pro on 14 of 16 shared benchmarks — losing only GPQA Diamond (90.9 vs 92.4)
and HLE (36.8 vs 42.7). The agentic gaps are not close:

| Benchmark | Flash | V4-Pro | Claude Opus 5 |
| --- | --- | --- | --- |
| Terminal-Bench 3.0 | 30.0 | 11.8 | 43.3 |
| Terminal-Bench 4.0 | 31.2 | 12.4 | 51.8 |
| DeepSWE v1.1 | **74.2** | 62.7 | 74.0 |
| Automation-Bench | **54.8** | 43.2 | 50.3 |
| Agents' Last Exam | **31.8** | 25.7 | 28.6 |
| NL2Repo-Bench | 65.4 | 61.5 | **75.3** |
| ProgramBench | 20.3 | 15.5 | **37.0** |

Flash is a 552B MoE with a causal encoder–decoder split — 8B active params on
input, 16B on output. That is where the price comes from.

These are vendor-published numbers. Treat them as a reason to try Flash first,
not as proof. What matters on the day is measured latency on our own prompts.

`.env` is set to `DEEPSEEK_MODEL=deepseek-flash`. `providers.py` refuses at
build time if `LLM_VISION=deepseek` while the model is v4-pro, rather than
letting it fail mid-demo with an opaque API error.

## Peak hours are a real cost lever

Off-peak is **half price**. Peak is **01:00–04:00 and 06:00–10:00 UTC, Monday
to Friday**; everything else is off-peak.

Today is Friday. Anything run before **10:00 UTC (11:00 in Casablanca)** bills
at double. Bulk generation, seeding, and eval sweeps should wait for 10:00 UTC
if they can. Interactive work during the build is too small to care about.

## How we split the roles

The hackathon stack names Gemini, so Gemini stays load-bearing rather than
decorative — and it already is: Nina's agent transcribes Reels with it.

| Role | Model | Why |
| --- | --- | --- |
| `vision` | Gemini | Required stack component, and genuinely good at it. Nina depends on it. |
| `fast` | Gemini Flash | Classification, routing, extraction. |
| `reasoner` | `deepseek-flash` | Best agentic scores per dirham we have access to. 1M context. |
| Orchestration, code, architecture | Claude (this session) | — |

Switching any row is a `.env` edit — `LLM_REASONER=deepseek` and so on.

## Note for the security angle

If the brief touches security, Flash is unusually strong there: CyberGym 88.1
(V4-Pro 83.3, GLM-5.3 84.5), SEC-Bench Pro 62.8 (V4-Pro 56.4), ExploitGym 15.3
(V4-Pro 5.4). GPT 5.6-Sol still leads SEC-Bench Pro at 74.3 and ExploitGym at
33.7. Worth knowing which way to route if the client's ask is defensive.

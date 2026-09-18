# Day plan — 6 hours

## Before the brief (done)

- Stack installed and smoke-tested, both Python and JS LangGraph.
- Model router in place: Gemini, Claude, DeepSeek, OpenAI behind one interface.
- Supabase audit table + RLS written.
- `make test` green with zero API keys — proves wiring independently of network.

## When the brief lands — first 30 minutes, no code

1. **Write the client's ask in one sentence.** If we cannot, we have not
   understood it. Re-read before typing anything.
2. **List the jury's acceptance criteria verbatim** from the rules they hand
   out. These become the demo script, in order.
3. **Cut scope to what we can demo.** A judge sees one run. Anything that does
   not appear in that run is not worth six hours.
4. **Decide the shape**: agent (LangGraph + API), dashboard (Next + Supabase),
   or both. Only then open an editor.

## Timeline

| Time | Goal |
| --- | --- |
| 0:00–0:30 | Understand brief, fix scope, write the demo script first |
| 0:30–1:00 | Schema + contracts. Freeze the API shape so both halves can move |
| 1:00–3:30 | Build. Vertical slice end-to-end before any polish |
| 3:30–4:30 | Real data in, real run through. Fix what breaks |
| 4:30–5:15 | Demo rehearsal, twice, timed. Fix only what the demo exposes |
| 5:15–6:00 | Slides, README, buffer for the thing that always breaks |

## Rules we hold ourselves to

- **Nothing fake.** No mocked numbers presented as real, no screenshots standing
  in for a working path. If a feature is not finished we say so and demo what is.
  A jury that catches one invented result discounts everything else.
- **Vertical slice first.** One path working end-to-end at hour 2 beats four
  half-features at hour 5.
- **Commit every working state.** `git commit` after each slice lands.
- **The demo script is the spec.** If a task does not serve a line in it, it waits.

## Model routing — who does what

| Role | Default | Why |
| --- | --- | --- |
| `reasoner` | Gemini 2.5 Pro | Long context, generous free tier, strong on structured output |
| `fast` | Gemini 2.5 Flash | Classification, routing, extraction — cheap and quick |
| Deep planning | Claude (this session) | Architecture, code, debugging |
| Overflow | DeepSeek | Bulk generation when a quota tightens; OpenAI-compatible |

Switching is a `.env` edit. Decide by measured latency and output quality on the
day, not in advance.

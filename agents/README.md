# NAIOM agents

Three Claude Code subagents, unpacked from the zips that were uploaded to this
branch. They are **loaded automatically** — their definitions live in
`.claude/agents/`, so this session can delegate to them by name.

| Agent | Name | Model | Does |
| --- | --- | --- | --- |
| **Nina** | `veille` | sonnet | Instagram trend watch. Scrapes a hashtag's Reels via Apify, ranks by **views**, transcribes the spoken script with Gemini. |
| **Sacha** | `prospection` | sonnet | B2B lead gen (IAcquisition™): detect → enrich → personalise → contact, with a Pipeline tab in the platform. |
| **Victor** | `proposition` | opus | Turns an analysed sales call (Fireflies) into a signable commercial proposal, rendered to PDF via Puppeteer. |

All three are French-language, B2B, and share a hard rule worth keeping:
**never invent a figure.** Nina refuses to present Instagram's masked `-1` like
count as real data; Sacha bans invented performance claims; Victor requires every
number to come from the call or be labelled an estimate. That is the same law the
AiOO station runs on, and the same one we hold for the jury demo.

## What was deduplicated

Each zip carried its own full copy of `naiom-platform/` (~24 MB). The three
copies are byte-identical except for one line in `.env.example`:

```
OWNED_AGENT=veille | prospection | proposition
```

So the platform is checked in **once** at `/naiom-platform`, and `OWNED_AGENT`
selects which agent it serves. 66 MB of zips became 24 MB of source.

`brand.md` was also identical in all three; it lives at `agents/brand.md`.

Each agent's original `CLAUDE.md` is kept as `INSTALLER-PROMPT.md` — it is an
end-user onboarding script ("run npm install, open localhost:3000"), not
guidance for this repo, so it is deliberately not at the root.

## The platform

`/naiom-platform` — Next.js 16, React 19, Tailwind v4, Vercel AI SDK +
`@ai-sdk/anthropic`, Puppeteer for PDF. Around 40 API routes already exist:
chat, prospection, veille, propositions, carousels, analytics, compta, plus
Gmail / Drive / Fireflies / YouTube integrations.

If the brief turns out to be an agent platform or an ops dashboard, this is a
large head start. Note `public/avatars` is 15 MB across 13 unoptimised PNGs —
worth compressing before any deploy, not before the demo.

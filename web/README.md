# Frontend

Empty on purpose — scaffolded once we know whether the brief needs a UI.

Fastest path when it does: `ika-tracker` already runs Next.js 16 + Tailwind v4
+ `@supabase/ssr` + `@anthropic-ai/sdk` on React 19. Copy its `package.json`,
`tsconfig.json`, `postcss.config.mjs` and `next.config.ts` rather than running
`create-next-app` and re-resolving versions under time pressure.

The agent is at `http://localhost:8000` — `/chat` for request/response,
`/chat/stream` for SSE token streaming.

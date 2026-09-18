-- Baseline schema. Idea-agnostic: only the agent's own audit trail lives here.
-- Add the domain tables under the marker at the bottom once the brief lands.

create extension if not exists "pgcrypto";

-- Every agent turn, kept so the demo can show real history instead of claims.
create table if not exists public.agent_runs (
  id          uuid primary key default gen_random_uuid(),
  thread_id   text not null,
  input       text not null,
  output      text,
  meta        jsonb not null default '{}'::jsonb,
  created_at  timestamptz not null default now()
);

create index if not exists agent_runs_thread_idx  on public.agent_runs (thread_id, created_at desc);
create index if not exists agent_runs_created_idx on public.agent_runs (created_at desc);

alter table public.agent_runs enable row level security;

-- The agent service writes with the service-role key, which bypasses RLS.
-- The browser gets read-only access and nothing else, so an anon key leaking
-- from the frontend cannot forge history.
drop policy if exists agent_runs_read on public.agent_runs;
create policy agent_runs_read
  on public.agent_runs for select
  to anon, authenticated
  using (true);

-- >>> DOMAIN TABLES GO BELOW THIS LINE <<<

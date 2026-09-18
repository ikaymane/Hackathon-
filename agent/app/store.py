"""Supabase access.

Optional by design: with no credentials the helpers no-op instead of raising,
so the agent still runs in a demo where the database is not wired yet.
"""
from __future__ import annotations

import logging
from functools import lru_cache
from typing import Any

from app.config import settings

log = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def client():
    """Service-role client, or None when Supabase is not configured."""
    if not (settings.supabase_url and (settings.supabase_service_key or settings.supabase_anon_key)):
        return None
    from supabase import create_client

    return create_client(settings.supabase_url, settings.supabase_service_key or settings.supabase_anon_key)


def is_configured() -> bool:
    return client() is not None


def insert(table: str, row: dict[str, Any]) -> dict[str, Any] | None:
    sb = client()
    if sb is None:
        log.debug("supabase not configured; skipping insert into %s", table)
        return None
    return sb.table(table).insert(row).execute().data


def log_run(thread_id: str, user_input: str, output: str, meta: dict[str, Any] | None = None) -> None:
    """Best-effort audit trail. A logging failure must never break a demo."""
    try:
        insert(
            "agent_runs",
            {"thread_id": thread_id, "input": user_input, "output": output, "meta": meta or {}},
        )
    except Exception:  # noqa: BLE001 - telemetry is not worth a 500
        log.exception("failed to log run for thread %s", thread_id)

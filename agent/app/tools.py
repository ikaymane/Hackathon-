"""Tool registry.

Add the hackathon's real tools here. Everything registered shows up in the
agent automatically, so a new capability is one function, not a graph edit.
"""
from __future__ import annotations

import datetime as _dt

from langchain_core.tools import BaseTool, tool


@tool
def now_utc() -> str:
    """Return the current UTC timestamp in ISO-8601 format."""
    return _dt.datetime.now(_dt.timezone.utc).isoformat()


def registry() -> list[BaseTool]:
    """Every tool the agent may call. Keep this the single source of truth."""
    return [now_utc]

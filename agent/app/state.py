"""Shared graph state.

`messages` is the conversation; everything else is scratch space nodes write
for each other. Keep additions here rather than smuggling data through
message text — it stays inspectable in the LangGraph trace.
"""
from __future__ import annotations

from typing import Annotated, Any, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict, total=False):
    messages: Annotated[list[BaseMessage], add_messages]
    # Scratch space — rename/extend once the brief lands.
    context: dict[str, Any]
    trace: list[str]

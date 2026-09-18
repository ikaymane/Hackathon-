"""The LangGraph the service runs.

Deliberately thin: a tool-using agent with a checkpointer, so conversation
state survives across turns keyed by `thread_id`. Replace `build_graph` with
the real topology once the brief lands — `main.py` only depends on the
compiled object exposing `astream_events` / `ainvoke`.
"""
from __future__ import annotations

from langchain.agents import create_agent
from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.memory import InMemorySaver

from app.providers import get_model
from app.tools import registry

SYSTEM_PROMPT = """You are the team\'s agent. Be concrete and brief.
State only what you can support from the tools and context you were given.
When you do not know something, say so instead of inventing it."""


def build_graph(
    model: BaseChatModel | None = None,
    checkpointer: BaseCheckpointSaver | None = None,
):
    """Compile the agent graph.

    `model` is injectable so tests can drive the whole graph with a fake chat
    model and no API key.
    """
    return create_agent(
        model=model or get_model("reasoner"),
        tools=registry(),
        system_prompt=SYSTEM_PROMPT,
        checkpointer=checkpointer or InMemorySaver(),
    )

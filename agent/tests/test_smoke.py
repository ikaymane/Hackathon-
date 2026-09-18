"""Smoke tests that run with NO API keys set.

Their job is to prove the wiring — config, tool registry, graph compilation,
checkpointed multi-turn memory, and the HTTP surface — so that when a real key
is added the only new variable is the network call itself.
"""
from __future__ import annotations

from typing import Any, Sequence

import pytest
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langgraph.checkpoint.memory import InMemorySaver

from app.graph import build_graph
from app.providers import ProviderNotConfigured, ROLES, get_model, routing_table
from app.tools import registry


class EchoModel(BaseChatModel):
    """Answers without calling tools, and remembers nothing on its own —
    so any memory the test observes came from the checkpointer."""

    @property
    def _llm_type(self) -> str:
        return "echo"

    def bind_tools(self, tools: Sequence[Any], **kwargs: Any) -> "EchoModel":
        return self

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: CallbackManagerForLLMRun | None = None,
        **kwargs: Any,
    ) -> ChatResult:
        turns = sum(1 for m in messages if m.type == "human")
        return ChatResult(
            generations=[ChatGeneration(message=AIMessage(f"turn={turns}"))]
        )


def test_tool_registry_is_non_empty_and_named():
    tools = registry()
    assert tools, "registry() must expose at least one tool"
    assert all(t.name and t.description for t in tools)


def test_routing_table_covers_every_role():
    assert set(routing_table()) == set(ROLES)


def test_unknown_role_is_rejected():
    with pytest.raises(ValueError):
        get_model("astrologer")


@pytest.mark.parametrize("provider", ["gemini", "anthropic", "deepseek", "openai"])
def test_missing_key_raises_a_named_error(provider):
    """A missing key must fail loudly at build time, not silently at demo time.

    Skipped for any provider whose key really is present in the environment.
    """
    from app import providers

    if provider in providers.settings.configured_providers():
        pytest.skip(f"{provider} is configured in this environment")
    with pytest.raises(ProviderNotConfigured):
        providers._build(provider, fast=False, temperature=0.0)


def test_graph_compiles_and_answers_without_any_api_key():
    graph = build_graph(model=EchoModel(), checkpointer=InMemorySaver())
    out = graph.invoke(
        {"messages": [("user", "bonjour")]},
        {"configurable": {"thread_id": "t1"}},
    )
    assert out["messages"][-1].content == "turn=1"


def test_checkpointer_carries_history_across_turns():
    graph = build_graph(model=EchoModel(), checkpointer=InMemorySaver())
    config = {"configurable": {"thread_id": "t2"}}
    graph.invoke({"messages": [("user", "first")]}, config)
    out = graph.invoke({"messages": [("user", "second")]}, config)
    # The model counts human turns it was shown; 2 proves turn 1 was replayed.
    assert out["messages"][-1].content == "turn=2"


def test_health_endpoint_reports_only_what_is_configured():
    from fastapi.testclient import TestClient

    from app.main import app

    body = TestClient(app).get("/health").json()
    assert body["status"] == "ok"
    assert set(body["routing"]) == set(ROLES)
    assert isinstance(body["providers_configured"], list)

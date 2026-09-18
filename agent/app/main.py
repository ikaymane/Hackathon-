"""FastAPI front door for the agent: one JSON endpoint, one SSE endpoint."""
from __future__ import annotations

import json
import logging
import uuid
from typing import Any, AsyncIterator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field

from app import store
from app.config import settings
from app.graph import build_graph
from app.providers import ProviderNotConfigured, routing_table

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

app = FastAPI(title="Hackathon Agent", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(ProviderNotConfigured)
async def _provider_not_configured(request: Request, exc: ProviderNotConfigured) -> JSONResponse:
    """A missing key is a configuration problem, not a server fault — say so
    plainly instead of dumping a stack trace during a demo."""
    return JSONResponse(
        status_code=503,
        content={
            "error": "provider_not_configured",
            "detail": str(exc),
            "routing": routing_table(),
            "providers_configured": settings.configured_providers(),
        },
    )


_graph = None


def graph():
    """Built lazily so `import app.main` works without provider keys."""
    global _graph
    if _graph is None:
        _graph = build_graph()
    return _graph


class ChatRequest(BaseModel):
    message: str
    thread_id: str = Field(default_factory=lambda: str(uuid.uuid4()))


@app.get("/health")
def health() -> dict[str, Any]:
    """Reports only what the process can actually prove."""
    return {
        "status": "ok",
        "providers_configured": settings.configured_providers(),
        "routing": routing_table(),
        "supabase": store.is_configured(),
    }


@app.post("/chat")
async def chat(req: ChatRequest) -> dict[str, Any]:
    config = {"configurable": {"thread_id": req.thread_id}}
    result = await graph().ainvoke({"messages": [HumanMessage(req.message)]}, config)
    reply = result["messages"][-1].content
    store.log_run(req.thread_id, req.message, str(reply))
    return {"thread_id": req.thread_id, "reply": reply}


async def _sse(req: ChatRequest) -> AsyncIterator[str]:
    config = {"configurable": {"thread_id": req.thread_id}}
    chunks: list[str] = []
    async for event in graph().astream_events(
        {"messages": [HumanMessage(req.message)]}, config, version="v2"
    ):
        if event["event"] == "on_chat_model_stream":
            piece = event["data"]["chunk"].content
            if piece:
                text = piece if isinstance(piece, str) else json.dumps(piece)
                chunks.append(text)
                yield f"data: {json.dumps({'type': 'token', 'value': text})}\n\n"
        elif event["event"] == "on_tool_start":
            yield f"data: {json.dumps({'type': 'tool', 'name': event['name']})}\n\n"
    store.log_run(req.thread_id, req.message, "".join(chunks))
    yield f"data: {json.dumps({'type': 'done', 'thread_id': req.thread_id})}\n\n"


@app.post("/chat/stream")
async def chat_stream(req: ChatRequest) -> StreamingResponse:
    return StreamingResponse(_sse(req), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=True)

"""One place that knows how to build a chat model.

Every node asks for a *role* ("reasoner", "fast", "vision") instead of a
vendor. Swapping Gemini for DeepSeek mid-hackathon is then a .env edit, not a
code change — which is the difference between a 30-second pivot and a rewrite.
"""
from __future__ import annotations

from functools import lru_cache

from langchain_core.language_models.chat_models import BaseChatModel

from app.config import settings

ROLES = ("reasoner", "fast", "vision")


class ProviderNotConfigured(RuntimeError):
    """Raised when a role maps to a provider whose API key is missing."""


def _build(provider: str, *, fast: bool, temperature: float) -> BaseChatModel:
    if provider == "gemini":
        if not settings.google_api_key:
            raise ProviderNotConfigured("GOOGLE_API_KEY is not set")
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(
            model=settings.gemini_fast_model if fast else settings.gemini_model,
            google_api_key=settings.google_api_key,
            temperature=temperature,
        )

    if provider == "anthropic":
        if not settings.anthropic_api_key:
            raise ProviderNotConfigured("ANTHROPIC_API_KEY is not set")
        from langchain_anthropic import ChatAnthropic

        return ChatAnthropic(
            model=settings.anthropic_model,
            api_key=settings.anthropic_api_key,
            temperature=temperature,
        )

    if provider in ("deepseek", "openai"):
        # DeepSeek speaks the OpenAI wire format, so one adapter covers both.
        from langchain_openai import ChatOpenAI

        if provider == "deepseek":
            if not settings.deepseek_api_key:
                raise ProviderNotConfigured("DEEPSEEK_API_KEY is not set")
            return ChatOpenAI(
                model=settings.deepseek_model,
                api_key=settings.deepseek_api_key,
                base_url=settings.deepseek_base_url,
                temperature=temperature,
            )
        if not settings.openai_api_key:
            raise ProviderNotConfigured("OPENAI_API_KEY is not set")
        return ChatOpenAI(model="gpt-4.1", api_key=settings.openai_api_key, temperature=temperature)

    raise ValueError(f"unknown provider {provider!r}; expected one of gemini|anthropic|deepseek|openai")


@lru_cache(maxsize=None)
def get_model(role: str = "reasoner", *, temperature: float = 0.0) -> BaseChatModel:
    if role not in ROLES:
        raise ValueError(f"unknown role {role!r}; expected one of {ROLES}")
    provider = getattr(settings, role)
    return _build(provider, fast=(role == "fast"), temperature=temperature)


def routing_table() -> dict[str, str]:
    """What each role currently resolves to — surfaced by /health."""
    return {role: getattr(settings, role) for role in ROLES}

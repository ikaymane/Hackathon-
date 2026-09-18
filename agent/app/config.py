"""Environment-driven settings. Nothing here fails at import time so the
graph can be built and tested without any API key present."""
from __future__ import annotations

import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()


def _csv(name: str, default: str = "") -> list[str]:
    return [p.strip() for p in os.getenv(name, default).split(",") if p.strip()]


@dataclass(frozen=True)
class Settings:
    google_api_key: str = field(default_factory=lambda: os.getenv("GOOGLE_API_KEY", ""))
    anthropic_api_key: str = field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY", ""))
    deepseek_api_key: str = field(default_factory=lambda: os.getenv("DEEPSEEK_API_KEY", ""))
    openai_api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))

    reasoner: str = field(default_factory=lambda: os.getenv("LLM_REASONER", "gemini"))
    fast: str = field(default_factory=lambda: os.getenv("LLM_FAST", "gemini"))
    vision: str = field(default_factory=lambda: os.getenv("LLM_VISION", "gemini"))

    gemini_model: str = field(default_factory=lambda: os.getenv("GEMINI_MODEL", "gemini-2.5-pro"))
    gemini_fast_model: str = field(default_factory=lambda: os.getenv("GEMINI_FAST_MODEL", "gemini-2.5-flash"))
    anthropic_model: str = field(default_factory=lambda: os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5"))
    deepseek_model: str = field(default_factory=lambda: os.getenv("DEEPSEEK_MODEL", "deepseek-chat"))
    deepseek_base_url: str = field(default_factory=lambda: os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"))

    supabase_url: str = field(default_factory=lambda: os.getenv("SUPABASE_URL", ""))
    supabase_anon_key: str = field(default_factory=lambda: os.getenv("SUPABASE_ANON_KEY", ""))
    supabase_service_key: str = field(default_factory=lambda: os.getenv("SUPABASE_SERVICE_ROLE_KEY", ""))

    host: str = field(default_factory=lambda: os.getenv("AGENT_HOST", "0.0.0.0"))
    port: int = field(default_factory=lambda: int(os.getenv("AGENT_PORT", "8000")))
    cors_origins: list[str] = field(default_factory=lambda: _csv("AGENT_CORS_ORIGINS", "http://localhost:3000"))

    def configured_providers(self) -> list[str]:
        """Providers that actually have a key — used by /health so the demo
        never claims a capability the process cannot prove."""
        pairs = (
            ("gemini", self.google_api_key),
            ("anthropic", self.anthropic_api_key),
            ("deepseek", self.deepseek_api_key),
            ("openai", self.openai_api_key),
        )
        return [name for name, key in pairs if key]


settings = Settings()

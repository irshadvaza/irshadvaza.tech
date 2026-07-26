"""
provider.py — One switch, two backends.

This module is the heart of the "test free, ship on Azure" workflow:

  LLM_PROVIDER=groq   -> free, open-source-hosted models on Groq (great for
                          learning, no Azure account needed, generous free tier)
  LLM_PROVIDER=azure  -> Azure AI / Azure OpenAI GPT models (production path)

Every lesson script in this project calls `get_agent(...)` from here instead
of building a client directly, so you can flip providers by editing ONE line
in your .env file — no code changes required.
"""

from __future__ import annotations

import os
from typing import Any, Callable, Sequence

from dotenv import load_dotenv

load_dotenv()


def _build_groq_client():
    """Free / open-source path: Groq's OpenAI-compatible API.

    Groq hosts open-source models (Llama, Gemma, Qwen, OpenAI's gpt-oss, etc.)
    on ultra-fast custom hardware, and offers a free API tier — perfect for
    running this whole course with zero cloud cost.

    Get a free key at: https://console.groq.com/keys
    """
    from agent_framework.openai import OpenAIChatClient

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GROQ_API_KEY is not set. Get a free key at "
            "https://console.groq.com/keys and add it to your .env file."
        )

    model = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")

    return OpenAIChatClient(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
        model=model,
    )


def _build_azure_client():
    """Production path: Azure AI / Azure OpenAI GPT models.

    Uses Azure AD auth (`az login`) by default so no API key needs to be
    stored anywhere. Set AZURE_AUTH=key in .env if you'd rather use an
    API key (e.g. for CI or a service without az CLI access).
    """
    from agent_framework.azure import AzureOpenAIChatClient

    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")
    if not endpoint or not deployment:
        raise EnvironmentError(
            "AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_DEPLOYMENT_NAME must be "
            "set in .env. See docs/02-azure-ai-foundry-setup.md."
        )

    if os.environ.get("AZURE_AUTH", "cli").lower() == "key":
        api_key = os.environ.get("AZURE_OPENAI_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "AZURE_AUTH=key requires AZURE_OPENAI_API_KEY to be set."
            )
        return AzureOpenAIChatClient(
            endpoint=endpoint,
            deployment_name=deployment,
            api_key=api_key,
        )

    # Default: keyless auth via `az login` (recommended for local dev)
    from azure.identity import AzureCliCredential

    return AzureOpenAIChatClient(
        endpoint=endpoint,
        deployment_name=deployment,
        credential=AzureCliCredential(),
    )


def get_chat_client():
    """Return a chat client for whichever provider LLM_PROVIDER points to."""
    provider = os.environ.get("LLM_PROVIDER", "groq").strip().lower()

    if provider == "groq":
        return _build_groq_client()
    if provider == "azure":
        return _build_azure_client()

    raise ValueError(
        f"Unknown LLM_PROVIDER='{provider}'. Use 'groq' or 'azure' in your .env file."
    )


def get_agent(
    name: str,
    instructions: str,
    tools: Sequence[Callable] | None = None,
    **agent_kwargs: Any,
):
    """Build an Agent on top of whichever provider is active.

    Every lesson script should call this instead of constructing a client +
    Agent by hand, so switching providers never requires touching lesson code.
    """
    client = get_chat_client()
    return client.as_agent(
        name=name,
        instructions=instructions,
        tools=list(tools) if tools else None,
        **agent_kwargs,
    )


def active_provider() -> str:
    """Handy for printing a banner like '🟢 Running on: groq (llama-3.3-70b-versatile)'."""
    provider = os.environ.get("LLM_PROVIDER", "groq").strip().lower()
    if provider == "groq":
        model = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
    else:
        model = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME", "unknown")
    return f"{provider} ({model})"

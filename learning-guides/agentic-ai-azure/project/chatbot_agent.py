"""
chatbot_agent.py — Agent "Alex" with a greeting tool, a web-search tool, and
multi-turn memory. Works identically on Groq (free) or Azure (production) —
only .env changes.

Run:
    uv run python chatbot_agent.py
    (or) python chatbot_agent.py
"""

import asyncio

import requests

from provider import get_agent, active_provider


def say_hello(name: str) -> str:
    """Greet a user by name. Call this once, at the very start of a new conversation."""
    return f"👋 Hello, {name}! Great to meet you."


def web_search(query: str) -> str:
    """Search the public web for current information and return a short summary.

    Uses DuckDuckGo's free Instant Answer API — no API key required, so this
    tool works out of the box on both the Groq and Azure paths. Swap this for
    Azure AI Foundry's Bing Grounding tool if you want higher-quality results
    on the Azure path (see docs/05-tools-and-function-calling.md).
    """
    try:
        resp = requests.get(
            "https://api.duckduckgo.com/",
            params={"q": query, "format": "json", "no_html": 1},
            timeout=10,
        )
        data = resp.json()
        summary = data.get("AbstractText")
        if summary:
            return summary
        related = data.get("RelatedTopics", [])
        if related and isinstance(related[0], dict) and related[0].get("Text"):
            return related[0]["Text"]
        return "No summary found for that query."
    except Exception as exc:  # keep the tool resilient — never crash the agent
        return f"Search failed: {exc}"


agent = get_agent(
    name="Alex",
    instructions=(
        "You are Alex, a warm and helpful assistant. Always greet the user by "
        "name using the say_hello tool at the start of a new conversation. "
        "Use web_search for anything time-sensitive or requiring current "
        "information you might not know."
    ),
    tools=[say_hello, web_search],
)


async def main() -> None:
    print(f"🤖 Alex is online — running on {active_provider()}")
    print("Type 'q' to quit.\n")

    thread = agent.get_new_thread()  # multi-turn memory for this session

    while True:
        query = input("Ask Query: ")
        if query.strip().lower() == "q":
            print("👋 Goodbye!")
            break

        result = await agent.run(query, thread=thread)
        print(f"Alex: {result}\n")


if __name__ == "__main__":
    asyncio.run(main())

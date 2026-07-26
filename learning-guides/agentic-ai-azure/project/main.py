"""
main.py — Minimal terminal chatbot.

Works with EITHER provider — flip it in .env:
    LLM_PROVIDER=groq   (free, no Azure account needed)
    LLM_PROVIDER=azure  (Azure AI / Azure OpenAI GPT models)

Run:
    uv run python main.py
    (or) python main.py
"""

import asyncio

from provider import get_agent, active_provider

agent = get_agent(
    name="HelloAgent",
    instructions="You are a friendly, concise assistant.",
)


async def main() -> None:
    print(f"🤖 HelloAgent ready — running on {active_provider()}")
    print("Type 'q' to quit.\n")

    while True:
        query = input("Ask Query: ")
        if query.strip().lower() == "q":
            print("👋 Goodbye!")
            break

        result = await agent.run(query)
        print(f"Agent: {result}\n")


if __name__ == "__main__":
    asyncio.run(main())

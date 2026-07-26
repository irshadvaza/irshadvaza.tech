"""
multi_agent.py — Triage agent that hands off to billing / tech / general
specialist agents. Works on Groq (free) or Azure (production).

Run:
    uv run python multi_agent.py
    (or) python multi_agent.py
"""

import asyncio

from provider import get_agent, active_provider

# ── Specialist agents ───────────────────────────────────────────────────

billing_agent = get_agent(
    name="BillingAgent",
    instructions="You handle billing questions: invoices, payments, refunds. Be precise about amounts.",
)

tech_agent = get_agent(
    name="TechSupportAgent",
    instructions="You handle technical issues: bugs, errors, how-to questions. Ask for error messages if missing.",
)

general_agent = get_agent(
    name="GeneralAgent",
    instructions="You handle general questions that aren't billing or technical.",
)


# ── Specialists exposed as tools for the triage agent ───────────────────

async def ask_billing_agent(question: str) -> str:
    """Route a billing-related question to the billing specialist."""
    return str(await billing_agent.run(question))


async def ask_tech_agent(question: str) -> str:
    """Route a technical support question to the tech specialist."""
    return str(await tech_agent.run(question))


async def ask_general_agent(question: str) -> str:
    """Route a general question to the general-purpose specialist."""
    return str(await general_agent.run(question))


triage_agent = get_agent(
    name="TriageAgent",
    instructions=(
        "You are a triage agent. For every user message, decide whether it "
        "is a billing, technical, or general question, and delegate by "
        "calling exactly one of: ask_billing_agent, ask_tech_agent, "
        "ask_general_agent. Return the specialist's answer to the user."
    ),
    tools=[ask_billing_agent, ask_tech_agent, ask_general_agent],
)


async def main() -> None:
    print(f"🧭 Triage agent ready — running on {active_provider()}")
    print("Type 'q' to quit.\n")

    thread = triage_agent.get_new_thread()

    while True:
        query = input("Ask Query: ")
        if query.strip().lower() == "q":
            print("👋 Goodbye!")
            break

        result = await triage_agent.run(query, thread=thread)
        print(f"Agent: {result}\n")


if __name__ == "__main__":
    asyncio.run(main())

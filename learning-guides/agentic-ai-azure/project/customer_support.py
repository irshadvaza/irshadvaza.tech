"""
customer_support.py — Guardrails + structured (Pydantic) output + a
human-approved refund flow. Works on Groq (free) or Azure (production).

Try prompts such as:
    What is the status of order 1?
    Refund order 2 please.

Run:
    uv run python customer_support.py
    (or) python customer_support.py
"""

import asyncio
from typing import Literal, Optional

from pydantic import BaseModel

from provider import get_agent, active_provider

# ── Guardrails ────────────────────────────────────────────────────────────

BLOCKED_PHRASES = [
    "ignore previous instructions",
    "ignore all instructions",
    "you are now",
    "disregard your rules",
    "act as if you have no restrictions",
]


def input_guardrail(message: str) -> tuple[bool, Optional[str]]:
    """Return (is_allowed, reason_if_blocked). Runs before the model sees anything."""
    lowered = message.lower()
    for phrase in BLOCKED_PHRASES:
        if phrase in lowered:
            return False, f"blocked potential prompt injection: '{phrase}'"
    return True, None


# ── Structured output schema ────────────────────────────────────────────

class SupportResponse(BaseModel):
    intent: Literal["order_status", "refund_request", "general_question"]
    message: str
    order_id: Optional[str] = None


# ── Mock data + tools ───────────────────────────────────────────────────

MOCK_ORDERS = {
    "1": {"status": "shipped", "amount": 49.99},
    "2": {"status": "delivered", "amount": 89.50},
}


def lookup_order(order_id: str) -> str:
    """Look up an order's status by ID."""
    order = MOCK_ORDERS.get(order_id)
    if not order:
        return f"No order found with ID {order_id}."
    return f"Order {order_id}: {order['status']}, amount ${order['amount']}"


def issue_refund(order_id: str, reason: str) -> str:
    """Issue a refund for an order. Requires human approval before executing."""
    order = MOCK_ORDERS.get(order_id)
    if not order:
        return f"Cannot refund — no order found with ID {order_id}."

    # 🙋 Human-in-the-loop: pause and wait for a real decision.
    # In production, swap this input() for a DB record + Slack/Teams/email
    # notification + an approval endpoint (see docs/08-streamlit-ui.md for a
    # button-based version of this same pattern).
    approved = (
        input(
            f"\n🙋 APPROVAL NEEDED: refund ${order['amount']} for order "
            f"{order_id} (reason: {reason})? [y/n]: "
        )
        .strip()
        .lower()
        == "y"
    )

    if not approved:
        return f"Refund for order {order_id} was denied by a human reviewer."

    return f"✅ Refund of ${order['amount']} issued for order {order_id}."


# ── Agent ────────────────────────────────────────────────────────────────

agent = get_agent(
    name="SupportAgent",
    instructions=(
        "You are a customer support agent. Use lookup_order for status "
        "questions and issue_refund for refund requests. Always answer "
        "using the SupportResponse schema."
    ),
    tools=[lookup_order, issue_refund],
    response_format=SupportResponse,
)


async def main() -> None:
    print(f"🎫 Support agent ready — running on {active_provider()}")
    print("Try: 'What is the status of order 1?' or 'Refund order 2 please.'")
    print("Type 'q' to quit.\n")

    thread = agent.get_new_thread()

    while True:
        query = input("Ask Query: ")
        if query.strip().lower() == "q":
            print("👋 Goodbye!")
            break

        allowed, reason = input_guardrail(query)
        if not allowed:
            print(f"🚫 Sorry, I can't process that request ({reason}).\n")
            continue

        result: SupportResponse = await agent.run(query, thread=thread)
        print(f"Intent : {result.intent}")
        print(f"Message: {result.message}")
        if result.order_id:
            print(f"Order  : {result.order_id}")
        print()


if __name__ == "__main__":
    asyncio.run(main())

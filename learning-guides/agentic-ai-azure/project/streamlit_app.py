"""
streamlit_app.py — Web UI for the support agent, with a real human-approval
button instead of a blocking input() call. Works on Groq (free) or Azure
(production) — the provider badge in the sidebar shows which is active.

Run:
    uv run streamlit run streamlit_app.py
    (or) streamlit run streamlit_app.py
"""

import asyncio
from typing import Literal, Optional

import streamlit as st
from pydantic import BaseModel

from provider import get_agent, active_provider

st.set_page_config(page_title="🎫 Agentic AI Support", page_icon="🤖")
st.title("🎫 Agentic AI Support Agent")
st.caption("Free-tier Groq models for testing, Azure AI GPT models for production.")
st.sidebar.info(f"🟢 Active provider: **{active_provider()}**")
st.sidebar.caption("Change LLM_PROVIDER in your .env file to switch (groq / azure).")


# ── Data + tools ─────────────────────────────────────────────────────────

MOCK_ORDERS = {
    "1": {"status": "shipped", "amount": 49.99},
    "2": {"status": "delivered", "amount": 89.50},
}


class SupportResponse(BaseModel):
    intent: Literal["order_status", "refund_request", "general_question"]
    message: str
    order_id: Optional[str] = None


def lookup_order(order_id: str) -> str:
    """Look up an order's status by ID."""
    order = MOCK_ORDERS.get(order_id)
    if not order:
        return f"No order found with ID {order_id}."
    return f"Order {order_id}: {order['status']}, amount ${order['amount']}"


def issue_refund(order_id: str, reason: str) -> str:
    """Issue a refund. A human must approve via the UI before this completes."""
    order = MOCK_ORDERS.get(order_id)
    if not order:
        return f"Cannot refund — no order found with ID {order_id}."
    st.session_state.pending_refund = {
        "order_id": order_id,
        "reason": reason,
        "amount": order["amount"],
    }
    return f"Refund of ${order['amount']} for order {order_id} is pending human approval."


# ── Agent (built once, cached across reruns) ────────────────────────────

@st.cache_resource
def build_agent():
    return get_agent(
        name="SupportAgent",
        instructions=(
            "You are a customer support agent. Use lookup_order and "
            "issue_refund as needed. Always respond using the "
            "SupportResponse schema."
        ),
        tools=[lookup_order, issue_refund],
        response_format=SupportResponse,
    )


agent = build_agent()

# ── Session state ────────────────────────────────────────────────────────

if "thread" not in st.session_state:
    st.session_state.thread = agent.get_new_thread()
if "history" not in st.session_state:
    st.session_state.history = []
if "pending_refund" not in st.session_state:
    st.session_state.pending_refund = None

if st.sidebar.button("🔄 New conversation"):
    st.session_state.thread = agent.get_new_thread()
    st.session_state.history = []
    st.session_state.pending_refund = None
    st.rerun()

# ── Render chat history ──────────────────────────────────────────────────

for turn in st.session_state.history:
    with st.chat_message(turn["role"]):
        st.write(turn["content"])

# ── Pending human approval banner ────────────────────────────────────────

if st.session_state.pending_refund:
    r = st.session_state.pending_refund
    st.warning(
        f"🙋 Approval needed: refund **${r['amount']}** for order "
        f"**{r['order_id']}** (reason: {r['reason']})"
    )
    col1, col2 = st.columns(2)
    if col1.button("✅ Approve refund"):
        st.session_state.history.append(
            {"role": "assistant", "content": f"✅ Refund of ${r['amount']} approved and issued."}
        )
        st.session_state.pending_refund = None
        st.rerun()
    if col2.button("❌ Deny refund"):
        st.session_state.history.append(
            {"role": "assistant", "content": "❌ Refund request denied by reviewer."}
        )
        st.session_state.pending_refund = None
        st.rerun()

# ── Chat input ────────────────────────────────────────────────────────────

if prompt := st.chat_input("Ask about an order, e.g. 'Refund order 2 please.'"):
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result: SupportResponse = asyncio.run(
                agent.run(prompt, thread=st.session_state.thread)
            )
        st.write(result.message)
        st.session_state.history.append({"role": "assistant", "content": result.message})

    st.rerun()

# 🤖 Azure AI Agent Framework — A Beginner-to-Pro Learning Guide

> A friendly, step-by-step guide to **Microsoft Agent Framework (MAF)**

This section is written so that **anyone — even a complete beginner** — can go from "what even is an AI agent?" to building, running, and understanding multi-tool, multi-turn, structured-output AI agents on Azure.

Every page explains code in plain English first, then shows the real code, then explains *why* it works that way. Diagrams are included so you can *see* the flow, not just read about it.

---

## 🗺️ How this guide is organized

| # | Page | What you'll learn |
|---|------|--------------------|
| 1 | [History & Why This Framework Exists](01-history-and-why-it-exists.md) | The story of Semantic Kernel + AutoGen merging into one framework — and why Microsoft did it |
| 2 | [Installation & Setup](02-installation-and-setup.md) | Get your environment, Azure OpenAI, and credentials ready — step by step |
| 3 | [Core Concepts & Architecture](03-architecture-and-concepts.md) | Agents, Threads, Tools, Workflows — the building blocks, explained with diagrams |
| 4 | [Example 1 — Your First Agent](04-example-1-your-first-agent.md) | Build a "Mood Analyzer" agent from scratch, in plain, simple steps |
| 5 | [Example 2 — Agents with Tools](05-example-2-agent-with-tools.md) | Give your agent "hands" — call live weather APIs as a tool |
| 6 | [Example 3 — Multi-Turn Conversations & Memory](06-example-3-multi-turn-conversations.md) | Make your agent remember context using Threads |
| 7 | [Example 4 — Structured Output](07-example-4-structured-output.md) | Turn messy text (like a resume PDF) into clean JSON |
| 8 | [Workflows & Multi-Agent Orchestration](08-workflows-multi-agent-orchestration.md) | How multiple agents can work together like a team |
| 9 | [YouTube Video Script (Voice-Over Ready)](09-youtube-script-voiceover.md) | A ready-to-record narration script for your video, matching every example above |

---

## 🎯 Who this is for

- **Total beginners** who have never built an AI agent before.
- **Azure / .NET / Python developers** who know some code but are new to agentic AI.
- **Content creators** (like you!) who want an accurate, well-researched script to turn into a YouTube tutorial.

## 🧰 What you need before you start

- A little bit of Python knowledge (variables, functions, `async/await`).
- An **Azure subscription** with access to **Azure OpenAI** (or you can use GitHub Models for free experimentation).
- 20–30 minutes and a curious mind. That's it.

## 📁 About the source repository
```
Microsoft-Agent-Framework/
├── 01-create_agent.ipynb                          # Your first agent
├── 02-create-agent-with-function-tool.ipynb        # Agents that call tools/APIs
├── 03-multi-turn conversation.ipynb                # Threads & memory
├── 04-producing-structured-output-with-agents.ipynb# JSON/Pydantic structured output
├── Images/thread management.png                    # Diagram used in Example 3
├── data/                                            # Sample PDFs (invoice, resume)
└── requirements.txt                                 # agent-framework, python-dotenv, PyPDF2, pymupdf
```

Start here 👉 **[Page 1: History & Why This Framework Exists](01-history-and-why-it-exists.md)**

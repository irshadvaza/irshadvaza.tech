# 3️⃣ Core Concepts & Architecture

Before touching code, let's build a mental model. If you understand these five building blocks, the rest of the framework will feel obvious.

## 🧱 The Five Building Blocks

```mermaid
flowchart TB
    subgraph MAF["Microsoft Agent Framework"]
    A["🧠 Chat Client<br/>(connects to the model — e.g. Azure OpenAI)"]
    B["🤖 Agent<br/>(a persona with instructions & tools)"]
    C["🧵 Thread<br/>(remembers conversation history)"]
    D["🛠️ Tools / Functions<br/>(let the agent DO things, not just talk)"]
    E["🕸️ Workflows<br/>(connect multiple agents into a graph)"]
    end
    A --> B --> C
    B --> D
    B --> E
```

### 1. Chat Client — the "phone line" to the model
The **Chat Client** is what actually talks to an LLM provider (Azure OpenAI, OpenAI, GitHub Models, etc.). You create one client, then use it to build one or more agents on top of it.

```python
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential

client = AzureOpenAIChatClient(credential=AzureCliCredential())
```

### 2. Agent — a "character" with a job
An **Agent** is created from a chat client. You give it:
- **`instructions`** — its personality and rules (a system prompt)
- **`name`** — an identifier
- optionally **`tools`** — abilities it can use

```python
agent = client.create_agent(
    instructions="You are an expert psychologist AI...",
    name="MoodAnalyzer"
)
```

Think of an agent as a **stateless actor**: on its own, it does **not** remember previous messages. Every `agent.run(...)` call is like meeting the agent for the first time — unless you hand it a *Thread*.

### 3. Thread — the agent's short-term memory
Agents are stateless by design (this keeps them scalable and cheap to run). If you want a **multi-turn conversation** — where the agent remembers what you said two messages ago — you create a **Thread** and pass it along with every call:

```python
thread = agent.get_new_thread()
result1 = await agent.run("Tell me a joke about a pirate.", thread=thread)
result2 = await agent.run("Now tell it in the voice of a pirate's parrot.", thread=thread)
```

```mermaid
sequenceDiagram
    participant You
    participant Agent
    participant Thread as Thread (memory)

    You->>Agent: run("Tell me a joke", thread=T)
    Agent->>Thread: read history (empty)
    Agent-->>You: joke #1
    Agent->>Thread: save joke #1

    You->>Agent: run("Now add emojis", thread=T)
    Agent->>Thread: read history (has joke #1)
    Agent-->>You: joke #1 + emojis
    Agent->>Thread: save updated response
```

> 🧒 **Beginner analogy:** Think of the Agent as a very smart person with amnesia, and the Thread as their notebook. Every time you talk to them, they read their notebook first to remember what you already discussed, then write down the new conversation.

### 4. Tools / Function Calling — giving the agent "hands"
By default, an agent can only *talk*. **Tools** let it *act* — call a weather API, query a database, read a file. You write a normal Python function, describe it, and hand it to the agent. The model decides *on its own* when it needs to call that tool.

```python
from agent_framework import ai_function

@ai_function(name="weather_tool", description="Retrieves weather information for any location")
def get_weather(location: str) -> dict:
    ...

agent = client.create_agent(instructions="...", tools=get_weather)
```

```mermaid
sequenceDiagram
    participant You
    participant Agent
    participant Tool as get_weather() function
    participant API as External Weather API

    You->>Agent: "What's the weather in Pune?"
    Agent->>Agent: Decides it needs the weather tool
    Agent->>Tool: calls get_weather("Pune")
    Tool->>API: HTTP request
    API-->>Tool: raw weather data
    Tool-->>Agent: structured result
    Agent-->>You: friendly natural-language answer
```

### 5. Workflows — connecting multiple agents like a team
A single agent is great, but real problems often need a **team**: one agent researches, another writes, another reviews. **Workflows** are graph-based orchestrations that connect multiple agents and functions into sequential, concurrent, hand-off, or group-collaboration patterns. We cover this in depth in [Page 8](08-workflows-multi-agent-orchestration.md).

## 🏗️ The big picture: how a request flows through the system

```mermaid
flowchart LR
    U["👤 User Input"] --> AG["🤖 Agent<br/>(instructions + reasoning)"]
    AG -->|"needs data?"| T["🛠️ Tool Call"]
    T --> AG
    AG -->|"needs memory?"| TH["🧵 Thread"]
    TH --> AG
    AG -->|"needs structured result?"| SO["📦 response_format<br/>(Pydantic model)"]
    SO --> AG
    AG --> OUT["✅ Final Response<br/>(text / JSON / stream)"]
```

## 📊 Response types you'll work with

| Method | What it returns |
|---|---|
| `agent.run(message)` | Full response at once (`result.text`) |
| `agent.run_stream(message)` | Response streamed chunk-by-chunk, like ChatGPT's typing effect |
| `agent.run(message, response_format=MyModel)` | A structured, validated object (`result.value`) instead of free text |

## 🔑 Key takeaway

> **Agent = brain. Thread = memory. Tools = hands. Workflow = teamwork.**

Keep this mental model in mind as we move into hands-on examples next.

---

⬅️ [Back: Installation & Setup](02-installation-and-setup.md) | ➡️ Next: [Example 1 — Your First Agent](04-example-1-your-first-agent.md)

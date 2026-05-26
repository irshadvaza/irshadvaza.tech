# 🔥 PyTorch — Complete Learning Guide

> **From Zero to Research-Grade Mastery**
> A comprehensive, interview-ready guide covering every concept with simple examples, intuitions, and research-company interview Q&A.

---

## 📚 Table of Contents

| # | File | Topics Covered |
|---|------|----------------|
| 01 | [Foundations & Core Concepts](01_foundations.md) | Tensors, Autograd, Computational Graph, Dynamic vs Static graphs |
| 02 | [Neural Network Building Blocks](02_neural_networks.md) | `nn.Module`, layers, activations, `nn.Sequential`, custom modules |
| 03 | [Training Loop & Optimization](03_training_loop.md) | Loss functions, optimizers, schedulers, gradient clipping |
| 04 | [Data Pipeline](04_data_pipeline.md) | `Dataset`, `DataLoader`, transforms, custom datasets |
| 05 | [Advanced Autograd & Custom Ops](05_advanced_autograd.md) | Custom backward, `torch.autograd.Function`, hooks |
| 06 | [GPU & Performance](06_gpu_performance.md) | CUDA, `device`, mixed precision, `torch.compile`, profiling |
| 07 | [Model Saving & Deployment](07_saving_deployment.md) | `state_dict`, checkpointing, TorchScript, ONNX export |
| 08 | [Research Patterns & Advanced Topics](08_research_advanced.md) | Distributed training, custom layers, meta-learning patterns |
| 09 | [Interview Q&A — All Levels](09_interview_qa.md) | 60+ questions: Beginner → Expert → Research company level |
| 10 | [Quick Reference Cheatsheet](10_cheatsheet.md) | One-page reference of all key APIs |

---

## 🧠 Why PyTorch for Research?

PyTorch was **purpose-built for research** at Facebook AI Research (FAIR) in 2016. Here's why every top research lab (Google Brain, DeepMind, OpenAI, Meta AI) uses it:

```
Static Graph (TensorFlow 1.x)          Dynamic Graph (PyTorch) ✅
────────────────────────────           ─────────────────────────
1. Define the ENTIRE graph             1. Run Python code normally
2. Compile it                          2. Graph builds AS YOU RUN
3. Then run with data                  3. Debug with pdb/print()
                                       4. Change architecture mid-run ✅
→ Rigid, hard to debug                 → Flexible, Pythonic, research-friendly
```

### Key Design Philosophy
- **"Define by Run"** — The graph is created dynamically each forward pass
- **Python-first** — Every operation is a real Python call, fully debuggable
- **Eager by default** — Results are immediate, no sessions needed
- **Research speed** — Prototype an idea in hours, not days

---

## 🗺️ Learning Path

```
Week 1: Foundations (Files 01–02)
  └─ Tensors → Autograd → nn.Module → Basic training

Week 2: Full Pipeline (Files 03–04)
  └─ DataLoader → Loss → Optimizer → Training loop

Week 3: Advanced (Files 05–06)
  └─ Custom ops → GPU optimization → Mixed precision

Week 4: Research & Interview Prep (Files 07–09)
  └─ Deployment → Research patterns → All 60+ interview Q&As
```

---

## ⚡ Quick Start — Your First PyTorch Model in 30 Lines

```python
import torch
import torch.nn as nn

# 1. Data
X = torch.randn(100, 2)          # 100 samples, 2 features
y = (X[:, 0] + X[:, 1] > 0).float().unsqueeze(1)  # binary labels

# 2. Model
model = nn.Sequential(
    nn.Linear(2, 8),
    nn.ReLU(),
    nn.Linear(8, 1),
    nn.Sigmoid()
)

# 3. Training setup
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
loss_fn   = nn.BCELoss()

# 4. Training loop
for epoch in range(100):
    pred = model(X)                    # forward pass
    loss = loss_fn(pred, y)            # compute loss
    optimizer.zero_grad()              # clear old gradients
    loss.backward()                    # compute new gradients
    optimizer.step()                   # update weights

    if epoch % 20 == 0:
        print(f"Epoch {epoch:3d} | Loss: {loss.item():.4f}")
```

---

## 🏢 Companies That Interview on PyTorch

| Company | What They Ask |
|---------|--------------|
| **Meta AI / FAIR** | Autograd internals, distributed training, C++ extensions |
| **Google DeepMind** | Custom backward passes, memory optimization, research patterns |
| **OpenAI** | Large model training, mixed precision, FSDP/DDP |
| **Hugging Face** | Model serialization, custom datasets, deployment |
| **NVIDIA** | CUDA tensors, profiling, kernel fusion |
| **Startups** | End-to-end pipeline, debugging, practical optimization |

---

> 💡 **Tip:** Each file has a **TL;DR** summary at the top, then deep dives with examples.
> Start with File 01 and work through in order — concepts build on each other.

---

*Guide maintained for PyTorch 2.x | Last updated 2025*

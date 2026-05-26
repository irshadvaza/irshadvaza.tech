# 03 — Training Loop & Optimization

> **TL;DR:** The training loop is always: Forward → Loss → Zero grads → Backward → Step.
> Never change this order. Understand why each step exists.

---

## Table of Contents
- [1. The 5-Step Training Loop](#1-the-5-step-training-loop)
- [2. Loss Functions](#2-loss-functions)
- [3. Optimizers](#3-optimizers)
- [4. Learning Rate Schedulers](#4-learning-rate-schedulers)
- [5. The Complete Training Script](#5-the-complete-training-script)
- [6. Gradient Clipping](#6-gradient-clipping)
- [7. Monitoring Training](#7-monitoring-training)
- [8. Common Training Bugs](#8-common-training-bugs)

---

## 1. The 5-Step Training Loop

**Every single training step in PyTorch follows exactly this pattern:**

```python
for batch_x, batch_y in dataloader:
    # Step 1: Forward pass — compute predictions
    predictions = model(batch_x)

    # Step 2: Compute loss
    loss = loss_fn(predictions, batch_y)

    # Step 3: Zero gradients — MUST do before backward!
    optimizer.zero_grad()

    # Step 4: Backward pass — compute gradients
    loss.backward()

    # Step 5: Update weights
    optimizer.step()
```

### Why This Order?

```
Step 1: Forward
  → PyTorch builds the computation graph
  → Records every operation on requires_grad tensors

Step 2: Loss
  → Computes a scalar value we want to minimize

Step 3: Zero Gradients  ← most beginners forget this!
  → Gradients ACCUMULATE by default in PyTorch
  → If we don't zero them, old gradients add to new ones
  → Wrong gradients → wrong weight updates

Step 4: Backward
  → Walks the graph backwards (chain rule)
  → Fills in .grad for every leaf tensor

Step 5: Step
  → optimizer uses .grad values to update .data of parameters
```

---

## 2. Loss Functions

### Classification Losses

```python
import torch
import torch.nn as nn

# ── Cross Entropy Loss ──────────────────────────────────────────────
# For multi-class classification (most common)
# Model outputs: raw logits (no softmax needed — it does it internally!)
ce_loss = nn.CrossEntropyLoss()

logits = torch.tensor([[2.0, 0.5, -1.0],    # sample 1: class 0 most likely
                        [0.1, 3.0,  0.5]])   # sample 2: class 1 most likely
labels = torch.tensor([0, 1])               # true classes

loss = ce_loss(logits, labels)
print(f"CE Loss: {loss.item():.4f}")

# ── Binary Cross Entropy ────────────────────────────────────────────
# For binary classification (0 or 1)
bce = nn.BCELoss()          # expects sigmoid output [0, 1]
bce_logits = nn.BCEWithLogitsLoss()  # expects raw logits ← prefer this!

logits_bin = torch.tensor([2.0, -1.0, 0.5])
labels_bin = torch.tensor([1.0, 0.0, 1.0])

loss_bin = bce_logits(logits_bin, labels_bin)  # numerically stable ✅
```

### Regression Losses

```python
# ── Mean Squared Error (MSE) ────────────────────────────────────────
mse = nn.MSELoss()
pred = torch.tensor([1.5, 2.3, 0.8])
true = torch.tensor([1.0, 2.0, 1.0])
print(mse(pred, true))   # mean of (pred - true)²

# ── Mean Absolute Error (MAE / L1 Loss) ────────────────────────────
mae = nn.L1Loss()
print(mae(pred, true))   # mean of |pred - true|  ← robust to outliers

# ── Huber Loss (Smooth L1) ──────────────────────────────────────────
# Best of both: MSE for small errors, L1 for large errors
huber = nn.HuberLoss(delta=1.0)
smooth_l1 = nn.SmoothL1Loss()
```

### Similarity / Embedding Losses

```python
# ── Cosine Embedding Loss ───────────────────────────────────────────
# Used in siamese networks, metric learning
cosine_loss = nn.CosineEmbeddingLoss()

# ── Triplet Margin Loss ─────────────────────────────────────────────
# anchor, positive, negative — used in face recognition, retrieval
triplet_loss = nn.TripletMarginLoss(margin=1.0)

anchor   = torch.randn(8, 128)
positive = torch.randn(8, 128)
negative = torch.randn(8, 128)
loss = triplet_loss(anchor, positive, negative)

# ── KL Divergence ───────────────────────────────────────────────────
# Measures how one distribution differs from another
# Used in VAEs, knowledge distillation
kl = nn.KLDivLoss(reduction='batchmean')
# NOTE: input must be log-probabilities!
```

### Custom Loss Function
```python
class FocalLoss(nn.Module):
    """
    Focal Loss: down-weights easy examples, focuses on hard ones.
    Used in object detection (RetinaNet).
    FL(p) = -(1 - p)^gamma * log(p)
    """
    def __init__(self, gamma=2.0, alpha=0.25):
        super().__init__()
        self.gamma = gamma
        self.alpha = alpha

    def forward(self, logits, targets):
        bce = nn.functional.binary_cross_entropy_with_logits(
            logits, targets.float(), reduction='none'
        )
        probs = torch.sigmoid(logits)
        p_t   = probs * targets + (1 - probs) * (1 - targets)
        focal_weight = (1 - p_t) ** self.gamma
        loss  = focal_weight * bce
        return loss.mean()
```

---

## 3. Optimizers

### SGD (Stochastic Gradient Descent)
```python
# w = w - lr * gradient
optimizer = torch.optim.SGD(
    model.parameters(),
    lr=0.01,
    momentum=0.9,      # accumulate gradient direction (faster convergence)
    weight_decay=1e-4, # L2 regularization (prevents overfitting)
    nesterov=True      # look-ahead momentum (slightly better)
)
```

### Adam
```python
# Adaptive learning rate per parameter
# Combines momentum + RMSprop
# Best default choice for most tasks
optimizer = torch.optim.Adam(
    model.parameters(),
    lr=1e-3,
    betas=(0.9, 0.999),  # (momentum beta, sq gradient beta)
    eps=1e-8,            # numerical stability
    weight_decay=1e-4    # L2 regularization
)
```

### AdamW (Adam + Proper Weight Decay)
```python
# AdamW fixes a bug in Adam: weight decay should NOT be applied to
# adaptive learning rate (Adam's way of doing L2 is wrong!)
# Use AdamW as the default for transformers!
optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=1e-4,
    betas=(0.9, 0.999),
    weight_decay=0.01    # separate from gradient update
)
```

### Parameter Groups — Different LR for Different Layers
```python
# Common pattern: lower LR for pre-trained backbone, higher for new head
optimizer = torch.optim.AdamW([
    {'params': model.backbone.parameters(), 'lr': 1e-5},   # pre-trained: small LR
    {'params': model.head.parameters(),     'lr': 1e-3},   # new head: larger LR
], weight_decay=0.01)
```

### Optimizer Comparison

| Optimizer | Best For | Key Feature |
|-----------|----------|-------------|
| **SGD + momentum** | CNNs, ResNet | Better generalization, needs tuning |
| **Adam** | Quick experiments, RNNs | Adaptive LR, fast convergence |
| **AdamW** | Transformers (BERT, GPT) | Correct weight decay |
| **RMSprop** | RNNs, online learning | Adaptive, no momentum |
| **LARS/LAMB** | Very large batches | Scales to 32k+ batch size |

---

## 4. Learning Rate Schedulers

### StepLR — Decay by factor every N epochs
```python
scheduler = torch.optim.lr_scheduler.StepLR(
    optimizer, step_size=30, gamma=0.1
)
# LR: 0.1 → (epoch 30) → 0.01 → (epoch 60) → 0.001
```

### CosineAnnealingLR — Smooth cosine decay (most popular)
```python
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
    optimizer,
    T_max=100,     # total epochs (or steps)
    eta_min=1e-6   # minimum LR
)
# LR follows a cosine curve from lr_max down to eta_min
```

### OneCycleLR — Warmup + Anneal (for fast training)
```python
# Very effective! Used in fast.ai and many SOTA recipes
scheduler = torch.optim.lr_scheduler.OneCycleLR(
    optimizer,
    max_lr=0.01,
    steps_per_epoch=len(dataloader),
    epochs=10
)
# Phase 1 (warmup): LR increases 0 → max_lr
# Phase 2 (anneal): LR decreases max_lr → 0
```

### ReduceLROnPlateau — Reduce when stuck
```python
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
    optimizer,
    mode='min',       # 'min' for loss, 'max' for accuracy
    factor=0.5,       # multiply LR by this when plateaued
    patience=5,       # wait this many epochs before reducing
    verbose=True
)
# In the training loop:
scheduler.step(val_loss)   # pass the metric you're monitoring
```

### Using Scheduler in Training Loop
```python
for epoch in range(num_epochs):
    # Training
    model.train()
    for batch in train_loader:
        loss = compute_loss(batch)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        # Some schedulers step per batch
        # scheduler.step()   ← OneCycleLR

    # Most schedulers step per epoch
    scheduler.step()   # ← StepLR, CosineAnnealingLR

    print(f"Epoch {epoch}: LR = {optimizer.param_groups[0]['lr']:.6f}")
```

---

## 5. The Complete Training Script

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

def train_one_epoch(model, loader, optimizer, loss_fn, device):
    model.train()
    total_loss = 0.0
    correct    = 0
    total      = 0
    
    for X, y in loader:
        X, y = X.to(device), y.to(device)

        # Forward
        logits = model(X)
        loss   = loss_fn(logits, y)

        # Backward
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # Metrics
        total_loss += loss.item() * X.size(0)
        preds = logits.argmax(dim=1)
        correct += (preds == y).sum().item()
        total   += X.size(0)

    return total_loss / total, correct / total


@torch.no_grad()
def evaluate(model, loader, loss_fn, device):
    model.eval()
    total_loss = 0.0
    correct    = 0
    total      = 0
    
    for X, y in loader:
        X, y = X.to(device), y.to(device)
        logits = model(X)
        loss   = loss_fn(logits, y)
        
        total_loss += loss.item() * X.size(0)
        preds = logits.argmax(dim=1)
        correct += (preds == y).sum().item()
        total   += X.size(0)

    return total_loss / total, correct / total


def train(model, train_loader, val_loader, config):
    device    = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model     = model.to(device)
    loss_fn   = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=config['lr'],
                                   weight_decay=config['weight_decay'])
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
                    optimizer, T_max=config['epochs'])
    
    best_val_acc = 0.0
    
    for epoch in range(config['epochs']):
        train_loss, train_acc = train_one_epoch(model, train_loader,
                                                optimizer, loss_fn, device)
        val_loss,   val_acc   = evaluate(model, val_loader, loss_fn, device)
        scheduler.step()
        
        print(f"Epoch {epoch+1:3d}/{config['epochs']} | "
              f"Train Loss: {train_loss:.4f} Acc: {train_acc:.3f} | "
              f"Val Loss: {val_loss:.4f} Acc: {val_acc:.3f} | "
              f"LR: {optimizer.param_groups[0]['lr']:.2e}")
        
        # Save best model
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), 'best_model.pth')
            print(f"  ✅ New best model saved! Val Acc: {val_acc:.3f}")
    
    return model
```

---

## 6. Gradient Clipping

Prevents exploding gradients, especially in RNNs and transformers.

```python
# Clip by global norm — most common
for batch in dataloader:
    loss = compute_loss(batch)
    optimizer.zero_grad()
    loss.backward()
    
    # Clip gradient norm to 1.0
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
    
    optimizer.step()

# Clip by value (less common)
torch.nn.utils.clip_grad_value_(model.parameters(), clip_value=0.5)

# How to choose max_norm:
# - Start with 1.0 (works for most models)
# - Monitor gradient norm during training:
grad_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), float('inf'))
print(f"Grad norm: {grad_norm:.4f}")   # if this is consistently > 10, clipping helps
```

---

## 7. Monitoring Training

### Tracking Metrics
```python
# Simple metric tracker
class MetricTracker:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.total_loss = 0.0
        self.n = 0
    
    def update(self, loss, n=1):
        self.total_loss += loss * n
        self.n += n
    
    @property
    def avg(self):
        return self.total_loss / self.n if self.n > 0 else 0.0
```

### TensorBoard Integration
```python
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter('runs/experiment_1')

for epoch in range(num_epochs):
    train_loss, train_acc = train_one_epoch(...)
    val_loss,   val_acc   = evaluate(...)
    
    # Log scalars
    writer.add_scalar('Loss/train', train_loss, epoch)
    writer.add_scalar('Loss/val',   val_loss,   epoch)
    writer.add_scalar('Acc/train',  train_acc,  epoch)
    writer.add_scalar('Acc/val',    val_acc,    epoch)
    writer.add_scalar('LR',         optimizer.param_groups[0]['lr'], epoch)

writer.close()
# Then run: tensorboard --logdir=runs
```

---

## 8. Common Training Bugs

### ❌ Bug 1: Model in eval() during training
```python
# ❌ Wrong
model.eval()   # dropout OFF, batchnorm uses running stats
for batch in train_loader:
    loss = compute_loss(batch)
    loss.backward()
    optimizer.step()

# ✅ Always:
model.train()  # training mode
for batch in train_loader:
    ...

model.eval()   # only for validation/inference
with torch.no_grad():
    evaluate(...)
```

### ❌ Bug 2: Loss not scalar
```python
# ❌ Wrong — loss must be a scalar for backward()
loss = model(x) - y        # shape (batch,) — NOT scalar!
loss.backward()            # RuntimeError!

# ✅ Reduce to scalar
loss = ((model(x) - y) ** 2).mean()   # MSE
loss.backward()            # ✅
```

### ❌ Bug 3: Updating non-leaf tensor
```python
# ❌ Wrong — you can't update gradients of non-leaf tensors
for param in model.parameters():
    param = param - lr * param.grad   # creates new tensor, doesn't update model!

# ✅ Use optimizer, or update .data directly (but use optimizer)
optimizer.step()   # ✅ correct way
# or
with torch.no_grad():
    for param in model.parameters():
        param.data -= lr * param.grad   # manual SGD
```

### ❌ Bug 4: Validation loss with gradient tracking
```python
# ❌ Wastes memory and time
for X, y in val_loader:
    pred = model(X)     # builds graph — unnecessary for val!
    loss = loss_fn(pred, y)

# ✅ Use no_grad for validation
with torch.no_grad():
    for X, y in val_loader:
        pred = model(X)
        loss = loss_fn(pred, y)
```

---

## 📝 Summary

| Step | Code | Why |
|------|------|-----|
| Forward | `pred = model(x)` | Build graph, get prediction |
| Loss | `loss = loss_fn(pred, y)` | Scalar to minimize |
| Zero grad | `optimizer.zero_grad()` | Prevent gradient accumulation |
| Backward | `loss.backward()` | Fill `.grad` for all params |
| Update | `optimizer.step()` | Apply gradients to params |
| Eval mode | `model.eval()` + `no_grad()` | Turn off dropout/BN + save memory |

---

⬅️ **Previous:** [02 — Neural Networks](02_neural_networks.md) | ➡️ **Next:** [04 — Data Pipeline](04_data_pipeline.md)

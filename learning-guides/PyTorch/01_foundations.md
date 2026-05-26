# 01 — PyTorch Foundations & Core Concepts

> **TL;DR:** PyTorch = NumPy arrays + automatic differentiation + GPU support.
> Master tensors and autograd, and everything else follows naturally.

---

## Table of Contents
- [1. What is a Tensor?](#1-what-is-a-tensor)
- [2. Creating Tensors](#2-creating-tensors)
- [3. Tensor Operations](#3-tensor-operations)
- [4. Reshaping & Indexing](#4-reshaping--indexing)
- [5. Autograd — Automatic Differentiation](#5-autograd--automatic-differentiation)
- [6. The Computational Graph](#6-the-computational-graph)
- [7. Dynamic vs Static Graphs](#7-dynamic-vs-static-graphs)
- [8. Gradient Flow & `requires_grad`](#8-gradient-flow--requires_grad)
- [9. Common Pitfalls](#9-common-pitfalls)

---

## 1. What is a Tensor?

Think of tensors as **super-powered NumPy arrays** that can live on GPU and know how to compute their own gradients.

```
Scalar (0D)    →  just a number:    42
Vector (1D)    →  a list:           [1, 2, 3]
Matrix (2D)    →  rows × cols:      [[1,2],[3,4]]
Tensor (3D+)   →  batches, images:  shape (batch, height, width)
```

```python
import torch

scalar = torch.tensor(42.0)          # shape: []
vector = torch.tensor([1., 2., 3.])  # shape: [3]
matrix = torch.tensor([[1., 2.],
                        [3., 4.]])   # shape: [2, 2]
image  = torch.zeros(3, 224, 224)    # shape: [3, 224, 224]  (C, H, W)

print(scalar.shape)  # torch.Size([])
print(matrix.shape)  # torch.Size([2, 2])
print(image.shape)   # torch.Size([3, 224, 224])
```

---

## 2. Creating Tensors

```python
import torch

# ── From data ──────────────────────────────────────────────────────
a = torch.tensor([1, 2, 3])              # from Python list
b = torch.tensor([1, 2, 3], dtype=torch.float32)

# ── Filled tensors ─────────────────────────────────────────────────
zeros = torch.zeros(3, 4)               # all 0s, shape (3,4)
ones  = torch.ones(2, 2)                # all 1s
full  = torch.full((3,), 7.0)           # [7.0, 7.0, 7.0]
eye   = torch.eye(3)                    # identity matrix 3×3

# ── Random tensors ─────────────────────────────────────────────────
rand  = torch.rand(3, 3)                # uniform [0, 1)
randn = torch.randn(3, 3)              # standard normal (mean=0, std=1)
torch.manual_seed(42)                   # reproducibility ← always set this!

# ── Like another tensor ────────────────────────────────────────────
x = torch.tensor([1., 2., 3.])
zeros_like = torch.zeros_like(x)        # same shape & dtype as x
ones_like  = torch.ones_like(x)

# ── From NumPy ─────────────────────────────────────────────────────
import numpy as np
arr = np.array([1., 2., 3.])
t   = torch.from_numpy(arr)             # shares memory! (no copy)
t2  = torch.tensor(arr)                 # copies the data

# ── Back to NumPy ──────────────────────────────────────────────────
back = t.numpy()                        # shares memory if on CPU
```

### Data Types (dtypes)

| dtype | Description | Use Case |
|-------|-------------|----------|
| `torch.float32` | 32-bit float (default) | Most neural networks |
| `torch.float16` | 16-bit float | Mixed precision training |
| `torch.bfloat16`| Brain float | TPUs, A100 GPUs |
| `torch.int64`   | 64-bit int | Indices, class labels |
| `torch.bool`    | Boolean | Masks |

```python
x = torch.randn(3)
print(x.dtype)          # torch.float32

y = x.to(torch.float16) # cast dtype
z = x.double()          # shortcut for float64
```

---

## 3. Tensor Operations

### Basic Math
```python
a = torch.tensor([1., 2., 3.])
b = torch.tensor([4., 5., 6.])

# Element-wise operations
print(a + b)        # tensor([5., 7., 9.])
print(a * b)        # tensor([ 4., 10., 18.])
print(a ** 2)       # tensor([1., 4., 9.])
print(torch.sqrt(a))

# Reduction operations
print(a.sum())      # tensor(6.)
print(a.mean())     # tensor(2.)
print(a.max())      # tensor(3.)
print(a.min())      # tensor(1.)
print(a.std())      # standard deviation
```

### Matrix Operations
```python
A = torch.randn(3, 4)
B = torch.randn(4, 5)

C = A @ B           # matrix multiply → shape (3, 5)  ← use this!
C = torch.mm(A, B)  # same thing

# Batch matrix multiply
batch_A = torch.randn(32, 3, 4)   # 32 matrices of shape (3,4)
batch_B = torch.randn(32, 4, 5)
batch_C = torch.bmm(batch_A, batch_B)  # shape (32, 3, 5)

# Dot product
x = torch.tensor([1., 2., 3.])
y = torch.tensor([4., 5., 6.])
print(torch.dot(x, y))   # 1*4 + 2*5 + 3*6 = 32
```

### Broadcasting — Powerful but Tricky!
```python
# Broadcasting: smaller tensor "expands" to match larger
# Rule: dimensions align from the right; size-1 dims expand

a = torch.ones(3, 1)   # shape (3, 1)
b = torch.ones(1, 4)   # shape (1, 4)
c = a + b              # shape (3, 4) ← broadcast both!

# Real example: add bias to a batch
batch  = torch.randn(32, 128)    # 32 samples, 128 features
bias   = torch.randn(128)        # one bias per feature
result = batch + bias            # (32, 128) + (128,) → (32, 128) ✅
```

---

## 4. Reshaping & Indexing

### Reshaping
```python
x = torch.arange(12.)   # [0, 1, 2, ..., 11]  shape (12,)

# Reshape (total elements must match!)
a = x.reshape(3, 4)     # shape (3, 4)
b = x.reshape(2, 2, 3)  # shape (2, 2, 3)
c = x.reshape(4, -1)    # -1 = infer → (4, 3)

# View (same memory, must be contiguous)
d = x.view(3, 4)        # shape (3, 4)

# Squeeze / Unsqueeze — add or remove size-1 dimensions
t = torch.randn(3)       # shape (3,)
t_col = t.unsqueeze(1)   # shape (3, 1)  ← column vector
t_row = t.unsqueeze(0)   # shape (1, 3)  ← row vector
t_back = t_col.squeeze() # shape (3,)    ← back to 1D

# Flatten
img = torch.randn(32, 3, 224, 224)
flat = img.flatten(1)   # flatten from dim 1 → shape (32, 150528)
```

### Indexing
```python
x = torch.tensor([[1., 2., 3.],
                   [4., 5., 6.],
                   [7., 8., 9.]])

# Standard indexing
print(x[0])         # first row: tensor([1., 2., 3.])
print(x[0, 1])      # element (0,1): tensor(2.)
print(x[:, 1])      # all rows, col 1: tensor([2., 5., 8.])
print(x[1:, :2])    # rows 1+, cols 0-1

# Boolean masking
mask = x > 5
print(x[mask])      # tensor([6., 7., 8., 9.])
x[mask] = 0         # in-place modification

# Fancy indexing
idx = torch.tensor([0, 2])
print(x[idx])       # rows 0 and 2
```

---

## 5. Autograd — Automatic Differentiation

This is PyTorch's **superpower**. It automatically computes derivatives (gradients) so you never have to do calculus by hand.

### The Mental Model

```
Forward pass:  compute output AND record the operations
Backward pass: walk the recorded operations in reverse → apply chain rule
```

```python
import torch

# Tell PyTorch: "track gradients for this tensor"
x = torch.tensor(3.0, requires_grad=True)

# Forward pass — builds the computation graph
y = x ** 2          # y = x²
z = y + 2 * x + 1  # z = x² + 2x + 1  (= (x+1)²)

print(z)            # tensor(16., grad_fn=<AddBackward0>)

# Backward pass — compute dz/dx automatically
z.backward()

# dz/dx = 2x + 2 = 2(3) + 2 = 8
print(x.grad)       # tensor(8.)  ✅
```

### Gradient of Loss w.r.t. Weights
```python
# This is what PyTorch does in every training step
w = torch.randn(3, requires_grad=True)    # model weights
x = torch.tensor([1., 2., 3.])            # input (no grad needed)

# Forward
pred = (w * x).sum()    # simple linear model
loss = (pred - 10) ** 2 # MSE-style loss

# Backward
loss.backward()

print(w.grad)   # dloss/dw for each weight
```

---

## 6. The Computational Graph

PyTorch builds a **Dynamic Computational Graph** (DAG) during the forward pass.

```
x ──┐
    ├──[*]──> y ──[+]──> z
x ──┘         2 ──┘
```

Each node stores:
1. The operation that created it (`grad_fn`)
2. References to its inputs
3. How to compute the gradient (the backward function)

```python
x = torch.tensor(2.0, requires_grad=True)
y = torch.tensor(3.0, requires_grad=True)

z = x * y + x ** 2   # z = xy + x²

print(z.grad_fn)              # <AddBackward0>
print(z.grad_fn.next_functions) # shows the graph structure

z.backward()
# dz/dx = y + 2x = 3 + 4 = 7
# dz/dy = x = 2
print(x.grad)   # tensor(7.)
print(y.grad)   # tensor(2.)
```

### Key Rules of the Graph
- **Created fresh each forward pass** — this is why it's "dynamic"!
- **Freed after `backward()`** — to save memory
- **Leaf tensors** = tensors YOU created (not results of ops)
- **Non-leaf tensors** = intermediate computations

```python
x = torch.randn(3, requires_grad=True)  # leaf
y = x * 2                                # non-leaf
z = y.sum()                              # non-leaf

print(x.is_leaf)  # True
print(y.is_leaf)  # False

z.backward()
print(x.grad)     # [2., 2., 2.] — only leaf tensors accumulate grad
print(y.grad)     # None — non-leaf grads discarded by default
```

---

## 7. Dynamic vs Static Graphs

### Static Graph (TensorFlow 1.x style)
```python
# ❌ Old TensorFlow approach (NOT PyTorch)
# 1. Define the blueprint first
graph = tf.Graph()
with graph.as_default():
    x = tf.placeholder(tf.float32)
    y = tf.placeholder(tf.float32)
    z = x * y   # just a blueprint, nothing computed yet

# 2. Run it with data
with tf.Session(graph=graph) as sess:
    result = sess.run(z, feed_dict={x: 3.0, y: 4.0})
# Problem: Can't debug with print(), can't change structure dynamically
```

### Dynamic Graph (PyTorch) ✅
```python
import torch

def forward(x, use_relu=True):
    # The graph is built RIGHT NOW as this code runs
    out = x @ weight_matrix
    if use_relu:
        out = torch.relu(out)  # different graph each call!
    return out

# You can:
# ✅ Use Python conditionals (if/else)
# ✅ Use Python loops (for/while)
# ✅ Print intermediate values for debugging
# ✅ Change the model structure based on input
# ✅ Use any Python data structure
```

### Why This Matters for Research
```python
# Example: Variable-length sequence processing (RNN without padding)
def process_sequences(sequences):
    results = []
    for seq in sequences:         # different lengths = different graphs!
        output = model(seq)       # PyTorch handles this naturally
        results.append(output)
    return results

# Research: Try different architectures in the same script
for arch in ['skip_connection', 'dense_connection', 'attention']:
    model = build_model(arch)     # different graph structure
    result = model(test_input)    # works perfectly
```

---

## 8. Gradient Flow & `requires_grad`

### Controlling Gradient Tracking
```python
x = torch.randn(3, requires_grad=True)

# Method 1: torch.no_grad() context — fastest, most common
with torch.no_grad():
    y = x * 2   # no graph built, no grad tracked
    # Used for: inference, evaluation, data preprocessing

# Method 2: detach() — get a tensor without gradient history
z = x * 3
z_detached = z.detach()   # new tensor, shares data, no grad_fn
# Used for: stopping gradient flow through part of a network

# Method 3: requires_grad_(False)
x.requires_grad_(False)   # turn off in-place
```

### The Gradient Accumulation Trap
```python
# ❌ Bug: forgetting to zero gradients
w = torch.tensor(1.0, requires_grad=True)
for i in range(3):
    loss = w * i
    loss.backward()
    print(w.grad)   # 0, 1, 3 ← accumulates! (0+1=1, 1+2=3)

# ✅ Correct: zero before each backward
w = torch.tensor(1.0, requires_grad=True)
for i in range(3):
    if w.grad is not None:
        w.grad.zero_()
    loss = w * i
    loss.backward()
    print(w.grad)   # 0, 1, 2 ← correct!
```

---

## 9. Common Pitfalls

### ❌ Pitfall 1: In-place Operations Break Autograd
```python
x = torch.randn(3, requires_grad=True)
y = x * 2

# ❌ This will error — in-place modifies tensor needed for backward
y += 1   # RuntimeError: a leaf Variable that requires grad has been used in an in-place operation

# ✅ Use out-of-place
y = y + 1   # creates new tensor, graph stays valid
```

### ❌ Pitfall 2: Detaching When You Shouldn't
```python
# In a GAN: generator should receive gradient from discriminator loss
# ❌ Wrong
fake = generator(noise)
d_fake = discriminator(fake.detach())   # gradient stops here!
# Generator never learns from discriminator feedback

# ✅ Correct (for generator update)
fake = generator(noise)
d_fake = discriminator(fake)   # gradient flows back to generator
```

### ❌ Pitfall 3: `.item()` vs Tensor
```python
loss = compute_loss(pred, target)

# ❌ Appending tensor to list keeps entire graph in memory!
losses = []
for batch in dataloader:
    loss = compute_loss(...)
    losses.append(loss)         # memory leak!

# ✅ Use .item() to get Python float (detaches from graph)
losses.append(loss.item())
```

### ❌ Pitfall 4: Forgetting `.to(device)`
```python
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = MyModel().to(device)  # model on GPU

# ❌ Input still on CPU
x = torch.randn(1, 3, 224, 224)
out = model(x)   # RuntimeError: Expected all tensors on same device

# ✅ Move input too
x = x.to(device)
out = model(x)   # ✅
```

---

## 📝 Summary

| Concept | Key Point |
|---------|-----------|
| **Tensor** | N-dimensional array with dtype, shape, device |
| **requires_grad** | Tells PyTorch to track operations for this tensor |
| **Forward pass** | Runs computation AND builds the graph |
| **backward()** | Walks the graph in reverse; computes all gradients |
| **Dynamic graph** | Graph rebuilt every forward pass — Python-native, debuggable |
| **no_grad()** | Skip graph building (use for inference) |
| **detach()** | Get tensor without gradient history |
| **zero_grad()** | Must clear gradients before each backward pass |

---

➡️ **Next:** [02 — Neural Network Building Blocks](02_neural_networks.md)

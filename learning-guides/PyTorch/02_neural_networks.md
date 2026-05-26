# 02 — Neural Network Building Blocks

> **TL;DR:** `nn.Module` is the base class for EVERYTHING in PyTorch.
> Every model, every layer, every block — it's all just a `Module`.

---

## Table of Contents
- [1. nn.Module — The Foundation](#1-nnmodule--the-foundation)
- [2. Built-in Layers](#2-built-in-layers)
- [3. Activation Functions](#3-activation-functions)
- [4. nn.Sequential — Quick Models](#4-nnsequential--quick-models)
- [5. Custom Modules — The Right Way](#5-custom-modules--the-right-way)
- [6. Parameters vs Buffers](#6-parameters-vs-buffers)
- [7. Normalization Layers](#7-normalization-layers)
- [8. Dropout & Regularization](#8-dropout--regularization)
- [9. Common Architectures](#9-common-architectures)

---

## 1. nn.Module — The Foundation

`nn.Module` is PyTorch's base class for all neural network components. Think of it as a **smart container** that:
- Holds learnable parameters
- Can be nested (modules inside modules)
- Knows how to move everything to GPU with `.to(device)`
- Can save/load itself

```python
import torch
import torch.nn as nn

class MyFirstModule(nn.Module):
    def __init__(self):
        super().__init__()          # ← ALWAYS call this first!
        self.linear = nn.Linear(10, 5)   # learnable layer
        self.relu   = nn.ReLU()

    def forward(self, x):           # ← define the forward pass
        x = self.linear(x)
        x = self.relu(x)
        return x

model = MyFirstModule()

# nn.Module magic: automatically finds all parameters
for name, param in model.named_parameters():
    print(f"{name}: shape={param.shape}")
# linear.weight: shape=torch.Size([5, 10])
# linear.bias:   shape=torch.Size([5])

# Count parameters
total = sum(p.numel() for p in model.parameters())
print(f"Total parameters: {total}")   # 55

# Move entire model to GPU
model = model.to('cuda')   # ALL parameters move! ✅
```

---

## 2. Built-in Layers

### Linear (Fully Connected)
```python
# nn.Linear(in_features, out_features, bias=True)
layer = nn.Linear(784, 256)

# What it does:  output = input @ weight.T + bias
# input shape:   (batch, 784)
# weight shape:  (256, 784)
# output shape:  (batch, 256)

x = torch.randn(32, 784)   # batch of 32
out = layer(x)              # shape: (32, 256)
```

### Convolutional Layers
```python
# nn.Conv2d(in_channels, out_channels, kernel_size, stride=1, padding=0)
conv = nn.Conv2d(3, 64, kernel_size=3, padding=1)

# input shape:   (batch, 3,  H,   W)
# output shape:  (batch, 64, H,   W)  ← same H,W with padding=1
x = torch.randn(8, 3, 224, 224)
out = conv(x)   # shape: (8, 64, 224, 224)

# Common pattern: depthwise separable convolution (efficiency trick)
depthwise = nn.Conv2d(64, 64, 3, padding=1, groups=64)  # groups=channels
pointwise = nn.Conv2d(64, 128, 1)                        # 1×1 conv
```

### Pooling
```python
max_pool  = nn.MaxPool2d(kernel_size=2, stride=2)
avg_pool  = nn.AvgPool2d(kernel_size=2, stride=2)
adaptive  = nn.AdaptiveAvgPool2d((1, 1))  # output always (1,1) regardless of input size

x = torch.randn(8, 64, 224, 224)
print(max_pool(x).shape)   # (8, 64, 112, 112)
print(adaptive(x).shape)   # (8, 64, 1, 1)
```

### Recurrent Layers
```python
# LSTM: Long Short-Term Memory
lstm = nn.LSTM(
    input_size=128,    # features per timestep
    hidden_size=256,   # hidden state size
    num_layers=2,      # stacked LSTMs
    batch_first=True,  # input shape: (batch, seq, features)
    dropout=0.1        # dropout between layers
)

x = torch.randn(32, 50, 128)   # (batch=32, seq_len=50, features=128)
output, (h_n, c_n) = lstm(x)
print(output.shape)  # (32, 50, 256) — output at each timestep
print(h_n.shape)     # (2, 32, 256)  — final hidden state (num_layers, batch, hidden)

# GRU: simpler, often performs similarly
gru = nn.GRU(128, 256, batch_first=True)
output, h_n = gru(x)
```

### Embedding Layer
```python
# Converts integer token IDs to dense vectors
embed = nn.Embedding(
    num_embeddings=10000,   # vocabulary size
    embedding_dim=512       # vector size
)

token_ids = torch.tensor([[1, 42, 999, 5]])   # shape (1, 4)
vectors = embed(token_ids)                     # shape (1, 4, 512)
```

---

## 3. Activation Functions

```python
x = torch.tensor([-2., -1., 0., 1., 2.])

# ReLU: max(0, x) — most common, fast
relu = nn.ReLU()
print(relu(x))   # [0, 0, 0, 1, 2]

# GELU: Gaussian Error — used in transformers (BERT, GPT)
gelu = nn.GELU()
# Smoother than ReLU, better gradient flow

# Sigmoid: squashes to (0, 1) — for binary classification output
sigmoid = nn.Sigmoid()
print(sigmoid(x))   # [0.12, 0.27, 0.50, 0.73, 0.88]

# Tanh: squashes to (-1, 1) — used in RNN gates
tanh = nn.Tanh()
print(tanh(x))   # [-0.96, -0.76, 0, 0.76, 0.96]

# Softmax: converts logits to probabilities (sum to 1)
softmax = nn.Softmax(dim=-1)
logits = torch.tensor([2., 1., 0.5])
print(softmax(logits))   # [0.66, 0.24, 0.10]

# SiLU (Swish): x * sigmoid(x) — used in MobileNet, EfficientNet
silu = nn.SiLU()

# LeakyReLU: small slope for negative values (avoids dying ReLU)
leaky = nn.LeakyReLU(negative_slope=0.01)
```

### Choosing Activations

| Layer Type | Best Activation |
|-----------|----------------|
| Hidden layers (general) | ReLU |
| Transformer / BERT | GELU |
| EfficientNet / MobileNet | SiLU (Swish) |
| Output: binary classification | Sigmoid |
| Output: multi-class | Softmax |
| Output: regression | None |
| RNN gates | Tanh |

---

## 4. nn.Sequential — Quick Models

Use `nn.Sequential` for simple, linear pipelines (one output feeds the next input).

```python
# Simple MLP
mlp = nn.Sequential(
    nn.Linear(784, 512),
    nn.ReLU(),
    nn.Dropout(0.3),
    nn.Linear(512, 256),
    nn.ReLU(),
    nn.Dropout(0.3),
    nn.Linear(256, 10)
)

x = torch.randn(32, 784)
out = mlp(x)   # shape: (32, 10)
print(out.shape)

# With named layers (better for debugging)
mlp_named = nn.Sequential(
    nn.OrderedDict([
        ('fc1',  nn.Linear(784, 512)),
        ('relu1', nn.ReLU()),
        ('drop1', nn.Dropout(0.3)),
        ('fc2',  nn.Linear(512, 10)),
    ])
)
print(mlp_named.fc1)   # access layer by name
```

### Limitation of Sequential
```python
# ❌ Can't do this with Sequential — skip connections, multiple inputs
# → Use nn.Module instead
```

---

## 5. Custom Modules — The Right Way

Build complex architectures by subclassing `nn.Module`:

### Residual Block (used in ResNet)
```python
class ResidualBlock(nn.Module):
    """
    ResNet basic block with skip connection.
    
    Input ──► Conv ──► BN ──► ReLU ──► Conv ──► BN ──► [+] ──► ReLU ──► Output
      └─────────────────────────────────────────────────┘
                          skip connection
    """
    def __init__(self, channels):
        super().__init__()
        self.conv1 = nn.Conv2d(channels, channels, 3, padding=1, bias=False)
        self.bn1   = nn.BatchNorm2d(channels)
        self.conv2 = nn.Conv2d(channels, channels, 3, padding=1, bias=False)
        self.bn2   = nn.BatchNorm2d(channels)
        self.relu  = nn.ReLU(inplace=True)

    def forward(self, x):
        residual = x                     # save input for skip connection
        
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)
        
        out = self.conv2(out)
        out = self.bn2(out)
        
        out = out + residual             # skip connection (element-wise add)
        out = self.relu(out)
        
        return out

# Use it
block = ResidualBlock(64)
x = torch.randn(8, 64, 56, 56)
out = block(x)
print(out.shape)   # (8, 64, 56, 56) — same shape!
```

### Multi-Head Self-Attention (Transformer building block)
```python
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, n_heads):
        super().__init__()
        assert d_model % n_heads == 0
        self.d_model  = d_model
        self.n_heads  = n_heads
        self.d_head   = d_model // n_heads
        
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)
        
    def forward(self, x, mask=None):
        B, T, C = x.shape   # batch, seq_len, channels
        
        Q = self.W_q(x)   # (B, T, d_model)
        K = self.W_k(x)
        V = self.W_v(x)
        
        # Reshape for multi-head: (B, T, n_heads, d_head) → (B, n_heads, T, d_head)
        Q = Q.view(B, T, self.n_heads, self.d_head).transpose(1, 2)
        K = K.view(B, T, self.n_heads, self.d_head).transpose(1, 2)
        V = V.view(B, T, self.n_heads, self.d_head).transpose(1, 2)
        
        # Scaled dot-product attention
        scale = self.d_head ** -0.5
        attn  = (Q @ K.transpose(-2, -1)) * scale   # (B, n_heads, T, T)
        
        if mask is not None:
            attn = attn.masked_fill(mask == 0, float('-inf'))
        
        attn = torch.softmax(attn, dim=-1)
        
        out = attn @ V   # (B, n_heads, T, d_head)
        out = out.transpose(1, 2).contiguous().view(B, T, C)
        out = self.W_o(out)
        return out

attn = MultiHeadAttention(d_model=512, n_heads=8)
x = torch.randn(2, 10, 512)   # (batch=2, seq_len=10, d_model=512)
print(attn(x).shape)           # (2, 10, 512)
```

---

## 6. Parameters vs Buffers

```python
class MyLayer(nn.Module):
    def __init__(self):
        super().__init__()
        
        # Parameter: LEARNABLE, moves to GPU, saved in state_dict
        self.weight = nn.Parameter(torch.randn(10, 10))
        
        # Buffer: NOT learnable, but moves to GPU, saved in state_dict
        # Good for: running mean/var in BatchNorm, positional encodings
        self.register_buffer('running_mean', torch.zeros(10))
        
        # Attribute: plain tensor — NOT moved to GPU, NOT saved
        self.some_constant = torch.ones(10)  # ← bad practice if you need it on GPU!

layer = MyLayer()
print([n for n, _ in layer.named_parameters()])   # ['weight']
print([n for n, _ in layer.named_buffers()])       # ['running_mean']

# When you call .to('cuda'):
layer = layer.to('cuda')
print(layer.weight.device)        # cuda
print(layer.running_mean.device)  # cuda ← buffer moved too!
print(layer.some_constant.device) # cpu  ← plain tensor NOT moved!
```

---

## 7. Normalization Layers

### Batch Normalization
```python
# Normalizes across the batch dimension
# Used heavily in CNNs (ResNet, VGG, etc.)
bn = nn.BatchNorm2d(num_features=64)   # for 4D input (B, C, H, W)
bn1d = nn.BatchNorm1d(num_features=256)  # for 2D input (B, features)

# What it does per channel:
# 1. Compute mean and var across the batch
# 2. Normalize: (x - mean) / sqrt(var + eps)
# 3. Scale and shift: gamma * x_norm + beta  ← learnable!

# Training mode: uses batch statistics
# Eval mode:     uses running statistics (accumulated during training)
bn.train()   # training mode
bn.eval()    # eval mode ← IMPORTANT to set before inference!
```

### Layer Normalization
```python
# Normalizes across the FEATURE dimension (not batch)
# Used in Transformers — works with batch_size=1, variable lengths
ln = nn.LayerNorm(normalized_shape=512)

x = torch.randn(32, 10, 512)   # (batch, seq, features)
out = ln(x)                     # normalizes over the last dim (512)
print(out.shape)                # (32, 10, 512)

# Why transformers use LayerNorm (not BatchNorm):
# - Works with variable sequence lengths
# - Works well with small batches
# - More stable for language models
```

### GroupNorm & InstanceNorm
```python
gn = nn.GroupNorm(num_groups=8, num_channels=64)   # divide channels into groups
ins = nn.InstanceNorm2d(64)                          # normalize per sample per channel
```

---

## 8. Dropout & Regularization

```python
# Randomly zeros p fraction of elements during training
# Acts as ensemble of many sub-networks
dropout = nn.Dropout(p=0.5)   # 50% dropout

x = torch.randn(5, 10)
# During training: some elements become 0, others scaled by 1/(1-p)
print(dropout(x))

# CRITICAL: Dropout is ONLY active in training mode!
model.train()   # dropout ON
model.eval()    # dropout OFF → use full network for inference

# Spatial dropout (better for CNNs — drops entire feature maps)
dropout2d = nn.Dropout2d(p=0.3)

# Alpha Dropout (for SELU activation — maintains self-normalizing property)
alpha_drop = nn.AlphaDropout(p=0.1)
```

---

## 9. Common Architectures — Full Examples

### Simple CNN for CIFAR-10
```python
class SimpleCNN(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        
        # Feature extractor
        self.features = nn.Sequential(
            # Block 1
            nn.Conv2d(3, 32, 3, padding=1),   # (B, 32, 32, 32)
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),                   # (B, 32, 16, 16)
            
            # Block 2
            nn.Conv2d(32, 64, 3, padding=1),  # (B, 64, 16, 16)
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),                   # (B, 64, 8, 8)
            
            # Block 3
            nn.Conv2d(64, 128, 3, padding=1), # (B, 128, 8, 8)
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),                   # (B, 128, 4, 4)
        )
        
        # Classifier
        self.classifier = nn.Sequential(
            nn.Flatten(),                      # (B, 128*4*4 = 2048)
            nn.Linear(128 * 4 * 4, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(512, num_classes)
        )
    
    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x

model = SimpleCNN(num_classes=10)
x = torch.randn(8, 3, 32, 32)   # CIFAR-10 input
out = model(x)
print(out.shape)   # (8, 10)

total_params = sum(p.numel() for p in model.parameters())
print(f"Parameters: {total_params:,}")   # ~1.3M
```

---

## 📝 Summary

| Concept | Key Point |
|---------|-----------|
| `nn.Module` | Base class; always call `super().__init__()` |
| `forward()` | Define the computation; called by `model(x)` |
| `nn.Parameter` | Learnable tensor; auto-tracked by optimizer |
| `register_buffer` | Non-learnable tensor; moves with model |
| `.train()` / `.eval()` | Controls BatchNorm & Dropout behavior |
| `nn.Sequential` | Linear pipeline shortcut |
| Residual connections | `out = layer(x) + x` — enables very deep networks |
| LayerNorm vs BatchNorm | Transformers use LayerNorm; CNNs use BatchNorm |

---

⬅️ **Previous:** [01 — Foundations](01_foundations.md) | ➡️ **Next:** [03 — Training Loop](03_training_loop.md)

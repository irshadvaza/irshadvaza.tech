# 🐳☸️ Docker, Kubernetes & Azure AKS — The Complete Baby-Steps Guide

> **From "what is a container?" to running production workloads on Azure Kubernetes Service — explained so simply that a complete beginner can follow along.**

![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![Azure](https://img.shields.io/badge/Azure-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white)
![AKS](https://img.shields.io/badge/AKS-0078D4?style=for-the-badge&logo=kubernetes&logoColor=white)

---

## 👋 Welcome

This repository is a **hands-on, chapter-by-chapter training course**. Every chapter builds on the previous one, uses **real commands you can copy-paste**, and includes **diagrams** so you can *see* what's happening, not just read about it.

No prior DevOps experience needed. If you can open a terminal, you can follow this guide. 🚀

### 🧭 How this guide is organized

Each chapter is a **standalone Markdown file**. Read them in order the first time; use them as a reference afterward.

```mermaid
flowchart LR
    A[🐳 Docker Basics] --> B[📦 Images & Dockerfiles]
    B --> C[🧩 Docker Compose]
    C --> D[🌐 Networking & Volumes]
    D --> E[☸️ Kubernetes Basics]
    E --> F[🧱 Core K8s Objects]
    F --> G[🔐 Config & Secrets]
    G --> H[🌍 Networking & Ingress]
    H --> I[📈 Scaling & Health]
    I --> J[☁️ AKS Getting Started]
    J --> K[🚀 AKS Advanced & CI/CD]
    K --> L[🏆 Capstone Project]

    style A fill:#2496ED,color:#fff
    style B fill:#2496ED,color:#fff
    style C fill:#2496ED,color:#fff
    style D fill:#2496ED,color:#fff
    style E fill:#326CE5,color:#fff
    style F fill:#326CE5,color:#fff
    style G fill:#326CE5,color:#fff
    style H fill:#326CE5,color:#fff
    style I fill:#326CE5,color:#fff
    style J fill:#0078D4,color:#fff
    style K fill:#0078D4,color:#fff
    style L fill:#F7B93E,color:#000
```

---

## 📚 Table of Contents

### Part 1 — 🐳 Docker
| # | Chapter | What you'll learn |
|---|---------|--------------------|
| 01 | [Introduction to Containers](./01-introduction-to-containers.md) | Why containers exist, VMs vs containers, install Docker |
| 02 | [Docker Fundamentals](./02-docker-fundamentals.md) | Core commands, running your first containers |
| 03 | [Dockerfiles & Images](./03-dockerfile-and-images.md) | Build your own images step by step |
| 04 | [Docker Compose](./04-docker-compose.md) | Run multi-container apps with one command |
| 05 | [Networking & Volumes](./05-docker-networking-volumes.md) | Persist data, connect containers |

### Part 2 — ☸️ Kubernetes
| # | Chapter | What you'll learn |
|---|---------|--------------------|
| 06 | [Kubernetes Introduction](./06-kubernetes-introduction.md) | What K8s solves, architecture, install Minikube |
| 07 | [Core Kubernetes Objects](./07-kubernetes-core-objects.md) | Pods, ReplicaSets, Deployments, Services |
| 08 | [Config, Secrets & Storage](./08-kubernetes-config-secrets-storage.md) | ConfigMaps, Secrets, Volumes, PVCs |
| 09 | [Networking & Ingress](./09-kubernetes-networking-ingress.md) | Service types, Ingress, DNS |
| 10 | [Scaling & Health Checks](./10-kubernetes-scaling-healthchecks.md) | HPA, probes, rolling updates |

### Part 3 — ☁️ Azure Kubernetes Service (AKS)
| # | Chapter | What you'll learn |
|---|---------|--------------------|
| 11 | [AKS Getting Started](./11-aks-getting-started.md) | Create a real AKS cluster on Azure, deploy to it |
| 12 | [AKS Advanced, Monitoring & CI/CD](./12-aks-advanced-cicd-monitoring.md) | Autoscaling, Azure Monitor, GitHub Actions pipeline |

### Part 4 — 🏆 Final Project
| # | Chapter | What you'll learn |
|---|---------|--------------------|
| 13 | [Capstone Project](./13-capstone-project.md) | Build, containerize, and ship a full app to AKS end-to-end |

---

## 🛠️ Prerequisites

| Tool | Why you need it | Install link |
|------|------------------|---------------|
| 💻 A terminal (bash/PowerShell) | Run commands | Built into your OS |
| 🐳 Docker Desktop | Build & run containers | [docker.com/get-started](https://www.docker.com/get-started) |
| ☸️ kubectl | Talk to Kubernetes clusters | [kubernetes.io/docs/tasks/tools](https://kubernetes.io/docs/tasks/tools/) |
| 📦 Minikube or Kind | Run K8s locally | [minikube.sigs.k8s.io](https://minikube.sigs.k8s.io/) |
| ☁️ Azure CLI | Manage Azure resources | [learn.microsoft.com/cli/azure](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) |
| 🆓 Azure free account | To create an AKS cluster | [azure.microsoft.com/free](https://azure.microsoft.com/free/) |

> 💡 **Tip:** You don't need all of these on day one. Each chapter tells you exactly what to install right before you need it.

---

## 🗺️ The Big Picture (Why these three technologies together?)

```mermaid
graph TD
    subgraph "Your Laptop"
        Code[📝 Application Code]
        Code -->|Dockerfile| Image[🐳 Docker Image]
    end

    Image -->|docker push| Registry[📦 Container Registry<br/>Docker Hub / Azure Container Registry]

    subgraph "Kubernetes Cluster"
        Pod1[🧊 Pod]
        Pod2[🧊 Pod]
        Pod3[🧊 Pod]
        Svc[🌐 Service]
        Svc --> Pod1
        Svc --> Pod2
        Svc --> Pod3
    end

    Registry -->|kubectl apply / deploy| Pod1
    Registry --> Pod2
    Registry --> Pod3

    subgraph "Azure Cloud"
        AKS[☸️ AKS - Managed Kubernetes]
        AKS -.hosts.-> Pod1
        AKS -.hosts.-> Pod2
        AKS -.hosts.-> Pod3
    end

    User[👤 User] -->|https://your-app.com| LB[⚖️ Load Balancer]
    LB --> Svc
```

**In one sentence each:**
- 🐳 **Docker** packages your app + everything it needs into a portable box called an *image*.
- ☸️ **Kubernetes** runs, heals, scales, and manages many of those boxes (*containers*) automatically.
- ☁️ **AKS** is Microsoft Azure's managed Kubernetes — Azure handles the hard cluster-management parts for you.

---

## ✅ How to use this repo

1. Clone or download this repo.
2. Start at [Chapter 01](./01-introduction-to-containers.md).
3. Type out every command yourself — don't just copy-paste blindly. Muscle memory matters.
4. Each chapter ends with a **"🎯 Try It Yourself"** section — do it before moving on.
5. Struggling? Each chapter has a **"🩹 Common Errors"** section — check there first.

Happy learning! ⭐ If this helped you, consider starring the repo.

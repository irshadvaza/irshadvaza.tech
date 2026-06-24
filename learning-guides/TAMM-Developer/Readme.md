# 🏛️ TAMM Abu Dhabi — Developer Training & Guidelines

> A comprehensive training guide for developers working on Abu Dhabi's TAMM digital government services platform, covering Node.js, React.js, Angular, and the full TAMM service lifecycle.

---

## 📋 Table of Contents

- [About This Repository](#about-this-repository)
- [Who Is This For?](#who-is-this-for)
- [Roadmap](#roadmap)
- [Repository Structure](#repository-structure)
- [How to Use This Guide](#how-to-use-this-guide)
- [Contributing](#contributing)

---

## About This Repository

This repository is the official developer training hub for the **TAMM Abu Dhabi** engineering team. It provides structured, step-by-step guidance for beginner to intermediate developers who are building, maintaining, or extending services on the TAMM platform.

Every module is self-contained with real-world examples drawn directly from TAMM service patterns.

---

## Who Is This For?

| Level | Description |
|---|---|
| 🟢 Beginner | Developers new to Node.js, React, or Angular |
| 🟡 Intermediate | Developers familiar with JS but new to the TAMM ecosystem |
| 🔵 Team Leads | Engineering managers reviewing code standards and architecture |

---

## 🗺️ Roadmap

The training is split into **6 progressive modules**. Each module builds on the previous one.

```
MODULE 0 — TAMM Platform Overview
MODULE 1 — Node.js Fundamentals for TAMM
MODULE 2 — React.js for TAMM Front-End
MODULE 3 — Angular for TAMM Service Portals
MODULE 4 — TAMM Service Lifecycle
MODULE 5 — Integration, Testing & Deployment
```

---

### 📦 MODULE 0 — TAMM Platform Overview
> **File:** [`docs/00-tamm-overview.md`](docs/00-tamm-overview.md)

- What is TAMM?
- Brief History of TAMM
- TAMM Architecture at a Glance
- TAMM Service Lifecycle
  - 🎨 Service Design
  - 🧭 User Journeys
  - 🔄 State Management
  - ⚙️ Service Configuration
- Key Terminology

---

### 📦 MODULE 1 — Node.js for TAMM
> **File:** [`docs/01-nodejs.md`](docs/01-nodejs.md)

- What is Node.js & Why TAMM Uses It
- Brief History of Node.js
- Core Features
- Node.js Architecture (Event Loop, Non-Blocking I/O)
- Key Components
  - Modules & `require` / `import`
  - npm & Package Management
  - Express.js for TAMM APIs
  - File System, Streams, Buffers
  - Environment Variables & Config
- Step-by-Step Examples
  - Hello World
  - Building a TAMM REST API endpoint
  - Connecting to a TAMM database
- Best Practices

---

### 📦 MODULE 2 — React.js for TAMM
> **File:** [`docs/02-reactjs.md`](docs/02-reactjs.md)  *(coming soon)*

- What is React & Why TAMM Uses It
- Brief History of React
- JSX, Components, Props & State
- Hooks (`useState`, `useEffect`, `useContext`)
- TAMM UI Component Library
- Step-by-Step: Building a TAMM Service Form
- State Management with Redux / Context API

---

### 📦 MODULE 3 — Angular for TAMM
> **File:** [`docs/03-angular.md`](docs/03-angular.md)  *(coming soon)*

- What is Angular & Why TAMM Uses It
- Angular Architecture: Modules, Components, Services
- Routing & Guards in TAMM Portals
- Forms (Reactive & Template-Driven)
- HttpClient & TAMM API Integration
- Step-by-Step: Building a TAMM Service Portal Page

---

### 📦 MODULE 4 — TAMM Service Lifecycle (Deep Dive)
> **File:** [`docs/04-service-lifecycle.md`](docs/04-service-lifecycle.md)  *(coming soon)*

- End-to-End Service Flow
- Service Versioning
- Approval Workflows
- Notification & Messaging Architecture
- Error Handling Patterns

---

### 📦 MODULE 5 — Integration, Testing & Deployment
> **File:** [`docs/05-integration-testing-deployment.md`](docs/05-integration-testing-deployment.md)  *(coming soon)*

- API Gateway Integration
- Unit Testing with Jest / Jasmine
- E2E Testing with Cypress
- CI/CD Pipeline for TAMM
- Environment Management (Dev / Staging / Prod)

---

## 📁 Repository Structure

```
tamm-developer-training/
│
├── README.md                         ← You are here (Roadmap)
│
├── docs/
│   ├── 00-tamm-overview.md           ← TAMM intro + Service Lifecycle
│   ├── 01-nodejs.md                  ← Node.js full module
│   ├── 02-reactjs.md                 ← React.js full module
│   ├── 03-angular.md                 ← Angular full module
│   ├── 04-service-lifecycle.md       ← Deep dive lifecycle
│   └── 05-integration-testing.md     ← Testing & deployment
│
├── examples/
│   ├── nodejs/
│   │   ├── hello-world/
│   │   ├── tamm-api-server/
│   │   └── tamm-db-connector/
│   ├── reactjs/
│   │   ├── tamm-service-form/
│   │   └── tamm-dashboard/
│   └── angular/
│       ├── tamm-portal-page/
│       └── tamm-auth-guard/
│
├── assets/
│   └── diagrams/
│       ├── tamm-architecture.png
│       └── service-lifecycle-flow.png
│
└── .github/
    └── CONTRIBUTING.md
```

---

## 🚀 How to Use This Guide

1. **Start at Module 0** — even if you know JavaScript, reading the TAMM overview will give you context that makes every other module make sense.
2. **Follow modules in order** — each one references concepts from the previous.
3. **Run every example** — copy the code in `examples/`, run it locally, and modify it.
4. **Use the TAMM Service Lifecycle as your reference** — all code patterns trace back to it.

---

## 🤝 Contributing

Team members are welcome to improve these docs. Please see [`.github/CONTRIBUTING.md`](.github/CONTRIBUTING.md) for guidelines on adding new modules, fixing examples, or updating API references.

---

> 📌 **Maintained by the TAMM Engineering Team, Abu Dhabi**  
> For questions, open an issue or contact the team lead.

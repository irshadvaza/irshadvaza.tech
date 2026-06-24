# 📗 Module 1 — Node.js for TAMM Developers

> **Prerequisites:** [Module 0 — TAMM Overview](./00-tamm-overview.md)  
> **Time to complete:** ~2–3 hours  
> **Next Module:** [02-reactjs.md](./02-reactjs.md) *(coming soon)*

---

## Table of Contents

1. [What is Node.js?](#1-what-is-nodejs)
2. [Why TAMM Uses Node.js](#2-why-tamm-uses-nodejs)
3. [Brief History of Node.js](#3-brief-history-of-nodejs)
4. [Core Features](#4-core-features)
5. [How Node.js Works — The Event Loop](#5-how-nodejs-works--the-event-loop)
6. [Key Components](#6-key-components)
   - [6.1 Modules](#61-modules)
   - [6.2 npm & Package Management](#62-npm--package-management)
   - [6.3 Express.js for TAMM APIs](#63-expressjs-for-tamm-apis)
   - [6.4 File System & Streams](#64-file-system--streams)
   - [6.5 Environment Variables](#65-environment-variables)
7. [Step-by-Step Examples](#7-step-by-step-examples)
   - [Example 1: Hello World](#example-1-hello-world)
   - [Example 2: Building a TAMM REST API](#example-2-building-a-tamm-rest-api)
   - [Example 3: Connecting to a Database](#example-3-connecting-to-a-database)
   - [Example 4: Document Upload Service](#example-4-document-upload-service)
8. [Best Practices for TAMM](#8-best-practices-for-tamm)
9. [Common Mistakes & How to Avoid Them](#9-common-mistakes--how-to-avoid-them)
10. [Summary & What's Next](#10-summary--whats-next)

---

## 1. What is Node.js?

**Node.js** is a runtime environment that allows you to run JavaScript code **outside of a web browser** — on a server, your local machine, or any operating system.

Before Node.js existed, JavaScript could only run in a browser. Node.js changed that by using **Google's V8 JavaScript engine** (the same engine that powers Chrome) and wrapping it with system-level capabilities: reading files, making network requests, managing databases, and running HTTP servers.

In simple terms:

> **Node.js = JavaScript + the ability to do server-side things**

```
Without Node.js:
  JavaScript → runs in browser only → can show dynamic web pages

With Node.js:
  JavaScript → runs anywhere → can build web servers, APIs, CLI tools, microservices
```

---

## 2. Why TAMM Uses Node.js

TAMM chose Node.js for its backend microservices for several well-reasoned technical and operational reasons:

| Reason | Explanation |
|---|---|
| **Non-blocking I/O** | Government services involve many simultaneous API calls (eligibility checks, document verification, payment). Node.js handles thousands of concurrent requests without spawning new threads |
| **JSON-native** | TAMM services communicate via JSON APIs. Node.js handles JSON natively with zero conversion overhead |
| **Shared language** | Front-end (React/Angular) and back-end both use JavaScript, meaning developers can work across the stack and share utility libraries |
| **Rich ecosystem** | npm has packages for every TAMM need: authentication, PDF generation, document OCR, SMS, payment gateways |
| **Microservices fit** | Node.js starts fast and has a small memory footprint — ideal for the microservices architecture TAMM uses |
| **UAE adoption** | Major government tech vendors operating in the UAE (Microsoft Azure, AWS Middle East) provide first-class Node.js SDK support |

---

## 3. Brief History of Node.js

Understanding the history helps you understand the *why* behind design decisions you'll encounter in the codebase.

### 2009 — Ryan Dahl's Insight

In 2009, a developer named **Ryan Dahl** was frustrated. He was building a file upload progress bar and found that popular web servers (Apache at the time) blocked their threads waiting for I/O operations to complete. Thousands of users waiting for uploads meant thousands of blocked threads — hugely wasteful.

Dahl's insight: *"What if a server never waited? What if it registered callbacks for I/O and moved on immediately?"*

He took Google's V8 engine (open-source, very fast), added non-blocking I/O using the **libuv** library, and released **Node.js** in May 2009. His demo at JSConf EU that year showed a Node.js server handling thousands of concurrent connections with minimal memory — a revelation at the time.

### 2010 — npm Arrives

In 2010, **npm** (Node Package Manager) was created by Isaac Z. Schlueter. Suddenly, sharing reusable Node.js code became trivial. npm grew to become the largest software registry in the world.

### 2011–2014 — Enterprise Adoption

LinkedIn, PayPal, Netflix, and Walmart adopted Node.js. PayPal reported that switching from Java to Node.js let them handle **double the requests per second** with fewer servers. Netflix reported a **70% reduction in startup time**. Government agencies took notice.

### 2015 — io.js Fork & The Node.js Foundation

A community disagreement about Node.js's release pace led to a fork called **io.js**. The conflict was resolved in 2015 when both projects merged under the newly formed **Node.js Foundation**, and Node.js v4 was released — marking the beginning of the modern, stable Node.js era.

### 2018 — N-API & Enterprise Stability

Node.js introduced **N-API**, a stable C++ API for native add-ons. This gave enterprise users (including government platforms) the confidence that native extensions would not break with each Node version.

### 2020–Present — Long-Term Support & Maturity

Node.js now follows a predictable **Long-Term Support (LTS)** release cycle. Even-numbered versions (18, 20, 22) are LTS and supported for 3 years — critical for government platforms that cannot upgrade frequently. TAMM's infrastructure standardises on **Node.js LTS versions** for production workloads.

```
Node.js Timeline (Selected Milestones)

2009 ────── Ryan Dahl releases Node.js at JSConf EU
2010 ────── npm created
2011 ────── LinkedIn, PayPal adopt Node.js
2015 ────── Node.js Foundation formed; v4.0 (first LTS)
2018 ────── N-API stable; widespread enterprise adoption
2020 ────── Node.js 14 LTS; strong UAE cloud adoption
2022 ────── Node.js 18 LTS (TAMM baseline)
2024 ────── Node.js 20 LTS (TAMM upgrade target)
```

---

## 4. Core Features

### 4.1 Asynchronous & Non-Blocking

Node.js **never waits**. When it needs to read a file or call an API, it hands off the task and immediately starts doing something else. When the task completes, a callback (or Promise) is triggered.

```javascript
// ❌ BLOCKING (not how Node.js works — this is synchronous pseudocode)
const data = readFileSync("large-document.pdf");  // Everything STOPS here
processDocument(data);

// ✅ NON-BLOCKING (how Node.js actually works)
fs.readFile("large-document.pdf", (err, data) => {
  // This runs when the file is ready — Node didn't block waiting
  if (err) throw err;
  processDocument(data);
});
// Node.js continues executing other code here WHILE the file is being read
```

### 4.2 Single-Threaded with a Thread Pool

Node.js runs your JavaScript code in a **single thread** — but it uses a background **thread pool** (via libuv) for heavy I/O tasks (disk reads, DNS lookups). This gives you the simplicity of single-threaded programming with the performance of multi-threading for I/O.

### 4.3 npm Ecosystem

Over **2 million packages** on npm. Any functionality you need — JWT authentication, PDF generation, email sending, database ORM — is one `npm install` away.

### 4.4 Fast Execution via V8

Google's V8 engine compiles JavaScript to native machine code. Node.js is exceptionally fast for network-heavy, I/O-bound applications like API servers.

### 4.5 Cross-Platform

One Node.js codebase runs on Linux (TAMM production servers), macOS (developer machines), and Windows — no changes required.

---

## 5. How Node.js Works — The Event Loop

The **Event Loop** is the heart of Node.js. Understanding it will help you write correct, performant TAMM services.

```
  ┌──────────────────────────────────────────────┐
  │              YOUR NODE.JS CODE               │
  │     console.log, API handlers, logic...      │
  └────────────────────┬─────────────────────────┘
                       │  "do this when you're done"
                       ▼
  ┌──────────────────────────────────────────────┐
  │               CALL STACK                     │
  │  Executes synchronous code line by line      │
  └────────────────────┬─────────────────────────┘
                       │  encounters async task
                       ▼
  ┌──────────────────────────────────────────────┐
  │           NODE.JS APIs / libuv               │
  │  File reads, HTTP requests, timers...        │
  │  These run in the background                 │
  └────────────────────┬─────────────────────────┘
                       │  task complete → callback ready
                       ▼
  ┌──────────────────────────────────────────────┐
  │              CALLBACK QUEUE                  │
  │  Completed async tasks wait here             │
  └────────────────────┬─────────────────────────┘
                       │  EVENT LOOP checks: "Is call stack empty?"
                       ▼
  ┌──────────────────────────────────────────────┐
  │              CALL STACK (again)              │
  │  Event loop pushes callback here to execute  │
  └──────────────────────────────────────────────┘
```

### Practical Example

```javascript
console.log("1: Start TAMM service check");

setTimeout(() => {
  console.log("3: Eligibility check result received (async)");
}, 2000);  // Simulates a 2-second API call to a backend service

console.log("2: Waiting for result — but NOT blocking other requests");

// Output:
// 1: Start TAMM service check
// 2: Waiting for result — but NOT blocking other requests
// 3: Eligibility check result received (async)    ← appears 2 seconds later
```

Notice that line 2 printed *before* the setTimeout callback — Node.js did not wait.

---

## 6. Key Components

### 6.1 Modules

Node.js code is organised into **modules** — files that export functions, classes, or values for other files to use.

#### CommonJS (Traditional — most TAMM backend code)

```javascript
// utils/formatDate.js  ← defining a module
function formatArabicDate(isoString) {
  const date = new Date(isoString);
  return date.toLocaleDateString("ar-AE", {
    year: "numeric",
    month: "long",
    day: "numeric"
  });
}

module.exports = { formatArabicDate };
```

```javascript
// services/application.service.js  ← using the module
const { formatArabicDate } = require("../utils/formatDate");

const submissionDate = formatArabicDate("2024-06-15T09:30:00Z");
console.log(submissionDate);  // ١٥ يونيو ٢٠٢٤
```

#### ES Modules (Modern — newer TAMM services)

```javascript
// utils/formatDate.mjs
export function formatArabicDate(isoString) {
  const date = new Date(isoString);
  return date.toLocaleDateString("ar-AE", { year: "numeric", month: "long", day: "numeric" });
}
```

```javascript
// services/application.service.mjs
import { formatArabicDate } from "../utils/formatDate.mjs";
```

> 💡 **TAMM Standard:** Newer TAMM microservices use ES Modules (`"type": "module"` in package.json). Legacy services use CommonJS. Check your service's `package.json` before writing new files.

---

### 6.2 npm & Package Management

**npm** (Node Package Manager) is Node.js's built-in tool for installing, managing, and publishing JavaScript packages.

#### Essential npm Commands

```bash
# Initialise a new Node.js project
npm init -y

# Install a package (saves to dependencies)
npm install express

# Install a development-only package
npm install --save-dev jest

# Install all packages listed in package.json
npm install

# Check for outdated packages
npm outdated

# Run a script defined in package.json
npm run start
npm run test
```

#### The package.json File

Every Node.js project has a `package.json`. Here is what a TAMM microservice's `package.json` looks like:

```json
{
  "name": "tamm-building-permit-service",
  "version": "2.1.0",
  "description": "TAMM microservice for building permit applications",
  "main": "src/index.js",
  "scripts": {
    "start": "node src/index.js",
    "dev": "nodemon src/index.js",
    "test": "jest --coverage",
    "lint": "eslint src/"
  },
  "dependencies": {
    "express": "^4.18.2",
    "dotenv": "^16.3.1",
    "jsonwebtoken": "^9.0.0",
    "multer": "^1.4.5",
    "axios": "^1.6.0",
    "morgan": "^1.10.0",
    "helmet": "^7.0.0"
  },
  "devDependencies": {
    "jest": "^29.0.0",
    "supertest": "^6.3.0",
    "nodemon": "^3.0.0",
    "eslint": "^8.0.0"
  },
  "engines": {
    "node": ">=18.0.0"
  }
}
```

> ⚠️ **Always commit `package-lock.json`** — it locks exact package versions. This ensures every developer and every deployment uses identical dependencies. Never delete it.

---

### 6.3 Express.js for TAMM APIs

**Express.js** is the web framework TAMM uses to build HTTP API servers in Node.js. It is minimal, flexible, and the industry standard for Node.js APIs.

#### Core Express Concepts

| Concept | What it does |
|---|---|
| `app.get()` | Handle HTTP GET requests |
| `app.post()` | Handle HTTP POST requests |
| `app.put()` | Handle HTTP PUT requests |
| `app.delete()` | Handle HTTP DELETE requests |
| **Middleware** | Functions that run on every request (logging, authentication, parsing) |
| **Router** | Groups related routes together |
| **req** | The incoming request (URL, headers, body, params) |
| **res** | The outgoing response (status code, JSON, files) |

#### Basic Express Server Structure

```javascript
// src/index.js

const express = require("express");
const helmet = require("helmet");        // Security headers
const morgan = require("morgan");        // Request logging
const config = require("./config");

const app = express();

// ── Middleware ──────────────────────────────────────────────────
app.use(helmet());                         // Security headers
app.use(morgan("combined"));               // Log all requests
app.use(express.json());                   // Parse JSON request bodies
app.use(express.urlencoded({ extended: true }));

// ── Routes ─────────────────────────────────────────────────────
const applicationRoutes = require("./routes/applications");
const documentRoutes = require("./routes/documents");
const healthRoutes = require("./routes/health");

app.use("/api/v1/applications", applicationRoutes);
app.use("/api/v1/documents", documentRoutes);
app.use("/health", healthRoutes);

// ── 404 Handler ────────────────────────────────────────────────
app.use((req, res) => {
  res.status(404).json({
    success: false,
    message: "Endpoint not found",
    path: req.path
  });
});

// ── Global Error Handler ───────────────────────────────────────
app.use((err, req, res, next) => {
  console.error("Unhandled error:", err);
  res.status(500).json({
    success: false,
    message: "An unexpected error occurred",
    code: "INTERNAL_SERVER_ERROR"
  });
});

// ── Start Server ───────────────────────────────────────────────
const PORT = config.port || 3000;
app.listen(PORT, () => {
  console.log(`🚀 TAMM Building Permit Service running on port ${PORT}`);
  console.log(`📋 Environment: ${config.environment}`);
});
```

---

### 6.4 File System & Streams

TAMM services frequently handle documents (PDFs, images). Node.js's built-in `fs` module handles file operations.

```javascript
const fs = require("fs");
const path = require("path");

// Read a file asynchronously (non-blocking ✅)
fs.readFile(path.join(__dirname, "templates", "permit-template.pdf"), (err, data) => {
  if (err) {
    console.error("Failed to read template:", err.message);
    return;
  }
  console.log(`Template loaded: ${data.length} bytes`);
});

// Write a file (e.g. generated permit)
fs.writeFile(
  path.join(__dirname, "output", "permit-12345.pdf"),
  generatedPdfBuffer,
  (err) => {
    if (err) throw err;
    console.log("Permit saved successfully");
  }
);

// Check if a file exists before processing
fs.access("uploads/doc-001.pdf", fs.constants.F_OK, (err) => {
  if (err) {
    console.log("Document not found");
  } else {
    console.log("Document exists, proceeding");
  }
});
```

---

### 6.5 Environment Variables

Environment variables allow the same code to behave differently in development, staging, and production. This is fundamental to TAMM service configuration.

```javascript
// .env file (NEVER commit this to git)
NODE_ENV=development
PORT=3001
TAMM_API_BASE_URL=https://dev-api.tamm.ae
JWT_SECRET=your-secret-key-here
DB_CONNECTION_STRING=postgresql://localhost:5432/tamm_dev
```

```javascript
// src/config/index.js
require("dotenv").config();

module.exports = {
  environment: process.env.NODE_ENV || "development",
  port: parseInt(process.env.PORT, 10) || 3000,
  tammApiBaseUrl: process.env.TAMM_API_BASE_URL,
  jwtSecret: process.env.JWT_SECRET,
  db: {
    connectionString: process.env.DB_CONNECTION_STRING
  }
};
```

> ⚠️ **Security Rule:** Never hardcode secrets in source code. Never commit `.env` files. Always add `.env` to `.gitignore`.

---

## 7. Step-by-Step Examples

### Example 1: Hello World

Let's set up your first Node.js project from scratch.

**Step 1: Create the project folder**

```bash
mkdir tamm-hello
cd tamm-hello
npm init -y
```

**Step 2: Create the entry file**

```javascript
// index.js
console.log("Hello from TAMM Node.js Service!");
console.log(`Node.js version: ${process.version}`);
console.log(`Platform: ${process.platform}`);
console.log(`Running environment: ${process.env.NODE_ENV || "not set"}`);
```

**Step 3: Run it**

```bash
node index.js
```

**Expected output:**
```
Hello from TAMM Node.js Service!
Node.js version: v20.11.0
Platform: linux
Running environment: not set
```

---

### Example 2: Building a TAMM REST API

Let's build a working API endpoint for retrieving application status — a core TAMM feature.

**Step 1: Install dependencies**

```bash
mkdir tamm-api-server
cd tamm-api-server
npm init -y
npm install express dotenv helmet morgan
npm install --save-dev nodemon
```

**Step 2: Add dev script to package.json**

```json
"scripts": {
  "start": "node src/index.js",
  "dev": "nodemon src/index.js"
}
```

**Step 3: Create the project structure**

```
tamm-api-server/
├── src/
│   ├── index.js
│   ├── routes/
│   │   └── applications.js
│   ├── controllers/
│   │   └── applications.controller.js
│   └── data/
│       └── mock-applications.js
└── .env
```

**Step 4: Mock data (simulating a database)**

```javascript
// src/data/mock-applications.js

const applications = [
  {
    id: "APP-2024-001",
    serviceId: "TAMM-MUN-2024-001",
    serviceName: "Building Permit Application",
    applicantName: "Mohammed Al Mansoori",
    submittedAt: "2024-06-10T09:00:00Z",
    status: "under_review",
    statusLabel: { en: "Under Review", ar: "قيد المراجعة" },
    estimatedCompletion: "2024-06-20T17:00:00Z"
  },
  {
    id: "APP-2024-002",
    serviceId: "TAMM-MUN-2024-001",
    serviceName: "Building Permit Application",
    applicantName: "Fatima Al Zaabi",
    submittedAt: "2024-06-08T11:30:00Z",
    status: "approved",
    statusLabel: { en: "Approved", ar: "تمت الموافقة" },
    estimatedCompletion: null,
    approvedAt: "2024-06-14T14:00:00Z"
  },
  {
    id: "APP-2024-003",
    serviceId: "TAMM-MUN-2024-001",
    serviceName: "Building Permit Application",
    applicantName: "Ahmed Al Rashidi",
    submittedAt: "2024-06-12T08:00:00Z",
    status: "documents_required",
    statusLabel: { en: "Documents Required", ar: "المستندات مطلوبة" },
    missingDocuments: ["Architectural Plans", "NOC from Neighbours"]
  }
];

module.exports = applications;
```

**Step 5: Controller**

```javascript
// src/controllers/applications.controller.js

const applications = require("../data/mock-applications");

// GET /api/v1/applications  — list all applications for the current user
function getAllApplications(req, res) {
  const lang = req.headers["accept-language"]?.includes("ar") ? "ar" : "en";

  const result = applications.map(app => ({
    id: app.id,
    serviceName: app.serviceName,
    status: app.status,
    statusLabel: app.statusLabel[lang],
    submittedAt: app.submittedAt
  }));

  res.status(200).json({
    success: true,
    count: result.length,
    data: result
  });
}

// GET /api/v1/applications/:id  — get a single application's details
function getApplicationById(req, res) {
  const { id } = req.params;
  const app = applications.find(a => a.id === id);

  if (!app) {
    return res.status(404).json({
      success: false,
      message: `Application ${id} not found`,
      code: "APPLICATION_NOT_FOUND"
    });
  }

  res.status(200).json({
    success: true,
    data: app
  });
}

module.exports = { getAllApplications, getApplicationById };
```

**Step 6: Routes**

```javascript
// src/routes/applications.js

const express = require("express");
const router = express.Router();
const { getAllApplications, getApplicationById } = require("../controllers/applications.controller");

// GET /api/v1/applications
router.get("/", getAllApplications);

// GET /api/v1/applications/:id
router.get("/:id", getApplicationById);

module.exports = router;
```

**Step 7: Main server file**

```javascript
// src/index.js

require("dotenv").config();
const express = require("express");
const helmet = require("helmet");
const morgan = require("morgan");

const app = express();

app.use(helmet());
app.use(morgan("dev"));
app.use(express.json());

// Routes
const applicationRoutes = require("./routes/applications");
app.use("/api/v1/applications", applicationRoutes);

// Health check
app.get("/health", (req, res) => {
  res.json({ status: "ok", service: "tamm-api-server", timestamp: new Date().toISOString() });
});

// 404
app.use((req, res) => {
  res.status(404).json({ success: false, message: "Not found" });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`✅ TAMM API Server running on http://localhost:${PORT}`);
});
```

**Step 8: Run and test**

```bash
npm run dev
```

Open your browser or use curl:

```bash
# List all applications
curl http://localhost:3000/api/v1/applications

# Get specific application
curl http://localhost:3000/api/v1/applications/APP-2024-001

# Get Arabic labels
curl -H "Accept-Language: ar" http://localhost:3000/api/v1/applications
```

**Expected Response:**
```json
{
  "success": true,
  "count": 3,
  "data": [
    {
      "id": "APP-2024-001",
      "serviceName": "Building Permit Application",
      "status": "under_review",
      "statusLabel": "Under Review",
      "submittedAt": "2024-06-10T09:00:00Z"
    }
  ]
}
```

---

### Example 3: Connecting to a Database

TAMM uses PostgreSQL for relational data. Here's how to connect using the `pg` library.

```bash
npm install pg
```

```javascript
// src/db/connection.js

const { Pool } = require("pg");

const pool = new Pool({
  connectionString: process.env.DB_CONNECTION_STRING,
  max: 10,               // Maximum number of connections in pool
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000
});

// Test connection on startup
pool.connect((err, client, release) => {
  if (err) {
    console.error("❌ Database connection failed:", err.message);
    return;
  }
  console.log("✅ Database connected successfully");
  release();
});

module.exports = pool;
```

```javascript
// src/repositories/applications.repository.js

const pool = require("../db/connection");

async function findApplicationsByUserId(userId) {
  const query = `
    SELECT 
      a.id,
      a.service_id,
      s.name_en AS service_name,
      a.status,
      a.submitted_at,
      a.updated_at
    FROM applications a
    JOIN services s ON a.service_id = s.id
    WHERE a.user_id = $1
    ORDER BY a.submitted_at DESC
  `;

  const result = await pool.query(query, [userId]);
  return result.rows;
}

async function findApplicationById(applicationId) {
  const query = `
    SELECT * FROM applications WHERE id = $1
  `;
  const result = await pool.query(query, [applicationId]);
  return result.rows[0] || null;
}

async function createApplication(applicationData) {
  const { userId, serviceId, formData } = applicationData;
  
  const query = `
    INSERT INTO applications (user_id, service_id, form_data, status, submitted_at)
    VALUES ($1, $2, $3, 'submitted', NOW())
    RETURNING id, status, submitted_at
  `;

  const result = await pool.query(query, [userId, serviceId, JSON.stringify(formData)]);
  return result.rows[0];
}

module.exports = { findApplicationsByUserId, findApplicationById, createApplication };
```

---

### Example 4: Document Upload Service

TAMM applications always involve document uploads. Here is a complete upload endpoint using `multer`.

```bash
npm install multer uuid
```

```javascript
// src/middleware/upload.middleware.js

const multer = require("multer");
const path = require("path");
const { v4: uuidv4 } = require("uuid");

const ALLOWED_MIME_TYPES = ["application/pdf", "image/jpeg", "image/png"];
const MAX_FILE_SIZE_MB = 10;

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, "uploads/documents/");
  },
  filename: (req, file, cb) => {
    // Generate a unique filename to prevent overwrites
    const ext = path.extname(file.originalname);
    const uniqueName = `${uuidv4()}${ext}`;
    cb(null, uniqueName);
  }
});

const fileFilter = (req, file, cb) => {
  if (ALLOWED_MIME_TYPES.includes(file.mimetype)) {
    cb(null, true);  // Accept file
  } else {
    cb(new Error(`File type not allowed. Permitted: PDF, JPEG, PNG`), false);
  }
};

const upload = multer({
  storage,
  fileFilter,
  limits: { fileSize: MAX_FILE_SIZE_MB * 1024 * 1024 }
});

module.exports = upload;
```

```javascript
// src/routes/documents.js

const express = require("express");
const router = express.Router();
const upload = require("../middleware/upload.middleware");

// POST /api/v1/documents/upload
router.post("/upload", upload.single("document"), (req, res) => {
  if (!req.file) {
    return res.status(400).json({
      success: false,
      message: "No file uploaded"
    });
  }

  res.status(201).json({
    success: true,
    message: "Document uploaded successfully",
    data: {
      documentId: req.file.filename.split(".")[0],  // UUID without extension
      filename: req.file.filename,
      originalName: req.file.originalname,
      size: req.file.size,
      mimeType: req.file.mimetype,
      uploadedAt: new Date().toISOString()
    }
  });
});

module.exports = router;
```

---

## 8. Best Practices for TAMM

```javascript
// ✅ Always use async/await with try/catch
async function getApplication(id) {
  try {
    const app = await findApplicationById(id);
    return app;
  } catch (error) {
    console.error(`Failed to get application ${id}:`, error.message);
    throw error;  // Let the error propagate to the route handler
  }
}

// ✅ Always validate input before processing
function validateApplicationId(id) {
  const pattern = /^APP-\d{4}-\d{3,6}$/;
  return pattern.test(id);
}

// ✅ Return consistent API responses
function successResponse(res, data, statusCode = 200) {
  return res.status(statusCode).json({ success: true, data });
}

function errorResponse(res, message, code, statusCode = 400) {
  return res.status(statusCode).json({ success: false, message, code });
}

// ✅ Log with context, not just messages
console.log({
  event: "application_submitted",
  applicationId: "APP-2024-001",
  userId: "USR-10021",
  serviceId: "TAMM-MUN-2024-001",
  timestamp: new Date().toISOString()
});
```

---

## 9. Common Mistakes & How to Avoid Them

| Mistake | Why It's a Problem | Fix |
|---|---|---|
| Blocking the event loop with sync code | Freezes the server for all users | Use async `fs.readFile` not `fs.readFileSync` |
| Forgetting `await` on async functions | Silent promise resolution, bugs hard to trace | Always `await` async calls; use `eslint-plugin-promise` |
| Committing `.env` files | Exposes secrets to the world | Add `.env` to `.gitignore` immediately |
| Not handling promise rejections | Unhandled rejections crash Node.js 18+ | Always `.catch()` or `try/catch` |
| Logging sensitive data | Privacy and security violation (UAE PDPL) | Never log Emirates IDs, passwords, or tokens |
| Missing input validation | Security vulnerabilities, bad data in DB | Validate every input with a library like `joi` |

---

## 10. Summary & What's Next

In this module you learned:

- ✅ **What Node.js is** — a JavaScript runtime for server-side code
- ✅ **Why TAMM uses Node.js** — non-blocking I/O, JSON-native, microservices-friendly
- ✅ **Node.js history** — from Ryan Dahl's 2009 demo to today's enterprise-grade platform
- ✅ **The Event Loop** — how Node.js handles thousands of concurrent requests without blocking
- ✅ **Key components:** modules, npm, Express.js, file system, environment variables
- ✅ **4 working examples:** Hello World → REST API → Database → Document Upload
- ✅ **Best practices** specific to the TAMM platform

---

### ➡️ Next: [Module 2 — React.js for TAMM](./02-reactjs.md) *(coming soon)*

Module 2 covers building TAMM's front-end service forms and dashboards with React.js — connecting to the API server you just built.

---

> 📌 **Module 1 of 5** | TAMM Developer Training  
> Last updated: June 2025

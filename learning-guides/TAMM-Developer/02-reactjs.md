# ⚛️ Module 2 — React.js for TAMM Developers

> **Prerequisites:** [Module 1 — Node.js](./01-nodejs.md)  
> **Time to complete:** ~3 hours  
> **Next Module:** [03-angular.md](./03-angular.md)

---

## Table of Contents

1. [What is React?](#1-what-is-react)
2. [Why TAMM Uses React](#2-why-tamm-uses-react)
3. [Brief History of React](#3-brief-history-of-react)
4. [Core Concepts](#4-core-concepts)
   - [4.1 JSX](#41-jsx)
   - [4.2 Components](#42-components)
   - [4.3 Props](#43-props)
   - [4.4 State with useState](#44-state-with-usestate)
   - [4.5 Side Effects with useEffect](#45-side-effects-with-useeffect)
   - [4.6 Context API](#46-context-api)
5. [TAMM-Specific Patterns](#5-tamm-specific-patterns)
   - [5.1 Bilingual Support (Arabic/English)](#51-bilingual-support-arabicenglish)
   - [5.2 RTL Layout Handling](#52-rtl-layout-handling)
   - [5.3 Service Journey Form Wizard](#53-service-journey-form-wizard)
   - [5.4 Document Upload Component](#54-document-upload-component)
   - [5.5 Application Status Tracker](#55-application-status-tracker)
6. [State Management with Redux Toolkit](#6-state-management-with-redux-toolkit)
7. [Connecting to TAMM APIs](#7-connecting-to-tamm-apis)
8. [Step-by-Step: Build a TAMM Service Page](#8-step-by-step-build-a-tamm-service-page)
9. [Best Practices](#9-best-practices)
10. [Summary & What's Next](#10-summary--whats-next)

---

## 1. What is React?

**React** is a JavaScript **library** for building user interfaces. It was created by Facebook (now Meta) and is the most widely used front-end library in the world.

React's core idea is simple but powerful:

> **Your UI is a function of your data. When data changes, React re-renders only what changed.**

```
Traditional web development:
  Data changes → you manually find DOM elements → you manually update them
  (error-prone, hard to scale, painful to maintain)

React:
  Data changes → React automatically figures out what changed → React updates only that part
  (predictable, fast, maintainable)
```

React doesn't tell you how to structure your entire application — it focuses on one thing: **rendering UI components**.

---

## 2. Why TAMM Uses React

| Reason | TAMM Context |
|---|---|
| **Component reusability** | A `DocumentUpload` component is built once and used across 700+ services |
| **Virtual DOM performance** | Complex forms with real-time validation re-render only changed fields |
| **Rich ecosystem** | Libraries for forms (React Hook Form), state (Redux), routing (React Router) |
| **Bilingual/RTL support** | React's conditional rendering makes Arabic/English switching clean |
| **Developer productivity** | Hot Module Replacement means developers see changes instantly |
| **React Native** | The TAMM mobile app shares logic with the web app via React Native |

---

## 3. Brief History of React

### 2011 — The Problem at Facebook

Facebook's engineering team was drowning. Their News Feed and the Ads management interface had grown so complex that a change to one part of the UI would silently break another. The issue: **two-way data binding** meant UI updates could cascade in unpredictable ways.

Engineer **Jordan Walke** started experimenting with a new approach he called **FaxJS** — a component-based model where UI was a direct function of data, with one-way data flow.

### 2013 — Open Source Release

Facebook open-sourced React at **JSConf US 2013**. The reception was initially skeptical — JSX (mixing HTML-like syntax into JavaScript) felt wrong to many developers. Tom Occhino and Jordan Walke's demo convinced doubters: React made complex UIs *understandable*.

### 2015 — React Native

Facebook released **React Native**, bringing React's component model to iOS and Android. TAMM's mobile app (launched 2019) uses React Native, meaning front-end developers could contribute to both web and mobile.

### 2016 — React 15 & Production Maturity

React became the undisputed leader of the front-end world. AirBnB, Netflix, Uber, Twitter all migrated to React. The pattern of building large-scale applications with React was proven.

### 2019 — React Hooks

**React Hooks** (introduced in 16.8) were the biggest change in React's history. Before hooks, complex logic required class components — verbose and hard to reuse. Hooks let you use state and lifecycle features in simple function components.

```javascript
// BEFORE Hooks (class component — still valid, but verbose)
class ApplicationStatus extends React.Component {
  constructor(props) {
    super(props);
    this.state = { status: "loading" };
  }
  componentDidMount() {
    fetchStatus(this.props.id).then(data => this.setState({ status: data.status }));
  }
  render() {
    return <div>{this.state.status}</div>;
  }
}

// AFTER Hooks (function component — the TAMM standard today)
function ApplicationStatus({ id }) {
  const [status, setStatus] = useState("loading");
  useEffect(() => {
    fetchStatus(id).then(data => setStatus(data.status));
  }, [id]);
  return <div>{status}</div>;
}
```

TAMM's front-end codebase uses **function components with hooks exclusively**. You will not write class components.

### 2022–Present — React 18 & Concurrent Features

React 18 introduced **Concurrent Mode** — React can now pause, interrupt, and resume rendering work, keeping the UI responsive even during heavy updates. TAMM's latest pages use React 18's `Suspense` for loading states.

---

## 4. Core Concepts

### 4.1 JSX

**JSX** is a syntax extension that lets you write HTML-like code inside JavaScript. It is compiled to regular JavaScript by Babel.

```jsx
// JSX (what you write)
const ServiceCard = () => (
  <div className="service-card">
    <h2>Building Permit Application</h2>
    <p>Department of Municipalities and Transport</p>
    <button onClick={() => alert("Starting application...")}>
      Apply Now
    </button>
  </div>
);

// What JSX compiles to (what the browser actually runs)
const ServiceCard = () => React.createElement(
  "div", { className: "service-card" },
  React.createElement("h2", null, "Building Permit Application"),
  React.createElement("p", null, "Department of Municipalities and Transport"),
  React.createElement("button", { onClick: () => alert("Starting...") }, "Apply Now")
);
```

> 💡 You write JSX. The browser runs the compiled version. You never need to write `React.createElement` manually.

#### JSX Rules

```jsx
// ✅ Must return one root element (or a Fragment)
return (
  <div>
    <h1>Title</h1>
    <p>Body</p>
  </div>
);

// ✅ Or use a Fragment to avoid extra div
return (
  <>
    <h1>Title</h1>
    <p>Body</p>
  </>
);

// ✅ className not class (class is a reserved JS word)
<div className="card">

// ✅ JavaScript expressions go inside curly braces {}
<p>Service: {serviceName}</p>
<p>Fee: {fee} AED</p>
<p>Date: {new Date().toLocaleDateString()}</p>

// ✅ Self-close tags that have no children
<input type="text" />
<img src={logoUrl} alt="TAMM logo" />
```

---

### 4.2 Components

A component is a **reusable, self-contained piece of UI**. Think of them as custom HTML elements you design yourself.

```jsx
// A simple TAMM service badge component
// components/ServiceBadge.jsx

function ServiceBadge({ category, color }) {
  const colors = {
    "Construction": "#E67E22",
    "Business": "#2980B9",
    "Healthcare": "#27AE60",
    "Education": "#8E44AD"
  };

  return (
    <span
      style={{
        background: colors[category] || "#95A5A6",
        color: "white",
        padding: "4px 12px",
        borderRadius: "20px",
        fontSize: "12px",
        fontWeight: "600"
      }}
    >
      {category}
    </span>
  );
}

export default ServiceBadge;
```

```jsx
// Using ServiceBadge in a parent component
import ServiceBadge from "./ServiceBadge";

function ServiceCard({ service }) {
  return (
    <div className="service-card">
      <ServiceBadge category={service.category} />
      <h3>{service.name}</h3>
      <p>{service.description}</p>
    </div>
  );
}
```

---

### 4.3 Props

**Props** (short for properties) are how you pass data **from parent to child** components. They are read-only — a child component never modifies its own props.

```jsx
// Parent passes data down via props
function ApplicationDashboard() {
  const applications = [
    { id: "APP-001", service: "Building Permit", status: "approved", date: "2024-06-15" },
    { id: "APP-002", service: "Trade Licence Renewal", status: "under_review", date: "2024-06-18" },
    { id: "APP-003", service: "Health Card", status: "documents_required", date: "2024-06-20" }
  ];

  return (
    <div className="dashboard">
      <h1>My Applications</h1>
      {applications.map(app => (
        <ApplicationRow
          key={app.id}           // ← React needs a unique key for lists
          id={app.id}
          service={app.service}
          status={app.status}
          date={app.date}
        />
      ))}
    </div>
  );
}

// Child receives props and renders them
function ApplicationRow({ id, service, status, date }) {
  const statusColors = {
    approved: "#27AE60",
    under_review: "#F39C12",
    documents_required: "#E74C3C"
  };

  return (
    <div className="application-row">
      <span className="app-id">{id}</span>
      <span className="app-service">{service}</span>
      <span style={{ color: statusColors[status] }}>
        {status.replace(/_/g, " ")}
      </span>
      <span className="app-date">{date}</span>
    </div>
  );
}
```

---

### 4.4 State with useState

**State** is data that lives inside a component and can change over time. When state changes, React re-renders the component.

```jsx
// Form with state — collecting applicant details
import { useState } from "react";

function ApplicantDetailsForm({ onSubmit }) {
  const [formData, setFormData] = useState({
    fullName: "",
    emiratesId: "",
    mobileNumber: "",
    email: ""
  });
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Update a single field without losing others
  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // Clear error for the field being edited
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: null }));
    }
  };

  const validate = () => {
    const newErrors = {};
    if (!formData.fullName.trim()) newErrors.fullName = "Full name is required";
    if (!/^\d{15}$/.test(formData.emiratesId)) newErrors.emiratesId = "Emirates ID must be 15 digits";
    if (!/^\+971\d{9}$/.test(formData.mobileNumber)) newErrors.mobileNumber = "Enter a valid UAE mobile (+9715XXXXXXXX)";
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) newErrors.email = "Enter a valid email address";
    return newErrors;
  };

  const handleSubmit = async () => {
    const validationErrors = validate();
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }
    setIsSubmitting(true);
    await onSubmit(formData);
    setIsSubmitting(false);
  };

  return (
    <div className="form-section">
      <h2>Applicant Details</h2>

      <div className="form-group">
        <label>Full Name</label>
        <input
          type="text"
          value={formData.fullName}
          onChange={e => handleChange("fullName", e.target.value)}
          placeholder="As per Emirates ID"
        />
        {errors.fullName && <span className="error">{errors.fullName}</span>}
      </div>

      <div className="form-group">
        <label>Emirates ID</label>
        <input
          type="text"
          value={formData.emiratesId}
          onChange={e => handleChange("emiratesId", e.target.value)}
          placeholder="784XXXXXXXXXXXX"
          maxLength={15}
        />
        {errors.emiratesId && <span className="error">{errors.emiratesId}</span>}
      </div>

      <div className="form-group">
        <label>Mobile Number</label>
        <input
          type="tel"
          value={formData.mobileNumber}
          onChange={e => handleChange("mobileNumber", e.target.value)}
          placeholder="+971XXXXXXXXX"
        />
        {errors.mobileNumber && <span className="error">{errors.mobileNumber}</span>}
      </div>

      <div className="form-group">
        <label>Email Address</label>
        <input
          type="email"
          value={formData.email}
          onChange={e => handleChange("email", e.target.value)}
          placeholder="you@example.com"
        />
        {errors.email && <span className="error">{errors.email}</span>}
      </div>

      <button
        onClick={handleSubmit}
        disabled={isSubmitting}
        className="btn-primary"
      >
        {isSubmitting ? "Saving..." : "Continue →"}
      </button>
    </div>
  );
}

export default ApplicantDetailsForm;
```

---

### 4.5 Side Effects with useEffect

`useEffect` runs code **after** a component renders. It's used for API calls, subscriptions, and anything that reaches outside the component.

```jsx
import { useState, useEffect } from "react";

function ApplicationStatusPage({ applicationId }) {
  const [application, setApplication] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Runs after the component mounts, and again if applicationId changes
  useEffect(() => {
    let cancelled = false;  // Prevents state updates if component unmounts

    async function fetchApplication() {
      try {
        setLoading(true);
        const res = await fetch(`/api/v1/applications/${applicationId}`, {
          headers: { Authorization: `Bearer ${getToken()}` }
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        if (!cancelled) setApplication(data.data);
      } catch (err) {
        if (!cancelled) setError(err.message);
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    fetchApplication();

    // Cleanup: if user navigates away before fetch completes
    return () => { cancelled = true; };

  }, [applicationId]);  // ← Dependency array: re-run when applicationId changes

  if (loading) return <div className="loading-spinner">Loading application...</div>;
  if (error) return <div className="error-banner">Failed to load: {error}</div>;
  if (!application) return null;

  return (
    <div className="status-page">
      <h1>Application {application.id}</h1>
      <StatusBadge status={application.status} />
      <p>Submitted: {new Date(application.submittedAt).toLocaleDateString()}</p>
    </div>
  );
}
```

> 💡 **Dependency Array Rules:**
> - `useEffect(() => {}, [])` — runs once on mount (like componentDidMount)
> - `useEffect(() => {}, [id])` — runs on mount AND whenever `id` changes
> - `useEffect(() => {})` — runs after every render (use sparingly — usually a bug)

---

### 4.6 Context API

**Context** lets you share data across the entire component tree without passing props through every level. TAMM uses Context for global data: the authenticated user, the current language, and the active journey session.

```jsx
// context/LanguageContext.jsx

import { createContext, useContext, useState } from "react";

const LanguageContext = createContext();

export function LanguageProvider({ children }) {
  const [language, setLanguage] = useState("en");
  const isRTL = language === "ar";

  const translate = (textObj) => {
    if (typeof textObj === "string") return textObj;
    return textObj[language] || textObj["en"] || "";
  };

  return (
    <LanguageContext.Provider value={{ language, setLanguage, isRTL, translate }}>
      <div dir={isRTL ? "rtl" : "ltr"} lang={language}>
        {children}
      </div>
    </LanguageContext.Provider>
  );
}

// Custom hook for easy access
export function useLanguage() {
  const context = useContext(LanguageContext);
  if (!context) throw new Error("useLanguage must be inside LanguageProvider");
  return context;
}
```

```jsx
// Using the context anywhere in the app — no prop drilling
function ServiceTitle({ service }) {
  const { translate } = useLanguage();
  return <h1>{translate(service.title)}</h1>;
  // If language is "ar", renders service.title.ar
  // If language is "en", renders service.title.en
}
```

---

## 5. TAMM-Specific Patterns

### 5.1 Bilingual Support (Arabic/English)

TAMM is natively bilingual. Every user-visible string must support both Arabic and English.

```jsx
// hooks/useTranslation.js  — TAMM's translation hook

import { useLanguage } from "../context/LanguageContext";

// All UI strings in one place
const translations = {
  en: {
    "apply_now": "Apply Now",
    "save_draft": "Save Draft",
    "required_field": "This field is required",
    "upload_document": "Upload Document",
    "file_too_large": "File must be under 10MB",
    "application_submitted": "Application submitted successfully",
    "steps_remaining": (n) => `${n} step${n !== 1 ? "s" : ""} remaining`,
  },
  ar: {
    "apply_now": "تقدم الآن",
    "save_draft": "حفظ المسودة",
    "required_field": "هذا الحقل مطلوب",
    "upload_document": "رفع المستند",
    "file_too_large": "يجب أن يكون حجم الملف أقل من 10 ميجابايت",
    "application_submitted": "تم تقديم الطلب بنجاح",
    "steps_remaining": (n) => `${n} ${n === 1 ? "خطوة" : "خطوات"} متبقية`,
  }
};

export function useTranslation() {
  const { language } = useLanguage();
  const t = (key, ...args) => {
    const val = translations[language]?.[key] || translations["en"][key] || key;
    return typeof val === "function" ? val(...args) : val;
  };
  return { t };
}
```

```jsx
// Using the translation hook
function JourneyProgress({ stepsRemaining }) {
  const { t } = useTranslation();
  return (
    <div className="progress-bar">
      <span>{t("steps_remaining", stepsRemaining)}</span>
      <button>{t("save_draft")}</button>
    </div>
  );
}
// English: "3 steps remaining"
// Arabic:  "٣ خطوات متبقية"
```

---

### 5.2 RTL Layout Handling

Arabic reads right-to-left. React handles this gracefully with CSS logical properties and the `dir` attribute.

```jsx
// components/ApplicationRow.jsx — RTL-aware layout

function ApplicationRow({ application, language }) {
  const isRTL = language === "ar";

  return (
    <div
      className="application-row"
      dir={isRTL ? "rtl" : "ltr"}
      style={{
        // CSS logical properties adapt automatically to text direction
        paddingInlineStart: "20px",   // = paddingLeft in LTR, paddingRight in RTL
        paddingInlineEnd: "20px",
        borderInlineStart: "4px solid #007DC6",  // Left border in LTR, Right in RTL
      }}
    >
      <span className="app-id">{application.id}</span>
      <span className="app-name">
        {isRTL ? application.serviceName.ar : application.serviceName.en}
      </span>
      <StatusBadge status={application.status} />
    </div>
  );
}
```

```css
/* styles/global.css — RTL-aware utilities */

[dir="rtl"] .icon-arrow {
  transform: scaleX(-1);  /* Flip directional icons for RTL */
}

[dir="rtl"] .breadcrumb-separator::before {
  content: "‹";   /* RTL breadcrumb separator */
}

[dir="ltr"] .breadcrumb-separator::before {
  content: "›";
}
```

---

### 5.3 Service Journey Form Wizard

This is the most important React pattern in TAMM — a multi-step form wizard that represents a service journey.

```jsx
// components/JourneyWizard.jsx

import { useState } from "react";
import { useTranslation } from "../hooks/useTranslation";

// Each step is a separate component
import Step_ApplicantDetails from "./steps/ApplicantDetails";
import Step_DocumentUpload from "./steps/DocumentUpload";
import Step_Review from "./steps/Review";
import Step_Payment from "./steps/Payment";
import Step_Confirmation from "./steps/Confirmation";

const STEPS = [
  { id: "applicant", label: { en: "Your Details", ar: "بياناتك" }, component: Step_ApplicantDetails },
  { id: "documents", label: { en: "Documents", ar: "المستندات" }, component: Step_DocumentUpload },
  { id: "review", label: { en: "Review", ar: "المراجعة" }, component: Step_Review },
  { id: "payment", label: { en: "Payment", ar: "الدفع" }, component: Step_Payment },
  { id: "confirmation", label: { en: "Confirmation", ar: "التأكيد" }, component: Step_Confirmation },
];

function JourneyWizard({ serviceId, onComplete }) {
  const { t } = useTranslation();
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [journeyData, setJourneyData] = useState({});
  const [completedSteps, setCompletedSteps] = useState(new Set());

  const currentStep = STEPS[currentStepIndex];
  const StepComponent = currentStep.component;
  const isLastStep = currentStepIndex === STEPS.length - 1;

  const handleStepComplete = (stepData) => {
    // Merge this step's data into the full journey data
    const updatedData = { ...journeyData, [currentStep.id]: stepData };
    setJourneyData(updatedData);
    setCompletedSteps(prev => new Set([...prev, currentStep.id]));

    if (isLastStep) {
      onComplete(updatedData);
    } else {
      setCurrentStepIndex(prev => prev + 1);
    }
  };

  const handleBack = () => {
    setCurrentStepIndex(prev => Math.max(0, prev - 1));
  };

  return (
    <div className="journey-wizard">
      {/* Progress Stepper */}
      <StepperBar
        steps={STEPS}
        currentIndex={currentStepIndex}
        completedSteps={completedSteps}
      />

      {/* Current Step */}
      <div className="step-content">
        <StepComponent
          existingData={journeyData[currentStep.id]}
          allData={journeyData}
          onComplete={handleStepComplete}
          onBack={currentStepIndex > 0 ? handleBack : null}
        />
      </div>
    </div>
  );
}

// ─── Stepper Bar ──────────────────────────────────────────────────────────────

function StepperBar({ steps, currentIndex, completedSteps }) {
  const { language } = useLanguage();

  return (
    <div className="stepper-bar" role="navigation" aria-label="Application steps">
      {steps.map((step, index) => {
        const isCompleted = completedSteps.has(step.id);
        const isCurrent = index === currentIndex;
        const isUpcoming = index > currentIndex;

        return (
          <div
            key={step.id}
            className={`step-indicator ${isCurrent ? "active" : ""} ${isCompleted ? "completed" : ""}`}
            aria-current={isCurrent ? "step" : undefined}
          >
            <div className="step-circle">
              {isCompleted ? "✓" : index + 1}
            </div>
            <span className="step-label">
              {language === "ar" ? step.label.ar : step.label.en}
            </span>
            {index < steps.length - 1 && <div className="step-connector" />}
          </div>
        );
      })}
    </div>
  );
}

export default JourneyWizard;
```

---

### 5.4 Document Upload Component

```jsx
// components/DocumentUpload.jsx

import { useState, useRef } from "react";
import { useTranslation } from "../hooks/useTranslation";

function DocumentUpload({ documentId, documentName, mandatory, onUpload }) {
  const { t } = useTranslation();
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState(null);
  const [uploadedDocId, setUploadedDocId] = useState(null);
  const inputRef = useRef();

  const ALLOWED_TYPES = ["application/pdf", "image/jpeg", "image/png"];
  const MAX_SIZE_MB = 10;

  const handleFileSelect = (e) => {
    const selected = e.target.files[0];
    if (!selected) return;

    // Validate type
    if (!ALLOWED_TYPES.includes(selected.type)) {
      setError("Only PDF, JPG, and PNG files are allowed");
      return;
    }

    // Validate size
    if (selected.size > MAX_SIZE_MB * 1024 * 1024) {
      setError(t("file_too_large"));
      return;
    }

    setError(null);
    setFile(selected);
    uploadFile(selected);
  };

  const uploadFile = async (fileToUpload) => {
    setUploading(true);
    setUploadProgress(0);

    try {
      const formData = new FormData();
      formData.append("document", fileToUpload);
      formData.append("documentId", documentId);

      // Simulated progress (in production, use XMLHttpRequest for real progress)
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => Math.min(prev + 15, 90));
      }, 200);

      const res = await fetch("/api/v1/documents/upload", {
        method: "POST",
        headers: { Authorization: `Bearer ${getToken()}` },
        body: formData
      });

      clearInterval(progressInterval);
      setUploadProgress(100);

      if (!res.ok) throw new Error("Upload failed");
      const data = await res.json();

      setUploadedDocId(data.data.documentId);
      onUpload(documentId, data.data.documentId);

    } catch (err) {
      setError("Upload failed. Please try again.");
      setFile(null);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className={`document-upload ${mandatory ? "required" : ""}`}>
      <div className="doc-header">
        <span className="doc-name">{documentName}</span>
        {mandatory && <span className="badge-required">Required</span>}
      </div>

      {!uploadedDocId ? (
        <div
          className="upload-zone"
          onClick={() => inputRef.current?.click()}
          onDragOver={(e) => e.preventDefault()}
          onDrop={(e) => {
            e.preventDefault();
            const dropped = e.dataTransfer.files[0];
            if (dropped) handleFileSelect({ target: { files: [dropped] } });
          }}
        >
          <input
            ref={inputRef}
            type="file"
            accept=".pdf,.jpg,.jpeg,.png"
            onChange={handleFileSelect}
            style={{ display: "none" }}
          />
          <div className="upload-icon">📎</div>
          <p>{t("upload_document")}</p>
          <p className="upload-hint">PDF, JPG, PNG — max 10MB</p>
        </div>
      ) : (
        <div className="upload-success">
          <span className="success-icon">✅</span>
          <span>{file?.name}</span>
          <button
            className="btn-remove"
            onClick={() => { setUploadedDocId(null); setFile(null); }}
          >
            Remove
          </button>
        </div>
      )}

      {uploading && (
        <div className="progress-bar">
          <div className="progress-fill" style={{ width: `${uploadProgress}%` }} />
        </div>
      )}

      {error && <p className="error-text">{error}</p>}
    </div>
  );
}

export default DocumentUpload;
```

---

### 5.5 Application Status Tracker

```jsx
// components/StatusTracker.jsx — Timeline showing application progress

function StatusTracker({ applicationId }) {
  const [timeline, setTimeline] = useState([]);

  useEffect(() => {
    fetch(`/api/v1/applications/${applicationId}/timeline`)
      .then(r => r.json())
      .then(data => setTimeline(data.events));
  }, [applicationId]);

  const statusConfig = {
    submitted:           { icon: "📋", color: "#3498DB", label: "Submitted" },
    under_review:        { icon: "🔍", color: "#F39C12", label: "Under Review" },
    documents_required:  { icon: "📎", color: "#E74C3C", label: "Documents Required" },
    approved:            { icon: "✅", color: "#27AE60", label: "Approved" },
    rejected:            { icon: "❌", color: "#C0392B", label: "Rejected" }
  };

  return (
    <div className="status-tracker">
      {timeline.map((event, index) => {
        const config = statusConfig[event.status] || {};
        const isLatest = index === timeline.length - 1;

        return (
          <div key={event.id} className={`timeline-event ${isLatest ? "latest" : ""}`}>
            <div className="timeline-icon" style={{ background: config.color }}>
              {config.icon}
            </div>
            <div className="timeline-content">
              <strong>{config.label}</strong>
              <p>{event.note}</p>
              <time>{new Date(event.timestamp).toLocaleString("en-AE")}</time>
            </div>
            {index < timeline.length - 1 && <div className="timeline-connector" />}
          </div>
        );
      })}
    </div>
  );
}
```

---

## 6. State Management with Redux Toolkit

For complex journey state that spans multiple steps, TAMM uses **Redux Toolkit (RTK)** — the modern, recommended way to use Redux.

```bash
npm install @reduxjs/toolkit react-redux
```

```javascript
// store/journeySlice.js — using Redux Toolkit's createSlice

import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";

// Async thunk for saving drafts
export const saveDraft = createAsyncThunk(
  "journey/saveDraft",
  async ({ journeyInstanceId, stepId, data }, thunkAPI) => {
    const res = await fetch("/api/v1/drafts", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${getToken()}`
      },
      body: JSON.stringify({ journeyInstanceId, stepId, data })
    });
    if (!res.ok) return thunkAPI.rejectWithValue("Draft save failed");
    return await res.json();
  }
);

const journeySlice = createSlice({
  name: "journey",
  initialState: {
    serviceId: null,
    currentStepId: null,
    formData: {},
    status: "idle",       // idle | in_progress | submitted | failed
    draftSaving: false,
    errors: {}
  },
  reducers: {
    startJourney(state, action) {
      state.serviceId = action.payload.serviceId;
      state.status = "in_progress";
      state.currentStepId = action.payload.firstStepId;
    },
    completeStep(state, action) {
      const { stepId, data } = action.payload;
      state.formData[stepId] = data;
    },
    navigateToStep(state, action) {
      state.currentStepId = action.payload;
    },
    setError(state, action) {
      const { stepId, message } = action.payload;
      state.errors[stepId] = message;
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(saveDraft.pending, (state) => { state.draftSaving = true; })
      .addCase(saveDraft.fulfilled, (state) => { state.draftSaving = false; })
      .addCase(saveDraft.rejected, (state) => { state.draftSaving = false; });
  }
});

export const { startJourney, completeStep, navigateToStep, setError } = journeySlice.actions;
export default journeySlice.reducer;
```

```javascript
// store/index.js
import { configureStore } from "@reduxjs/toolkit";
import journeyReducer from "./journeySlice";

export const store = configureStore({
  reducer: {
    journey: journeyReducer
  }
});
```

```jsx
// Using the store in a component
import { useSelector, useDispatch } from "react-redux";
import { completeStep, saveDraft } from "../store/journeySlice";

function ReviewStep({ onComplete }) {
  const dispatch = useDispatch();
  const { formData, draftSaving } = useSelector(state => state.journey);

  const handleSaveDraft = () => {
    dispatch(saveDraft({
      journeyInstanceId: "JRN-001",
      stepId: "review",
      data: formData
    }));
  };

  return (
    <div>
      <h2>Review Your Application</h2>
      <pre>{JSON.stringify(formData, null, 2)}</pre>
      <button onClick={handleSaveDraft} disabled={draftSaving}>
        {draftSaving ? "Saving..." : "Save Draft"}
      </button>
      <button onClick={() => dispatch(completeStep({ stepId: "review", data: {} }))}>
        Proceed to Payment
      </button>
    </div>
  );
}
```

---

## 7. Connecting to TAMM APIs

```javascript
// services/api.service.js — centralised API layer

const API_BASE = process.env.REACT_APP_TAMM_API_BASE || "https://api.tamm.ae";

async function tammFetch(endpoint, options = {}) {
  const token = localStorage.getItem("tamm_access_token");

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      "Accept-Language": localStorage.getItem("tamm_language") || "en",
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers
    }
  });

  if (response.status === 401) {
    // Token expired — redirect to UAE Pass re-authentication
    window.location.href = "/auth/uaepass";
    return;
  }

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.message || `Request failed: ${response.status}`);
  }

  return response.json();
}

export const ApplicationService = {
  getAll: () => tammFetch("/api/v1/applications"),
  getById: (id) => tammFetch(`/api/v1/applications/${id}`),
  submit: (data) => tammFetch("/api/v1/applications", { method: "POST", body: JSON.stringify(data) }),
  saveDraft: (data) => tammFetch("/api/v1/drafts", { method: "POST", body: JSON.stringify(data) })
};

export const ServiceCatalogueService = {
  getAll: () => tammFetch("/api/v1/services"),
  getById: (id) => tammFetch(`/api/v1/services/${id}`),
  search: (query) => tammFetch(`/api/v1/services/search?q=${encodeURIComponent(query)}`)
};
```

---

## 8. Step-by-Step: Build a TAMM Service Page

Let's build a complete TAMM service listing page with search.

```bash
npx create-react-app tamm-services-page
cd tamm-services-page
npm install axios
```

```jsx
// src/App.jsx

import { useState, useEffect } from "react";
import "./App.css";

// Mock service data
const MOCK_SERVICES = [
  { id: "SVC-001", name: { en: "Building Permit", ar: "رخصة بناء" }, category: "Construction", fee: 500, days: 10 },
  { id: "SVC-002", name: { en: "Trade Licence Renewal", ar: "تجديد رخصة تجارية" }, category: "Business", fee: 1200, days: 5 },
  { id: "SVC-003", name: { en: "Health Card Application", ar: "طلب بطاقة صحية" }, category: "Healthcare", fee: 0, days: 3 },
  { id: "SVC-004", name: { en: "Birth Certificate", ar: "شهادة ميلاد" }, category: "Civil", fee: 50, days: 2 },
];

const CATEGORIES = ["All", "Construction", "Business", "Healthcare", "Civil"];

function App() {
  const [language, setLanguage] = useState("en");
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [services, setServices] = useState(MOCK_SERVICES);
  const [filtered, setFiltered] = useState(MOCK_SERVICES);

  // Filter services whenever search or category changes
  useEffect(() => {
    let result = services;

    if (selectedCategory !== "All") {
      result = result.filter(s => s.category === selectedCategory);
    }

    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      result = result.filter(s =>
        s.name.en.toLowerCase().includes(q) ||
        s.name.ar.includes(q)
      );
    }

    setFiltered(result);
  }, [searchQuery, selectedCategory, services]);

  const t = (en, ar) => language === "ar" ? ar : en;

  return (
    <div className="app" dir={language === "ar" ? "rtl" : "ltr"}>
      {/* Header */}
      <header className="app-header">
        <div className="logo">
          <span className="logo-text">تمّ</span>
          <span className="logo-sub">TAMM Abu Dhabi</span>
        </div>
        <button
          className="lang-toggle"
          onClick={() => setLanguage(l => l === "en" ? "ar" : "en")}
        >
          {language === "en" ? "عربي" : "English"}
        </button>
      </header>

      {/* Hero */}
      <section className="hero">
        <h1>{t("Abu Dhabi Government Services", "خدمات حكومة أبوظبي")}</h1>
        <p>{t("Complete your government transactions anytime, anywhere", "أنجز معاملاتك الحكومية في أي وقت ومن أي مكان")}</p>
        <input
          className="search-bar"
          type="search"
          placeholder={t("Search services...", "ابحث عن الخدمات...")}
          value={searchQuery}
          onChange={e => setSearchQuery(e.target.value)}
        />
      </section>

      {/* Category Filter */}
      <nav className="category-nav">
        {CATEGORIES.map(cat => (
          <button
            key={cat}
            className={`category-btn ${selectedCategory === cat ? "active" : ""}`}
            onClick={() => setSelectedCategory(cat)}
          >
            {cat}
          </button>
        ))}
      </nav>

      {/* Service Grid */}
      <main className="services-grid">
        {filtered.length === 0 ? (
          <div className="empty-state">
            <p>{t("No services found", "لا توجد خدمات")}</p>
          </div>
        ) : (
          filtered.map(service => (
            <ServiceCard key={service.id} service={service} language={language} />
          ))
        )}
      </main>
    </div>
  );
}

function ServiceCard({ service, language }) {
  const t = (en, ar) => language === "ar" ? ar : en;
  const categoryColors = {
    Construction: "#E67E22", Business: "#2980B9",
    Healthcare: "#27AE60", Civil: "#8E44AD"
  };

  return (
    <div className="service-card">
      <div className="card-category" style={{ color: categoryColors[service.category] }}>
        {service.category}
      </div>
      <h3 className="card-title">
        {language === "ar" ? service.name.ar : service.name.en}
      </h3>
      <div className="card-meta">
        <span>💰 {service.fee === 0 ? t("Free", "مجاني") : `${service.fee} AED`}</span>
        <span>⏱ {service.days} {t("days", "أيام")}</span>
      </div>
      <button className="card-btn">
        {t("Apply Now →", "تقدم الآن ←")}
      </button>
    </div>
  );
}

export default App;
```

```css
/* src/App.css */

* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Segoe UI', 'Arial', sans-serif; background: #F5F7FA; color: #2C3E50; }

.app-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 16px 32px; background: #007DC6; color: white;
}
.logo-text { font-size: 28px; font-weight: bold; margin-inline-end: 8px; }
.logo-sub { font-size: 14px; opacity: 0.85; }
.lang-toggle {
  background: rgba(255,255,255,0.2); border: 1px solid rgba(255,255,255,0.4);
  color: white; padding: 6px 16px; border-radius: 20px; cursor: pointer;
}

.hero { text-align: center; padding: 60px 32px; background: white; }
.hero h1 { font-size: 36px; color: #007DC6; margin-bottom: 12px; }
.hero p { font-size: 18px; color: #7F8C8D; margin-bottom: 32px; }
.search-bar {
  width: 100%; max-width: 560px; padding: 14px 20px; font-size: 16px;
  border: 2px solid #BDC3C7; border-radius: 32px; outline: none;
}
.search-bar:focus { border-color: #007DC6; }

.category-nav { display: flex; gap: 10px; padding: 20px 32px; flex-wrap: wrap; }
.category-btn {
  padding: 8px 18px; border-radius: 20px; border: 2px solid #BDC3C7;
  background: white; cursor: pointer; font-size: 14px;
}
.category-btn.active { background: #007DC6; color: white; border-color: #007DC6; }

.services-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px; padding: 16px 32px 48px;
}
.service-card {
  background: white; border-radius: 12px; padding: 24px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08); transition: transform 0.2s;
}
.service-card:hover { transform: translateY(-4px); }
.card-category { font-size: 12px; font-weight: 600; text-transform: uppercase; margin-bottom: 8px; }
.card-title { font-size: 18px; font-weight: 600; margin-bottom: 16px; color: #2C3E50; }
.card-meta { display: flex; gap: 16px; font-size: 13px; color: #7F8C8D; margin-bottom: 20px; }
.card-btn {
  width: 100%; padding: 10px; background: #007DC6; color: white;
  border: none; border-radius: 8px; font-size: 15px; cursor: pointer;
}
.card-btn:hover { background: #005A8E; }
```

**Run it:**
```bash
npm start
```

You now have a bilingual TAMM services listing page with search and category filtering.

---

## 9. Best Practices

```jsx
// ✅ Use custom hooks to extract complex logic from components
function useApplicationStatus(id) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  useEffect(() => {
    ApplicationService.getById(id)
      .then(setData)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, [id]);
  return { data, loading, error };
}

// ✅ Memoize expensive calculations
const filteredServices = useMemo(
  () => services.filter(s => s.category === selectedCategory),
  [services, selectedCategory]  // Only recalculates when these change
);

// ✅ Accessibility: all interactive elements need aria labels
<button aria-label="Remove uploaded document" onClick={handleRemove}>✕</button>

// ✅ Always handle all three loading states
if (loading) return <LoadingSpinner />;
if (error) return <ErrorBanner message={error} />;
if (!data) return <EmptyState />;
return <DataDisplay data={data} />;
```

---

## 10. Summary & What's Next

In this module you learned:

- ✅ **What React is** — a UI library that re-renders based on state
- ✅ **React history** — from Jordan Walke's 2011 experiment to Hooks in 2019
- ✅ **Core concepts** — JSX, Components, Props, useState, useEffect, Context
- ✅ **TAMM patterns** — bilingual support, RTL layout, journey wizard, document upload, status tracker
- ✅ **Redux Toolkit** — managing complex cross-step journey state
- ✅ **Full example** — a working bilingual TAMM services page with search

### ➡️ Next: [Module 3 — Angular for TAMM](./03-angular.md)

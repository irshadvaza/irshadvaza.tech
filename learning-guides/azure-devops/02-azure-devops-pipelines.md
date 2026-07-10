# Azure DevOps Learning Guide
## Chapter 02: Azure DevOps Pipelines (CI/CD) for Python & Streamlit Applications

> **Author:** Irshad Vaza  
> **Category:** Azure DevOps • CI/CD • Python • Streamlit  
> **Level:** Beginner to Intermediate

---

# Introduction

After storing your source code in Azure DevOps Repositories, the next step is automation.

Imagine every time you make a code change:

- Code is automatically validated
- Dependencies are checked
- Tests are executed
- Deployment package is created
- Application is deployed automatically

Instead of performing these tasks manually, Azure DevOps Pipelines can do them for you.

This process is known as:

- **CI (Continuous Integration)**
- **CD (Continuous Delivery / Continuous Deployment)**

---

# What is CI/CD?

## Continuous Integration (CI)

Continuous Integration automatically validates your code whenever you push changes to the repository.

Example:

1. Developer updates app.py
2. Code is pushed to Azure DevOps
3. Pipeline starts automatically
4. Dependencies are installed
5. Tests run
6. Build succeeds or fails

---

## Continuous Delivery (CD)

Continuous Delivery automatically prepares your application for deployment.

Example:

1. Build completes successfully
2. Deployment package is generated
3. Package is deployed to Test environment
4. User validates the application

---

## Continuous Deployment

Continuous Deployment goes one step further.

Example:

1. Code pushed
2. Build successful
3. Application automatically deployed to Production

No manual intervention required.

---

# Why Use Azure DevOps Pipelines?

Without Pipeline

```text
Developer
   ↓
Copy files manually
   ↓
Remote Server
   ↓
Restart Application
```

Problems:

- Human errors
- Missed files
- Slow deployments
- No audit trail

---

With Pipeline

```text
Developer
   ↓
Git Push
   ↓
Azure DevOps Pipeline
   ↓
Build
   ↓
Test
   ↓
Deploy
```

Benefits:

✔ Faster deployment

✔ Reduced errors

✔ Version control

✔ Audit history

✔ Automated validation

✔ Team collaboration

---

# Pipeline Components

A typical Azure DevOps Pipeline contains:

```text
Source Code
     ↓
Build
     ↓
Test
     ↓
Package
     ↓
Deploy
```

---

# Azure DevOps Pipeline Types

## 1. Classic Pipeline

Uses graphical interface.

Advantages:

- Easy for beginners
- No YAML knowledge required

Disadvantages:

- Difficult to maintain
- Not stored in source control

---

## 2. YAML Pipeline (Recommended)

Pipeline configuration stored as code.

Advantages:

- Version controlled
- Easy to share
- Industry standard
- Reusable

Example:

```yaml
trigger:
- main

pool:
  vmImage: ubuntu-latest

steps:
- script: echo Hello Pipeline
```

---

# Pipeline Architecture Example

For a Streamlit application:

```text
VS Code
   ↓
Git Push
   ↓
Azure DevOps Repo
   ↓
Pipeline Trigger
   ↓
Install Python
   ↓
Install Requirements
   ↓
Run Tests
   ↓
Create Package
   ↓
Deploy
```

---

# Creating Your First Pipeline

## Step 1

Open Azure DevOps

```text
Project
   └── Pipelines
```

---

## Step 2

Click

```text
New Pipeline
```

---

## Step 3

Select Source

```text
Azure Repos Git
```

---

## Step 4

Select Repository

Example:

```text
FishCatchAI
```

---

## Step 5

Choose

```text
Starter Pipeline
```

Azure DevOps creates

```text
azure-pipelines.yml
```

---

# Understanding YAML Structure

Example

```yaml
trigger:
- main

pool:
  vmImage: ubuntu-latest

steps:
- script: echo Hello World
```

---

## trigger

```yaml
trigger:
- main
```

Meaning:

Whenever code is pushed to main branch, pipeline starts automatically.

---

## pool

```yaml
pool:
  vmImage: ubuntu-latest
```

Meaning:

Use Microsoft-hosted Ubuntu server to execute tasks.

---

## steps

```yaml
steps:
```

Contains pipeline actions.

---

# First Python Pipeline

Example

```yaml
trigger:
- main

pool:
  vmImage: ubuntu-latest

steps:

- task: UsePythonVersion@0
  inputs:
    versionSpec: '3.11'

- script: python --version
  displayName: Check Python Version
```

---

# Install Dependencies

Most Python projects contain:

```text
requirements.txt
```

Pipeline:

```yaml
- script: |
    pip install -r requirements.txt
  displayName: Install Packages
```

---

# Complete Streamlit Example

```yaml
trigger:
- main

pool:
  vmImage: ubuntu-latest

steps:

- task: UsePythonVersion@0
  inputs:
    versionSpec: '3.11'

- script: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt
  displayName: Install Dependencies

- script: |
    python --version
  displayName: Verify Python

- script: |
    echo Build Completed
  displayName: Build Validation
```

---

# Understanding Pipeline Execution

When developer executes:

```bash
git add .
git commit -m "New feature"
git push
```

Azure DevOps automatically:

```text
Pipeline Started
      ↓
Install Python
      ↓
Install Packages
      ↓
Validate Build
      ↓
Pipeline Success
```

---

# Viewing Pipeline Logs

Inside Azure DevOps:

```text
Pipelines
   ↓
Select Run
   ↓
Logs
```

You can see:

- Commands executed
- Errors
- Warnings
- Build duration

---

# Pipeline Status

Successful Run

```text
✔ Succeeded
```

Failed Run

```text
✖ Failed
```

Partially Successful

```text
⚠ Warning
```

---

# Common Pipeline Errors

## Missing Requirements File

Error

```text
requirements.txt not found
```

Solution

Verify file exists in repository root.

---

## Python Version Not Found

Error

```text
Python version unavailable
```

Solution

Use supported version.

Example:

```yaml
versionSpec: '3.11'
```

---

## Package Installation Failure

Error

```text
pip install failed
```

Solution

Check package name and version.

---

# Best Practices

## Keep Pipeline Simple

Start with:

```text
Install
Validate
Deploy
```

Add complexity gradually.

---

## Store Pipeline as Code

Always use:

```text
azure-pipelines.yml
```

Benefits:

- Version controlled
- Easy rollback
- Team visibility

---

## Use Requirements File

Avoid:

```yaml
pip install streamlit
pip install pandas
pip install numpy
```

Use:

```yaml
pip install -r requirements.txt
```

---

## Test Before Deployment

Validate application before deployment.

Example:

```yaml
pytest
```

---

# Real World Example

FishCatchAI Project

```text
Developer Updates Code
           ↓
Push to Azure DevOps
           ↓
Pipeline Triggered
           ↓
Install Python
           ↓
Install Streamlit
           ↓
Install OpenAI SDK
           ↓
Validate Build
           ↓
Deploy to Server
```

Benefits:

- Faster releases
- Consistent deployments
- Reduced production issues

---

# Key Terms

| Term | Meaning |
|--------|---------|
| CI | Continuous Integration |
| CD | Continuous Delivery |
| Pipeline | Automated workflow |
| Build | Validate and package code |
| Agent | Machine executing pipeline |
| YAML | Pipeline configuration file |
| Trigger | Event that starts pipeline |
| Deployment | Releasing application |

---

# Summary

In this chapter, you learned:

✔ What CI/CD means

✔ Why Azure DevOps Pipelines are important

✔ Difference between CI and CD

✔ How YAML pipelines work

✔ How to create a basic pipeline

✔ How to build Python applications

✔ How to install dependencies automatically

✔ How to monitor pipeline execution

✔ Best practices for production projects

---

# Next Chapter

➡ Chapter 03: Branching Strategy and Git Workflow

Topics:

- Main Branch
- Develop Branch
- Feature Branches
- Release Branches
- Hotfix Branches
- Git Flow Best Practices
- Real-World Team Collaboration

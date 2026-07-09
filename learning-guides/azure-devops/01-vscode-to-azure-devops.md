# Azure DevOps Learning Guide
## Connect an Existing VS Code Project to Azure DevOps Repository

> **Author:** Irshad Vaza  
> **Category:** Azure DevOps • Git • VS Code • Python • Streamlit  
> **Level:** Beginner to Intermediate

---

# Introduction

One of the first tasks every developer performs is connecting their local project to a source control repository.

This guide explains how to:

- Verify Git installation
- Check whether VS Code is already connected to another repository
- Disconnect an existing Git remote safely
- Initialize a new Git repository
- Connect the project to Azure DevOps
- Push the project to Azure DevOps
- Verify the connection
- Understand each Git command with examples

Although this guide uses a **Python + Streamlit + SQLite** project, the same process applies to any programming language.

---

# Prerequisites

Before starting, ensure you have:

- Visual Studio Code
- Git installed
- Azure DevOps Project
- Azure DevOps Repository
- Access permissions to push code
- Internet connection

---

# Step 1 — Verify Git Installation

Open the VS Code Terminal.

Run:

```bash
git --version
```

Example

```text
git version 2.49.0.windows.1
```

### What this command does

Checks whether Git is installed and displays the installed version.

---

# Step 2 — Navigate to Your Project

```bash
cd D:\Projects\FishCatchAI
```

or simply open the folder in VS Code.

### Why?

Git commands always execute against the current folder.

---

# Step 3 — Check Whether Git Is Already Initialized

Run

```bash
git status
```

Possible Result

```text
fatal: not a git repository
```

Meaning

The folder has never been initialized.

If you see

```text
On branch main
nothing to commit
```

then Git is already enabled.

---

# Step 4 — Check Existing Remote Repository

Run

```bash
git remote -v
```

Example

```text
origin https://github.com/company/FishAI.git
```

or

```text
origin https://dev.azure.com/company/project/_git/FishAI
```

### Why?

This command tells Git where your code will be pushed.

This is the most important command before changing repositories.

---

# Step 5 — View Git Configuration

Display all Git settings

```bash
git config --list
```

Display global settings

```bash
git config --global --list
```

Display username

```bash
git config user.name
```

Display email

```bash
git config user.email
```

These values are attached to every commit you create.

---

# Step 6 — Remove Existing Remote Repository

If your project is connected to another repository, remove it.

```bash
git remote remove origin
```

Verify

```bash
git remote -v
```

Expected Output

No output.

Meaning the connection has been removed successfully.

---

# Step 7 — Remove Existing Git History (Optional)

If you want a completely fresh repository

Windows CMD

```cmd
rmdir /s /q .git
```

PowerShell

```powershell
Remove-Item -Recurse -Force .git
```

This deletes all previous Git history.

---

# Step 8 — Initialize Git

```bash
git init
```

Output

```text
Initialized empty Git repository
```

### Purpose

Creates a new local Git repository.

---

# Step 9 — Create .gitignore

Example

```text
__pycache__/
*.pyc

.venv/
venv/

.env

.streamlit/secrets.toml

.vscode/

.idea/

logs/

*.log

*.db-journal
*.sqlite-journal
```

If your SQLite database contains production data

```text
*.db
```

---

# Step 10 — Stage All Files

```bash
git add .
```

### Purpose

Adds every changed file into the staging area.

Nothing is committed yet.

---

# Step 11 — Commit Your Code

```bash
git commit -m "Initial commit"
```

### Purpose

Creates a snapshot of your project.

---

# Step 12 — Create Azure DevOps Repository

Inside Azure DevOps

```
Project

    Repos

        New Repository
```

Copy the Clone URL.

Example

```
https://dev.azure.com/CompanyName/AIProject/_git/FishCatchAI
```

---

# Step 13 — Connect Local Repository

```bash
git remote add origin https://dev.azure.com/CompanyName/AIProject/_git/FishCatchAI
```

Verify

```bash
git remote -v
```

---

# Step 14 — Rename Default Branch

```bash
git branch -M main
```

### Why?

Ensures the default branch is named **main**.

---

# Step 15 — Push to Azure DevOps

```bash
git push -u origin main
```

The first push may ask you to authenticate.

After successful authentication your project will appear inside Azure DevOps Repos.

---

# Step 16 — Verify Upload

Open Azure DevOps

```
Repos
```

Refresh the page.

All files should now be visible.

---

# Frequently Used Git Commands

| Command | Purpose |
|----------|---------|
| git status | Shows modified files |
| git add . | Stage all changes |
| git commit -m "message" | Save changes |
| git push | Upload commits |
| git pull | Download latest changes |
| git branch | Show branches |
| git branch -M main | Rename branch |
| git remote -v | View connected repository |
| git remote remove origin | Remove repository connection |
| git log --oneline | View commit history |
| git config --list | Display Git configuration |

---

# Recommended Repository Structure

```
FishCatchAI/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env
├── database/
├── pages/
├── services/
├── prompts/
├── utils/
├── uploads/
├── logs/
└── .streamlit/
```

---

# Best Practices

✔ Commit frequently

✔ Write meaningful commit messages

✔ Never commit passwords

✔ Never commit API keys

✔ Ignore virtual environments

✔ Ignore log files

✔ Ignore temporary files

✔ Keep requirements.txt updated

✔ Create feature branches for new development

✔ Push code regularly

---

# Summary

After completing this guide you can confidently:

- Connect VS Code to Azure DevOps
- Check existing Git repositories
- Remove old Git connections
- Initialize a new repository
- Push projects to Azure DevOps
- Verify repository configuration
- Manage source code using Git best practices

---

## Next Learning Guide

➡ Azure DevOps Pipelines (CI/CD)

➡ Git Branching Strategy

➡ Pull Requests

➡ Merge Conflict Resolution

➡ Deploy Streamlit Applications Using Azure DevOps

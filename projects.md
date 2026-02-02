[Home](index.md) | [Projects](projects.md) | [Blogs](blogs.md) | [About](about.md) | [Contact](contact.md)

---

# 🚀 AI & Data Projects Portfolio

Welcome to my **enterprise-grade project showcase**, featuring real-world AI systems, intelligent automation platforms, and cloud data architectures designed for **production, governance, and scalability**.  

Each project below is presented as a **case study**, highlighting architecture, business impact, and technical depth.

---

## 🧩 SmartSQL  
### AI-Powered Natural Language → SQL Platform

![SmartSQL Banner](images/smartSQL_arch.png)

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/) [![Streamlit](https://img.shields.io/badge/Streamlit-UI-orange)](https://streamlit.io/) [![Azure AI](https://img.shields.io/badge/Azure_AI-blueviolet)](https://azure.microsoft.com/)

---

### 💡 Business Problem
Business users and analysts often depend on data teams to write SQL queries, creating **delays in decision-making** and **analytics bottlenecks**.

**SmartSQL** solves this by enabling **non-technical users to query enterprise databases directly using natural language**, while maintaining **security and governance**.

---

### 🛠 Solution Overview
SmartSQL leverages **Azure AI and Large Language Models (LLMs)** to:  

1. Convert natural language questions into **validated SQL queries**  
2. Execute queries securely on **SQL Server / Azure SQL**  
3. Present results in a **clean, interactive Streamlit interface**  

---

### ✨ Key Capabilities
- 🔹 Natural Language → SQL via LLMs  
- 🔹 Secure SQL validation layer  
- 🔹 Streamlit-based interactive web interface  
- 🔹 Support for On-Prem SQL Server & Azure SQL  
- 🔹 Optional **voice-based query input**  
- 🔹 Query history & result visualization  

---

### 🏗 Architecture & Workflow
```text
User (Natural Language Query)
        │
        ▼
   SmartSQL Frontend (Streamlit)
        │
        ▼
  LLM + Query Validation Layer
        │
        ▼
  SQL Server / Azure SQL
        │
        ▼
 Query Results → Streamlit Visualization

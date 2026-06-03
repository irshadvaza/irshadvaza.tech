# 🏭 Enterprise Inspection Copilot — Upgrade Guide

> **Your starting point:** A working Streamlit RAG app (Azure OpenAI embeddings + Groq LLM)  
> **Your goal:** A production-grade enterprise app with company/facility selection + multi-document RAG

---

## 📦 What You're Building — Big Picture

```
BEFORE (your current app):
  User uploads PDFs manually → one session → no company context

AFTER (enterprise app):
  ┌─────────────────────────────────────────────────────────┐
  │  STEP 1 — Select Company  (Dropdown)                    │
  │  STEP 2 — Select Facility (Dropdown — filtered by co.)  │
  │  STEP 3 — Pick Documents  (Multi-select list)           │
  │  STEP 4 — AI RAG Summary  (LangChain + Azure AI)        │
  └─────────────────────────────────────────────────────────┘
```

---

## 🗺️ Upgrade Roadmap (Step by Step)

| Phase | What You Build | Files Changed |
|-------|---------------|---------------|
| **STEP 1** | Company/Facility database + config | `company_data.py` (NEW) |
| **STEP 2** | Company & Facility dropdowns in UI | `app.py` (MODIFIED) |
| **STEP 3** | Document registry per facility | `company_data.py` (EXTENDED) |
| **STEP 4** | Multi-document selector | `app.py` (MODIFIED) |
| **STEP 5** | LangChain + Azure AI RAG on selected docs | `rag.py` (MODIFIED) |
| **STEP 6** | AI Summary panel | `app.py` + `ui_components.py` |

---

## STEP 1 — Company/Facility Database

### 🤔 What Is This?
Instead of users uploading files manually every time, we store a **registry** of companies, their facilities, and the documents belonging to each facility. Think of it like a phone book for your inspection documents.

### 📁 New File: `company_data.py`

```python
# company_data.py
# ─────────────────────────────────────────────────────────────
# PURPOSE: Central registry of all companies, facilities,
#          and their documents.
#
# In a real enterprise app, this data would come from a
# database (SQL Server, PostgreSQL, Azure Cosmos DB).
# For now, we use a Python dictionary — easy to understand,
# easy to replace later.
#
# STRUCTURE:
# COMPANIES = {
#   "company_id": {
#     "name": "Display Name",
#     "facilities": {
#       "facility_id": {
#         "name": "Facility Name",
#         "location": "City, Country",
#         "documents": [
#           { "id": "doc1", "name": "Display Name", "path": "actual/file/path.pdf" }
#         ]
#       }
#     }
#   }
# }
# ─────────────────────────────────────────────────────────────

COMPANIES = {
    "aramco": {
        "name": "Saudi Aramco",
        "facilities": {
            "dhahran_hq": {
                "name": "Dhahran HQ Complex",
                "location": "Dhahran, Saudi Arabia",
                "documents": [
                    {
                        "id": "dhahran_permit_2024",
                        "name": "Environmental Permit 2024",
                        "path": "documents/aramco/dhahran/permit_2024.pdf",
                        "type": "Permit"
                    },
                    {
                        "id": "dhahran_inspection_q1",
                        "name": "Q1 2024 Inspection Report",
                        "path": "documents/aramco/dhahran/inspection_q1_2024.pdf",
                        "type": "Inspection Report"
                    },
                    {
                        "id": "dhahran_eia",
                        "name": "EIA Study 2023",
                        "path": "documents/aramco/dhahran/eia_2023.pdf",
                        "type": "EIA Study"
                    }
                ]
            },
            "yanbu_refinery": {
                "name": "Yanbu Refinery",
                "location": "Yanbu, Saudi Arabia",
                "documents": [
                    {
                        "id": "yanbu_permit_2024",
                        "name": "Operating Permit 2024",
                        "path": "documents/aramco/yanbu/permit_2024.pdf",
                        "type": "Permit"
                    },
                    {
                        "id": "yanbu_violation_2023",
                        "name": "Violation Notice 2023",
                        "path": "documents/aramco/yanbu/violation_2023.pdf",
                        "type": "Enforcement"
                    }
                ]
            }
        }
    },
    "adnoc": {
        "name": "ADNOC",
        "facilities": {
            "ruwais": {
                "name": "Ruwais Industrial Complex",
                "location": "Ruwais, Abu Dhabi",
                "documents": [
                    {
                        "id": "ruwais_permit",
                        "name": "Facility Environmental Permit",
                        "path": "documents/adnoc/ruwais/permit.pdf",
                        "type": "Permit"
                    },
                    {
                        "id": "ruwais_monitoring",
                        "name": "Air Quality Monitoring 2024",
                        "path": "documents/adnoc/ruwais/air_monitoring_2024.pdf",
                        "type": "Monitoring"
                    }
                ]
            },
            "hamriyah": {
                "name": "Al Hamriyah Free Zone",
                "location": "Sharjah, UAE",
                "documents": [
                    {
                        "id": "hamriyah_inspection",
                        "name": "2024 Compliance Audit",
                        "path": "documents/adnoc/hamriyah/audit_2024.pdf",
                        "type": "Inspection Report"
                    }
                ]
            }
        }
    },
    "emaar": {
        "name": "Emaar Properties",
        "facilities": {
            "downtown_dubai": {
                "name": "Downtown Dubai Development",
                "location": "Dubai, UAE",
                "documents": [
                    {
                        "id": "downtown_eia",
                        "name": "EIA Study Phase 2",
                        "path": "documents/emaar/downtown/eia_phase2.pdf",
                        "type": "EIA Study"
                    }
                ]
            }
        }
    }
}


# ─────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# These functions let app.py query the registry cleanly.
# They act like a simple "database API".
# ─────────────────────────────────────────────────────────────

def get_company_list():
    """
    Returns list of (id, display_name) tuples for the dropdown.
    
    Example return:
        [("aramco", "Saudi Aramco"), ("adnoc", "ADNOC"), ...]
    """
    return [(cid, cdata["name"]) for cid, cdata in COMPANIES.items()]


def get_facilities_for_company(company_id: str):
    """
    Given a company ID, returns its facilities as (id, name) tuples.
    
    Example:
        get_facilities_for_company("aramco")
        → [("dhahran_hq", "Dhahran HQ Complex"), ("yanbu_refinery", "Yanbu Refinery")]
    """
    if company_id not in COMPANIES:
        return []
    facilities = COMPANIES[company_id]["facilities"]
    return [(fid, fdata["name"]) for fid, fdata in facilities.items()]


def get_documents_for_facility(company_id: str, facility_id: str):
    """
    Returns list of document dicts for a specific facility.
    Each dict has: id, name, path, type
    
    Example:
        get_documents_for_facility("aramco", "dhahran_hq")
        → [{"id": "dhahran_permit_2024", "name": "Environmental Permit 2024", ...}, ...]
    """
    try:
        return COMPANIES[company_id]["facilities"][facility_id]["documents"]
    except KeyError:
        return []


def get_facility_info(company_id: str, facility_id: str):
    """
    Returns full info dict for a facility (name, location, documents).
    Used to display facility details in the sidebar.
    """
    try:
        return COMPANIES[company_id]["facilities"][facility_id]
    except KeyError:
        return {}
```

---

## STEP 2 — Add Dropdowns to the UI

### 🤔 What Is This?
We add two dropdowns to `app.py`:
1. **Company dropdown** — shows all companies
2. **Facility dropdown** — updates automatically based on selected company

### ✏️ Modify `app.py` — Replace the Upload Section

Find the `# ═══ SCREEN A — UPLOAD SCREEN` section in your `app.py`.  
**Replace the entire upload section** with this:

```python
# ─────────────────────────────────────────────────────────────
# ADD THIS IMPORT at the top of app.py (after existing imports)
# ─────────────────────────────────────────────────────────────
from company_data import (
    get_company_list,
    get_facilities_for_company,
    get_documents_for_facility,
    get_facility_info,
)

# ─────────────────────────────────────────────────────────────
# ADD THESE to SESSION_DEFAULTS dictionary
# ─────────────────────────────────────────────────────────────
SESSION_DEFAULTS = {
    # ... your existing defaults ...
    "document_uploaded": False,
    "vector_store":      None,
    "llm":               None,
    "messages":          [],
    "doc_names":         [],
    "chunk_count":       0,
    "show_report":       False,
    "last_report":       "",
    # NEW entries below:
    "selected_company":  None,   # company ID string
    "selected_facility": None,   # facility ID string
    "selected_doc_ids":  [],     # list of selected document IDs
}
```

### The New Upload Screen (full replacement):

```python
# ═══════════════════════════════════════════════════════════════
#  SCREEN A — SELECTION SCREEN (replaces upload screen)
# ═══════════════════════════════════════════════════════════════
if not st.session_state.document_uploaded:

    render_upload_header()  # keep your existing header

    # ── CARD 1: Company Selection ─────────────────────────────
    st.markdown('<div class="ui-card">', unsafe_allow_html=True)
    st.markdown('<div class="ui-card-title">Step 1 — Select Company</div>',
                unsafe_allow_html=True)

    # Build dropdown options: [("", "— Select —"), ("aramco", "Saudi Aramco"), ...]
    company_options = [("", "— Select a Company —")] + get_company_list()
    company_labels  = [label for _, label in company_options]
    company_ids     = [cid   for cid, _  in company_options]

    # st.selectbox shows labels, but we need the underlying ID
    selected_company_label = st.selectbox(
        "Company / Organization",
        options=company_labels,
        index=0,  # default: first item (the "Select" placeholder)
        help="Select the company whose facilities you want to inspect"
    )

    # Convert the displayed label back to the ID
    selected_company_idx = company_labels.index(selected_company_label)
    selected_company_id  = company_ids[selected_company_idx]

    # Save to session_state so it survives re-runs
    st.session_state.selected_company = selected_company_id

    st.markdown('</div>', unsafe_allow_html=True)

    # ── CARD 2: Facility Selection ────────────────────────────
    # Only shown after a company is selected
    if selected_company_id:

        st.markdown('<div class="ui-card">', unsafe_allow_html=True)
        st.markdown('<div class="ui-card-title">Step 2 — Select Facility</div>',
                    unsafe_allow_html=True)

        # Get facilities for the chosen company
        facility_options = [("", "— Select a Facility —")] + \
                           get_facilities_for_company(selected_company_id)
        facility_labels = [label for _, label in facility_options]
        facility_ids    = [fid   for fid, _  in facility_options]

        selected_facility_label = st.selectbox(
            "Facility / Site",
            options=facility_labels,
            index=0,
            help="Select the specific facility to inspect"
        )

        selected_facility_idx = facility_labels.index(selected_facility_label)
        selected_facility_id  = facility_ids[selected_facility_idx]

        st.session_state.selected_facility = selected_facility_id

        # Show facility info (location, doc count) as a small info box
        if selected_facility_id:
            finfo = get_facility_info(selected_company_id, selected_facility_id)
            st.info(f"📍 **Location:** {finfo.get('location', 'N/A')} — "
                    f"**{len(finfo.get('documents', []))} documents** available")

        st.markdown('</div>', unsafe_allow_html=True)

        # ── CARD 3: Document Selection ─────────────────────────
        # Only shown after a facility is selected
        if selected_facility_id:

            st.markdown('<div class="ui-card">', unsafe_allow_html=True)
            st.markdown('<div class="ui-card-title">Step 3 — Select Documents</div>',
                        unsafe_allow_html=True)

            docs_available = get_documents_for_facility(
                selected_company_id, selected_facility_id
            )

            # Build multiselect: show document names, track by ID
            doc_name_to_obj = {d["name"]: d for d in docs_available}
            doc_names_list  = list(doc_name_to_obj.keys())

            selected_doc_names = st.multiselect(
                "Choose one or more documents to analyze",
                options=doc_names_list,
                default=[],
                help="Hold Ctrl (or Cmd) to select multiple documents"
            )

            # Show type badges for selected documents
            if selected_doc_names:
                cols = st.columns(len(selected_doc_names))
                for i, dname in enumerate(selected_doc_names):
                    dtype = doc_name_to_obj[dname]["type"]
                    cols[i].success(f"📄 {dtype}")

            # Save selected document objects
            selected_docs = [doc_name_to_obj[n] for n in selected_doc_names]
            st.session_state.selected_doc_ids = [d["id"] for d in selected_docs]

            st.markdown('</div>', unsafe_allow_html=True)

            # ── Process Button ─────────────────────────────────
            if selected_docs:

                col_btn, _ = st.columns([1, 2])
                with col_btn:
                    process_btn = st.button(
                        "🚀  Process & Analyze Documents",
                        use_container_width=True
                    )

                if process_btn:
                    with st.spinner("Loading and indexing documents..."):
                        try:
                            # Collect the actual file paths for selected docs
                            doc_paths = [d["path"] for d in selected_docs]

                            # Call rag.py — same function, now with specific paths
                            vector_db, llm, chunk_count = process_documents_by_path(doc_paths)

                            st.session_state.vector_store = vector_db
                            st.session_state.llm          = llm
                            st.session_state.chunk_count  = chunk_count
                            st.session_state.doc_names    = [d["name"] for d in selected_docs]
                            st.session_state.document_uploaded = True

                            # Welcome message mentions company + facility
                            finfo   = get_facility_info(selected_company_id, selected_facility_id)
                            welcome = (
                                f"✅ **Ready!** Indexed **{len(selected_docs)} document(s)** "
                                f"({chunk_count} chunks) for "
                                f"**{finfo['name']}** — {finfo['location']}\n\n"
                                "**Loaded:**\n"
                                + "\n".join(f"- {d['name']}" for d in selected_docs)
                                + "\n\nAsk any question or click **Generate Report**."
                            )
                            st.session_state.messages.append(
                                {"role": "assistant", "content": welcome}
                            )
                            st.rerun()

                        except Exception as e:
                            st.error(f"❌ Processing failed: {str(e)}")
```

---

## STEP 3 — Update `rag.py` for Path-Based Loading

### 🤔 What Is This?
Your current `process_documents()` loads **all PDFs from a folder**.  
Now we need to load **specific files by path** (the ones the user picked from the dropdown).

### ✏️ Add This New Function to `rag.py`

```python
# ─────────────────────────────────────────────────────────────
# NEW FUNCTION: process_documents_by_path()
#
# WHY NEW FUNCTION (not replace old one)?
# The old process_documents(folder_path) still works for 
# manual uploads. This new function handles the enterprise
# path-based loading. Both can coexist.
#
# INPUT:  list of file paths  e.g. ["documents/aramco/dhahran/permit.pdf"]
# OUTPUT: (vector_db, llm, chunk_count) — same as before
# ─────────────────────────────────────────────────────────────
from langchain_community.document_loaders import PyPDFLoader  # ADD THIS IMPORT

def process_documents_by_path(file_paths: list):
    """
    Load specific PDF files by path (not a whole folder).
    
    Args:
        file_paths: list of PDF file path strings
        
    Returns:
        tuple: (vector_db, llm, chunk_count) — same as process_documents()
    """
    all_docs = []

    for path in file_paths:
        # PyPDFLoader loads ONE specific PDF file
        # (vs PyPDFDirectoryLoader which loads a whole folder)
        loader = PyPDFLoader(path)
        docs   = loader.load()
        all_docs.extend(docs)

    if not all_docs:
        raise ValueError("No documents could be loaded from the selected paths.")

    # Split into chunks — same as before
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(all_docs)

    # Build embeddings + vector store — same as before
    embeddings = AzureOpenAIEmbeddings(
        model="text-embedding-3-large",
        azure_deployment=AZURE_OPENAI_DEPLOYMENT,
        openai_api_version="2024-02-01",
        api_key=AZURE_OPENAI_API_KEY,
        azure_endpoint=AZURE_OPENAI_ENDPOINT
    )

    vector_db = InMemoryVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=GROQ_API_KEY
    )

    return vector_db, llm, len(chunks)
```

---

## STEP 4 — AI RAG Summary on Selected Documents

### 🤔 What Is This?
When the user clicks a **"Generate AI Summary"** button, we run a special RAG query that reads all selected documents and produces a **structured summary** — not just a Q&A answer, but a full formatted brief.

This is LangChain's power: we chain together retrieval → prompt → LLM → output.

### ✏️ Add This to `rag.py`

```python
# ─────────────────────────────────────────────────────────────
# NEW FUNCTION: generate_rag_summary()
#
# This is a CHAIN: retrieval → prompt template → LLM → output
# Using LangChain's LCEL (LangChain Expression Language)
# 
# LCEL uses the | (pipe) operator to chain steps:
#   retriever | prompt | llm | output_parser
#
# This is the "proper LangChain way" vs manually calling
# similarity_search() + llm.invoke() like the existing code.
# Both work; LCEL is more composable and readable.
# ─────────────────────────────────────────────────────────────
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

def generate_rag_summary(
    vector_db,
    llm,
    company_name: str,
    facility_name: str,
    doc_names: list
) -> str:
    """
    Generates a structured AI summary of selected documents using
    LangChain RAG chain (LCEL syntax).

    Args:
        vector_db     : InMemoryVectorStore (already built)
        llm           : ChatGroq instance
        company_name  : e.g. "Saudi Aramco"
        facility_name : e.g. "Dhahran HQ Complex"
        doc_names     : list of document names that were loaded

    Returns:
        str: structured markdown summary
    """

    if vector_db is None or llm is None:
        return "❌ Documents not loaded. Please process documents first."

    # ── Step A: Create a retriever from the vector store ─────
    # A retriever is a wrapper around similarity_search().
    # search_kwargs={"k": 12} means "retrieve top 12 chunks".
    # We use more chunks here (12 vs 5) because a summary needs
    # broader coverage than a specific Q&A question.
    retriever = vector_db.as_retriever(search_kwargs={"k": 12})

    # ── Step B: Define the prompt template ───────────────────
    # ChatPromptTemplate lets us define placeholders {context}
    # and {question} that get filled in at runtime.
    # This is cleaner than f-strings and allows reuse.
    prompt = ChatPromptTemplate.from_template("""
You are a senior environmental compliance officer with 20 years of experience.

You are reviewing documents for:
- Company: {company_name}
- Facility: {facility_name}
- Documents analyzed: {doc_names}

DOCUMENT CONTEXT (retrieved relevant sections):
{context}

Generate a structured compliance summary in EXACTLY this format:

# 📋 FACILITY COMPLIANCE SUMMARY
**Company:** {company_name} | **Facility:** {facility_name}

## 🏭 FACILITY OVERVIEW
- What type of facility this is and its main operations
- Key environmental aspects based on documents

## ✅ CURRENT COMPLIANCE STATUS
- Overall compliance rating (Compliant / Partially Compliant / Non-Compliant)
- Valid permits and their expiry dates [cite source]
- Recent inspection outcomes [cite source]

## ⚠️ KEY RISKS & VIOLATIONS
- **[CRITICAL]** Description + date + source
- **[HIGH]** Description + date + source  
- **[MEDIUM]** Description + date + source

## 📅 UPCOMING DEADLINES & ACTIONS
- Permit renewals, monitoring reports due, corrective actions [cite source]

## 💡 INSPECTOR RECOMMENDATIONS
- Top 3 things to verify during the next site visit

Use ONLY facts from the provided context. Cite [Source: filename | Page N] for every fact.
If information is missing, write *(not documented in provided records)*.
""")

    # ── Step C: Helper to format retrieved docs ───────────────
    # The retriever returns Document objects.
    # We need to convert them to a single string for the prompt.
    def format_docs(docs):
        return "\n\n".join([
            f"[Source: {doc.metadata.get('source', 'Unknown')} "
            f"| Page {doc.metadata.get('page', 0) + 1}]\n"
            f"{doc.page_content}"
            for doc in docs
        ])

    # ── Step D: Build the RAG chain using LCEL ───────────────
    # This reads as:
    # 1. "compliance summary environmental violations risks" → retriever → top 12 chunks
    # 2. format those chunks into a string
    # 3. fill the prompt template with context + metadata
    # 4. send to LLM
    # 5. parse the output as a plain string
    
    chain = (
        {
            # The retriever runs a fixed broad query to get all relevant context.
            # RunnablePassthrough() passes other values through unchanged.
            "context":       retriever | format_docs,
            "company_name":  RunnablePassthrough(),
            "facility_name": RunnablePassthrough(),
            "doc_names":     RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    # ── Step E: Run the chain ─────────────────────────────────
    # We pass a query string; the retriever uses it to find chunks.
    # The other variables (company_name etc.) are passed directly to prompt.
    result = chain.invoke({
        "context":       "compliance violations risks permits inspection enforcement",
        # ↑ This is what the retriever searches for (broad coverage query)
        "company_name":  company_name,
        "facility_name": facility_name,
        "doc_names":     ", ".join(doc_names),
    })

    return result
```

---

## STEP 5 — Connect the Summary to the UI

### ✏️ Add to `app.py` — In the Chat Screen Section

Find the action buttons section in Screen B and add a new button:

```python
# In the "action buttons row" section of SCREEN B:
col1, col2, col3, col4 = st.columns(4)  # add a 4th column
with col1:
    gen_report  = st.button("📊  Generate Inspection Report", use_container_width=True)
with col2:
    quick_risk  = st.button("⚠️  List Key Risks",            use_container_width=True)
with col3:
    ai_summary  = st.button("🤖  AI RAG Summary",            use_container_width=True)  # NEW
with col4:
    clear_btn   = st.button("🗑️  Clear Chat",                use_container_width=True)


# ── Handle: AI RAG Summary ────────────────────────────────────
# ADD THIS BLOCK after the existing button handlers
if ai_summary:
    # Get company/facility names for the summary header
    company_id   = st.session_state.get("selected_company", "")
    facility_id  = st.session_state.get("selected_facility", "")

    from company_data import get_facility_info
    finfo = get_facility_info(company_id, facility_id) if company_id and facility_id else {}

    company_name  = COMPANIES.get(company_id, {}).get("name", "Unknown Company") if company_id else "Uploaded Documents"
    facility_name = finfo.get("name", "Unknown Facility")

    with st.spinner("🤖 Running AI RAG analysis across all selected documents..."):
        try:
            from rag import generate_rag_summary
            summary = generate_rag_summary(
                vector_db     = st.session_state.vector_store,
                llm           = st.session_state.llm,
                company_name  = company_name,
                facility_name = facility_name,
                doc_names     = st.session_state.doc_names,
            )
            st.session_state.last_report = summary
            st.session_state.show_report = True
            st.session_state.messages.append({
                "role": "assistant",
                "content": "🤖 **AI RAG Summary generated** — see the briefing block below."
            })
            st.rerun()
        except Exception as e:
            st.error(f"❌ Summary failed: {str(e)}")
```

---

## STEP 6 — Update `requirements.txt`

```text
# requirements.txt — updated for enterprise features

# UI
streamlit>=1.35.0

# LangChain core
langchain>=0.2.0
langchain-core>=0.2.0
langchain-community>=0.2.0

# Azure OpenAI (embeddings)
langchain-openai>=0.1.0
openai>=1.30.0

# Groq LLM
langchain-groq>=0.1.0

# PDF loading
pypdf>=4.0.0

# Environment variables
python-dotenv>=1.0.0

# LangGraph (for future agent features)
langgraph>=0.1.0
```

---

## 📁 Final Project Structure

```
copilot_app/
├── app.py              ← modified (dropdowns + AI Summary button)
├── rag.py              ← modified (process_documents_by_path + generate_rag_summary)
├── company_data.py     ← NEW (company/facility/document registry)
├── styles.py           ← unchanged
├── ui_components.py    ← unchanged
├── requirements.txt    ← updated
├── .env                ← unchanged (Azure + Groq keys)
├── .streamlit/
│   └── config.toml     ← unchanged
└── documents/          ← NEW folder (your actual PDFs go here)
    ├── aramco/
    │   ├── dhahran/
    │   │   ├── permit_2024.pdf
    │   │   └── inspection_q1_2024.pdf
    │   └── yanbu/
    │       └── permit_2024.pdf
    └── adnoc/
        └── ruwais/
            └── permit.pdf
```

---

## 🧪 How to Test (Step by Step)

```bash
# 1. Install new requirements
pip install -r requirements.txt

# 2. Create the documents folder and add your PDFs
mkdir -p documents/aramco/dhahran
cp your_permit.pdf documents/aramco/dhahran/permit_2024.pdf

# 3. Update company_data.py paths to match your actual files

# 4. Run the app
streamlit run app.py
```

### What You Should See:
1. App opens → shows **Select Company** dropdown
2. Pick a company → **Select Facility** dropdown appears
3. Pick a facility → **Document list** appears as multi-select
4. Select 1+ documents → **Process button** appears
5. Click Process → Loading spinner → Chat screen opens
6. Click **🤖 AI RAG Summary** → LangChain chain runs → structured summary appears

---

## 🔮 Future Layers (Ready When You Need Them)

| Layer | What It Does | When to Add |
|-------|-------------|-------------|
| **Security** | Azure AD login, role-based access (which users can see which companies) | After basic flow works |
| **Persistence** | Azure Blob Storage for PDFs, Azure SQL for metadata (replace the Python dict) | When you have real production data |
| **Governance** | Audit logs (who accessed what, when), document version tracking | For compliance/regulatory requirements |
| **Operability** | Health checks, error monitoring (Azure App Insights), usage dashboards | Before going live to many users |
| **Caching** | Cache vector stores per facility so they don't rebuild every time | When processing speed becomes an issue |

Each of these is a separate, addable module — none requires rewriting what you've built here.

# Autonomous Multi-Agent Expense Report Pipeline
## End-Term Final Jury Examination Report — Group 4

**Course:** Agentic AI (AIA_7)  
**Evaluation Window:** November 23 – 26, 2026  
**Team Members:** Aryan Maradwar · Asta Joseph · **Dhiraj Sarawale (Lead)** · Ridhima Maliya  
**GitHub Repository:** [https://github.com/Dhiraj2822/expense-report-agent.git](https://github.com/Dhiraj2822/expense-report-agent.git)  

---

### Table of Contents
1. **Title & Executive Summary**
2. **Project Objectives & Problem Formulation**
3. **Enterprise Agentic Design Principles**
4. **Technical Model Details & Specifications**
5. **System Block Diagram**
6. **Agentic Workflow State Machine Flowchart**
7. **Multi-Agent Shared Blackboard Architecture & FIPA-ACL Messaging**
8. **Step-by-Step Model Execution Traces & Screenshots**
9. **Fault Tolerance, Checkpointing & Historical Archival**
10. **Individual Member Contributions, Automated Tests & Conclusion**

---

### 1. Title & Executive Summary
- **Title:** Autonomous Multi-Agent Expense Report Pipeline with Long-Term Memory, Fault-Tolerant Checkpointing, and Adjustable Autonomy.
- **Executive Summary:** This report documents the design, implementation, and empirical verification of an autonomous multi-agent pipeline designed to solve the industrial prompt: *"Generate my travel expense report for last month and email it to finance."*
- Operating entirely on offline, local open-source models, the system couples LangGraph state-machine orchestration with local vector memory (ChromaDB + `BAAI/bge-small-en-v1.5`), an adaptive missing-data feedback loop (Act-Observe-Reflect-Adjust), 5 specialized agent roles communicating via IEEE FIPA-ACL speech acts on a shared blackboard, on-disk SQLite checkpointing for crash resilience, and an explicit Human Approval Gate before financial dispatch.

---

### 2. Project Objectives & Problem Formulation
- **Scenario:** The agent ingests raw transactional CSV records, evaluates calendar dates to isolate the previous month, categorizes ambiguous merchants, computes category totals, generates a professional ReportLab PDF, and drafts an email to corporate finance.
- **Key Objectives:**
  1. *Zero-Hallucination Determinism:* Isolate all arithmetic and sums to Python; prevent LLM hallucination on financial numbers.
  2. *Continuous Semantic Learning:* Index historical classifications and user corrections in ChromaDB to bypass costly LLM inference on known merchants.
  3. *Adaptive Environment Feedback:* Build a 4-stage feedback loop (Act-Observe-Reflect-Adjust) with a 2-retry budget to handle missing values dynamically.
  4. *Distributed Agency:* Decompose tasks into 5 roles (Coordinator, Retriever, Categorizer, Auditor, Reporter) coordinated via a shared blackboard.
  5. *Durable Fault Tolerance:* Use `SqliteSaver` checkpoints to ensure server crashes at any node resume immediately from the failure point.
  6. *Human Governance:* Ensure irreversible external actions (emailing finance) require explicit operator sign-off.

---

### 3. Enterprise Agentic Design Principles
- **Separation of Concerns:** Pure Python for math and date validation; local LLM (Qwen2.5) for semantic classification, few-shot reasoning, and drafting.
- **Explicit DAG State Machine:** LangGraph Directed Acyclic Graph prevents circular, runaway autonomous loops.
- **Distributed Agent Roles:** Single responsibility per agent role; asynchronous coordination via typed blackboard state.
- **Durable Persistence:** Atomic commits to SQLite checkpoints after every node transition ensure production resilience.

---

### 4. Technical Model Details & Specifications
- **Agent Orchestrator:** LangGraph 1.2.16 (`StateGraph`, `TypedDict`)
- **State Checkpointer:** `langgraph.checkpoint.sqlite.SqliteSaver` (`data/checkpoints.db`)
- **Local LLM:** Ollama `qwen2.5:7b` via `langchain-ollama` (100% offline fallback to keyword heuristics)
- **Vector Database:** ChromaDB `PersistentClient` (`data/chroma_db`)
- **Embedding Model:** `BAAI/bge-small-en-v1.5` (384-dimensional dense vectors)
- **Document Engine:** ReportLab 4.x Platypus (`expense_report.pdf` & `reports/`)
- **Web Dashboard:** Streamlit 1.30+ (`streamlit_app.py`)
- **Quality Assurance:** Pytest 8.x (`tests/test_agent.py`)

---

### 5. System Block Diagram
*(Refer to `submision/3_Diagrams_and_Visuals/01_system_block_diagram.png`)*
The system architecture spans 4 distinct layers:
- **Layer 1: Input & Intent Parsing Layer:** Regex & prompt intent extractor parsing target recipients, date scopes, and category filters.
- **Layer 2: Multi-Agent Orchestration & Blackboard Layer:** Coordinator, Retriever, Categorizer, Auditor, and Reporter communicating over `AgentBlackboardState`.
- **Layer 3: Memory & Fault-Tolerance Infrastructure:** ChromaDB vector store, 4-stage feedback loop, and SQLite checkpoint database.
- **Layer 4: Gate, Delivery & Artifact Archive Layer:** Human Approval Gate, ReportLab PDF publisher, and RFC 822 EML outbox.

---

### 6. Agentic Workflow State Machine Flowchart
*(Refer to `submision/3_Diagrams_and_Visuals/02_agentic_workflow_flowchart.png`)*
The discrete state transitions proceed as follows:
`START` -> `COORDINATOR (Intent Parsing)` -> `RETRIEVER (Date Boundary Filtering)` -> `CATEGORIZER (ChromaDB Memory Sim >= 0.85 vs LLM Few-Shot)` -> `AUDITOR (Feedback Loop: Act-Observe-Reflect-Adjust; Retry <= 2)` -> `REPORTER (Deterministic Math & PDF Generation)` -> `HUMAN APPROVAL GATE (Approve -> Dispatch & Archive | Reject -> Abort)` -> `CONFIRM & END`.

---

### 7. Multi-Agent Shared Blackboard Architecture & FIPA-ACL
*(Refer to `submision/3_Diagrams_and_Visuals/03_multi_agent_blackboard_diagram.png`)*
The typed blackboard state (`AgentBlackboardState`) stores all operational artifacts:
- `raw_expenses`, `filtered_expenses`, `categorized_expenses`, `exceptions`
- `totals` (`category_totals`, `grand_total`)
- `date_range` (`first_day`, `last_day`)
- `message_log` (FIPA-ACL communication transcript)
- `step_log` (Sliding-window short-term context)
Communication uses IEEE FIPA-ACL performatives: `REQUEST`, `INFORM`, `ACCEPT-PROPOSAL`, and `REFUSE`.

---

### 8. Step-by-Step Model Execution Traces & Screenshots
*(Refer to `submision/4_Screenshots_and_Execution_Traces/`)*
- **Step 1: Coordinator Initialization:** Decomposes user instruction and initializes FIPA-ACL message transcript.
- **Step 2: Retriever Calendar Filtering:** Loads 20 rows from CSV; filters for last calendar month (2026-09-01 to 2026-09-30).
- **Step 3: Categorizer Memory Lookup:** Resolves 12/20 rows directly from ChromaDB (similarity >= 0.85), applying user-correction priorities.
- **Step 4: Auditor Feedback Loop:** Identifies 3 missing amounts, resolves Lyft (₹38.25) and Parking Authority (₹85.00) via scripted answers, escalates Southwest Airlines to PDF appendix.
- **Step 5: Reporter & Human Approval Gate:** Recalculates grand total (₹3,653.25), generates PDF report, presents Human Gate, and dispatches email upon approval.

---

### 9. Fault Tolerance, Checkpoint Recovery & Historical Archival
- **Crash Recovery Demonstration:**
  When a simulated crash is triggered at Node 3 (`categorizer`), all prior steps remain committed to `data/checkpoints.db`. Resuming execution with thread ID `session_demo_1` immediately executes `categorizer` without repeating `coordinator` or `retriever`.
- **Historical Report Archival:**
  Every run automatically archives timestamped PDFs to `reports/expense_report_YYYYMMDD_HHMMSS.pdf` with companion `.json` metadata. In Streamlit, users can view and download previous reports without re-running the agent.
- **Dynamic Prompts:**
  Custom emails (e.g. `audit@firm.com`) and date scopes (*all expenses*) are dynamically parsed and executed.

---

### 10. Individual Member Contributions & Conclusion
| Member Name | Core Ownership | Specific Deliverables |
|---|---|---|
| **Dhiraj Sarawale (Lead)** | System Architecture, LangGraph DAG & Fault Tolerance | Built StateGraph engine, SQLite checkpoint recovery, dynamic intent parser & Streamlit crash demo. |
| **Aryan Maradwar** | Unit 3 Long-Term Vector Memory & Ingestion | Integrated ChromaDB vector store with BGE embeddings, similarity thresholding & user correction memory. |
| **Asta Joseph** | Unit 4 Role-Based Multi-Agent Architecture | Engineered 5 role agents, IEEE FIPA-ACL structured messaging protocol & execution trace verification. |
| **Ridhima Maliya** | Unit 3 Feedback Loops & Unit 4 Governance | Built Act-Observe-Reflect-Adjust feedback loop, Human Approval Gate & ReportLab PDF publishing engine. |

- **Automated Test Results:** All 4 tests in `tests/test_agent.py` pass with **100% success rate**.
- **Final Conclusion:** Group 4 has successfully developed a robust, production-aligned multi-agent system combining local LLM reasoning, deterministic math, vector memory, fault tolerance, and human governance.

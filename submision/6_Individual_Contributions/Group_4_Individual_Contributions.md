# Group 4 Individual Contributions & Technical Deliverables
## Course: Agentic AI (AIA_7) — End-Term Final Jury Examination (Nov 2026)

### Project Title:
**Autonomous Multi-Agent Expense Report Pipeline with Long-Term Memory, Fault-Tolerant Checkpointing, and Adjustable Autonomy**

---

### Team Roster & Role Summary

| Member Name | Student Role | Primary Subsystem Ownership | Core Technology Stack |
|---|---|---|---|
| **Dhiraj Sarawale** | Project Lead & Core Architect | LangGraph DAG Engine, SQLite Checkpointing, Dynamic Intent Parser, Streamlit UI | LangGraph, SqliteSaver, Streamlit, Python |
| **Aryan Maradwar** | AI & Vector Memory Lead | Long-Term Semantic Vector Memory, Ingestion & Seed Automation | ChromaDB, Sentence-Transformers (BGE-small), Pandas |
| **Asta Joseph** | Multi-Agent Systems Lead | Role-Based Agents, FIPA-ACL Protocol, Observability Traces | Python, IEEE FIPA-ACL, TypedDict Blackboard |
| **Ridhima Maliya** | Auditing & Governance Lead | Missing-Data Feedback Loop, Human Approval Gate, ReportLab Publishing | ReportLab, RFC 822 EML, Anomaly Heuristics |

---

### Detailed Technical Contributions

#### 1. Dhiraj Sarawale (Project Lead & Core Architect)
- **LangGraph StateGraph Architecture:** Engineered the underlying Directed Acyclic Graph (DAG) using `langgraph.graph.StateGraph` and designed the unified `AgentBlackboardState` TypedDict to eliminate state-overwrite bugs during agent transitions.
- **Durable Fault Tolerance & Crash Recovery:** Designed and integrated `SqliteSaver` (`data/checkpoints.db`) to enable atomic commits after every node transition. Engineered the crash simulation and resume engine (`--simulate-crash-at <node>` and `thread_id` resumption) ensuring zero compute loss if server crashes occur.
- **Dynamic Prompt & Intent Extraction:** Built the natural language intent parser (`parse_prompt_instruction`) to dynamically extract target recipients, date scopes (*all expenses* vs *last month*), and specific category filters (*only Meals*).
- **Interactive Observability Dashboard:** Built `streamlit_app.py`, featuring real-time blackboard state snapshots, FIPA-ACL communication transcripts, crash simulation controls, and past reports archive viewers.
- **Integration & Testing:** Led end-to-end integration and authored core test modules in `tests/test_agent.py`.

#### 2. Aryan Maradwar (AI & Vector Memory Lead)
- **ChromaDB Vector Store Integration:** Implemented the persistent vector database (`ExpenseMemoryStore` in `unit3_memory/memory_store.py`) powered by `BAAI/bge-small-en-v1.5` dense embeddings.
- **Cosine Similarity Thresholding:** Implemented the mathematical similarity engine (`similarity >= 0.85`), allowing the agent to resolve 60%+ of ambiguous merchant transactions directly from memory, eliminating LLM latency and hallucination risk.
- **Continuous Learning & User Correction Memory:** Designed the persistent user-correction priority rule (`--correct "Olive Garden=Meals"`), ensuring human overrides are stored with `source='user_correction'` and strictly take precedence over model inferences.
- **Dataset Seed Generation:** Developed `data/seed.py` to deterministically regenerate mock expense datasets across arbitrary reference dates with realistic corporate noise.

#### 3. Asta Joseph (Multi-Agent Systems Lead)
- **Role-Based Agent Decomposition:** Decomposed the monolithic system into 5 specialized cooperative agents:
  - `agent_coordinator_init`: Goal decomposition and workflow scheduling.
  - `agent_retriever`: Strict temporal boundary filtering and tabular ingestion.
  - `agent_categorizer`: Semantic vector memory lookups and few-shot LLM guidance.
  - `agent_auditor`: Anomaly detection, duplicate detection, and feedback loop management.
  - `agent_reporter`: Deterministic calculation, PDF rendering, and approval handling.
- **IEEE FIPA-ACL Messaging Standard:** Implemented `unit4_agents/acl_message.py` supporting standard performatives (`REQUEST`, `INFORM`, `ACCEPT-PROPOSAL`, `REFUSE`).
- **Observability Traces:** Built structured execution trace loggers (`print_trace`) outputting inputs, outputs, and intermediate states for live viva auditability.
- **Multi-Agent Test Suite:** Co-authored multi-agent interaction tests in `tests/test_agent.py`.

#### 4. Ridhima Maliya (Auditing & Governance Lead)
- **Adaptive Missing-Data Feedback Loop:** Designed and implemented `FeedbackLoopManager` (`unit3_memory/feedback_loop.py`) operating on the 4-stage *Act -> Observe -> Reflect -> Adjust* cycle with a strict 2-retry budget.
- **Adjustable Autonomy Human Approval Gate:** Engineered the Human Approval Gate before external communication is triggered, presenting the human operator with grand totals, period boundaries, and Auditor anomaly warnings with branching logic (`approve` vs `reject`).
- **Deterministic ReportLab PDF Publishing:** Built the publication-grade PDF generator (`tools.py:generate_pdf_report`) creating structured category tables, itemized transactions, and audit appendixes for unresolved items.
- **RFC 822 Email Archiving:** Implemented MIME and RFC 822 `.eml` packaging (`tools.py:send_email_with_pdf`), archiving complete email records with embedded PDF attachments into `./outbox`.

---

### Team Self-Assessment & Sign-Off

All four members have actively participated in the design, implementation, debugging, documentation, and live testing of the Autonomous Multi-Agent Expense Report Pipeline. All code has been pushed and verified on the official GitHub repository.

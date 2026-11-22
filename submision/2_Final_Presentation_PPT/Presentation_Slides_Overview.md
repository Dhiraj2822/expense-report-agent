# Agentic AI Final Jury Presentation — Slide Deck Overview
## Presentation Title: Autonomous Multi-Agent Expense Report Pipeline
**Team:** AIA_7 Group 4 (Aryan Maradwar · Asta Joseph · Dhiraj Sarawale · Ridhima Maliya)  
**File:** `Agentic_AI_Final_Jury_Group_4.pptx` (16:9 Widescreen, 16 Slides)

---

### Slide 1: Title Slide (Dark Navy)
- **Title:** Autonomous Multi-Agent Expense Report Pipeline
- **Subtitle:** A Fault-Tolerant, Distributed Multi-Agent DAG with Long-Term Memory, Feedback Loops & Human Governance
- **Presenter Notes:** Introduce Group 4 and state that our goal was to build a production-aligned, offline-capable multi-agent system answering the college scenario with enterprise robustness.

### Slide 2: Problem Statement & Industrial Scenario
- **Scenario:** “Generate my travel expense report for last month and email it to finance.”
- **Core Challenges:** Ambiguous merchant names, calendar boundary enforcement, zero-hallucination math, and irreversible email dispatch.
- **Presenter Notes:** Emphasize that single-prompt scripts fail because LLMs hallucinate sums, forget corrections, crash without recovery, and dispatch emails blindly.

### Slide 3: Project Objectives & Core Deliverables
- **Core Deliverables:** Zero-hallucination determinism, ChromaDB vector memory, 4-stage feedback loop, 5 role-based agents, SQLite checkpoint recovery, and adjustable autonomy gate.
- **Presenter Notes:** Highlight our progression from base monolithic pipeline to extended multi-agent system with fault tolerance.

### Slide 4: Enterprise Design Philosophy
- **Principles:** Determinism over generative hallucination, structured DAG state machine, distributed agency with single responsibility, and durable resilience.
- **Presenter Notes:** Explain that real corporate platforms like Ramp, Brex, and SAP Concur use these exact patterns: deterministic math + LLM reasoning.

### Slide 5: Technical Model & Technology Stack
- **Table:** LangGraph, SqliteSaver, Local Ollama (Qwen2.5), ChromaDB (BGE-small), ReportLab, Streamlit, and Pytest.
- **Presenter Notes:** Note that the entire solution runs 100% locally with zero external API fees or internet reliance.

### Slide 6: System Block Diagram
- **Visual:** High-resolution diagram showing the 4 architectural layers.
- **Presenter Notes:** Walk the jury through the Ingestion Layer, Multi-Agent Blackboard Layer, Memory/Fault-Tolerance Layer, and Delivery Artifact Layer.

### Slide 7: Multi-Agent Roles & Shared Blackboard
- **Visual:** Central blackboard orbited by Coordinator, Retriever, Categorizer, Auditor, and Reporter.
- **Presenter Notes:** Explain how agents communicate via IEEE FIPA-ACL speech acts (REQUEST, INFORM, ACCEPT-PROPOSAL, REFUSE) over `AgentBlackboardState`.

### Slide 8: Workflow Flowchart & State Machine
- **Visual:** Step-by-step state machine flowchart with memory thresholding and feedback retries.
- **Presenter Notes:** Point out the memory branch (cosine similarity >= 0.85 skips LLM) and the feedback loop retry budget (max 2 retries).

### Slide 9: Unit 3 Long-Term Semantic Vector Memory
- **Details:** ChromaDB vector database using `BAAI/bge-small-en-v1.5` embeddings.
- **Key Feature:** User Correction Priority Rule (`--correct 'Olive Garden=Meals'`).
- **Presenter Notes:** Explain how vector memory eliminates 60%+ of LLM calls on known vendors while learning continuously from user corrections.

### Slide 10: Unit 3 Adaptive Missing-Data Feedback Loop
- **Details:** 4 stages: Act (scan data), Observe (quantify missing), Reflect (check retry budget <= 2), Adjust (resolve via answers/human).
- **Presenter Notes:** Show that incomplete data triggers automated inquiry rather than crashing or inventing numbers.

### Slide 11: Unit 4 Human Approval Gate & Governance
- **Details:** Synchronous pause before SMTP dispatch. Displays total, period, and Auditor warnings.
- **Presenter Notes:** Explain Adjustable Autonomy: approved submissions trigger email and EML archival; rejected submissions return control to Coordinator safely.

### Slide 12: Phase 4 Fault Tolerance & Crash Recovery (SqliteSaver)
- **Details:** The professor's question answered: "What happens if server crashes at Step 3?"
- **Solution:** Atomic SQLite checkpoints in `data/checkpoints.db`. Re-running with the same thread ID resumes from Step 3 without repeating prior steps.
- **Presenter Notes:** This is our killer feature for the jury demonstration.

### Slide 13: Phase 4 Dynamic Prompts & Historical Report Archival
- **Details:** Dynamic Intent Parser extracts custom recipients (e.g. `audit@firm.com`), date scopes (*all expenses*), and categories (*only meals*). Historical reports are permanently archived in `reports/` with JSON metadata.
- **Presenter Notes:** Answers the professor's question: "Why must users recreate reports every time?"

### Slide 14: Step-by-Step Execution Screenshots
- **Visual:** 4 terminal trace cards (Step 1 Coordinator, Step 2 Retriever, Step 3 Categorizer, Step 4 Auditor).
- **Presenter Notes:** Walk the jury through the real execution trace logs demonstrating that every agent performs its verified role.

### Slide 15: Automated Pytest Verification & Quality Metrics
- **Details:** 4 automated test modules in `tests/test_agent.py` passing with 100% success rate.
- **Presenter Notes:** Emphasize that our code is verified by unit tests covering math, memory, feedback loops, and checkpoint resume.

### Slide 16: Individual Member Contributions & Conclusion
- **Details:** Clear table of responsibilities for Aryan Maradwar, Asta Joseph, Dhiraj Sarawale (Lead), and Ridhima Maliya.
- **Conclusion:** Summary of how Group 4 delivered an enterprise-grade agentic solution.

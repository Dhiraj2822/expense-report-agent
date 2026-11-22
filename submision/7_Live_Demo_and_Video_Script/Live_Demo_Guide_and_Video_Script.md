# Live Demo Guide & Video Presentation Script (5-Minute Walkthrough)
## Autonomous Multi-Agent Expense Report Agent — Group 4

**Final Jury Exam:** Agentic AI (Nov 2026)  
**Team Members:** Aryan Maradwar · Asta Joseph · Dhiraj Sarawale · Ridhima Maliya  

---

### Part 1: Quick-Start Demo Execution

To launch the interactive dashboard live for the jury:
```powershell
# Open terminal in project root
streamlit run streamlit_app.py
```
Or double-click:
`submision/7_Live_Demo_and_Video_Script/Quick_Demo_Runner.bat`

---

### Part 2: Step-by-Step 5-Minute Jury Demo Script

#### Minute 0:00 – 1:00: Introduction & Problem Framing
- **Speaker:** "Good morning, respected Jury Members. We are Group 4. Today we present our Autonomous Multi-Agent Expense Reporting Pipeline."
- **Action:** Open the Streamlit dashboard on screen.
- **Talking Points:**
  - "Our target prompt is: *'Generate my travel expense report for last month and email it to finance.'*"
  - "Traditional single-prompt agents fail in corporate environments because LLMs hallucinate financial sums, crash without recovery, forget user corrections, and send emails without human governance."
  - "We solved this with an enterprise-grade LangGraph state machine, local ChromaDB vector memory, an adaptive feedback loop, and fault-tolerant SQLite checkpoints."

#### Minute 1:00 – 2:00: Demo 1 — Normal Multi-Agent Execution & Determinism
- **Action:**
  1. Click the preset button: **"📌 Default Prompt"**.
  2. Ensure *"Auto-Approve Human Gate"* is checked (or uncheck to demonstrate manual prompt).
  3. Click **"🚀 Execute Agent Pipeline"**.
- **Talking Points:**
  - "Notice our 5 agents coordinating live: Coordinator decomposes the goal, Retriever filters the September calendar window, Categorizer queries vector memory, Auditor detects anomalies, and Reporter builds the report."
  - "Look at the **Financial Breakdown** tab: The grand total is exactly ₹3,653.25. This was computed deterministically in Python—zero LLM math hallucination."
  - "In the **Multi-Agent ACL Log** tab, you can see real-time IEEE FIPA-ACL messages exchanged across the shared blackboard."

#### Minute 2:00 – 3:00: Demo 2 — The Killer Feature: Fault Tolerance & Crash Recovery
- **Speaker:** "Now we answer the key question: *What happens if the server crashes at Step 3?*"
- **Action:**
  1. Go to the sidebar section: **"💥 Server Crash & Recovery Demo"**.
  2. Select **"Simulate Server Crash At:"** -> `categorizer (Step 3)`.
  3. Click **"🚀 Execute Agent Pipeline"**.
  4. Point out the red alert: `💥 SERVER CRASH TRIGGERED! Node: categorizer`.
  5. Explain: "The server crashed at Step 3. But all previous steps—Node 1 Coordinator and Node 2 Retriever—are safely preserved in SQLite (`data/checkpoints.db`)."
  6. Now click **"🔄 Resume Interrupted Checkpoint"**.
  7. Show the result: The pipeline immediately picks up at `Categorizer` -> `Auditor` -> `Reporter` and completes **without re-running earlier steps!**
  8. Click the **"💾 Checkpoint State"** tab to show the saved SQLite thread snapshot.

#### Minute 3:00 – 4:00: Demo 3 — Long-Term Memory & Historical Archival
- **Speaker:** "Next, why must users recreate reports every time? And how does the agent learn?"
- **Action:**
  1. Show the sidebar: **"📂 Past Generated Reports"**.
  2. Select any archived report and click **"📥 Download"**.
  3. Explain: "Every run is permanently archived with timestamp and JSON metadata. Users can retrieve past reports instantly without calling the LLM."
  4. Now show **"🧠 Long-Term Memory Correction"** in the sidebar:
     - Vendor: `Olive Garden` -> Category: `Meals`.
     - Click **"Save Correction to ChromaDB"**.
     - "ChromaDB stores this user correction. In all future runs, Olive Garden and similar restaurants will always be classified as Meals with 100% priority over model guesses."

#### Minute 4:00 – 5:00: Demo 4 — Dynamic Prompt Flexibility & Conclusion
- **Action:**
  1. Click the preset button: **"✉️ Custom Recipient"**:
     `"Generate travel expense report for last month and email to internal-audit@enterprise.org"`
  2. Click **"🚀 Execute Agent Pipeline"**.
  3. Show the **"✉️ Drafted Email"** tab: The agent dynamically extracted the recipient `internal-audit@enterprise.org` instead of defaulting to finance!
- **Concluding Statement:**
  - "In conclusion, our project demonstrates that enterprise-ready AI requires structured agentic workflows rather than simple prompt chaining. We have verified 100% test pass rate with Pytest, zero-hallucination math, and full fault tolerance. Thank you, and we welcome your questions!"

---

### Part 3: Anticipated Technical Q&A for Jury

1. **Q: Why use LangGraph instead of simple sequential functions?**
   - *A:* LangGraph provides an explicit Directed Acyclic Graph (DAG) state machine with a shared blackboard (`AgentBlackboardState`). It enables atomic state checkpointing via `SqliteSaver`, non-linear branching (e.g. feedback loops and human gates), and full auditability of agent transitions.

2. **Q: How do you prevent the LLM from making arithmetic mistakes?**
   - *A:* The LLM is strictly isolated from calculations. Category totals and grand totals are calculated by pure deterministic Python functions (`calculate_totals`) in `tools.py`. The LLM only receives calculated numbers to draft the textual email body.

3. **Q: How does crash recovery work under the hood?**
   - *A:* We use LangGraph's `SqliteSaver` checkpointer. After each node returns, its output dictionary is merged into the typed blackboard state and written to `data/checkpoints.db` under a session `thread_id`. Upon resumption, LangGraph queries the last completed checkpoint and executes only the pending node.

4. **Q: What embedding model do you use for ChromaDB?**
   - *A:* We use HuggingFace's `BAAI/bge-small-en-v1.5`, a 384-dimensional dense semantic embedding model that runs completely locally without external API dependencies.

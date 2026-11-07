# Expense Report Agent
**AIA_7 · Group 4** — Aryan Maradwar · Asta Joseph · **Dhiraj Sarawale** · Ridhima Maliya

> _"Generate my travel expense report for last month and email it to finance."_

A fully offline, open-source AI agent built with **LangGraph + local Ollama** that
retrieves expenses, categorises them using an LLM, generates a PDF report, and emails
it — all without any paid API keys.

---

## Quick Start

### Prerequisites
```bash
# 1. Install Ollama (https://ollama.com)
ollama pull qwen2.5:7b        # ~4 GB download

# 2. Clone and setup
git clone <repo>
cd "Agentic AI Mini Project"

pip install -r requirements.txt

# 3. Copy and configure environment
copy .env.example .env        # Windows
# Leave SMTP_USER/PASS empty for demo mode (simulated send)
```

### Run Base Pipeline
```bash
$env:PYTHONIOENCODING="utf-8"   # PowerShell — supports emoji in output
python main.py                  # or: python main.py --mode base
```

### Run Extended Pipeline (Phase 1 — long-term memory + feedback loop)
```bash
python main.py --mode extended
```

### Save a User Category Correction
```bash
python main.py --correct "Olive Garden=Meals"
# Next run will use this from long-term memory, skipping the LLM
```

### Regenerate CSV for any date
```bash
python data/seed.py --date 2026-10-01   # regenerates Sept 2026 data
```

---

## Project Structure

```
.
├── main.py                  # LangGraph 9-node pipeline (base + extended entry)
├── llm_config.py            # Local Ollama config (open-source only, no API keys)
├── tools.py                 # All tool functions (retrieve, filter, categorize, …)
├── requirements.txt
├── .env.example
├── data/
│   ├── mock_expenses.csv    # 20-row demo expense data (September 2026)
│   └── seed.py              # Regenerate CSV with any reference date
├── unit3_memory/            # Phase 1: Long-term memory + feedback loop
│   ├── memory_store.py      # ChromaDB + sentence-transformers embeddings
│   └── extended_main.py     # Extended LangGraph pipeline
├── unit4_agents/            # Phase 2: Role-based agents + blackboard
├── tests/                   # Phase 3: pytest tests
├── run_demo.py              # Phase 3: 3 scripted demo scenarios
└── ARCHITECTURE.md          # Mermaid diagram + design rationale
```

---

## Modes

| Command | What it does |
|---|---|
| `python main.py` | Base pipeline (Ollama LLM for categorise + email) |
| `python main.py --mode base` | Same as above |
| `python main.py --mode extended` | Phase 1: memory + feedback loop |
| `python main.py --correct "Vendor=Cat"` | Save user correction to long-term memory |
| `python main.py --answers answers.json` | Scripted missing-data answers (Phase 1) |
| `python main.py --mode extended --auto-approve` | Skip human approval gate (Phase 2) |

---

## Fallback Mode (Offline Safety)

If Ollama is not running, the agent automatically falls back to:
- **Categorisation**: keyword rules (no LLM needed)
- **Email**: professional template (no LLM needed)
- A clear `⚠ FALLBACK MODE` message is printed

The pipeline **never crashes** due to a missing LLM.

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `OLLAMA_MODEL` | `qwen2.5:7b` | Local Ollama model |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `REPORT_TODAY` | (real date) | Override "today" for reproducible demos |
| `FINANCE_EMAIL` | `finance@yourcompany.com` | Email recipient |
| `SMTP_HOST/PORT/USER/PASS` | Mailtrap sandbox | SMTP credentials |
| `CHROMA_PERSIST_DIR` | `chroma_db` | ChromaDB storage folder |
| `MEMORY_TOP_K` | `3` | How many memory matches to retrieve |
| `MEMORY_SIMILARITY_THRESHOLD` | `0.85` | Above this score → skip LLM |
| `SHORT_TERM_WINDOW` | `5` | Steps to keep in sliding window |

---

## Course Concepts Demonstrated

| Phase | Concept | Where |
|---|---|---|
| Base | **Tool use** (ReAct pattern) | `tools.py` |
| Base | **Agentic pipeline** (LangGraph DAG) | `main.py` |
| Base | **Local/open-source LLM** with fallback | `llm_config.py` |
| Phase 1 | **Long-term memory** (ChromaDB + embeddings) | `unit3_memory/memory_store.py` |
| Phase 1 | **Feedback loop** (LangGraph conditional edges) | `unit3_memory/extended_main.py` |
| Phase 2 | **Role-based agents** (Coordinator, Retriever, Auditor, Reporter) | `unit4_agents/` |
| Phase 2 | **Blackboard architecture** (shared LangGraph state) | `unit4_agents/` |
| Phase 2 | **FIPA-ACL messaging** between agents | `unit4_agents/` |
| Phase 2 | **Human approval gate** (adjustable autonomy) | `unit4_agents/` |

---

## Expected Output (Base Run)

```
============================================================
   EXPENSE REPORT AGENT — Starting Up
   Mode: BASE
============================================================

 Instruction: "Generate my travel expense report for last month..."

  Initialising LLM …
   Provider resolved: Local Ollama (qwen2.5:7b)

============================================================
 NODE 1 | RETRIEVE — Loading expenses from CSV
   => 20 expense rows loaded from data/mock_expenses.csv

 NODE 2 | FILTER — Keeping only last calendar month
   => Date range: 2026-09-01 to 2026-09-30

 NODE 3 | CATEGORIZE — Inferring missing categories
   => LLM provider: Local Ollama (qwen2.5:7b)

 NODE 5 | CALCULATE — Computing totals
   => Grand total: $3,530.00
      Flights: $2,075.00
      Hotels:  $1,051.60
      Meals:   $138.25
      Transport: $265.15

 NODE 6 | GENERATE PDF
   => PDF saved: expense_report.pdf

 NODE 8 | SEND EMAIL
   => Send status: simulated (demo mode)

  +-----------------------------------------------+
  |         EXPENSE REPORT AGENT -- DONE          |
  +-----------------------------------------------+
  | Grand Total : $3,530.00
  | Flagged     : 2 items (missing amount)
  +-----------------------------------------------+
```

---

## Fault Tolerance, Crash Recovery & Intent Features (Phase 4)

### 1. Crash Recovery at Any Step (`SqliteSaver`)
Every node transition in the LangGraph multi-agent pipeline is saved to an on-disk SQLite checkpoint (`data/checkpoints.db`).
- **Simulate a crash at any step (CLI):**
  ```bash
  python main.py --mode extended --auto-approve --answers data/answers.json --thread-id session_viva --simulate-crash-at categorizer
  ```
- **Resume from the checkpoint without repeating earlier nodes:**
  ```bash
  python main.py --mode extended --auto-approve --answers data/answers.json --thread-id session_viva
  ```

### 2. Historical Reports Archive
Every report generated is automatically archived in `reports/` (`expense_report_YYYYMMDD_HHMMSS.pdf` + `.json` metadata). Users can view and download past reports from the Streamlit UI without running the pipeline again.

### 3. Dynamic Prompt & Intent Extraction
The Coordinator agent dynamically parses user prompts to extract:
- **Custom Recipient:** e.g., `"Generate report and email to external-audit@firm.com"`
- **Date Scope:** e.g., `"Generate report for all expenses in the file"` (bypasses default last-calendar-month filter)
- **Category Filter:** e.g., `"Generate report for only Meals expenses"`

---

## Streamlit Observability Dashboard (Phase 3 & 4)

Launch the interactive web interface:
```bash
streamlit run streamlit_app.py
```
Provides:
- **Crash Simulation & Live Resume:** Simulate server failures at Step 1, 2, 3, 4, or 5 and click *'Resume Interrupted Checkpoint'* to demonstrate fault tolerance.
- **Past Reports Viewer:** Browse, preview, and download previously generated PDF reports instantly.
- **Dynamic Prompt Presets:** One-click preset prompt buttons (Custom Recipient, Meals Only, All Expenses).
- **LangGraph Checkpoint Inspector:** Real-time visibility into pending nodes and thread checkpoint records.
- **Live Blackboard State & FIPA-ACL Logs:** Full transcript of agent-to-agent communication.
- **Interactive Human Approval Gate & Long-Term Memory Correction:** User-in-the-loop controls.

---

## Automated Test Suite (Pytest)

Run the automated test suite covering Units 3 & 4:
```bash
python -m pytest -p no:asyncio -v tests/test_agent.py
```

---

## License
MIT — open-source, educational use.

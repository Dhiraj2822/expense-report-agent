# Final Jury Submission Package — Agentic AI (Group 4)
## Autonomous Multi-Agent Expense Report Pipeline

**Course:** Agentic AI (AIA_7) — End-Term Final ESE Jury Examination  
**Jury Dates:** November 23 – 26, 2026  
**Team Group 4:**
- **Aryan Maradwar**
- **Asta Joseph**
- **Dhiraj Sarawale (Lead)**
- **Ridhima Maliya**

**Official Repository:** [https://github.com/Dhiraj2822/expense-report-agent.git](https://github.com/Dhiraj2822/expense-report-agent.git)

---

### Submission Package Directory Structure

This folder (`submision/`) contains all materials required for the Final Jury Examination:

```
submision/
│
├── 1_Project_Report_10_Pages/
│   ├── Final_Jury_Report_Group_4.pdf     # << OFFICIAL 10-PAGE JURY REPORT (Formatted PDF)
│   ├── Final_Jury_Report_Group_4.md      # Full Markdown transcript of the 10-page report
│   └── generate_report.py                # Python ReportLab compilation script
│
├── 2_Final_Presentation_PPT/
│   ├── Agentic_AI_Final_Jury_Group_4.pptx # << OFFICIAL 16-SLIDE JURY PRESENTATION (.pptx)
│   ├── Presentation_Slides_Overview.md   # Slide-by-slide presenter notes & transcript
│   └── generate_pptx.py                  # Python-pptx generation script
│
├── 3_Diagrams_and_Visuals/
│   ├── 01_system_block_diagram.png       # Layered 4-tier System Block Diagram (High-Res)
│   ├── 02_agentic_workflow_flowchart.png # State Machine Workflow Flowchart (High-Res)
│   ├── 03_multi_agent_blackboard_diagram.png # Multi-Agent Blackboard Architecture Diagram
│   ├── 04_feedback_loop_diagram.png      # Act-Observe-Reflect-Adjust Loop Diagram
│   └── generate_diagrams.py              # Visual generator script
│
├── 4_Screenshots_and_Execution_Traces/
│   ├── step1_coordinator_init.png        # Step 1: Goal decomposition & intent parsing
│   ├── step2_retriever_filtering.png     # Step 2: Calendar window CSV filtering
│   ├── step3_categorizer_memory_llm.png  # Step 3: ChromaDB vector memory resolution
│   ├── step4_auditor_feedback_loop.png   # Step 4: Missing data feedback recovery
│   ├── step5_reporter_approval_gate.png  # Step 5: Deterministic math & human approval
│   ├── step6_crash_simulation_recovery.png # Step 6: SQLite checkpoint crash resumption
│   ├── step7_past_reports_archive.png    # Step 7: Timestamped reports archive & viewer
│   └── step8_pytest_test_results.png     # Step 8: Pytest 100% pass verification
│
├── 5_Dataset_and_Model_Files/
│   ├── mock_expenses.csv                 # 20-row test dataset (September 2026 expenses)
│   ├── seed.py                           # Dataset generation utility
│   ├── answers.json                      # Scripted answers for feedback loop
│   ├── check_totals.py                   # Deterministic verification script
│   ├── vector_store_metadata.json        # ChromaDB & BGE embedding configuration
│   └── checkpoints_schema.sql            # SQLite checkpointer database schema
│
├── 6_Individual_Contributions/
│   └── Group_4_Individual_Contributions.md # Detailed breakdown of all 4 members
│
├── 7_Live_Demo_and_Video_Script/
│   ├── Live_Demo_Guide_and_Video_Script.md # 5-minute step-by-step viva presentation guide
│   └── Quick_Demo_Runner.bat             # 1-click launcher for the live Streamlit dashboard
│
└── README.md                             # This index file
```

---

### Core Deliverables Checklist (Jury Requirements Verification)

- [x] **1. Fully working project + source code:** Complete repository with LangGraph DAG, ChromaDB, and local Ollama fallback.
- [x] **2. Dataset, model files & report:** Mock expense dataset, seed generators, vector store config, and checkpoints schema in `5_Dataset_and_Model_Files/`.
- [x] **3. Final PPT + README:** 16-slide PowerPoint (`Agentic_AI_Final_Jury_Group_4.pptx`) in `2_Final_Presentation_PPT/` + root and subfolder READMEs.
- [x] **4. Screenshots, test results & demo video guide:** 8 step-by-step execution screenshot cards in `4_Screenshots_and_Execution_Traces/` and 5-minute video presentation script in `7_Live_Demo_and_Video_Script/`.
- [x] **5. Formal 10-Page Project Report:** `Final_Jury_Report_Group_4.pdf` in `1_Project_Report_10_Pages/` (precisely 10 pages, includes Title, Objectives, Design Principles, Technical Model, Block Diagram, Flowchart, Screenshots, Crash Recovery, and Individual Contributions).
- [x] **6. Individual contribution of all 4 members:** Dedicated matrix and detailed technical breakdown for Aryan Maradwar, Asta Joseph, Dhiraj Sarawale (Lead), and Ridhima Maliya in `6_Individual_Contributions/`.
- [x] **7. Answers to Critical Jury Questions:**
  - *Server Crash at Step 3:* Solved via LangGraph `SqliteSaver` checkpoints in `data/checkpoints.db` (instant resumption).
  - *Viewing Past Reports:* Solved via timestamped PDF & JSON archival in `reports/` with Streamlit viewer.
  - *Dynamic Prompts:* Solved via dynamic intent parser handling custom recipients, date scopes, and category filters.

---

### How to Run the Live Project

```powershell
# 1. Run the interactive Streamlit Web UI:
streamlit run streamlit_app.py

# 2. Run automated tests (100% pass):
pytest -p no:asyncio -v tests/test_agent.py

# 3. Run full multi-agent pipeline via CLI:
python main.py --mode extended --auto-approve --answers data/answers.json

# 4. Demonstrate crash recovery at Step 3:
python main.py --mode extended --auto-approve --answers data/answers.json --thread-id demo_session --simulate-crash-at categorizer
python main.py --mode extended --auto-approve --answers data/answers.json --thread-id demo_session
```

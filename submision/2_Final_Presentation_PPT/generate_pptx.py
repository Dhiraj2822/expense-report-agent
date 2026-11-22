"""
submision/2_Final_Presentation_PPT/generate_pptx.py
───────────────────────────────────────────────────
Generates a comprehensive 16-slide PowerPoint presentation (.pptx)
for the Agentic AI Final Jury Examination (Group 4).
Includes:
  - Title & Team Metadata
  - College Problem Statement & Scenario
  - Objectives & Core Deliverables
  - Enterprise Design Philosophy & Determinism
  - Technical Stack & Component Model
  - System Block Diagram (embedded image)
  - Workflow State Machine Flowchart (embedded image)
  - Multi-Agent Roles & Shared Blackboard (embedded image)
  - Unit 3 Long-Term Memory (ChromaDB + BGE)
  - Unit 3 Adaptive Feedback Loop (Act-Observe-Reflect-Adjust)
  - Unit 4 Human Approval Gate & Governance
  - Phase 4 Fault Tolerance, SQLite Checkpoints & Crash Recovery
  - Phase 4 Dynamic Intent Parsing & Historical Report Archival
  - Step-by-Step Execution Screenshots (embedded grid)
  - Automated Pytest Verification & Quality Metrics (100% Pass)
  - Individual Member Contributions & Final Jury Conclusion
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))
DIAGRAMS_DIR = os.path.join(ROOT_DIR, "submision", "3_Diagrams_and_Visuals")
SCREENSHOTS_DIR = os.path.join(ROOT_DIR, "submision", "4_Screenshots_and_Execution_Traces")
PPTX_OUTPUT = os.path.join(BASE_DIR, "Agentic_AI_Final_Jury_Group_4.pptx")

# Enterprise Color Palette
NAVY_PRIMARY = RGBColor(26, 39, 68)     # #1a2744
BLUE_ACCENT  = RGBColor(26, 115, 232)   # #1a73e8
DARK_GRAY    = RGBColor(32, 33, 36)     # #202124
LIGHT_BG     = RGBColor(248, 250, 252)  # #f8fafc
WHITE        = RGBColor(255, 255, 255)
GREEN_ACCENT = RGBColor(19, 115, 51)    # #137333

def set_slide_background(slide, color):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_header(slide, title_text, category_text="AGENTIC AI · END-TERM JURY EXAMINATION · GROUP 4"):
    # Header banner
    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.9))
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_cat = tf.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = BLUE_ACCENT

    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = NAVY_PRIMARY

def add_bullet_point(text_frame, title, body, pt_size=13):
    p = text_frame.add_paragraph()
    p.space_after = Pt(8)
    run_title = p.add_run()
    run_title.text = f"• {title}: "
    run_title.font.bold = True
    run_title.font.size = Pt(pt_size)
    run_title.font.color.rgb = NAVY_PRIMARY

    run_body = p.add_run()
    run_body.text = body
    run_body.font.bold = False
    run_body.font.size = Pt(pt_size)
    run_body.font.color.rgb = DARK_GRAY

def create_presentation():
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # ─────────────────────────────────────────────────────────────────────────
    # SLIDE 1: Title Slide (Dark Navy)
    # ─────────────────────────────────────────────────────────────────────────
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1, NAVY_PRIMARY)

    title_box = slide1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(4.5))
    tf1 = title_box.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "AGENTIC ARTIFICIAL INTELLIGENCE · FINAL JURY 2026"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = RGBColor(138, 180, 248)
    p0.space_after = Pt(12)

    p1 = tf1.add_paragraph()
    p1.text = "Autonomous Multi-Agent Expense Report Pipeline"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    p1.space_after = Pt(10)

    p2 = tf1.add_paragraph()
    p2.text = "A Fault-Tolerant, Distributed Multi-Agent DAG with Long-Term Memory, Feedback Loops & Human Governance"
    p2.font.size = Pt(16)
    p2.font.color.rgb = RGBColor(218, 224, 233)
    p2.space_after = Pt(28)

    p3 = tf1.add_paragraph()
    p3.text = "Group 4: Aryan Maradwar · Asta Joseph · Dhiraj Sarawale (Lead) · Ridhima Maliya"
    p3.font.size = Pt(14)
    p3.font.bold = True
    p3.font.color.rgb = RGBColor(129, 201, 149)

    p4 = tf1.add_paragraph()
    p4.text = "Stack: LangGraph · ChromaDB (BGE-small-en-v1.5) · Local Ollama · SqliteSaver · ReportLab · Streamlit"
    p4.font.size = Pt(12)
    p4.font.color.rgb = RGBColor(170, 180, 195)

    # ─────────────────────────────────────────────────────────────────────────
    # SLIDE 2: Problem Statement & Industrial Scenario
    # ─────────────────────────────────────────────────────────────────────────
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2, LIGHT_BG)
    add_header(slide2, "Target Scenario & Problem Formulation")

    left_box = slide2.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.2))
    tf2_l = left_box.text_frame
    tf2_l.word_wrap = True
    p2_q = tf2_l.paragraphs[0]
    p2_q.text = "Target Problem Scenario"
    p2_q.font.size = Pt(16)
    p2_q.font.bold = True
    p2_q.font.color.rgb = BLUE_ACCENT
    p2_q.space_after = Pt(10)

    p2_quote = tf2_l.add_paragraph()
    p2_quote.text = "“Generate my travel expense report for last month and email it to finance.”"
    p2_quote.font.size = Pt(16)
    p2_quote.font.italic = True
    p2_quote.font.bold = True
    p2_quote.font.color.rgb = NAVY_PRIMARY
    p2_quote.space_after = Pt(16)

    add_bullet_point(tf2_l, "Data Source", "Tabular CSV records containing dates, ambiguous vendor names, descriptions, and amounts.")
    add_bullet_point(tf2_l, "Temporal Constraint", "Must dynamically enforce strict calendar boundaries for the preceding month.")
    add_bullet_point(tf2_l, "Categorization", "Map ambiguous transactions into tax-deductible buckets (Meals, Hotels, Flights, Transport, Misc).")

    right_box = slide2.shapes.add_textbox(Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.2))
    tf2_r = right_box.text_frame
    tf2_r.word_wrap = True
    p2_r = tf2_r.paragraphs[0]
    p2_r.text = "Why Traditional LLM Prompts Fail"
    p2_r.font.size = Pt(16)
    p2_r.font.bold = True
    p2_r.font.color.rgb = RGBColor(197, 34, 31)
    p2_r.space_after = Pt(10)

    add_bullet_point(tf2_r, "Mathematical Hallucination", "LLMs cannot guarantee deterministic addition over tabular currency rows.")
    add_bullet_point(tf2_r, "No Persistence", "Single scripts forget merchant corrections immediately upon process termination.")
    add_bullet_point(tf2_r, "Crash Vulnerability", "If a crash happens halfway through, execution restarts from scratch.")
    add_bullet_point(tf2_r, "Unsafe Irreversibility", "Dispatching emails to corporate finance without approval causes financial damage.")

    # ─────────────────────────────────────────────────────────────────────────
    # SLIDE 3: Project Objectives & Core Deliverables
    # ─────────────────────────────────────────────────────────────────────────
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3, LIGHT_BG)
    add_header(slide3, "Project Objectives & Key Deliverables")

    box3 = slide3.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(11.7), Inches(5.4))
    tf3 = box3.text_frame
    tf3.word_wrap = True

    add_bullet_point(tf3, "1. Zero-Hallucination Determinism", "Pure Python arithmetic execution for category totals and grand totals. LLM is strictly isolated to natural language classification and email drafting.")
    add_bullet_point(tf3, "2. Long-Term Vector Memory (ChromaDB)", "Index historical merchant classifications with BAAI/bge-small-en-v1.5 embeddings. Skips LLM calls when cosine similarity >= 0.85 and prioritizes user corrections.")
    add_bullet_point(tf3, "3. Adaptive Feedback Loop (Act-Observe-Reflect-Adjust)", "Automated recovery cycle for missing transactional data with budget limit (max 2 retries) before escalating to the audit appendix.")
    add_bullet_point(tf3, "4. Distributed Role-Based Agents & Shared Blackboard", "5 specialized roles (Coordinator, Retriever, Categorizer, Auditor, Reporter) communicating via IEEE FIPA-ACL structured performatives.")
    add_bullet_point(tf3, "5. Fault-Tolerant State Checkpointing (SqliteSaver)", "Every node transition commits state to SQLite (data/checkpoints.db). Server crashes at any stage can be resumed instantly.")
    add_bullet_point(tf3, "6. Human-in-the-Loop Governance & Dynamic Prompts", "Adjustable Autonomy approval gate before email dispatch, coupled with natural language intent extraction for custom recipients and scopes.")

    # ─────────────────────────────────────────────────────────────────────────
    # SLIDE 4: Enterprise Design Principles
    # ─────────────────────────────────────────────────────────────────────────
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4, LIGHT_BG)
    add_header(slide4, "Enterprise Agentic Design Philosophy")

    cards = [
        ("Deterministic Math", "Never let an LLM sum currency.\nPython calculations prevent hallucinations and guarantee compliance.", Inches(0.8), Inches(1.6), Inches(2.7), Inches(4.8)),
        ("Structured DAG State", "Avoid wild autonomous loops.\nLangGraph explicit state machine provides full auditability and trace logs.", Inches(3.8), Inches(1.6), Inches(2.7), Inches(4.8)),
        ("Distributed Roles", "Single responsibilities per agent.\nCoordinator, Retriever, Categorizer, Auditor, and Reporter communicate on a Blackboard.", Inches(6.8), Inches(1.6), Inches(2.7), Inches(4.8)),
        ("Durable Resilience", "Survive production crashes.\nSqliteSaver checkpointing saves state so interrupted pipelines resume cleanly.", Inches(9.8), Inches(1.6), Inches(2.7), Inches(4.8)),
    ]

    for title, desc, cx, cy, cw, ch in cards:
        shape = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, cy, cw, ch)
        shape.fill.solid()
        shape.fill.fore_color.rgb = WHITE
        shape.line.color.rgb = BLUE_ACCENT
        shape.line.width = Pt(1.5)

        tf_c = shape.text_frame
        tf_c.word_wrap = True
        p_c1 = tf_c.paragraphs[0]
        p_c1.text = title
        p_c1.font.size = Pt(14)
        p_c1.font.bold = True
        p_c1.font.color.rgb = NAVY_PRIMARY
        p_c1.space_after = Pt(14)

        p_c2 = tf_c.add_paragraph()
        p_c2.text = desc
        p_c2.font.size = Pt(11)
        p_c2.font.color.rgb = DARK_GRAY

    # ─────────────────────────────────────────────────────────────────────────
    # SLIDE 5: Technical Model & Technology Stack
    # ─────────────────────────────────────────────────────────────────────────
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5, LIGHT_BG)
    add_header(slide5, "Technical Architecture & System Stack")

    rows = 9
    cols = 3
    table_shape = slide5.shapes.add_table(rows, cols, Inches(0.8), Inches(1.5), Inches(11.7), Inches(5.2))
    table = table_shape.table
    table.columns[0].width = Inches(2.6)
    table.columns[1].width = Inches(3.6)
    table.columns[2].width = Inches(5.5)

    headers = ["Subsystem", "Technology / Model", "Role in Agentic Workflow"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY_PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = WHITE

    specs_data = [
        ("Agent DAG Engine", "LangGraph 1.2.16 (StateGraph)", "Explicit state machine orchestration & shared blackboard"),
        ("State Checkpointing", "SqliteSaver (aiosqlite / sqlite-vec)", "Atomic on-disk serialization for crash recovery & thread resume"),
        ("Local LLM Inference", "Ollama (Qwen2.5:7b / ChatOllama)", "Local semantic classification, few-shot reasoning, email drafting"),
        ("Vector Database", "ChromaDB (PersistentClient)", "Persistent local vector store indexing historical vendor memories"),
        ("Embedding Model", "BAAI/bge-small-en-v1.5", "384-dimensional dense semantic embeddings for cosine similarity"),
        ("PDF Generation", "ReportLab 4.x (Platypus)", "Deterministic, styled PDF reporting with exception appendix"),
        ("Observability Dashboard", "Streamlit 1.30+", "Live state inspector, ACL message transcript, crash simulation UI"),
        ("Test Suite", "Pytest 8.x + pytest-cov", "Automated regression tests verifying math, memory, loops & checkpoints"),
    ]

    for r_idx, row in enumerate(specs_data, start=1):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(9.5)
            p.font.color.rgb = DARK_GRAY
            if c_idx == 0:
                p.font.bold = True

    # ─────────────────────────────────────────────────────────────────────────
    # SLIDE 6: System Block Diagram (Embedded)
    # ─────────────────────────────────────────────────────────────────────────
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6, LIGHT_BG)
    add_header(slide6, "System Block Diagram (Layered Architecture)")

    img_path1 = os.path.join(DIAGRAMS_DIR, "01_system_block_diagram.png")
    if os.path.exists(img_path1):
        slide6.shapes.add_picture(img_path1, Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.5))

    # ─────────────────────────────────────────────────────────────────────────
    # SLIDE 7: Multi-Agent Roles & Shared Blackboard (Embedded)
    # ─────────────────────────────────────────────────────────────────────────
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7, LIGHT_BG)
    add_header(slide7, "Unit 4 Multi-Agent Roles & Shared Blackboard")

    img_path3 = os.path.join(DIAGRAMS_DIR, "03_multi_agent_blackboard_diagram.png")
    if os.path.exists(img_path3):
        slide7.shapes.add_picture(img_path3, Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.5))

    # ─────────────────────────────────────────────────────────────────────────
    # SLIDE 8: Workflow Flowchart & State Machine (Embedded)
    # ─────────────────────────────────────────────────────────────────────────
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8, LIGHT_BG)
    add_header(slide8, "Agentic Workflow State Machine Flowchart")

    img_path2 = os.path.join(DIAGRAMS_DIR, "02_agentic_workflow_flowchart.png")
    if os.path.exists(img_path2):
        slide8.shapes.add_picture(img_path2, Inches(1.8), Inches(1.4), Inches(9.7), Inches(5.6))

    # ─────────────────────────────────────────────────────────────────────────
    # SLIDE 9: Unit 3 Long-Term Memory (ChromaDB + BGE)
    # ─────────────────────────────────────────────────────────────────────────
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9, LIGHT_BG)
    add_header(slide9, "Unit 3: Long-Term Semantic Vector Memory")

    box9_l = slide9.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.2))
    tf9_l = box9_l.text_frame
    tf9_l.word_wrap = True
    p9_t = tf9_l.paragraphs[0]
    p9_t.text = "Why Vector Memory in Financial Agents?"
    p9_t.font.size = Pt(16)
    p9_t.font.bold = True
    p9_t.font.color.rgb = BLUE_ACCENT
    p9_t.space_after = Pt(10)

    add_bullet_point(tf9_l, "Ambiguous Merchant Names", "Real receipts contain cryptic names: 'The Capital Grille', 'Starbucks #492', 'Lyft *Ride'. Calling LLMs for every row is slow and non-deterministic.")
    add_bullet_point(tf9_l, "ChromaDB + BGE Embeddings", "Uses BAAI/bge-small-en-v1.5 to map vendor descriptions into a 384-dimensional vector space.")
    add_bullet_point(tf9_l, "Cosine Similarity Threshold", "When cosine similarity >= 0.85, the agent reuses the remembered category directly and skips the LLM entirely (100% deterministic).")

    box9_r = slide9.shapes.add_textbox(Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.2))
    tf9_r = box9_r.text_frame
    tf9_r.word_wrap = True
    p9_r = tf9_r.paragraphs[0]
    p9_r.text = "User Correction Priority Rule"
    p9_r.font.size = Pt(16)
    p9_r.font.bold = True
    p9_r.font.color.rgb = GREEN_ACCENT
    p9_r.space_after = Pt(10)

    add_bullet_point(tf9_r, "Continuous Learning", "Users can teach the agent new merchant rules via CLI (--correct 'Olive Garden=Meals') or the Streamlit sidebar.")
    add_bullet_point(tf9_r, "Precedence Hierarchy", "User corrections are stored with source='user_correction' and take strict precedence over model predictions.")
    add_bullet_point(tf9_r, "Few-Shot Fallback", "If similarity is below threshold, retrieved matches are injected into the prompt as few-shot in-context examples for Ollama.")

    # ─────────────────────────────────────────────────────────────────────────
    # SLIDE 10: Unit 3 Missing-Data Feedback Loop
    # ─────────────────────────────────────────────────────────────────────────
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide10, LIGHT_BG)
    add_header(slide10, "Unit 3: Adaptive Missing-Data Feedback Loop")

    img_path4 = os.path.join(DIAGRAMS_DIR, "04_feedback_loop_diagram.png")
    if os.path.exists(img_path4):
        slide10.shapes.add_picture(img_path4, Inches(0.8), Inches(1.5), Inches(5.8), Inches(5.2))

    box10_r = slide10.shapes.add_textbox(Inches(6.9), Inches(1.5), Inches(5.6), Inches(5.2))
    tf10_r = box10_r.text_frame
    tf10_r.word_wrap = True
    p10_r = tf10_r.paragraphs[0]
    p10_r.text = "Act - Observe - Reflect - Adjust"
    p10_r.font.size = Pt(16)
    p10_r.font.bold = True
    p10_r.font.color.rgb = NAVY_PRIMARY
    p10_r.space_after = Pt(10)

    add_bullet_point(tf10_r, "1. ACT", "Auditor agent scans expense dataset for missing amounts, unparseable dates, or empty categories.")
    add_bullet_point(tf10_r, "2. OBSERVE", "Quantifies missing count and vendor details (e.g. Lyft, Parking Authority).")
    add_bullet_point(tf10_r, "3. REFLECT", "Evaluates retry budget (max 2 retries). Formulates recovery strategy via scripted answers or user prompt.")
    add_bullet_point(tf10_r, "4. ADJUST", "Resolves missing numbers, updates blackboard rows, and recomputes totals. Unresolved items escalate to the PDF appendix.")

    # ─────────────────────────────────────────────────────────────────────────
    # SLIDE 11: Unit 4 Human Approval Gate & Governance
    # ─────────────────────────────────────────────────────────────────────────
    slide11 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide11, LIGHT_BG)
    add_header(slide11, "Unit 4: Human Approval Gate & Adjustable Autonomy")

    box11_l = slide11.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.2))
    tf11_l = box11_l.text_frame
    tf11_l.word_wrap = True
    p11_l = tf11_l.paragraphs[0]
    p11_l.text = "Why Adjustable Autonomy?"
    p11_l.font.size = Pt(16)
    p11_l.font.bold = True
    p11_l.font.color.rgb = RGBColor(197, 34, 31)
    p11_l.space_after = Pt(10)

    add_bullet_point(tf11_l, "Irreversible External Action", "Sending an expense report to corporate finance triggers corporate disbursements and legal compliance audits.")
    add_bullet_point(tf11_l, "Autonomous Draft, Human Sign-Off", "The agent performs 100% of the retrieval, math, categorization, and drafting autonomously, but halts for human confirmation.")
    add_bullet_point(tf11_l, "Auditor Warning Injection", "Displays anomalies (e.g., Delta Airlines >= Rs. 1,000 threshold, potential duplicate charges) directly on the approval screen.")

    box11_r = slide11.shapes.add_textbox(Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.2))
    tf11_r = box11_r.text_frame
    tf11_r.word_wrap = True
    p11_r = tf11_r.paragraphs[0]
    p11_r.text = "Branching Decision Paths"
    p11_r.font.size = Pt(16)
    p11_r.font.bold = True
    p11_r.font.color.rgb = NAVY_PRIMARY
    p11_r.space_after = Pt(10)

    add_bullet_point(tf11_r, "If Approved ('approve')", "Signs off report, triggers SMTP send, archives RFC 822 EML file to ./outbox, and marks workflow as COMPLETED.")
    add_bullet_point(tf11_r, "If Rejected ('reject')", "Cancels email dispatch, logs FIPA-ACL REFUSE speech act, and returns control to Coordinator for adjustment.")
    add_bullet_point(tf11_r, "Automated CI/CD Flag", "Supports --auto-approve for automated headless evaluations and regression testing.")

    # ─────────────────────────────────────────────────────────────────────────
    # SLIDE 12: Phase 4 Fault Tolerance, Checkpoints & Crash Recovery
    # ─────────────────────────────────────────────────────────────────────────
    slide12 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide12, LIGHT_BG)
    add_header(slide12, "Phase 4: Fault Tolerance & Crash Recovery (SqliteSaver)")

    box12_l = slide12.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.2))
    tf12_l = box12_l.text_frame
    tf12_l.word_wrap = True
    p12_l = tf12_l.paragraphs[0]
    p12_l.text = "The Jury Challenge Answered"
    p12_l.font.size = Pt(16)
    p12_l.font.bold = True
    p12_l.font.color.rgb = BLUE_ACCENT
    p12_l.space_after = Pt(10)

    add_bullet_point(tf12_l, "Question", "“What happens if the server crashes at Step 3? Does it start from scratch?”")
    add_bullet_point(tf12_l, "Our Solution", "Integrated LangGraph's SqliteSaver checkpointer. Every completed node atomically commits the typed blackboard state into data/checkpoints.db.")
    add_bullet_point(tf12_l, "Instant Resume", "Re-invoking with the same session thread_id skips completed steps (Coordinator, Retriever) and resumes immediately at Step 3.")

    s6_img = os.path.join(SCREENSHOTS_DIR, "step6_crash_simulation_recovery.png")
    if os.path.exists(s6_img):
        slide12.shapes.add_picture(s6_img, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.5))

    # ─────────────────────────────────────────────────────────────────────────
    # SLIDE 13: Phase 4 Dynamic Prompts & Historical Report Archival
    # ─────────────────────────────────────────────────────────────────────────
    slide13 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide13, LIGHT_BG)
    add_header(slide13, "Phase 4: Dynamic Intent Parsing & Report Archival")

    box13_l = slide13.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.2))
    tf13_l = box13_l.text_frame
    tf13_l.word_wrap = True
    p13_l = tf13_l.paragraphs[0]
    p13_l.text = "1. Dynamic Prompt Parsing"
    p13_l.font.size = Pt(16)
    p13_l.font.bold = True
    p13_l.font.color.rgb = BLUE_ACCENT
    p13_l.space_after = Pt(10)

    add_bullet_point(tf13_l, "Custom Recipients", "Detects target emails in instruction (e.g. 'email to audit@firm.com') and routes output dynamically.")
    add_bullet_point(tf13_l, "Flexible Date Scopes", "Instructions requesting 'all expenses' or 'all records' bypass default last-month filter.")
    add_bullet_point(tf13_l, "Category Filtering", "Prompts requesting 'only Meals' or 'flights only' filter the categorized table automatically.")

    box13_r = slide13.shapes.add_textbox(Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.2))
    tf13_r = box13_r.text_frame
    tf13_r.word_wrap = True
    p13_r = tf13_r.paragraphs[0]
    p13_r.text = "2. Historical Report Archival"
    p13_r.font.size = Pt(16)
    p13_r.font.bold = True
    p13_r.font.color.rgb = GREEN_ACCENT
    p13_r.space_after = Pt(10)

    add_bullet_point(tf13_r, "Persistent Storage", "Every run generates a timestamped artifact: reports/expense_report_YYYYMMDD_HHMMSS.pdf.")
    add_bullet_point(tf13_r, "JSON Metadata", "Saves grand total, date range, items count, and category breakdown alongside each PDF.")
    add_bullet_point(tf13_r, "Streamlit Archive Selector", "Users can browse, preview, and download past reports instantly without re-running LLM or pipeline.")

    # ─────────────────────────────────────────────────────────────────────────
    # SLIDE 14: Step-by-Step Execution Screenshots Grid
    # ─────────────────────────────────────────────────────────────────────────
    slide14 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide14, LIGHT_BG)
    add_header(slide14, "Step-by-Step Model Execution Traces")

    s1 = os.path.join(SCREENSHOTS_DIR, "step1_coordinator_init.png")
    s2 = os.path.join(SCREENSHOTS_DIR, "step2_retriever_filtering.png")
    s3 = os.path.join(SCREENSHOTS_DIR, "step3_categorizer_memory_llm.png")
    s4 = os.path.join(SCREENSHOTS_DIR, "step4_auditor_feedback_loop.png")

    coords = [
        (s1, Inches(0.8), Inches(1.5), Inches(5.6), Inches(2.5)),
        (s2, Inches(6.8), Inches(1.5), Inches(5.6), Inches(2.5)),
        (s3, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.5)),
        (s4, Inches(6.8), Inches(4.3), Inches(5.6), Inches(2.5)),
    ]
    for s_img, sx, sy, sw, sh in coords:
        if os.path.exists(s_img):
            slide14.shapes.add_picture(s_img, sx, sy, sw, sh)

    # ─────────────────────────────────────────────────────────────────────────
    # SLIDE 15: Automated Test Suite & Quality Verification (100% Pass)
    # ─────────────────────────────────────────────────────────────────────────
    slide15 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide15, LIGHT_BG)
    add_header(slide15, "Automated Pytest Verification & Quality Metrics")

    box15_l = slide15.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.2))
    tf15_l = box15_l.text_frame
    tf15_l.word_wrap = True
    p15_l = tf15_l.paragraphs[0]
    p15_l.text = "Automated Test Suite (tests/test_agent.py)"
    p15_l.font.size = Pt(16)
    p15_l.font.bold = True
    p15_l.font.color.rgb = GREEN_ACCENT
    p15_l.space_after = Pt(10)

    add_bullet_point(tf15_l, "test_tools_deterministic_math", "Verifies that category totals and grand total equal exact Python sum (zero LLM math). [PASSED]")
    add_bullet_point(tf15_l, "test_chromadb_memory_store_priority", "Verifies user corrections take strict precedence over semantic similarity matches. [PASSED]")
    add_bullet_point(tf15_l, "test_feedback_loop_act_observe_adjust", "Verifies missing items trigger recovery and resolve via scripted answers. [PASSED]")
    add_bullet_point(tf15_l, "test_langgraph_sqlite_checkpoint_resume", "Verifies state persistence in SQLite and seamless resumption after crash. [PASSED]")

    s8_img = os.path.join(SCREENSHOTS_DIR, "step8_pytest_test_results.png")
    if os.path.exists(s8_img):
        slide15.shapes.add_picture(s8_img, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.5))

    # ─────────────────────────────────────────────────────────────────────────
    # SLIDE 16: Individual Member Contributions & Conclusion
    # ─────────────────────────────────────────────────────────────────────────
    slide16 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide16, NAVY_PRIMARY)

    title16_box = slide16.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.0))
    tf16_t = title16_box.text_frame
    p16_cat = tf16_t.paragraphs[0]
    p16_cat.text = "GROUP 4 INDIVIDUAL CONTRIBUTIONS & CONCLUSION"
    p16_cat.font.size = Pt(10)
    p16_cat.font.bold = True
    p16_cat.font.color.rgb = RGBColor(138, 180, 248)
    p16_h = tf16_t.add_paragraph()
    p16_h.text = "Technical Ownership & Final Jury Summary"
    p16_h.font.size = Pt(22)
    p16_h.font.bold = True
    p16_h.font.color.rgb = WHITE

    table16_shape = slide16.shapes.add_table(5, 3, Inches(0.8), Inches(1.5), Inches(11.7), Inches(4.3))
    t16 = table16_shape.table
    t16.columns[0].width = Inches(2.5)
    t16.columns[1].width = Inches(3.8)
    t16.columns[2].width = Inches(5.4)

    h16 = ["Member Name", "Core Ownership", "Key Technical Deliverables"]
    for i, h in enumerate(h16):
        c = t16.cell(0, i)
        c.text = h
        c.fill.solid()
        c.fill.fore_color.rgb = BLUE_ACCENT
        p = c.text_frame.paragraphs[0]
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = WHITE

    contribs = [
        ("Dhiraj Sarawale\n(Integration Lead)", "System Architecture, LangGraph DAG & Fault Tolerance", "Built StateGraph engine, SQLite checkpoint recovery, dynamic intent parser & Streamlit crash demo."),
        ("Aryan Maradwar", "Unit 3 Long-Term Vector Memory & Ingestion", "Integrated ChromaDB vector DB with BGE embeddings, similarity thresholding & user correction memory."),
        ("Asta Joseph", "Unit 4 Role-Based Multi-Agent Architecture", "Engineered 5 role agents, IEEE FIPA-ACL structured messaging protocol & execution trace verification."),
        ("Ridhima Maliya", "Unit 3 Feedback Loops & Unit 4 Governance", "Built Act-Observe-Reflect-Adjust feedback loop, Human Approval Gate & ReportLab PDF publishing engine."),
    ]
    for r_idx, row in enumerate(contribs, start=1):
        for c_idx, val in enumerate(row):
            c = t16.cell(r_idx, c_idx)
            c.text = val
            c.fill.solid()
            c.fill.fore_color.rgb = RGBColor(38, 52, 85)
            p = c.text_frame.paragraphs[0]
            p.font.size = Pt(9.5)
            p.font.color.rgb = WHITE
            if c_idx == 0:
                p.font.bold = True

    concl_box = slide16.shapes.add_textbox(Inches(0.8), Inches(6.0), Inches(11.7), Inches(1.0))
    tf16_c = concl_box.text_frame
    p_concl = tf16_c.paragraphs[0]
    p_concl.text = "Conclusion: Autonomous agents in finance require deterministic engineering, durable state checkpoints, and human governance. Group 4 has delivered a verifiable, enterprise-grade multi-agent solution ready for live deployment."
    p_concl.font.size = Pt(11)
    p_concl.font.italic = True
    p_concl.font.color.rgb = RGBColor(129, 201, 149)

    prs.save(PPTX_OUTPUT)
    print(f"✔ 16-Slide Presentation generated successfully: {PPTX_OUTPUT}")

if __name__ == "__main__":
    create_presentation()

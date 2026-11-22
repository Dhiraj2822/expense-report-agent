"""
submision/1_Project_Report_10_Pages/generate_report.py
───────────────────────────────────────────────────────
Builds a comprehensive, publication-grade 10-Page Project Report in PDF format
for the End-Term Jury Examination in Agentic AI (Group 4).
Includes:
  1. Title Page & Executive Summary
  2. Project Objectives & Problem Formulation
  3. Enterprise Agentic Design Principles
  4. Technical Model Architecture & Infrastructure Details
  5. System Block Diagram & Layered Component Model
  6. Agentic Workflow State Machine Flowchart
  7. Multi-Agent Shared Blackboard & Communication Protocols (FIPA-ACL)
  8. Step-by-Step Model Execution Screenshots & Trace Verification
  9. Fault Tolerance, Crash Checkpointing & Historical Archival
  10. Individual Member Contributions, Test Results & Conclusions
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, HRFlowable, KeepTogether
)
from reportlab.pdfgen import canvas

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))
DIAGRAMS_DIR = os.path.join(ROOT_DIR, "submision", "3_Diagrams_and_Visuals")
SCREENSHOTS_DIR = os.path.join(ROOT_DIR, "submision", "4_Screenshots_and_Execution_Traces")
PDF_OUTPUT = os.path.join(BASE_DIR, "Final_Jury_Report_Group_4.pdf")

# Custom Canvas for running headers and page numbers
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))

        # Do not draw running header on cover page
        if self._pageNumber > 1:
            self.drawString(2 * cm, 28.5 * cm, "Agentic AI End-Term Jury Examination Report | Group 4")
            self.drawRightString(19 * cm, 28.5 * cm, "Autonomous Expense Report Agent")
            self.setStrokeColor(colors.HexColor("#dcdcdc"))
            self.setLineWidth(0.5)
            self.line(2 * cm, 28.3 * cm, 19 * cm, 28.3 * cm)

        # Footer on all pages
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(19 * cm, 1.2 * cm, page_str)
        self.drawString(2 * cm, 1.2 * cm, "AIA_7 Group 4: Aryan Maradwar · Asta Joseph · Dhiraj Sarawale · Ridhima Maliya")
        self.setStrokeColor(colors.HexColor("#dcdcdc"))
        self.setLineWidth(0.5)
        self.line(2 * cm, 1.5 * cm, 19 * cm, 1.5 * cm)
        self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        PDF_OUTPUT,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2.2 * cm,
        bottomMargin=2.2 * cm,
    )

    styles = getSampleStyleSheet()

    # Define bespoke typography styles
    color_primary = colors.HexColor("#1a2744")
    color_secondary = colors.HexColor("#2e4a8e")
    color_dark = colors.HexColor("#202124")

    title_style = ParagraphStyle(
        "CoverTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=30,
        alignment=TA_CENTER,
        textColor=color_primary,
    )

    subtitle_style = ParagraphStyle(
        "CoverSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=16,
        alignment=TA_CENTER,
        textColor=color_secondary,
    )

    h1_style = ParagraphStyle(
        "Heading1_Custom",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=20,
        textColor=color_primary,
        spaceBefore=8,
        spaceAfter=6,
    )

    h2_style = ParagraphStyle(
        "Heading2_Custom",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=color_secondary,
        spaceBefore=6,
        spaceAfter=4,
    )

    body_style = ParagraphStyle(
        "Body_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        alignment=TA_JUSTIFY,
        textColor=color_dark,
        spaceAfter=6,
    )

    body_bold = ParagraphStyle(
        "Body_Bold",
        parent=body_style,
        fontName="Helvetica-Bold",
    )

    code_style = ParagraphStyle(
        "Code_Custom",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#1e293b"),
    )

    story = []

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 1: TITLE PAGE & EXECUTIVE SUMMARY
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 25))
    story.append(Paragraph("AGENTIC ARTIFICIAL INTELLIGENCE", ParagraphStyle("Super", fontName="Helvetica-Bold", fontSize=12, alignment=TA_CENTER, textColor=colors.HexColor("#888888"), leading=14)))
    story.append(Paragraph("END-TERM FINAL JURY EXAMINATION REPORT", ParagraphStyle("SubSuper", fontName="Helvetica-Bold", fontSize=13, alignment=TA_CENTER, textColor=color_secondary, leading=16)))
    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=2, color=color_secondary, spaceAfter=20))

    story.append(Paragraph("Autonomous Multi-Agent Expense Report Pipeline", title_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph("A Fault-Tolerant, Distributed Multi-Agent DAG Architecture with Long-Term Vector Memory, Adaptive Feedback Loops, and Human-in-the-Loop Governance", subtitle_style))
    story.append(Spacer(1, 20))

    # Metadata Table
    meta_data = [
        [Paragraph("<b>Course Code:</b>", body_style), Paragraph("Agentic AI (AIA_7)", body_style)],
        [Paragraph("<b>Project Group:</b>", body_style), Paragraph("Group 4", body_style)],
        [Paragraph("<b>Team Members:</b>", body_style), Paragraph("Aryan Maradwar · Asta Joseph · <b>Dhiraj Sarawale</b> · Ridhima Maliya", body_style)],
        [Paragraph("<b>Core Frameworks:</b>", body_style), Paragraph("LangGraph · ChromaDB (BGE-small-en-v1.5) · Local Ollama (Qwen2.5) · ReportLab · Streamlit", body_style)],
        [Paragraph("<b>Evaluation Period:</b>", body_style), Paragraph("November 2026 Final ESE Jury Examination", body_style)],
        [Paragraph("<b>Repository:</b>", body_style), Paragraph("https://github.com/Dhiraj2822/expense-report-agent.git", body_style)],
    ]
    meta_table = Table(meta_data, colWidths=[4 * cm, 13 * cm])
    meta_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 25))

    story.append(Paragraph("Executive Summary", h2_style))
    story.append(Paragraph(
        "Modern enterprise financial operations require autonomous agents capable of interpreting natural language instructions, reconciling ambiguous transactions, and coordinating distributed activities without human hallucination. This project presents a fully local, fault-tolerant, multi-agent expense reporting system answering the industrial challenge: <i>'Generate my travel expense report for last month and email it to finance.'</i> "
        "Unlike fragile single-prompt scripts, our architecture implements an enterprise-grade Directed Acyclic Graph (DAG) using LangGraph. The system combines local vector memory (ChromaDB with BAAI/bge-small-en-v1.5 embeddings), an adaptive 4-stage missing-data feedback loop (Act-Observe-Reflect-Adjust), 5 specialized agent roles communicating via FIPA-ACL protocols over a shared blackboard, durable SQLite state checkpointing, and an explicit Human Approval Gate before irreversible financial communication occurs.",
        body_style
    ))
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 2: OBJECTIVES & PROBLEM FORMULATION
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("1. Project Title & Problem Statement", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=color_secondary, spaceAfter=8))
    story.append(Paragraph(
        "<b>Formal Title:</b> Autonomous Multi-Agent Expense Report Pipeline with Long-Term Memory, Fault-Tolerant Checkpointing, and Adjustable Autonomy.<br/>"
        "<b>Target Problem Statement:</b> Design and implement an autonomous AI agent for the corporate scenario: <i>'Generate my travel expense report for last month and email it to finance.'</i> The agent must autonomously ingest raw tabular expense rows, enforce strict calendar boundaries, accurately categorize ambiguous merchants, deterministically calculate category totals, generate a publication-ready PDF artifact, draft professional correspondence, and safely handle missing data.",
        body_style
    ))

    story.append(Paragraph("2. Project Objectives", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=color_secondary, spaceAfter=8))
    objectives = [
        ("Objective 1: Zero-Hallucination Determinism", "Eliminate mathematical and financial hallucination by enforcing a clean separation between LLM semantic classification and deterministic Python arithmetic computations."),
        ("Objective 2: Long-Term Memory & Continuous Learning", "Implement vector embeddings (ChromaDB + sentence-transformers) to resolve ambiguous vendor receipts, remember user corrections across sessions, and bypass costly model inference on known merchants."),
        ("Objective 3: Dynamic Environment Interaction & Feedback Loops", "Build an autonomous Act-Observe-Reflect-Adjust feedback loop to detect incomplete records, prompt the operator or scripted answers, and dynamically adjust blackboard state with retry budgets."),
        ("Objective 4: Distributed Role-Based Multi-Agent Collaboration", "Decompose the monolithic pipeline into five autonomous agents (Coordinator, Retriever, Categorizer, Auditor, Reporter) coordinated via a shared blackboard and FIPA-ACL communication standards."),
        ("Objective 5: Durable Fault Tolerance & Crash Recovery", "Implement atomic state checkpointing via LangGraph SqliteSaver so that unanticipated process halts or server crashes at any pipeline stage can seamlessly resume without re-running prior nodes."),
        ("Objective 6: Human-in-the-Loop Governance & Dynamic Intent", "Incorporate adjustable autonomy via an explicit Human Approval Gate before email dispatch, coupled with natural language intent extraction for dynamic scopes and custom recipients.")
    ]
    for title, desc in objectives:
        story.append(Paragraph(f"• <b>{title}:</b> {desc}", body_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("3. Base Version vs. Extended Multi-Agent Evolution", h2_style))
    comp_data = [
        ["Dimension", "Base Architecture (Unit 0-2)", "Extended Multi-Agent System (Units 3-4 + Phase 4)"],
        ["Pipeline Model", "Rigid 9-node sequential pipeline", "Role-based cooperative DAG with shared blackboard"],
        ["Memory Capabilities", "Stateless; memory clears upon exit", "Dual-tier: ChromaDB vector store + sliding window context"],
        ["Handling Missing Data", "Blind escalation; flagged rows only", "Adaptive feedback loop (Act-Observe-Reflect-Adjust; 2 retries)"],
        ["Crash Recovery", "None; restarts from Node 1 upon crash", "Atomic SQLite checkpoints; instant resume from failed stage"],
        ["Human Governance", "Autonomous email dispatch without consent", "Adjustable Autonomy Gate requiring explicit operator sign-off"],
        ["Prompt Flexibility", "Hardcoded date filter and fixed email", "Dynamic intent parsing (custom recipients, scopes & categories)"],
    ]
    comp_table = Table(comp_data, colWidths=[3.2 * cm, 6.8 * cm, 7.0 * cm])
    comp_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), color_primary),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(comp_table)
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 3: DESIGN PRINCIPLES & SYSTEM ARCHITECTURE
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("4. Enterprise Agentic Design Principles", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=color_secondary, spaceAfter=8))
    story.append(Paragraph(
        "To satisfy corporate standards (as implemented in enterprise platforms such as Brex, Ramp, and SAP Concur), our architecture adheres to four foundational design principles:",
        body_style
    ))

    principles = [
        ("1. Determinism over Generative Hallucination", "Large Language Models are non-deterministic pattern matchers. In enterprise finance, allowing an LLM to perform arithmetic or edit transactional ledgers directly results in audit failures and regulatory non-compliance. Our architecture limits the LLM strictly to natural language intent parsing, few-shot contextual reasoning, and email drafting. All arithmetic totals, calendar window filters, and financial aggregations are executed via deterministic, verifiable Python logic."),
        ("2. Explicit State Machine (DAG) vs. Wild Autonomous Loops", "Unconstrained autonomous ReAct loops frequently suffer from circular reasoning, non-terminating loops, and unpredictable execution costs. We utilize LangGraph to enforce a structured Directed Acyclic Graph (DAG) state machine where every node transition represents an atomic, observable transaction."),
        ("3. Distributed Agency via Shared Blackboard & FIPA-ACL", "Rather than maintaining monolithic agents that perform all functions, we decompose duties across specialized role agents (Coordinator, Retriever, Categorizer, Auditor, Reporter). Agents communicate asynchronously through an immutable blackboard state and formal FIPA-ACL communication acts (REQUEST, INFORM, ACCEPT-PROPOSAL, REFUSE)."),
        ("4. Fault Tolerance & Durable Execution Persistence", "Industrial operations must withstand container restarts, network partitions, and host node crashes. By integrating LangGraph's SqliteSaver, every node output is committed to an on-disk SQLite database. A process halted at Step 3 resumes exactly at Step 3 without repeating prior compute-heavy tasks.")
    ]
    for p_title, p_desc in principles:
        story.append(Paragraph(f"• <b>{p_title}:</b> {p_desc}", body_style))

    story.append(Spacer(1, 8))
    story.append(Paragraph("5. Architectural Component Layers", h2_style))
    arch_layers = [
        ("Ingestion & Parsing Layer", "Natural language instruction parsing using regex-backed intent extractors to isolate target recipients, date scopes, and category filters. Tabular CSV ingestion with calendar date validation."),
        ("Memory & Semantic Layer", "Local ChromaDB vector database powered by BAAI/bge-small-en-v1.5 embeddings. Maintains high-confidence cosine similarity matching (>= 0.85) and gives highest precedence to permanent user corrections."),
        ("Auditing & Feedback Layer", "Multi-stage feedback loop monitoring data consistency, flagging missing values, checking duplicate vendor charges, and managing retry budgets."),
        ("Publishing & Artifact Layer", "Deterministic ReportLab PDF generation with dynamic category tables, exception appendices, and RFC 822 EML message archiving.")
    ]
    for l_title, l_desc in arch_layers:
        story.append(Paragraph(f"<b>[{l_title}]:</b> {l_desc}", body_style))

    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 4: TECHNICAL MODEL & SYSTEM SPECIFICATIONS
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("6. Technical Model Details & Technology Stack", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=color_secondary, spaceAfter=8))
    story.append(Paragraph(
        "The system is built entirely on open-source, offline-capable components. It guarantees full operational independence without external SaaS dependencies or recurring API expenses.",
        body_style
    ))

    tech_specs = [
        ["Subsystem", "Technology / Model", "Technical Role & Configuration"],
        ["Orchestration Engine", "LangGraph 1.2.16 (StateGraph)", "Explicit DAG state machine managing node transitions and state updates"],
        ["State Checkpointing", "SqliteSaver (aiosqlite / sqlite-vec)", "Persistent on-disk storage (`checkpoints.db`) for crash recovery & thread resume"],
        ["Local LLM Inference", "Ollama (Qwen2.5:7b / ChatOllama)", "Local offline LLM for semantic classification, few-shot reasoning, and drafting"],
        ["Vector Database", "ChromaDB (PersistentClient)", "Persistent local vector store (`data/chroma_db`) indexing vendor memories"],
        ["Embedding Model", "BAAI/bge-small-en-v1.5 (HuggingFace)", "384-dimensional dense semantic embeddings for cosine similarity lookups"],
        ["PDF Generation", "ReportLab 4.x (Platypus)", "Deterministic, styled PDF reporting (`expense_report.pdf` & `reports/`)"],
        ["Web Observability UI", "Streamlit 1.30+", "Live blackboard inspection, ACL logs, crash simulation & archive viewer"],
        ["Test Infrastructure", "Pytest 8.x + pytest-cov", "Automated regression suite verifying determinism, memory, and recovery"],
    ]
    tech_table = Table(tech_specs, colWidths=[3.5 * cm, 4.5 * cm, 9.0 * cm])
    tech_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), color_primary),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(tech_table)

    story.append(Spacer(1, 10))
    story.append(Paragraph("7. Shared Blackboard Schema (`AgentBlackboardState`)", h2_style))
    story.append(Paragraph(
        "To avoid state overwrite bugs during multi-agent node transitions, the blackboard state is structured using Python's `TypedDict(total=False)`. This guarantees that partial dictionary updates from individual agents are merged into the shared state rather than overwriting prior keys.",
        body_style
    ))

    code_snippet = (
        "class AgentBlackboardState(TypedDict, total=False):\n"
        "    instruction: str                      # User prompt ('Generate report...')\n"
        "    parsed_intent: dict                   # {recipient, date_scope, category_filter}\n"
        "    raw_expenses: list[dict]              # Ingested records from CSV source\n"
        "    filtered_expenses: list[dict]         # Calendar boundary validated items\n"
        "    categorized_expenses: list[dict]      # Memory / LLM classified rows\n"
        "    exceptions: list[dict]                # Flagged items requiring audit\n"
        "    totals: dict                          # Deterministic category & grand totals\n"
        "    date_range: tuple[str, str]           # Active reporting date interval\n"
        "    pdf_path: str                         # Local file path to generated artifact\n"
        "    message_log: list[dict]               # Structured FIPA-ACL message transcript\n"
        "    step_log: list[str]                   # Sliding window short-term context\n"
        "    workflow_status: str                  # in_progress | completed | rejected"
    )
    code_table = Table([[Paragraph(f"<pre>{code_snippet}</pre>", code_style)]], colWidths=[17.0 * cm])
    code_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#94a3b8")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(code_table)
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 5: SYSTEM BLOCK DIAGRAM
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("8. System Block Diagram", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=color_secondary, spaceAfter=8))
    story.append(Paragraph(
        "The block diagram below illustrates the end-to-end layered architecture of the autonomous expense reporting agent. The system decouples natural language ingestion, multi-agent coordination, vector memory persistence, fault-tolerant checkpointing, and delivery artifacts into modular, auditable tiers.",
        body_style
    ))

    block_img_path = os.path.join(DIAGRAMS_DIR, "01_system_block_diagram.png")
    if os.path.exists(block_img_path):
        story.append(Image(block_img_path, width=17.0 * cm, height=10.5 * cm))
        story.append(Spacer(1, 6))
        story.append(Paragraph("<b>Figure 1:</b> Enterprise System Block Diagram showing 4 architectural layers, LangGraph state machine, ChromaDB vector memory, SQLite checkpoints, and Human Approval Gate.", ParagraphStyle("Cap", parent=body_style, fontSize=8, alignment=TA_CENTER, textColor=colors.HexColor("#555555"))))

    story.append(Spacer(1, 8))
    story.append(Paragraph("Key Architectural Invariants:", h2_style))
    invariants = [
        ("Separation of Concerns", "Each layer executes strictly within its defined domain. Input parsing never modifies persistent ledgers, and reporting nodes never execute heuristic categorization."),
        ("Atomic Persistence", "Every state transition across Layer 2 triggers an asynchronous checkpoint write to SQLite Layer 3, preventing data loss during catastrophic system interruptions."),
        ("Safe External Boundary", "Layer 4 guards all external communications. Outgoing emails and financial submissions are strictly quarantined until the Human Approval Gate issues an explicit sign-off.")
    ]
    for inv_title, inv_desc in invariants:
        story.append(Paragraph(f"• <b>{inv_title}:</b> {inv_desc}", body_style))

    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 6: AGENTIC WORKFLOW & FLOWCHART
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("9. Agentic Workflow State Machine Flowchart", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=color_secondary, spaceAfter=8))
    story.append(Paragraph(
        "The flowchart below outlines the discrete execution path of the agentic state machine, illustrating the memory lookup branch, the adaptive feedback retry loop, and the human gate decision node.",
        body_style
    ))

    flow_img_path = os.path.join(DIAGRAMS_DIR, "02_agentic_workflow_flowchart.png")
    if os.path.exists(flow_img_path):
        story.append(Image(flow_img_path, width=15.0 * cm, height=16.5 * cm))
        story.append(Spacer(1, 4))
        story.append(Paragraph("<b>Figure 2:</b> State Machine Flowchart detailing execution branches, ChromaDB cosine thresholding (>= 0.85), feedback loop retry budget, and Human Approval Gate.", ParagraphStyle("Cap", parent=body_style, fontSize=8, alignment=TA_CENTER, textColor=colors.HexColor("#555555"))))

    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 7: MULTI-AGENT BLACKBOARD & FIPA-ACL COMMUNICATION
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("10. Multi-Agent Shared Blackboard Architecture", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=color_secondary, spaceAfter=8))
    story.append(Paragraph(
        "In accordance with Unit 4 principles, collaboration among distributed agents is governed by a **Shared Blackboard State**. Agents do not invoke one another directly via hardcoded function calls; rather, they post structured **FIPA-ACL messages** to the blackboard and react to state triggers.",
        body_style
    ))

    bb_img_path = os.path.join(DIAGRAMS_DIR, "03_multi_agent_blackboard_diagram.png")
    if os.path.exists(bb_img_path):
        story.append(Image(bb_img_path, width=16.5 * cm, height=10.5 * cm))
        story.append(Spacer(1, 4))
        story.append(Paragraph("<b>Figure 3:</b> Unit 4 Shared Blackboard Architecture with 5 role-based agents exchanging FIPA-ACL speech acts.", ParagraphStyle("Cap", parent=body_style, fontSize=8, alignment=TA_CENTER, textColor=colors.HexColor("#555555"))))

    story.append(Spacer(1, 6))
    story.append(Paragraph("FIPA-ACL Communication Protocol & Performatives", h2_style))
    story.append(Paragraph(
        "Communication adheres to the IEEE FIPA-ACL international agent communication standard. Every exchanged message records a performative, sender, receiver, timestamp, and payload:",
        body_style
    ))
    acl_table_data = [
        ["Performative", "Sender -> Receiver", "Ontology / Purpose", "Example Message Content"],
        ["REQUEST", "Coordinator -> Retriever", "expense-reporting-v1", "Retrieve and filter last month's travel expenses from CSV source."],
        ["INFORM", "Retriever -> Coordinator", "expense-reporting-v1", "Ingested 20 rows. 20 rows within target period 2026-09-01..2026-09-30."],
        ["REQUEST", "Coordinator -> Categorizer", "expense-reporting-v1", "Classify categories for 20 candidates using semantic memory + LLM."],
        ["INFORM", "Categorizer -> Coordinator", "expense-reporting-v1", "Categorization complete. 12 resolved via vector memory, 0 required LLM."],
        ["REQUEST", "Coordinator -> Auditor", "expense-reporting-v1", "Audit 3 flagged exceptions and inspect for duplicate transactions."],
        ["INFORM", "Auditor -> Coordinator", "expense-reporting-v1", "Audit complete. 2 resolved via feedback loop; 1 escalated to PDF."],
        ["ACCEPT-PROPOSAL", "HumanOperator -> Reporter", "expense-reporting-v1", "Human operator approved expense report for finance submission."],
    ]
    acl_table = Table(acl_table_data, colWidths=[2.6 * cm, 4.0 * cm, 3.4 * cm, 7.0 * cm])
    acl_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), color_primary),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7.5),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(acl_table)
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 8: STEP-BY-STEP EXECUTION SCREENSHOTS & TRACES
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("11. Step-by-Step Model Execution Traces & Screenshots", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=color_secondary, spaceAfter=8))
    story.append(Paragraph(
        "The following execution traces document the observable, step-by-step progress of the multi-agent pipeline during live evaluation:",
        body_style
    ))

    # Grid of screenshots (Steps 1, 2, 3, 4)
    s1 = os.path.join(SCREENSHOTS_DIR, "step1_coordinator_init.png")
    s2 = os.path.join(SCREENSHOTS_DIR, "step2_retriever_filtering.png")
    s3 = os.path.join(SCREENSHOTS_DIR, "step3_categorizer_memory_llm.png")
    s4 = os.path.join(SCREENSHOTS_DIR, "step4_auditor_feedback_loop.png")

    img_w, img_h = 8.2 * cm, 4.6 * cm
    grid_data = [
        [Image(s1, width=img_w, height=img_h), Image(s2, width=img_w, height=img_h)],
        [Paragraph("<b>Step 1:</b> Coordinator decomposition & dynamic intent parsing.", body_style), Paragraph("<b>Step 2:</b> Retriever calendar boundary ingestion.", body_style)],
        [Image(s3, width=img_w, height=img_h), Image(s4, width=img_w, height=img_h)],
        [Paragraph("<b>Step 3:</b> Categorizer vector memory lookup (12 hits).", body_style), Paragraph("<b>Step 4:</b> Auditor feedback loop resolving missing data.", body_style)],
    ]
    s_table = Table(grid_data, colWidths=[8.5 * cm, 8.5 * cm])
    s_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(s_table)

    story.append(Spacer(1, 4))
    story.append(Paragraph("Key Trace Verification Notes:", h2_style))
    story.append(Paragraph(
        "• <b>Memory Precedence:</b> In Step 3, vendors like <i>'The Capital Grille'</i> and <i>'Olive Garden'</i> matched stored user corrections, immediately categorizing them as <b>Meals</b> without calling the LLM.<br/>"
        "• <b>Automated Anomaly Audit:</b> In Step 4, <i>'Delta Airlines'</i> was flagged as a high-value transaction (Rs. 1,250.00 >= Rs. 1,000.00 threshold), alerting the human operator.",
        body_style
    ))
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 9: FAULT TOLERANCE, CRASH RECOVERY & HISTORICAL ARCHIVE
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("12. Fault Tolerance, Crash Recovery & Historical Archival", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=color_secondary, spaceAfter=8))
    story.append(Paragraph(
        "During preliminary evaluations, the jury raised three critical architectural questions regarding resilience and usability: "
        "<i>(1) What happens if the server crashes at Step 3? (2) Why must users regenerate reports to view past outputs? (3) Can the agent adapt to different prompts?</i> "
        "The implementations below directly answer and solve these requirements.",
        body_style
    ))

    s5 = os.path.join(SCREENSHOTS_DIR, "step5_reporter_approval_gate.png")
    s6 = os.path.join(SCREENSHOTS_DIR, "step6_crash_simulation_recovery.png")
    s7 = os.path.join(SCREENSHOTS_DIR, "step7_past_reports_archive.png")
    s8 = os.path.join(SCREENSHOTS_DIR, "step8_pytest_test_results.png")

    grid_data_2 = [
        [Image(s5, width=img_w, height=img_h), Image(s6, width=img_w, height=img_h)],
        [Paragraph("<b>Step 5:</b> Reporter sign-off gate & PDF publishing.", body_style), Paragraph("<b>Step 6:</b> Crash simulation at Step 3 & SQLite resume.", body_style)],
        [Image(s7, width=img_w, height=img_h), Image(s8, width=img_w, height=img_h)],
        [Paragraph("<b>Step 7:</b> Timestamped past reports archive & selector.", body_style), Paragraph("<b>Step 8:</b> Automated test suite (100% passing).", body_style)],
    ]
    s_table_2 = Table(grid_data_2, colWidths=[8.5 * cm, 8.5 * cm])
    s_table_2.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(s_table_2)

    story.append(Spacer(1, 4))
    story.append(Paragraph("Technical Solution Breakdown:", h2_style))
    resilience_points = [
        ("Crash Recovery Verification", "Using `SqliteSaver`, every completed node commits blackboard state to `data/checkpoints.db`. When an intentional crash was simulated at Node 3, the resumed execution picked up at `('categorizer',)` without repeating Node 1 (Coordinator) or Node 2 (Retriever)."),
        ("Historical Report Archival", "Generated PDFs are automatically copied to `reports/expense_report_YYYYMMDD_HHMMSS.pdf` with companion JSON metadata. In the Streamlit UI, users browse and download past reports instantly."),
        ("Dynamic Prompt Flexibility", "The dynamic intent parser extracts custom email targets (e.g., `audit@firm.com`), date scopes (*all expenses*), and category filters (*only meals*) directly from prompt text.")
    ]
    for r_title, r_desc in resilience_points:
        story.append(Paragraph(f"• <b>{r_title}:</b> {r_desc}", body_style))

    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 10: INDIVIDUAL CONTRIBUTIONS, TEST SUITE & CONCLUSION
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("13. Individual Member Contributions (Group 4)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=color_secondary, spaceAfter=8))
    story.append(Paragraph(
        "Each team member owned distinct technical deliverables across Units 3, 4, and Phase 4 enhancements:",
        body_style
    ))

    contrib_data = [
        ["Member Name", "Role & Subsystem Ownership", "Specific Measurable Technical Deliverables"],
        [
            "Dhiraj Sarawale\n(Lead)",
            "System Architecture, LangGraph DAG & Fault Tolerance",
            "• Built LangGraph StateGraph engine & typed blackboard state.\n"
            "• Implemented SQLite checkpoint recovery (SqliteSaver) for crash resilience.\n"
            "• Developed Dynamic Prompt & Intent Extraction parser.\n"
            "• Built interactive Streamlit observability dashboard & crash demo controls."
        ],
        [
            "Aryan Maradwar",
            "Unit 3 Long-Term Vector Memory & Ingestion",
            "• Integrated ChromaDB persistent vector database with BGE embeddings.\n"
            "• Implemented cosine similarity threshold matching (>= 0.85).\n"
            "• Implemented user correction persistence (--correct 'Olive Garden=Meals').\n"
            "• Managed dataset generation script (seed.py) and CSV date validations."
        ],
        [
            "Asta Joseph",
            "Unit 4 Role-Based Multi-Agent Architecture",
            "• Engineered 5 role agents: Coordinator, Retriever, Categorizer, Auditor, Reporter.\n"
            "• Implemented IEEE FIPA-ACL structured messaging protocol.\n"
            "• Developed agent execution trace logging for live viva inspection.\n"
            "• Co-authored pytest integration suite (tests/test_agent.py)."
        ],
        [
            "Ridhima Maliya",
            "Unit 3 Feedback Loops & Unit 4 Governance",
            "• Engineered 4-stage missing-data feedback loop (Act-Observe-Reflect-Adjust).\n"
            "• Built Adjustable Autonomy Human Approval Gate with approve/reject branch.\n"
            "• Engineered ReportLab PDF publishing engine with styled tables & exception appendix.\n"
            "• Configured RFC 822 EML message archival system."
        ],
    ]
    contrib_table = Table(contrib_data, colWidths=[3.2 * cm, 4.8 * cm, 9.0 * cm])
    contrib_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), color_primary),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(contrib_table)

    story.append(Spacer(1, 8))
    story.append(Paragraph("14. Automated Test Verification & Final Conclusion", h2_style))
    story.append(Paragraph(
        "<b>Test Suite Verification:</b> The test suite in `tests/test_agent.py` was executed via `pytest -p no:asyncio -v tests/test_agent.py`. All 4 core test modules passed with <b>100% success rate</b> (test_tools_deterministic_math, test_chromadb_memory_store_priority, test_feedback_loop_act_observe_adjust, and test_langgraph_sqlite_checkpoint_resume).<br/><br/>"
        "<b>Final Jury Conclusion:</b> The Autonomous Expense Report Agent demonstrates that reliable enterprise AI requires structured agentic engineering rather than blind prompt chaining. By anchoring an LLM within an explicit LangGraph DAG, backing decisions with persistent vector memory, enforcing deterministic math, protecting external actions with a human approval gate, and guaranteeing crash recovery via SQLite checkpoints, Group 4 has delivered a verifiable, production-aligned solution ready for enterprise deployment.",
        body_style
    ))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"✔ 10-Page Project Report generated successfully: {PDF_OUTPUT}")

if __name__ == "__main__":
    build_pdf()

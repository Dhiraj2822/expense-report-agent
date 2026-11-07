"""
streamlit_app.py
────────────────
Streamlit Web UI for Expense Report Agent.
Course Concept: Interactive Multi-Agent Observability, Fault Tolerance,
Checkpoint Recovery & Human-in-the-Loop Gate.

Group 4: Aryan Maradwar · Asta Joseph · Dhiraj Sarawale · Ridhima Maliya

Usage:
  streamlit run streamlit_app.py
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
import streamlit as st

# Configure page
st.set_page_config(
    page_title="Expense Report Agent | Group 4",
    page_icon="💼",
    layout="wide",
)

st.title("💼 Expense Report Agent — AIA_7 Group 4")
st.caption("Autonomous Agentic Pipeline · LangGraph Checkpointing · ChromaDB · FIPA-ACL · Fault Tolerant")

# ─────────────────────────────────────────────────────────────────────────────
# Sidebar: Agent Configuration & Viva Demo Tools
# ─────────────────────────────────────────────────────────────────────────────
st.sidebar.header("⚙️ Agent Configuration")
run_mode = st.sidebar.selectbox("Pipeline Mode", ["extended", "base"], index=0)
auto_approve = st.sidebar.checkbox("Auto-Approve Human Gate", value=True)
answers_choice = st.sidebar.selectbox("Scripted Answers", ["data/answers.json", "None"], index=0)
answers_path = None if answers_choice == "None" else answers_choice

# Fault Tolerance & Crash Demo
st.sidebar.markdown("---")
st.sidebar.subheader("💥 Server Crash & Recovery Demo")
st.sidebar.caption("Simulate a server crash at any node to verify checkpoint persistence & resume.")
crash_stage_choice = st.sidebar.selectbox(
    "Simulate Server Crash At:",
    ["None", "coordinator (Step 1)", "retriever (Step 2)", "categorizer (Step 3)", "auditor (Step 4)", "reporter (Step 5)"],
    index=0,
)
simulate_crash_node = None
if crash_stage_choice != "None":
    simulate_crash_node = crash_stage_choice.split(" ")[0]

session_thread_id = st.sidebar.text_input("Session / Thread ID (SQLite)", value="demo_session_1")

# Past Reports Archive
st.sidebar.markdown("---")
st.sidebar.subheader("📂 Past Generated Reports")
reports_dir = Path(__file__).parent / "reports"
reports_dir.mkdir(parents=True, exist_ok=True)

# Also ensure root expense_report.pdf is archived if reports_dir is empty
root_pdf = Path(__file__).parent / "expense_report.pdf"
if root_pdf.exists() and not list(reports_dir.glob("*.pdf")):
    import shutil
    shutil.copy2(root_pdf, reports_dir / f"expense_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")

archived_pdfs = sorted(list(reports_dir.glob("*.pdf")), reverse=True)
if archived_pdfs:
    report_names = [p.name for p in archived_pdfs]
    selected_report_name = st.sidebar.selectbox("Select Archived Report", report_names)
    selected_pdf_path = reports_dir / selected_report_name
    
    # Check if companion json exists
    meta_path = selected_pdf_path.with_suffix(".json")
    if meta_path.exists():
        with open(meta_path, "r", encoding="utf-8") as jf:
            meta_data = json.load(jf)
            st.sidebar.caption(
                f"📅 Generated: {meta_data.get('generated_at', 'N/A')}\n\n"
                f"💰 Total: ₹{meta_data.get('grand_total', 0):,.2f} | Rows: {meta_data.get('num_items', '?')}"
            )

    with open(selected_pdf_path, "rb") as f:
        st.sidebar.download_button(
            label=f"📥 Download {selected_report_name}",
            data=f.read(),
            file_name=selected_report_name,
            mime="application/pdf",
        )
else:
    st.sidebar.caption("No archived reports yet. Run the agent to generate reports.")

# Long-term Memory Correction
st.sidebar.markdown("---")
st.sidebar.subheader("🧠 Long-Term Memory Correction")
corr_vendor = st.sidebar.text_input("Merchant Vendor", value="Olive Garden")
corr_cat = st.sidebar.selectbox("Correct Category", ["Meals", "Hotels", "Flights", "Transport", "Misc"], index=0)
if st.sidebar.button("Save Correction to ChromaDB"):
    from unit3_memory.memory_store import ExpenseMemoryStore
    ms = ExpenseMemoryStore()
    ms.add_user_correction(vendor=corr_vendor, category=corr_cat, description=f"Human correction via UI")
    st.sidebar.success(f"✔ Saved: '{corr_vendor}' -> '{corr_cat}' (source=user_correction)")

# ─────────────────────────────────────────────────────────────────────────────
# Main Page: Prompt Input & Dynamic Intent Presets
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("### 💬 User Instruction & Dynamic Intent")
st.caption("The agent parses your instruction dynamically: detects recipients, date ranges, and category filters.")

# Quick Preset Buttons
col_p1, col_p2, col_p3, col_p4 = st.columns(4)
preset_selected = None
if col_p1.button("📌 Default Prompt"):
    preset_selected = "Generate my travel expense report for last month and email it to finance."
if col_p2.button("✉️ Custom Recipient"):
    preset_selected = "Generate travel expense report for last month and email to internal-audit@enterprise.org"
if col_p3.button("🍽️ Filter Meals Only"):
    preset_selected = "Generate travel report for only Meals expenses for last month and email to finance."
if col_p4.button("🌐 All Expenses"):
    preset_selected = "Generate expense report for all expenses in the file and email to finance."

if preset_selected:
    st.session_state["instruction_input"] = preset_selected

default_instruction = st.session_state.get(
    "instruction_input",
    "Generate my travel expense report for last month and email it to finance.",
)

instruction = st.text_input("User Instruction", value=default_instruction)

# ─────────────────────────────────────────────────────────────────────────────
# Action Buttons: Execute vs Resume
# ─────────────────────────────────────────────────────────────────────────────
col_btn1, col_btn2 = st.columns([1, 1])

with col_btn1:
    btn_execute = st.button("🚀 Execute Agent Pipeline", type="primary", use_container_width=True)

with col_btn2:
    btn_resume = st.button("🔄 Resume Interrupted Checkpoint", type="secondary", use_container_width=True)

# ── Execute Agent Pipeline ──────────────────────────────────────────────────
if btn_execute:
    with st.spinner("Agent pipeline executing..."):
        from llm_config import get_llm
        _, llm_label = get_llm()
        csv_path = str(Path(__file__).parent / "data" / "mock_expenses.csv")
        config = {"configurable": {"thread_id": session_thread_id}}

        if run_mode == "extended":
            from unit3_memory.extended_main import build_extended_graph
            app = build_extended_graph(use_checkpointer=True)
            initial_state = {
                "instruction": instruction,
                "csv_path": csv_path,
                "mode": "extended",
                "llm_label": llm_label,
                "auto_approve": auto_approve,
                "answers_file": answers_path,
                "step_log": [],
                "message_log": [],
                "retry_count": 0,
                "simulate_crash_at": simulate_crash_node,
            }
            try:
                final_state = app.invoke(initial_state, config=config)
                st.session_state["final_state"] = final_state
                st.session_state.pop("crash_info", None)
            except RuntimeError as crash_err:
                st.session_state["crash_info"] = {
                    "error": str(crash_err),
                    "stage": simulate_crash_node,
                    "thread_id": session_thread_id,
                }
                st.session_state.pop("final_state", None)
        else:
            from main import build_graph
            app = build_graph()
            initial_state = {
                "instruction": instruction,
                "csv_path": csv_path,
                "mode": "base",
                "llm_label": llm_label,
                "step_log": [],
            }
            final_state = app.invoke(initial_state)
            st.session_state["final_state"] = final_state
            st.session_state.pop("crash_info", None)

# ── Resume Interrupted Checkpoint ───────────────────────────────────────────
if btn_resume:
    with st.spinner("Resuming execution from SQLite checkpoint..."):
        from unit3_memory.extended_main import build_extended_graph
        app = build_extended_graph(use_checkpointer=True)
        config = {"configurable": {"thread_id": session_thread_id}}

        state_tuple = app.get_state(config)
        if state_tuple and state_tuple.next:
            st.info(f"Resuming session `{session_thread_id}` from checkpoint. Next pending node: `{state_tuple.next}`")
            # Clear crash simulation so execution can finish cleanly
            app.update_state(config, {"simulate_crash_at": None})
            try:
                resumed_state = app.invoke(None, config=config)
                st.session_state["final_state"] = resumed_state
                st.session_state.pop("crash_info", None)
                st.success("✔ Checkpoint successfully resumed to completion!")
            except Exception as e:
                st.error(f"Error resuming checkpoint: {e}")
        else:
            st.warning(f"No pending interrupted checkpoint found for thread ID `{session_thread_id}`.")

# ─────────────────────────────────────────────────────────────────────────────
# Crash Alert Display
# ─────────────────────────────────────────────────────────────────────────────
if "crash_info" in st.session_state:
    crash_info = st.session_state["crash_info"]
    st.error(
        f"💥 **SERVER CRASH TRIGGERED!**\n\n"
        f"**Node/Stage:** `{crash_info['stage']}`\n\n"
        f"**Error Details:** `{crash_info['error']}`\n\n"
        f"**Fault Tolerance Status:** All prior steps are safely persisted in SQLite (`data/checkpoints.db`) under session `{crash_info['thread_id']}`. "
        f"Click **'🔄 Resume Interrupted Checkpoint'** above to resume immediately without starting over from Step 1!"
    )

# ─────────────────────────────────────────────────────────────────────────────
# Display Results if Available
# ─────────────────────────────────────────────────────────────────────────────
if "final_state" in st.session_state:
    state = st.session_state["final_state"]
    totals = state.get("totals", {})
    grand_total = totals.get("grand_total", 0.0)
    cat_totals = totals.get("category_totals", {})
    exceptions = state.get("exceptions", [])
    msg_log = state.get("message_log", [])
    pdf_path = state.get("pdf_path")
    email_body = state.get("email_body", "")
    parsed_intent = state.get("parsed_intent", {})

    # Top KPI Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Grand Total", f"₹{grand_total:,.2f}")
    c2.metric("Period", f"{state.get('date_range', ('?','?'))[0]} to {state.get('date_range', ('?','?'))[1]}")
    c3.metric("Exceptions / Flagged", len(exceptions))
    c4.metric("ACL Messages", len(msg_log))

    # Tabs for detailed views
    tab_summary, tab_blackboard, tab_messages, tab_pdf, tab_email, tab_checkpoints = st.tabs([
        "📊 Financial Breakdown",
        "📋 Shared Blackboard",
        "💬 Multi-Agent ACL Log",
        "📄 Generated PDF Report",
        "✉️ Drafted Email",
        "💾 Checkpoint State",
    ])

    with tab_summary:
        st.subheader("Category Totals (Deterministic)")
        cols = st.columns(len(cat_totals) if cat_totals else 1)
        for col, (cat, amt) in zip(cols, sorted(cat_totals.items())):
            col.metric(cat, f"₹{amt:,.2f}")

        if exceptions:
            st.warning(f"⚠️ {len(exceptions)} item(s) flagged for manual audit:")
            st.table(exceptions)

    with tab_blackboard:
        st.subheader("Shared Blackboard State Snapshot")
        st.json({
            "workflow_status": state.get("workflow_status", "completed"),
            "target_recipient": state.get("recipient", "finance@yourcompany.com"),
            "parsed_intent": parsed_intent,
            "raw_expenses_count": len(state.get("raw_expenses", [])),
            "filtered_expenses_count": len(state.get("filtered_expenses", [])),
            "categorized_expenses_count": len(state.get("categorized_expenses", [])),
            "grand_total": grand_total,
            "step_log": state.get("step_log", []),
        })

    with tab_messages:
        st.subheader("FIPA-ACL Multi-Agent Communication Transcript")
        if msg_log:
            for i, m in enumerate(msg_log, 1):
                st.markdown(
                    f"**{i:02d}. `[{m.get('performative','').upper()}]`** "
                    f"**{m.get('sender','')}** ➡️ **{m.get('receiver','')}**: "
                    f"{m.get('content','')}"
                )
        else:
            st.info("No ACL messages recorded (Base pipeline runs sequentially without multi-agent messaging).")

    with tab_pdf:
        st.subheader("ReportLab PDF Artifact")
        if pdf_path and Path(pdf_path).exists():
            st.success(f"✔ PDF generated: `{pdf_path}`")
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="⬇️ Download expense_report.pdf",
                    data=f.read(),
                    file_name="expense_report.pdf",
                    mime="application/pdf",
                )
        else:
            st.info("PDF has not been generated yet.")

    with tab_email:
        st.subheader(f"Email Content (Target: {state.get('recipient', 'finance@yourcompany.com')})")
        st.text_area("Email Body", value=email_body, height=250)
        eml_path = state.get("eml_path")
        if eml_path and Path(eml_path).exists():
            st.success(f"✔ RFC 822 EML File archived: `{eml_path}`")

    with tab_checkpoints:
        st.subheader("LangGraph SQLite Checkpoint Status")
        st.write(f"**Session Thread ID:** `{session_thread_id}`")
        st.write(f"**Storage Path:** `data/checkpoints.db`")
        from unit3_memory.extended_main import build_extended_graph
        app = build_extended_graph(use_checkpointer=True)
        st_state = app.get_state({"configurable": {"thread_id": session_thread_id}})
        if st_state:
            st.json({
                "thread_id": session_thread_id,
                "next_pending_node": list(st_state.next),
                "saved_step_log": st_state.values.get("step_log", []),
                "checkpoint_workflow_status": st_state.values.get("workflow_status", "unknown"),
            })

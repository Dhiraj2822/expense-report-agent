"""
streamlit_app.py
────────────────
Streamlit Web UI for Expense Report Agent.
Course Concept: Interactive Multi-Agent Observability, Fault Tolerance,
Checkpoint Recovery & Human-in-the-Loop Gate.

Usage:
  streamlit run streamlit_app.py
"""

import json
import os
from html import escape
from pathlib import Path
from datetime import datetime
from time import perf_counter
from typing import Any
from uuid import uuid4
import streamlit as st
from ui.progress import (
    WORKFLOW_LABELS,
    advance_workflow_progress,
    completed_workflow_progress,
    crashed_workflow_progress,
    mark_active_step_failed,
    new_workflow_progress,
    start_workflow_progress,
)
from ui.styles import hero, load_css, metric_card, pipeline_stepper

# Configure page
st.set_page_config(
    page_title="Expense Report Agent",
    page_icon="◈",
    layout="wide",
)

load_css()
hero()

with st.container(border=True):
    st.markdown("### Upload your expense data")
    st.caption(
        "Drop in a CSV or PDF statement here, or leave this empty and choose a sample dataset "
        "from the sidebar. An uploaded file takes priority until you remove it."
    )
    uploaded_file = st.file_uploader(
        "Choose a CSV or PDF statement",
        type=["csv", "pdf"],
        help="Supported formats: CSV spreadsheets and PDF expense statements.",
    )


def render_workflow_progress(
    progress: dict[str, str],
    stepper_slot: Any,
    progress_slot: Any,
    started_at: float | None = None,
) -> None:
    steps = [(label, progress[label]) for label in WORKFLOW_LABELS]
    with stepper_slot.container():
        st.markdown('<div class="section-eyebrow">Report progress</div>', unsafe_allow_html=True)
        pipeline_stepper(steps)

    completed = sum(status == "done" for status in progress.values())
    with progress_slot.container():
        st.progress(
            completed / len(WORKFLOW_LABELS),
            text=f"{completed} of {len(WORKFLOW_LABELS)} stages complete",
        )
        if started_at is not None:
            elapsed = perf_counter() - started_at
            active = next((label for label, status in progress.items() if status == "running"), None)
            failed = any(status == "failed" for status in progress.values())
            terminal = all(status in {"done", "failed"} for status in progress.values())
            description = (
                f"Running: {active}"
                if active
                else (
                    "Workflow completed with failures"
                    if failed and terminal
                    else "Workflow interrupted" if failed else "Workflow complete"
                )
            )
            st.caption(f"{description} · {elapsed:.1f}s elapsed")


def stream_graph_with_progress(
    app: Any,
    graph_input: Any,
    run_mode: str,
    config: dict | None,
    initial_state: dict,
    progress: dict[str, str],
    stepper_slot: Any,
    progress_slot: Any,
    started_at: float,
) -> dict:
    final_state = dict(initial_state)
    stream_kwargs: dict[str, Any] = {"stream_mode": "updates"}
    if config is not None:
        stream_kwargs["config"] = config

    received_update = False
    for event in app.stream(graph_input, **stream_kwargs):
        if not isinstance(event, dict):
            raise TypeError(f"Expected a LangGraph update mapping, received {type(event).__name__}.")
        for node_name, update in event.items():
            if not isinstance(update, dict):
                raise TypeError(f"Expected a state mapping from node {node_name!r}.")
            received_update = True
            final_state.update(update)
            advance_workflow_progress(run_mode, node_name, progress, update)
            render_workflow_progress(progress, stepper_slot, progress_slot, started_at)

    if not received_update:
        raise RuntimeError("The agent graph completed without producing any node updates.")
    return final_state


# ─────────────────────────────────────────────────────────────────────────────
# Sidebar: Agent Configuration & Viva Demo Tools
# ─────────────────────────────────────────────────────────────────────────────
st.sidebar.markdown(
    '<div class="sidebar-brand"><span class="brand-mark">◈</span>'
    '<span>Expense Report Agent<br><small style="color:#95A3BA;font:500 .68rem Inter,sans-serif">Expense workspace</small></span></div>',
    unsafe_allow_html=True,
)
st.sidebar.markdown('<div class="section-eyebrow">Configuration</div>', unsafe_allow_html=True)
st.sidebar.header("Agent Configuration")
auto_approve = st.sidebar.checkbox("Auto-Approve Human Gate", value=True)
answers_choice = st.sidebar.selectbox("Scripted Answers", ["data/answers.json", "None"], index=0)
answers_path = None if answers_choice == "None" else answers_choice

with st.sidebar.expander("Advanced workflow settings", expanded=False):
    run_mode = st.selectbox("Pipeline Mode", ["extended", "base"], index=0)
    crash_stage_choice = st.selectbox(
        "Simulate Server Crash At:",
        ["None", "coordinator (Step 1)", "retriever (Step 2)", "categorizer (Step 3)", "auditor (Step 4)", "reporter (Step 5)"],
        index=0,
    )
    simulate_crash_node = None
    if crash_stage_choice != "None":
        simulate_crash_node = crash_stage_choice.split(" ")[0]

    thread_id_default = st.query_params.get("thread_id") or f"session_{uuid4().hex[:12]}"
    session_thread_id = st.text_input(
        "Session / Thread ID (SQLite)",
        value=thread_id_default,
        help="Use the same run ID to reopen a saved workflow.",
    )
    if st.query_params.get("thread_id") != session_thread_id:
        st.query_params["thread_id"] = session_thread_id
    btn_resume = st.button("Resume saved run", type="secondary", use_container_width=True)

# Dataset Selection & File Ingestion (CSV / PDF)
st.sidebar.markdown("---")
st.sidebar.markdown('<div class="section-eyebrow">Dataset</div>', unsafe_allow_html=True)
st.sidebar.subheader("Choose a dataset")
dataset_choice = st.sidebar.selectbox(
    "Sample dataset",
    [
        "Corporate travel (September CSV)",
        "Cloud summit (October CSV)",
        "Expense statement (October PDF)",
    ],
    index=0,
    help="Choose one of the included examples. Upload your own CSV or PDF in the main panel above.",
)

active_dataset_path = None
if dataset_choice.startswith("Corporate travel"):
    active_dataset_path = str(Path(__file__).parent / "data" / "mock_expenses.csv")
elif dataset_choice.startswith("Cloud summit"):
    active_dataset_path = str(Path(__file__).parent / "data" / "october_expenses.csv")
elif dataset_choice.startswith("Expense statement"):
    active_dataset_path = str(Path(__file__).parent / "data" / "sample_expense_statement.pdf")
if uploaded_file is not None:
    uploads_dir = Path(__file__).parent / "data" / "uploads"
    uploads_dir.mkdir(parents=True, exist_ok=True)
    saved_upload_path = uploads_dir / uploaded_file.name
    with open(saved_upload_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    active_dataset_path = str(saved_upload_path)
    st.sidebar.success(f"Uploaded file active: `{uploaded_file.name}`")

# Past Reports Archive
st.sidebar.markdown("---")
st.sidebar.markdown('<div class="section-eyebrow">Report archive</div>', unsafe_allow_html=True)
st.sidebar.subheader("Past Generated Reports")
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
                f"Generated: {meta_data.get('generated_at', 'N/A')}\n\n"
                f"Total: ₹{meta_data.get('grand_total', 0):,.2f} | Rows: {meta_data.get('num_items', '?')}"
            )

    with open(selected_pdf_path, "rb") as f:
        st.sidebar.download_button(
            label=f"Download {selected_report_name}",
            data=f.read(),
            file_name=selected_report_name,
            mime="application/pdf",
        )
else:
    st.sidebar.caption("No archived reports yet. Run the agent to generate reports.")

# Long-term Memory Correction
st.sidebar.markdown("---")
st.sidebar.markdown('<div class="section-eyebrow">Memory</div>', unsafe_allow_html=True)
with st.sidebar.expander("Correct a merchant category", expanded=False):
    corr_vendor = st.text_input("Merchant", value="Olive Garden")
    corr_cat = st.selectbox("Category", ["Meals", "Hotels", "Flights", "Transport", "Misc"], index=0)
    if st.button("Save category correction"):
        from unit3_memory.memory_store import ExpenseMemoryStore
        ms = ExpenseMemoryStore()
        ms.add_user_correction(vendor=corr_vendor, category=corr_cat, description="Human correction via UI")
        st.success(f"Saved: {corr_vendor} → {corr_cat}")

# ─────────────────────────────────────────────────────────────────────────────
# Main Page: Prompt Input & Dynamic Intent Presets
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("## Create a report")
st.caption("Choose a starting point or describe the report you need.")

# Quick Preset Buttons
col_p1, col_p2, col_p3, col_p4 = st.columns(4)
preset_selected = None
if col_p1.button("Monthly travel"):
    preset_selected = "Generate my travel expense report for last month and email it to finance."
col_p1.markdown('<div class="preset-copy">Travel expenses from last month.</div>', unsafe_allow_html=True)
if col_p2.button("Custom recipient"):
    preset_selected = "Generate travel expense report for last month and email to internal-audit@enterprise.org"
col_p2.markdown('<div class="preset-copy">Route a copy to an audit contact.</div>', unsafe_allow_html=True)
if col_p3.button("Meals only"):
    preset_selected = "Generate travel report for only Meals expenses for last month and email to finance."
col_p3.markdown('<div class="preset-copy">Narrow the report to meal expenses.</div>', unsafe_allow_html=True)
if col_p4.button("All expenses"):
    preset_selected = "Generate expense report for all expenses in the file and email to finance."
col_p4.markdown('<div class="preset-copy">Include every record in the selected file.</div>', unsafe_allow_html=True)

if preset_selected:
    st.session_state["instruction_input"] = preset_selected

default_instruction = st.session_state.get(
    "instruction_input",
    "Generate my travel expense report for last month and email it to finance.",
)
st.markdown('<div class="section-eyebrow">Report request</div>', unsafe_allow_html=True)
instruction = st.text_input(
    "Report instruction",
    value=default_instruction,
    placeholder="For example: meals from last month, sent to finance",
)

# ── Dataset Inspection Preview ───────────────────────────────────────────────
from tools import retrieve_expenses
preview_items = []
try:
    preview_items = retrieve_expenses(active_dataset_path)
    file_type = "PDF Statement" if active_dataset_path.lower().endswith(".pdf") else "CSV Spreadsheet"
    with st.expander(
        f"Dataset preview · {Path(active_dataset_path).name} ({len(preview_items)} records | {file_type})",
        expanded=False,
    ):
        import pandas as pd
        df_preview = pd.DataFrame(preview_items)
        if "amount" in df_preview.columns:
            amount_values = (
                df_preview["amount"]
                .astype(str)
                .str.replace(r"[₹$€£,\s]", "", regex=True)
            )
            df_preview["amount"] = pd.to_numeric(amount_values, errors="coerce")
        preview_format = {"amount": "₹{:,.2f}"} if "amount" in df_preview.columns else {}
        preview_styler = df_preview.style.format(preview_format, na_rep="—")
        if "category" in df_preview.columns:
            category_colors = {
                "Flights": "color:#93C5FD;font-weight:600",
                "Hotels": "color:#C4B5FD;font-weight:600",
                "Meals": "color:#FCD34D;font-weight:600",
                "Transport": "color:#67E8F9;font-weight:600",
                "Misc": "color:#A7F3D0;font-weight:600",
            }
            preview_styler = preview_styler.map(
                lambda value: category_colors.get(value, "color:#94A3B8"),
                subset=["category"],
            )
        st.dataframe(preview_styler, use_container_width=True)
        st.caption(f"Source file: {Path(active_dataset_path).name}")
except Exception as e:
    st.info(f"Dataset preview ready upon file selection: {e}")

metric_columns = st.columns(2, gap="medium")
with metric_columns[0]:
    metric_card("Records loaded", str(len(preview_items)), "database", Path(active_dataset_path).name)
with metric_columns[1]:
    metric_card("Human gate", "Auto-approved" if auto_approve else "Approval required", "verified_user", "Approval setting")

# ─────────────────────────────────────────────────────────────────────────────
# Generate report
# ─────────────────────────────────────────────────────────────────────────────
btn_execute = st.button("Generate report", type="primary", use_container_width=True)

if "final_state" in st.session_state:
    workflow_progress = completed_workflow_progress(
        st.session_state["final_state"].get("email_result")
    )
elif "crash_info" in st.session_state:
    workflow_progress = crashed_workflow_progress(
        run_mode, st.session_state["crash_info"].get("stage")
    )
else:
    workflow_progress = new_workflow_progress()

stepper_slot = st.empty()
progress_slot = st.empty()
action_started_at = perf_counter() if btn_execute or btn_resume else None
render_workflow_progress(
    workflow_progress, stepper_slot, progress_slot, action_started_at
)

# ── Execute workflow ────────────────────────────────────────────────────────
if btn_execute:
    workflow_progress = new_workflow_progress()
    with st.spinner("Generating your report..."):
        csv_path = active_dataset_path

        if run_mode == "extended":
            workflow_progress = start_workflow_progress(run_mode)
            render_workflow_progress(
                workflow_progress, stepper_slot, progress_slot, action_started_at
            )
            from unit3_memory.extended_main import build_extended_graph
            app = build_extended_graph(use_checkpointer=True)
            config = {"configurable": {"thread_id": session_thread_id}}
            initial_state = {
                "instruction": instruction,
                "csv_path": csv_path,
                "mode": "extended",
                "llm_label": "Resolving during categorization",
                "auto_approve": auto_approve,
                "terminal_input": False,
                "answers_file": answers_path,
                "step_log": [],
                "message_log": [],
                "retry_count": 0,
                "simulate_crash_at": simulate_crash_node,
            }
            try:
                final_state = stream_graph_with_progress(
                    app,
                    initial_state,
                    run_mode,
                    config,
                    initial_state,
                    workflow_progress,
                    stepper_slot,
                    progress_slot,
                    action_started_at,
                )
                st.session_state["final_state"] = final_state
                st.session_state.pop("crash_info", None)
                workflow_progress = completed_workflow_progress(
                    final_state.get("email_result")
                )
                render_workflow_progress(
                    workflow_progress, stepper_slot, progress_slot, action_started_at
                )
                st.toast("Expense report generated successfully.", icon="✅")
            except RuntimeError as crash_err:
                st.session_state["crash_info"] = {
                    "error": str(crash_err),
                    "stage": simulate_crash_node,
                    "thread_id": session_thread_id,
                }
                st.session_state.pop("final_state", None)
                workflow_progress = crashed_workflow_progress(
                    run_mode, simulate_crash_node
                )
                if simulate_crash_node is None:
                    mark_active_step_failed(workflow_progress)
                render_workflow_progress(
                    workflow_progress, stepper_slot, progress_slot, action_started_at
                )
                st.toast("Pipeline stopped at the simulated crash point.", icon="⚠️")
        else:
            from llm_config import get_llm
            _, llm_label = get_llm()
            workflow_progress = start_workflow_progress(run_mode)
            render_workflow_progress(
                workflow_progress, stepper_slot, progress_slot, action_started_at
            )
            from main import build_graph
            app = build_graph()
            initial_state = {
                "instruction": instruction,
                "csv_path": csv_path,
                "mode": "base",
                "llm_label": llm_label,
                "step_log": [],
            }
            final_state = stream_graph_with_progress(
                app,
                initial_state,
                run_mode,
                None,
                initial_state,
                workflow_progress,
                stepper_slot,
                progress_slot,
                action_started_at,
            )
            st.session_state["final_state"] = final_state
            st.session_state.pop("crash_info", None)
            workflow_progress = completed_workflow_progress(
                final_state.get("email_result")
            )
            render_workflow_progress(
                workflow_progress, stepper_slot, progress_slot, action_started_at
            )
            st.toast("Expense report generated successfully.", icon="✅")

# ── Resume Interrupted Checkpoint ───────────────────────────────────────────
if btn_resume:
    if "crash_info" in st.session_state:
        workflow_progress = crashed_workflow_progress(
            "extended", st.session_state["crash_info"].get("stage")
        )
    else:
        workflow_progress = new_workflow_progress()
    render_workflow_progress(
        workflow_progress, stepper_slot, progress_slot, action_started_at
    )
    with st.spinner("Opening saved run..."):
        from unit3_memory.extended_main import build_extended_graph
        app = build_extended_graph(use_checkpointer=True)
        config = {"configurable": {"thread_id": session_thread_id}}

        state_tuple = app.get_state(config)
        if state_tuple and state_tuple.next:
            # Clear crash simulation so execution can finish cleanly
            app.update_state(
                config, {"simulate_crash_at": None, "terminal_input": False}
            )
            next_node = state_tuple.next[0]
            resume_labels = {
                "coordinator": "Parse Intent",
                "retriever": "Ingest",
                "categorizer": "Categorize",
                "auditor": "Validate",
                "reporter": "Generate Report",
                "confirm": "Email",
            }
            if next_node in resume_labels:
                workflow_progress[resume_labels[next_node]] = "running"
            render_workflow_progress(
                workflow_progress, stepper_slot, progress_slot, action_started_at
            )
            try:
                resumed_state = stream_graph_with_progress(
                    app,
                    None,
                    "extended",
                    config,
                    dict(state_tuple.values),
                    workflow_progress,
                    stepper_slot,
                    progress_slot,
                    action_started_at,
                )
                st.session_state["final_state"] = resumed_state
                st.session_state.pop("crash_info", None)
                workflow_progress = completed_workflow_progress(
                    resumed_state.get("email_result")
                )
                render_workflow_progress(
                    workflow_progress, stepper_slot, progress_slot, action_started_at
                )
                st.toast("Saved run completed.", icon="✅")
            except Exception as e:
                mark_active_step_failed(workflow_progress)
                render_workflow_progress(
                    workflow_progress, stepper_slot, progress_slot, action_started_at
                )
                st.toast("Checkpoint recovery failed.", icon="❌")
                st.error(f"Error resuming checkpoint: {e}")
        else:
            saved_values = dict(state_tuple.values) if state_tuple else {}
            if saved_values.get("workflow_status") == "completed":
                st.session_state["final_state"] = saved_values
                st.session_state.pop("crash_info", None)
                workflow_progress = completed_workflow_progress(
                    saved_values.get("email_result")
                )
                render_workflow_progress(
                    workflow_progress, stepper_slot, progress_slot, action_started_at
                )
                st.toast("Saved report restored.", icon="✅")
            else:
                st.info("No saved run is available to resume.")

render_workflow_progress(
    workflow_progress, stepper_slot, progress_slot, action_started_at
)

# ─────────────────────────────────────────────────────────────────────────────
# Run status
# ─────────────────────────────────────────────────────────────────────────────
if "crash_info" in st.session_state:
    st.warning("This run stopped before completion. Use Advanced workflow settings to resume it.")

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

    period = state.get("date_range", ("?", "?"))
    period_text = f"{period[0]} to {period[1]}" if len(period) >= 2 else "Period unavailable"
    result_metrics = st.columns(3, gap="medium")
    with result_metrics[0]:
        metric_card("Total spend", f"₹{grand_total:,.2f}", "payments", "Reconciled amount")
    with result_metrics[1]:
        metric_card("Reporting period", period_text, "calendar_month", "Filtered date range")
    with result_metrics[2]:
        metric_card("Items flagged", str(len(exceptions)), "fact_check", "Manual audit queue")
    tab_report, tab_logs, tab_messages, tab_checkpoints = st.tabs([
        "Report",
        "Activity",
        "Messages",
        "Run details",
    ])

    with tab_report:
        st.subheader("Spend overview")
        import pandas as pd

        if cat_totals:
            import plotly.express as px

            chart_data = pd.DataFrame(
                [{"Category": category, "Amount": amount} for category, amount in sorted(cat_totals.items())]
            )
            chart_colors = ["#818CF8", "#22D3EE", "#10B981", "#F59E0B", "#A78BFA", "#F472B6"]
            donut, bars = st.columns([1, 1], gap="large")
            with donut:
                pie = px.pie(
                    chart_data,
                    names="Category",
                    values="Amount",
                    hole=.66,
                    color_discrete_sequence=chart_colors,
                )
                pie.update_layout(
                    title="Category mix",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#DCE5F4",
                    legend_title_text="",
                    margin=dict(t=55, b=10, l=10, r=10),
                )
                st.plotly_chart(pie, use_container_width=True)
            with bars:
                bar = px.bar(
                    chart_data,
                    x="Category",
                    y="Amount",
                    color="Category",
                    color_discrete_sequence=chart_colors,
                )
                bar.update_layout(
                    title="Spend by category",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#DCE5F4",
                    showlegend=False,
                    margin=dict(t=55, b=10, l=10, r=10),
                    yaxis_title="Amount (₹)",
                )
                st.plotly_chart(bar, use_container_width=True)

            category_columns = st.columns(min(len(cat_totals), 5), gap="medium")
            for col, (category, amount) in zip(category_columns, sorted(cat_totals.items())):
                with col:
                    metric_card(category, f"₹{amount:,.2f}", "sell", "Category total")
        else:
            st.info("No categorized expenses are available for this report.")

        csv_frame = pd.DataFrame(state.get("categorized_expenses", []))
        st.markdown('<div class="section-eyebrow">Download your report</div>', unsafe_allow_html=True)
        download_columns = st.columns(2, gap="medium")
        with download_columns[0]:
            st.download_button(
                "Download expense data (CSV)",
                data=csv_frame.to_csv(index=False).encode("utf-8"),
                file_name="expense_report.csv",
                mime="text/csv",
                use_container_width=True,
            )
        with download_columns[1]:
            if pdf_path and Path(pdf_path).exists():
                with open(pdf_path, "rb") as report_file:
                    st.download_button(
                        "Download expense_report.pdf",
                        data=report_file.read(),
                        file_name="expense_report.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                    )
            else:
                st.info("PDF has not been generated yet.")

        email_result = state.get("email_result", {})
        email_status = email_result.get("status", "Not sent") if isinstance(email_result, dict) else str(email_result)
        st.markdown(
            f'<div class="glass-card"><strong>Email delivery</strong>'
            f'<div style="margin-top:.35rem;color:#AAB7CC">Status: {escape(str(email_status))} · '
            f'Recipient: {escape(str(state.get("recipient", "finance@yourcompany.com")))}</div></div>',
            unsafe_allow_html=True,
        )
        st.text_area("Email Body", value=email_body, height=180)
        eml_path = state.get("eml_path")
        if eml_path and Path(eml_path).exists():
            st.caption(f"RFC 822 email archive: `{eml_path}`")

        if exceptions:
            st.warning(f"{len(exceptions)} item(s) flagged for manual audit.")
            st.dataframe(pd.DataFrame(exceptions), use_container_width=True)

    with tab_logs:
        st.subheader("Report activity")
        step_log = state.get("step_log", [])
        if step_log:
            st.markdown(
                f'<div class="terminal">{escape(chr(10).join(str(entry) for entry in step_log))}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown('<div class="terminal">No detailed step log was emitted by this run.</div>', unsafe_allow_html=True)
        with st.expander("Shared Blackboard State Snapshot", expanded=False):
            st.json({
                "workflow_status": state.get("workflow_status", "completed"),
                "target_recipient": state.get("recipient", "finance@yourcompany.com"),
                "parsed_intent": parsed_intent,
                "raw_expenses_count": len(state.get("raw_expenses", [])),
                "filtered_expenses_count": len(state.get("filtered_expenses", [])),
                "categorized_expenses_count": len(state.get("categorized_expenses", [])),
                "grand_total": grand_total,
                "step_log": step_log,
            })

    with tab_messages:
        st.subheader("Messages")
        if msg_log:
            for i, message in enumerate(msg_log, 1):
                st.markdown(
                    f'<div class="glass-card" style="margin-bottom:.55rem">'
                    f'<span style="color:#A5B4FC;font-weight:700">{i:02d} · {escape(str(message.get("performative", "")).upper())}</span>'
                    f'<div style="margin-top:.3rem"><strong>{escape(str(message.get("sender", "")))}</strong> → '
                    f'<strong>{escape(str(message.get("receiver", "")))}</strong></div>'
                    f'<div style="color:#AAB7CC;margin-top:.3rem">{escape(str(message.get("content", "")))}</div></div>',
                    unsafe_allow_html=True,
                )
        else:
            st.info("No messages were recorded for this run.")

    with tab_checkpoints:
        st.subheader("Run details")
        st.write(f"**Run ID:** `{session_thread_id}`")
        if run_mode == "extended":
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
        else:
            st.info("Persistent SQLite checkpoints are enabled for the extended pipeline.")

"""Presentation state transitions for the visible agent workflow."""

WORKFLOW_LABELS = (
    "Ingest",
    "Parse Intent",
    "Categorize",
    "Validate",
    "Human Gate",
    "Generate Report",
    "Email",
)


def new_workflow_progress() -> dict[str, str]:
    return {label: "pending" for label in WORKFLOW_LABELS}


def start_workflow_progress(mode: str) -> dict[str, str]:
    progress = new_workflow_progress()
    progress["Parse Intent" if mode == "extended" else "Ingest"] = "running"
    return progress


def advance_workflow_progress(
    mode: str,
    node_name: str,
    progress: dict[str, str],
    update: dict | None = None,
) -> None:
    if mode == "extended":
        transitions = {
            "coordinator": (("Parse Intent",), ("Ingest",)),
            "retriever": (("Ingest",), ("Categorize",)),
            "categorizer": (("Categorize",), ("Validate",)),
            "auditor": (("Validate",), ("Generate Report",)),
        }
        if node_name in transitions:
            completed, running = transitions[node_name]
            for label in completed:
                progress[label] = "done"
            for label in running:
                progress[label] = "running"
        elif node_name == "reporter":
            progress["Generate Report"] = "done"
            progress["Human Gate"] = "done"
            email_result = (update or {}).get("email_result") or {}
            email_status = str(email_result.get("status", "")).lower()
            progress["Email"] = "failed" if email_status.startswith("failed") else "done"
        elif node_name == "confirm":
            for label in WORKFLOW_LABELS:
                if progress[label] == "pending":
                    progress[label] = "done"
    else:
        transitions = {
            "retrieve": (("Ingest",), ("Parse Intent",)),
            "filter": (("Parse Intent",), ("Categorize",)),
            "categorize": (("Categorize",), ("Validate",)),
            "handle_missing": (("Validate",), ("Human Gate",)),
            "calculate": (("Human Gate",), ("Generate Report",)),
            "generate_pdf": (("Generate Report",), ("Email",)),
        }
        if node_name in transitions:
            completed, running = transitions[node_name]
            for label in completed:
                progress[label] = "done"
            for label in running:
                progress[label] = "running"
        elif node_name == "send_email":
            email_result = (update or {}).get("email_result") or {}
            email_status = str(email_result.get("status", "")).lower()
            progress["Email"] = "failed" if email_status.startswith("failed") else "done"
        elif node_name == "confirm":
            for label in WORKFLOW_LABELS:
                if progress[label] == "pending":
                    progress[label] = "done"


def mark_active_step_failed(progress: dict[str, str]) -> None:
    for label in WORKFLOW_LABELS:
        if progress[label] == "running":
            progress[label] = "failed"
            return


def completed_workflow_progress(email_result: dict | None = None) -> dict[str, str]:
    progress = {label: "done" for label in WORKFLOW_LABELS}
    if str((email_result or {}).get("status", "")).lower().startswith("failed"):
        progress["Email"] = "failed"
    return progress


def crashed_workflow_progress(mode: str, stage: str | None) -> dict[str, str]:
    progress = new_workflow_progress()
    if mode == "extended":
        stage_steps = {
            "coordinator": ("Parse Intent",),
            "retriever": ("Parse Intent", "Ingest"),
            "categorizer": ("Parse Intent", "Ingest", "Categorize"),
            "auditor": ("Parse Intent", "Ingest", "Categorize", "Validate"),
            "reporter": ("Parse Intent", "Ingest", "Categorize", "Validate", "Human Gate", "Generate Report"),
        }
        completed_before = {
            "coordinator": (),
            "retriever": ("Parse Intent",),
            "categorizer": ("Parse Intent", "Ingest"),
            "auditor": ("Parse Intent", "Ingest", "Categorize"),
            "reporter": ("Parse Intent", "Ingest", "Categorize", "Validate", "Human Gate"),
        }
    else:
        stage_steps = {
            "retrieve": ("Ingest",),
            "filter": ("Ingest", "Parse Intent"),
            "categorize": ("Ingest", "Parse Intent", "Categorize"),
            "handle_missing": ("Ingest", "Parse Intent", "Categorize", "Validate"),
            "calculate": ("Ingest", "Parse Intent", "Categorize", "Validate", "Human Gate"),
            "generate_pdf": ("Ingest", "Parse Intent", "Categorize", "Validate", "Human Gate", "Generate Report"),
            "draft_email": ("Ingest", "Parse Intent", "Categorize", "Validate", "Human Gate", "Generate Report"),
            "send_email": ("Ingest", "Parse Intent", "Categorize", "Validate", "Human Gate", "Generate Report", "Email"),
        }
        completed_before = {
            "retrieve": (),
            "filter": ("Ingest",),
            "categorize": ("Ingest", "Parse Intent"),
            "handle_missing": ("Ingest", "Parse Intent", "Categorize"),
            "calculate": ("Ingest", "Parse Intent", "Categorize", "Validate"),
            "generate_pdf": ("Ingest", "Parse Intent", "Categorize", "Validate", "Human Gate"),
            "draft_email": ("Ingest", "Parse Intent", "Categorize", "Validate", "Human Gate", "Generate Report"),
            "send_email": ("Ingest", "Parse Intent", "Categorize", "Validate", "Human Gate", "Generate Report"),
        }

    failed_labels = stage_steps.get(stage or "", ())
    for label in completed_before.get(stage or "", ()):
        progress[label] = "done"
    if failed_labels:
        progress[failed_labels[-1]] = "failed"
    return progress

"""
tests/test_agent.py
───────────────────
Pytest test suite for Expense Report Agent.
Tests:
1. Date filtering with REPORT_TODAY override
2. Deterministic category & grand totals calculation
3. Missing-amount detection and feedback loop resolution
4. Long-term memory storage, cosine similarity retrieval, and LLM skipping
5. User correction priority over model predictions
"""

import os
import sys
from datetime import date
from pathlib import Path

# Add project root to path for reliable imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

from tools import (
    calculate_totals,
    filter_category_candidates,
    filter_expenses_by_category,
    filter_last_month,
    get_report_today,
    last_month_range,
    parse_prompt_instruction,
)
from unit3_memory.feedback_loop import FeedbackLoopManager
from unit3_memory.memory_store import ExpenseMemoryStore
from ui.progress import advance_workflow_progress, start_workflow_progress


def test_category_filter_keeps_candidates_for_inference_then_matches_exactly():
    rows = [
        {"vendor": "Cafe", "category": "Meals"},
        {"vendor": "Airline", "category": "Flights"},
        {"vendor": "Unclassified", "category": ""},
        {"vendor": "Unknown", "category": "Other"},
    ]

    candidates = filter_category_candidates(rows, "Meals")
    assert [row["vendor"] for row in candidates] == ["Cafe", "Unclassified", "Unknown"]
    assert [row["vendor"] for row in filter_expenses_by_category(candidates, "Meals")] == ["Cafe"]


@pytest.mark.parametrize(
    "instruction",
    [
        "Generate my travel expense report of meal only and email it to finance",
        "Generate my travel expense report of meals only and email it to finance",
        "Generate my travel expense report of meak only and email it to finance",
        "Generate my travel expense report for only meal expenses and email it to finance",
    ],
)
def test_prompt_parser_detects_singular_meal_only(instruction):
    assert parse_prompt_instruction(instruction)["category_filter"] == "Meals"


def test_extended_progress_advances_by_graph_node_and_reports_email_failure():
    progress = start_workflow_progress("extended")
    assert progress["Parse Intent"] == "running"

    advance_workflow_progress("extended", "coordinator", progress)
    assert progress["Parse Intent"] == "done"
    assert progress["Ingest"] == "running"

    advance_workflow_progress("extended", "retriever", progress)
    assert progress["Ingest"] == "done"
    assert progress["Categorize"] == "running"

    advance_workflow_progress("extended", "categorizer", progress)
    assert progress["Categorize"] == "done"
    assert progress["Validate"] == "running"

    advance_workflow_progress("extended", "auditor", progress)
    assert progress["Validate"] == "done"
    assert progress["Generate Report"] == "running"

    advance_workflow_progress(
        "extended",
        "reporter",
        progress,
        {"email_result": {"status": "failed — provider unavailable"}},
    )
    assert progress["Generate Report"] == "done"
    assert progress["Email"] == "failed"


def test_report_today_date_filtering(monkeypatch):
    """Test that REPORT_TODAY correctly sets reference date and last calendar month."""
    monkeypatch.setenv("REPORT_TODAY", "2026-10-15")
    today = get_report_today()
    assert today == date(2026, 10, 15)

    first, last = last_month_range()
    assert first == date(2026, 9, 1)
    assert last == date(2026, 9, 30)

    sample_rows = [
        {"date": "2026-09-10", "vendor": "Delta", "amount": "100.00"},
        {"date": "2026-08-31", "vendor": "Old Vendor", "amount": "50.00"},
        {"date": "2026-10-01", "vendor": "Future Vendor", "amount": "75.00"},
        {"date": "invalid-date", "vendor": "Bad Date", "amount": "20.00"},
    ]
    valid, exceptions = filter_last_month(sample_rows)
    assert len(valid) == 1
    assert valid[0]["vendor"] == "Delta"
    # Unparseable date is flagged as exception; out-of-range dates are filtered out
    assert len(exceptions) == 1
    assert "unparseable" in exceptions[0]["_flag"]


def test_calculate_totals():
    """Test deterministic calculation of category totals and grand total."""
    rows = [
        {"category": "Flights", "amount": "1250.00"},
        {"category": "Flights", "amount": "825.00"},
        {"category": "Meals", "amount": "45.50"},
        {"category": "Transport", "amount": "30.00"},
        {"category": "Hotels", "amount": ""},       # missing amount should be skipped
        {"category": "Hotels", "amount": "0.00"},     # zero should be skipped
        {"category": "Hotels", "amount": "300.00"},
    ]
    totals = calculate_totals(rows)
    cat_totals = totals["category_totals"]

    assert cat_totals["Flights"] == 2075.00
    assert cat_totals["Meals"] == 45.50
    assert cat_totals["Transport"] == 30.00
    assert cat_totals["Hotels"] == 300.00
    assert totals["grand_total"] == 2450.50


def test_feedback_loop_missing_amount_resolution(tmp_path):
    """Test that FeedbackLoopManager detects missing amounts and resolves them via answers dict."""
    import json
    answers_file = tmp_path / "test_answers.json"
    with open(answers_file, "w") as f:
        json.dump({"Lyft": 42.50}, f)

    manager = FeedbackLoopManager(answers_file=str(answers_file), max_retries=2)

    rows = [
        {"date": "2026-09-05", "vendor": "Lyft", "description": "Ride", "amount": ""},
        {"date": "2026-09-06", "vendor": "Unknown Parking", "description": "Parking", "amount": "0.00"},
    ]

    missing = manager.act_detect_missing(rows)
    assert len(missing) == 2

    obs = manager.observe(missing, iteration=0)
    should_retry, strategy = manager.reflect(obs)
    assert should_retry is True

    updated_rows, remaining_exceptions, logs = manager.adjust_resolve_items(
        rows=rows,
        missing_items=missing,
        auto_prompt=False,
    )

    # Lyft should be resolved, Unknown Parking should remain an exception
    assert len(remaining_exceptions) == 1
    assert remaining_exceptions[0]["vendor"] == "Unknown Parking"
    lyft_row = next(r for r in updated_rows if r["vendor"] == "Lyft")
    assert lyft_row["amount"] == "42.50"


def test_streamlit_auditor_skips_terminal_input_for_unresolved_amount(monkeypatch):
    from unit4_agents.roles import agent_auditor

    def reject_input(*args, **kwargs):
        pytest.fail("The Streamlit execution path must not wait for terminal input.")

    monkeypatch.setattr("builtins.input", reject_input)
    state = {
        "mode": "extended",
        "terminal_input": False,
        "categorized_expenses": [
            {
                "date": "2026-09-25",
                "vendor": "Southwest Airlines",
                "description": "Flight BOS to SFO",
                "category": "Flights",
                "amount": "",
            }
        ],
        "exceptions": [],
        "message_log": [],
        "step_log": [],
    }

    result = agent_auditor(state)

    assert len(result["exceptions"]) == 1
    assert result["exceptions"][0]["vendor"] == "Southwest Airlines"


def test_long_term_memory_reuse_and_user_correction(tmp_path):
    """Test ChromaDB long-term memory store: high similarity reuse and user correction."""
    db_path = str(tmp_path / "test_chroma")
    store = ExpenseMemoryStore(db_path=db_path, similarity_threshold=0.80)

    # Store a canonical memory
    store.store_memory(
        vendor="Acme Car Rental",
        description="Economy car rental for 2 days",
        category="Transport",
        source="model",
    )

    # Query exact or near-identical vendor
    cat, matches, reason = store.resolve_category("Acme Car Rental", "Car rental downtown")
    assert cat == "Transport"
    assert "memory match" in reason
    assert len(matches) > 0
    assert matches[0]["similarity"] >= 0.80

    # User correction priority
    store.add_user_correction("Bistro 42", "Meals", "Dinner with client")
    cat_corr, matches_corr, reason_corr = store.resolve_category("Bistro 42", "Business lunch")
    assert cat_corr == "Meals"
    assert "user_correction" in reason_corr


def test_pdf_and_multi_dataset_ingestion():
    """Test ingestion of alternate CSV and PDF expense statements."""
    from tools import retrieve_expenses, normalize_expense_date

    # 1. Date normalization test
    assert normalize_expense_date("2026-10-04") == "2026-10-04"
    assert normalize_expense_date("04/10/2026") == "2026-10-04"
    assert normalize_expense_date("4 Oct 2026") == "2026-10-04"

    # 2. October CSV ingestion test
    oct_rows = retrieve_expenses("data/october_expenses.csv")
    assert len(oct_rows) == 20
    assert any(r["vendor"] == "Delta Airlines" for r in oct_rows)

    # 3. PDF statement ingestion test
    pdf_rows = retrieve_expenses("data/sample_expense_statement.pdf")
    assert len(pdf_rows) == 12
    first_pdf_item = pdf_rows[0]
    assert first_pdf_item["date"] == "2026-10-02"
    assert first_pdf_item["vendor"] == "Delta Airlines"
    assert float(first_pdf_item["amount"]) == 640.00


def test_brevo_email_sends_pdf_and_parsed_subject(tmp_path, monkeypatch):
    import base64
    import json
    import tools

    pdf_path = tmp_path / "report.pdf"
    pdf_bytes = b"%PDF-1.4 test report"
    pdf_path.write_bytes(pdf_bytes)
    monkeypatch.setenv("EMAIL_PROVIDER", "brevo")
    monkeypatch.setenv("BREVO_API_KEY", "test-brevo-key")
    monkeypatch.setenv("SMTP_FROM", "reports@example.test")

    class MockResponse:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def getcode(self):
            return 201

        def read(self):
            return b'{"messageId":"test-message-id"}'

    captured = {}

    def fake_urlopen(request, timeout):
        captured["request"] = request
        captured["timeout"] = timeout
        return MockResponse()

    monkeypatch.setattr(tools, "urlopen", fake_urlopen)
    result = tools.send_email_with_pdf(
        "Subject: October expenses\n\nPlease review the attached report.",
        str(pdf_path),
        "finance@example.test",
    )

    request_payload = json.loads(captured["request"].data)
    assert captured["request"].full_url == "https://api.brevo.com/v3/smtp/email"
    assert captured["timeout"] == 15
    assert request_payload["subject"] == "October expenses"
    assert request_payload["textContent"] == "Please review the attached report."
    assert request_payload["sender"]["email"] == "reports@example.test"
    assert request_payload["attachment"][0]["content"] == base64.b64encode(pdf_bytes).decode("ascii")
    assert result["status"] == "sent"
    assert result["provider"] == "brevo"
    assert result["message_id"] == "test-message-id"


def test_brevo_missing_api_key_fails_without_network_call(tmp_path, monkeypatch):
    import tools

    pdf_path = tmp_path / "report.pdf"
    pdf_path.write_bytes(b"%PDF-1.4 test report")
    monkeypatch.setenv("EMAIL_PROVIDER", "brevo")
    monkeypatch.delenv("BREVO_API_KEY", raising=False)
    network_called = False

    def fake_urlopen(*args, **kwargs):
        nonlocal network_called
        network_called = True
        raise AssertionError("Network call must not happen without an API key.")

    monkeypatch.setattr(tools, "urlopen", fake_urlopen)
    result = tools.send_email_with_pdf("Report attached.", str(pdf_path), "finance@example.test")

    assert result["status"] == "failed — Brevo API key not configured"
    assert not network_called


def test_smtp_without_credentials_keeps_demo_mode(tmp_path, monkeypatch):
    import tools

    pdf_path = tmp_path / "report.pdf"
    pdf_path.write_bytes(b"%PDF-1.4 test report")
    monkeypatch.setenv("EMAIL_PROVIDER", "smtp")
    monkeypatch.setenv("SMTP_USER", "")
    monkeypatch.setenv("SMTP_PASS", "")

    result = tools.send_email_with_pdf("Report attached.", str(pdf_path), "finance@example.test")

    assert result["provider"] == "smtp"
    assert result["status"].startswith("simulated (demo mode:")


def test_brevo_http_error_reports_safe_provider_detail(tmp_path, monkeypatch):
    import io
    import tools
    from urllib.error import HTTPError

    pdf_path = tmp_path / "report.pdf"
    pdf_path.write_bytes(b"%PDF-1.4 test report")
    monkeypatch.setenv("EMAIL_PROVIDER", "brevo")
    monkeypatch.setenv("BREVO_API_KEY", "test-brevo-key")

    def fake_urlopen(request, timeout):
        body = b'{"code":"unauthorized","message":"transactional email permission required"}'
        raise HTTPError(request.full_url, 403, "Forbidden", {}, io.BytesIO(body))

    monkeypatch.setattr(tools, "urlopen", fake_urlopen)
    result = tools.send_email_with_pdf("Test body", str(pdf_path), "finance@example.test")

    assert result["status"] == "failed — Brevo API returned HTTP 403"
    assert result["error"] == "transactional email permission required"
    assert "test-brevo-key" not in repr(result)

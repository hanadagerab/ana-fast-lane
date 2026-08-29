from preservation import (
    evaluate_preservation,
    lookup_receiving_signal,
    run_preservation_decision,
)


def test_case_1_receiving_signal_present():
    result = lookup_receiving_signal("SPEI-48392")

    assert result["signal_found"] is True
    assert result["independent_receiving_signal"] is True
    assert result["signal_type"] == "pre_existing_internal_risk_flag"
    assert result["simulated"] is True


def test_case_2_receiving_signal_absent():
    result = lookup_receiving_signal("SPEI-58417")

    assert result["signal_found"] is True
    assert result["independent_receiving_signal"] is False
    assert result["signal_type"] == "none"


def test_case_3_receiving_signal_present():
    result = lookup_receiving_signal("SPEI-73105")

    assert result["signal_found"] is True
    assert result["independent_receiving_signal"] is True
    assert result["signal_type"] == "recent_independent_fraud_report"


def test_unknown_reference_has_no_independent_signal():
    result = lookup_receiving_signal("SPEI-UNKNOWN")

    assert result["signal_found"] is False
    assert result["independent_receiving_signal"] is False


def test_transaction_failure_blocks_hold():
    result = evaluate_preservation(
        transaction_verified=False,
        timely=True,
        evidence_consistent=True,
        independent_receiving_signal=True,
        reported_amount=18500,
        reference="SPEI-48392",
    )

    assert result["hold_eligible"] is False
    assert result["decision"] == "STOP"
    assert result["outcome"] == "Stop: transaction cannot be verified"


def test_late_report_blocks_hold_even_with_independent_signal():
    result = evaluate_preservation(
        transaction_verified=True,
        timely=False,
        evidence_consistent=True,
        independent_receiving_signal=True,
        reported_amount=22600,
        reference="SPEI-73105",
    )

    assert result["hold_eligible"] is False
    assert result["decision"] == "PRESERVATION_UNAVAILABLE"
    assert result["outcome"] == (
        "Preservation unavailable · restitution review continues"
    )


def test_inconsistent_ai_evidence_blocks_automatic_hold():
    result = evaluate_preservation(
        transaction_verified=True,
        timely=True,
        evidence_consistent=False,
        independent_receiving_signal=True,
        reported_amount=18500,
        reference="SPEI-48392",
    )

    assert result["hold_eligible"] is False
    assert result["decision"] == "NO_AUTOMATIC_HOLD"
    assert result["institutional_review_requested"] is True


def test_no_independent_signal_blocks_hold():
    result = evaluate_preservation(
        transaction_verified=True,
        timely=True,
        evidence_consistent=True,
        independent_receiving_signal=False,
        reported_amount=12400,
        reference="SPEI-58417",
    )

    assert result["hold_eligible"] is False
    assert result["decision"] == "NO_HOLD_REVIEW"
    assert result["outcome"] == (
        "Report verified · temporary preservation not authorized"
    )
    assert result["institutional_review_requested"] is True


def test_case_1_reaches_temporary_simulated_hold():
    result = run_preservation_decision(
        reference="SPEI-48392",
        reported_amount=18500,
        transaction_verified=True,
        timely=True,
        evidence_consistent=True,
    )

    assert result["hold_eligible"] is True
    assert result["decision"] == "TEMPORARY_HOLD_SIMULATED"
    assert result["outcome"] == "TEMPORARY HOLD ACTIVE — SIMULATED"


def test_case_2_reaches_no_hold_plus_review():
    result = run_preservation_decision(
        reference="SPEI-58417",
        reported_amount=12400,
        transaction_verified=True,
        timely=True,
        evidence_consistent=True,
    )

    assert result["hold_eligible"] is False
    assert result["decision"] == "NO_HOLD_REVIEW"
    assert result["institutional_review_requested"] is True


def test_case_3_reaches_preservation_unavailable():
    result = run_preservation_decision(
        reference="SPEI-73105",
        reported_amount=22600,
        transaction_verified=True,
        timely=False,
        evidence_consistent=True,
    )

    assert result["hold_eligible"] is False
    assert result["decision"] == "PRESERVATION_UNAVAILABLE"


def test_ai_suspicion_cannot_replace_independent_signal():
    result = run_preservation_decision(
        reference="SPEI-58417",
        reported_amount=12400,
        transaction_verified=True,
        timely=True,
        evidence_consistent=True,
    )

    assert result["independent_receiving_signal"] is False
    assert result["hold_eligible"] is False


def test_hold_scope_is_reported_transaction_only():
    result = run_preservation_decision(
        reference="SPEI-48392",
        reported_amount=18500,
        transaction_verified=True,
        timely=True,
        evidence_consistent=True,
    )

    assert result["hold_eligible"] is True
    assert result["hold_scope"]["scope"] == "reported_transaction_only"
    assert result["hold_scope"]["reference"] == "SPEI-48392"
    assert result["hold_scope"]["amount"] == 18500.0


def test_hold_requires_all_four_conditions():
    result = evaluate_preservation(
        transaction_verified=True,
        timely=True,
        evidence_consistent=True,
        independent_receiving_signal=True,
        reported_amount=18500,
        reference="SPEI-48392",
    )

    assert result["hold_eligible"] is True


from preservation import (
    HOLD_DURATION_SECONDS,
    format_countdown,
    get_hold_state,
)


def test_hold_is_active_before_expiry():
    result = get_hold_state(
        started_at_epoch=1000,
        current_epoch=1100,
        stronger_evidence=False,
    )

    assert result["hold_state"] == "ACTIVE"
    assert result["remaining_seconds"] == 800
    assert result["message"] == "TEMPORARY HOLD ACTIVE — SIMULATED"


def test_hold_expires_after_15_minutes():
    result = get_hold_state(
        started_at_epoch=1000,
        current_epoch=1000 + HOLD_DURATION_SECONDS,
        stronger_evidence=False,
    )

    assert result["hold_state"] == "EXPIRED"
    assert result["remaining_seconds"] == 0
    assert result["message"] == "Hold expired · simulated funds released"


def test_hold_escalates_before_expiry():
    result = get_hold_state(
        started_at_epoch=1000,
        current_epoch=1100,
        stronger_evidence=True,
    )

    assert result["hold_state"] == "ESCALATED"
    assert result["message"] == "Escalated to Human Reviewer — simulated"


def test_expiry_wins_after_hold_duration():
    result = get_hold_state(
        started_at_epoch=1000,
        current_epoch=1000 + HOLD_DURATION_SECONDS,
        stronger_evidence=True,
    )

    assert result["hold_state"] == "EXPIRED"


def test_expiry_and_escalation_are_mutually_exclusive():
    expired = get_hold_state(
        started_at_epoch=1000,
        current_epoch=2000,
        stronger_evidence=True,
    )

    escalated = get_hold_state(
        started_at_epoch=1000,
        current_epoch=1100,
        stronger_evidence=True,
    )

    assert expired["hold_state"] == "EXPIRED"
    assert escalated["hold_state"] == "ESCALATED"
    assert expired["hold_state"] != escalated["hold_state"]


def test_countdown_formats_minutes_and_seconds():
    assert format_countdown(872) == "14:32"
    assert format_countdown(60) == "01:00"
    assert format_countdown(0) == "00:00"

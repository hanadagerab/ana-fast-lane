from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional


RECEIVING_SIGNALS_PATH = (
    Path(__file__).parent / "data" / "receiving_signals.json"
)


def load_receiving_signals() -> List[Dict[str, Any]]:
    """
    Load the local synthetic receiving-side signal dataset.
    """
    with RECEIVING_SIGNALS_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def lookup_receiving_signal(
    reference: str,
    receiving_signals: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Look up an independent synthetic receiving-side signal.

    This data is intentionally separate from Ana's report and transaction data.
    """
    if receiving_signals is None:
        receiving_signals = load_receiving_signals()

    normalized_reference = reference.strip()

    for signal in receiving_signals:
        if signal["reference"] == normalized_reference:
            return {
                "signal_found": True,
                "independent_receiving_signal": bool(
                    signal.get(
                        "independent_receiving_side_signal",
                        False,
                    )
                ),
                "signal_type": signal.get("signal_type", "none"),
                "signal_source": signal.get(
                    "signal_source",
                    "synthetic_receiving_institution_data",
                ),
                "simulated": bool(signal.get("simulated", True)),
            }

    return {
        "signal_found": False,
        "independent_receiving_signal": False,
        "signal_type": "none",
        "signal_source": "synthetic_receiving_institution_data",
        "simulated": True,
    }


def evaluate_preservation(
    *,
    transaction_verified: bool,
    timely: bool,
    evidence_consistent: bool,
    independent_receiving_signal: bool,
    reported_amount: float,
    reference: str,
) -> Dict[str, Any]:
    """
    Apply the locked deterministic preservation rule.

    AI does not authorize preservation.
    Ana's allegation alone cannot authorize preservation.

    hold_eligible =
        transaction_verified
        AND timely
        AND evidence_consistent
        AND independent_receiving_signal
    """

    if not transaction_verified:
        return {
            "hold_eligible": False,
            "decision": "STOP",
            "outcome": "Stop: transaction cannot be verified",
            "institutional_review_requested": False,
            "hold_scope": None,
            "simulated": True,
        }

    if not timely:
        return {
            "hold_eligible": False,
            "decision": "PRESERVATION_UNAVAILABLE",
            "outcome": (
                "Preservation unavailable · restitution review continues"
            ),
            "institutional_review_requested": False,
            "hold_scope": None,
            "simulated": True,
        }

    if not evidence_consistent:
        return {
            "hold_eligible": False,
            "decision": "NO_AUTOMATIC_HOLD",
            "outcome": "No automatic hold",
            "institutional_review_requested": True,
            "hold_scope": None,
            "simulated": True,
        }

    if not independent_receiving_signal:
        return {
            "hold_eligible": False,
            "decision": "NO_HOLD_REVIEW",
            "outcome": (
                "Report verified · temporary preservation not authorized"
            ),
            "institutional_review_requested": True,
            "hold_scope": None,
            "simulated": True,
        }

    return {
        "hold_eligible": True,
        "decision": "TEMPORARY_HOLD_SIMULATED",
        "outcome": "TEMPORARY HOLD ACTIVE — SIMULATED",
        "institutional_review_requested": False,
        "hold_scope": {
            "reference": reference,
            "amount": float(reported_amount),
            "scope": "reported_transaction_only",
        },
        "simulated": True,
    }


def run_preservation_decision(
    *,
    reference: str,
    reported_amount: float,
    transaction_verified: bool,
    timely: bool,
    evidence_consistent: bool,
    receiving_signals: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Combine independent receiving-side signal lookup with
    the deterministic preservation decision.

    This function contains no AI logic.
    """
    signal_result = lookup_receiving_signal(
        reference=reference,
        receiving_signals=receiving_signals,
    )

    decision = evaluate_preservation(
        transaction_verified=transaction_verified,
        timely=timely,
        evidence_consistent=evidence_consistent,
        independent_receiving_signal=signal_result[
            "independent_receiving_signal"
        ],
        reported_amount=reported_amount,
        reference=reference,
    )

    return {
        **signal_result,
        **decision,
    }


HOLD_DURATION_SECONDS = 15 * 60


def get_hold_state(
    *,
    started_at_epoch: float,
    current_epoch: float,
    stronger_evidence: bool = False,
) -> Dict[str, Any]:
    """
    Determine the simulated hold lifecycle state.

    States:
    - ACTIVE
    - EXPIRED
    - ESCALATED

    Escalation takes priority only while the hold is still active.
    Expiry and escalation are mutually exclusive.
    """
    elapsed_seconds = max(0, current_epoch - started_at_epoch)
    remaining_seconds = max(0, HOLD_DURATION_SECONDS - elapsed_seconds)

    if elapsed_seconds >= HOLD_DURATION_SECONDS:
        return {
            "hold_state": "EXPIRED",
            "remaining_seconds": 0,
            "message": "Hold expired · simulated funds released",
            "simulated": True,
        }

    if stronger_evidence:
        return {
            "hold_state": "ESCALATED",
            "remaining_seconds": int(remaining_seconds),
            "message": "Escalated to Human Reviewer — simulated",
            "simulated": True,
        }

    return {
        "hold_state": "ACTIVE",
        "remaining_seconds": int(remaining_seconds),
        "message": "TEMPORARY HOLD ACTIVE — SIMULATED",
        "simulated": True,
    }


def format_countdown(remaining_seconds: int) -> str:
    """
    Format remaining hold time as MM:SS.
    """
    remaining_seconds = max(0, int(remaining_seconds))
    minutes, seconds = divmod(remaining_seconds, 60)
    return f"{minutes:02d}:{seconds:02d}"

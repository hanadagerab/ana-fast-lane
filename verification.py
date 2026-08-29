from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional


TRANSACTIONS_PATH = Path(__file__).parent / "data" / "transactions.json"
PRESERVATION_WINDOW_MINUTES = 30


def load_transactions() -> List[Dict[str, Any]]:
    """
    Load the local synthetic transaction dataset.
    """
    with TRANSACTIONS_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def find_transaction_by_reference(
    reference: str,
    transactions: Optional[List[Dict[str, Any]]] = None,
) -> Optional[Dict[str, Any]]:
    """
    Find one synthetic transaction by reference ID.
    """
    if transactions is None:
        transactions = load_transactions()

    normalized_reference = reference.strip()

    for transaction in transactions:
        if transaction["reference"] == normalized_reference:
            return transaction

    return None


def verify_transaction(
    reference: str,
    amount: float,
    recipient: str,
    transactions: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Verify Ana's reported transaction against the local synthetic dataset.

    The transaction is verified only when:
    - the reference exists;
    - the synthetic transaction is marked as existing;
    - the reference matches;
    - the amount matches;
    - the recipient matches.

    No preservation logic is performed here.
    """
    transaction = find_transaction_by_reference(reference, transactions)

    if transaction is None:
        return {
            "transaction_verified": False,
            "reason": "transaction_not_found",
            "transaction": None,
        }

    reference_matches = transaction["reference"] == reference.strip()
    amount_matches = float(transaction["amount"]) == float(amount)
    recipient_matches = transaction["recipient"].strip() == recipient.strip()
    transaction_exists = bool(transaction.get("transaction_exists", False))

    transaction_verified = all(
        [
            transaction_exists,
            reference_matches,
            amount_matches,
            recipient_matches,
        ]
    )

    if transaction_verified:
        reason = "transaction_verified"
    else:
        reason = "transaction_cannot_be_verified"

    return {
        "transaction_verified": transaction_verified,
        "reason": reason,
        "checks": {
            "transaction_exists": transaction_exists,
            "reference_matches": reference_matches,
            "amount_matches": amount_matches,
            "recipient_matches": recipient_matches,
        },
        "transaction": transaction,
    }


def check_timeliness(transfer_age_minutes: float) -> Dict[str, Any]:
    """
    Apply the locked prototype timeliness rule.

    <= 30 minutes -> timely
    > 30 minutes  -> too late for temporary preservation eligibility

    This is a prototype rule, not a real SPEI or bank rule.
    """
    age = float(transfer_age_minutes)
    timely = age <= PRESERVATION_WINDOW_MINUTES

    return {
        "timely": timely,
        "transfer_age_minutes": age,
        "preservation_window_minutes": PRESERVATION_WINDOW_MINUTES,
        "reason": "within_window" if timely else "outside_window",
    }


def verify_and_check_timeliness(
    reference: str,
    amount: float,
    recipient: str,
    transfer_age_minutes: float,
    transactions: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Run transaction verification first.

    Timeliness is evaluated only after the transaction is verified.
    """
    verification = verify_transaction(
        reference=reference,
        amount=amount,
        recipient=recipient,
        transactions=transactions,
    )

    if not verification["transaction_verified"]:
        return {
            **verification,
            "timeliness_checked": False,
            "timely": False,
            "outcome": "Stop: transaction cannot be verified",
        }

    timeliness = check_timeliness(transfer_age_minutes)

    if not timeliness["timely"]:
        outcome = "Preservation unavailable · restitution review continues"
    else:
        outcome = "Transaction verified · report is timely"

    return {
        **verification,
        **timeliness,
        "timeliness_checked": True,
        "outcome": outcome,
    }

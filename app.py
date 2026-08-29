import time

import streamlit as st

from preservation import (
    format_countdown,
    get_hold_state,
    run_preservation_decision,
)
from verification import verify_and_check_timeliness


st.set_page_config(
    page_title="Ana Fast-Lane",
    page_icon="🛡️",
    layout="centered",
)


DEMO_CASES = {
    "Case 1 — Fast + corroborated": {
        "reference": "SPEI-48392",
        "amount": 18500,
        "recipient": "Cuenta terminada en 2714",
        "transfer_age_minutes": 12,
        "evidence_consistent": True,
    },
    "Case 2 — Fast + uncorroborated": {
        "reference": "SPEI-58417",
        "amount": 12400,
        "recipient": "Cuenta terminada en 6408",
        "transfer_age_minutes": 8,
        "evidence_consistent": True,
    },
    "Case 3 — Too late": {
        "reference": "SPEI-73105",
        "amount": 22600,
        "recipient": "Cuenta terminada en 9032",
        "transfer_age_minutes": 47,
        "evidence_consistent": True,
    },
}


def initialize_session_state():
    defaults = {
        "decision_result": None,
        "hold_started_at": None,
        "stronger_evidence": False,
        "demo_elapsed_seconds": 0,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_hold_state():
    st.session_state.decision_result = None
    st.session_state.hold_started_at = None
    st.session_state.stronger_evidence = False
    st.session_state.demo_elapsed_seconds = 0


def render_hold_outcome(result):
    st.success("TEMPORARY HOLD ACTIVE — SIMULATED")

    st.metric(
        "Reported transaction amount",
        f"MX${result['hold_scope']['amount']:,.0f}",
    )

    st.write(f"**Reference:** {result['hold_scope']['reference']}")

    st.markdown(
        """
        ✓ Transaction verified  
        ✓ Evidence structured by AI  
        ✓ Independent receiving-side signal found  
        ✓ Simulated receiving-side signal
        """
    )

    if st.session_state.hold_started_at is None:
        st.session_state.hold_started_at = time.time()

    current_time = (
        time.time()
        + st.session_state.demo_elapsed_seconds
    )

    hold_state = get_hold_state(
        started_at_epoch=st.session_state.hold_started_at,
        current_epoch=current_time,
        stronger_evidence=st.session_state.stronger_evidence,
    )

    if hold_state["hold_state"] == "ACTIVE":
        countdown = format_countdown(
            hold_state["remaining_seconds"]
        )

        st.metric(
            "Temporary simulated hold remaining",
            countdown,
        )

        st.caption(
            "Temporary · Reversible · Auto-expiring"
        )

        st.warning("Preservation ≠ restitution")

        st.markdown("### Demo controls")

        if st.button(
            "Simulate time near expiry",
            use_container_width=True,
        ):
            st.session_state.demo_elapsed_seconds = 14 * 60 + 50
            st.rerun()

        if st.button(
            "Simulate stronger evidence",
            use_container_width=True,
        ):
            st.session_state.stronger_evidence = True
            st.rerun()

        if st.button(
            "Simulate hold expiry",
            use_container_width=True,
        ):
            st.session_state.demo_elapsed_seconds = 15 * 60
            st.rerun()

    elif hold_state["hold_state"] == "EXPIRED":
        st.warning(
            "Hold expired · simulated funds released"
        )
        st.caption(
            "No final restitution decision has been made."
        )

    elif hold_state["hold_state"] == "ESCALATED":
        st.info(
            "Escalated to Human Reviewer — simulated"
        )
        st.caption(
            "Human review does not imply guilt or final restitution."
        )


def render_no_hold_review():
    st.warning(
        "Report verified · temporary preservation not authorized"
    )
    st.info("Institutional review requested")

    st.caption(
        "No simulated hold was created because independent "
        "receiving-side evidence was not available."
    )

    st.warning("Preservation ≠ restitution")


def render_too_late():
    st.warning(
        "Preservation unavailable · restitution review continues"
    )

    st.caption(
        "The report falls outside the prototype 30-minute "
        "preservation eligibility window."
    )

    st.warning("Preservation ≠ restitution")


def main():
    initialize_session_state()

    st.title("Ana Fast-Lane")
    st.subheader("From Report to Temporary Preservation")

    st.warning(
        "SIMULATED PROTOTYPE — Synthetic data only. "
        "Not connected to Banco de México, SPEI, any real bank, "
        "police, or any real recipient account."
    )

    st.markdown(
        """
        **Core question:**  
        How fast can a verified fraud report become operational action?
        """
    )

    st.divider()

    selected_case = st.selectbox(
        "Demo case",
        options=list(DEMO_CASES.keys()),
        on_change=reset_hold_state,
    )

    case = DEMO_CASES[selected_case]

    st.markdown("### Ana's reported transaction")

    reference = st.text_input(
        "Transaction / reference ID",
        value=case["reference"],
    )

    amount = st.number_input(
        "Amount (MXN)",
        min_value=0.01,
        value=float(case["amount"]),
        step=100.0,
    )

    recipient = st.text_input(
        "Recipient",
        value=case["recipient"],
    )

    transfer_age_minutes = st.number_input(
        "Minutes since transfer",
        min_value=0.0,
        value=float(case["transfer_age_minutes"]),
        step=1.0,
    )

    narrative = st.text_area(
        "Short narrative",
        value=(
            "Ana says she was deceived into making this "
            "specific transfer."
        ),
    )

    screenshot = st.file_uploader(
        "Upload screenshot evidence",
        type=["png", "jpg", "jpeg"],
    )

    st.caption(
        "For this Phase 6 demo, the selected case uses locked "
        "synthetic AI evidence consistency. Real Gemini upload "
        "processing will be connected in the next UI step."
    )

    if st.button(
        "Report fraud & check preservation",
        type="primary",
        use_container_width=True,
    ):
        if not reference.strip():
            st.error("Transaction/reference ID is required.")
            return

        if amount <= 0:
            st.error("Amount must be positive.")
            return

        if not recipient.strip():
            st.error("Recipient is required.")
            return

        if not narrative.strip():
            st.error("Narrative is required.")
            return

        if screenshot is None:
            st.error("Screenshot evidence is required.")
            return

        verification = verify_and_check_timeliness(
            reference=reference,
            amount=amount,
            recipient=recipient,
            transfer_age_minutes=transfer_age_minutes,
        )

        if not verification["transaction_verified"]:
            st.session_state.decision_result = {
                "decision": "STOP",
                "outcome": "Stop: transaction cannot be verified",
            }

        elif not verification["timely"]:
            st.session_state.decision_result = {
                "decision": "PRESERVATION_UNAVAILABLE",
                "outcome": (
                    "Preservation unavailable · "
                    "restitution review continues"
                ),
            }

        else:
            st.session_state.decision_result = (
                run_preservation_decision(
                    reference=reference,
                    reported_amount=amount,
                    transaction_verified=True,
                    timely=True,
                    evidence_consistent=case[
                        "evidence_consistent"
                    ],
                )
            )

        if (
            st.session_state.decision_result["decision"]
            == "TEMPORARY_HOLD_SIMULATED"
        ):
            st.session_state.hold_started_at = time.time()
            st.session_state.stronger_evidence = False
            st.session_state.demo_elapsed_seconds = 0

    result = st.session_state.decision_result

    if result:
        st.divider()
        st.markdown("## Result")

        decision = result["decision"]

        if decision == "TEMPORARY_HOLD_SIMULATED":
            render_hold_outcome(result)

        elif decision == "NO_HOLD_REVIEW":
            render_no_hold_review()

        elif decision == "PRESERVATION_UNAVAILABLE":
            render_too_late()

        elif decision == "STOP":
            st.error("Stop: transaction cannot be verified")

        elif decision == "NO_AUTOMATIC_HOLD":
            st.warning("No automatic hold")
            st.info("Institutional review requested")

    st.divider()

    st.caption(
        "Prototype rules: 30-minute eligibility window · "
        "15-minute simulated hold · reported transaction only"
    )


if __name__ == "__main__":
    main()

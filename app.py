import time

import streamlit as st

from evidence import structure_evidence
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
    },
    "Case 2 — Fast + uncorroborated": {
        "reference": "SPEI-58417",
        "amount": 12400,
        "recipient": "Cuenta terminada en 6408",
        "transfer_age_minutes": 8,
    },
    "Case 3 — Too late": {
        "reference": "SPEI-73105",
        "amount": 22600,
        "recipient": "Cuenta terminada en 9032",
        "transfer_age_minutes": 47,
    },
}


def initialize_session_state():
    defaults = {
        "decision_result": None,
        "hold_started_at": None,
        "stronger_evidence": False,
        "demo_elapsed_seconds": 0,
        "evidence_result": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_hold_state():
    st.session_state.decision_result = None
    st.session_state.hold_started_at = None
    st.session_state.stronger_evidence = False
    st.session_state.demo_elapsed_seconds = 0
    st.session_state.evidence_result = None


def render_hold_outcome(result):
    st.success("TEMPORARY HOLD ACTIVE — SIMULATED")

    st.metric(
        "Amount temporarily preserved",
        f"MX${result['hold_scope']['amount']:,.0f}",
    )

    st.write(f"**Transaction reference:** {result['hold_scope']['reference']}")

    st.markdown(
        """
        Your reported transaction was verified and an independent simulated
        receiving-side signal was found.

        **This does not mean you have recovered your money.**
        The immediate goal is to keep the reported funds from moving while
        the case is reviewed.
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
            "Temporary hold time remaining",
            countdown,
        )

        st.caption(
            "This temporary hold will expire automatically unless the case "
            "is escalated during review."
        )

        st.markdown("### What happens now?")

        st.markdown(
            """
            - Your report remains active.
            - The reported transaction is temporarily preserved in this simulation.
            - The case can be escalated for human review if stronger evidence appears.
            - If the hold expires without escalation, the simulated funds are released.
            """
        )

        with st.expander("Demo controls"):
            st.caption(
                "These controls exist only to demonstrate prototype states."
            )

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
            "The temporary simulated hold has expired."
        )

        st.markdown(
            """
            **What happens now?**

            The simulated funds were released because the temporary hold ended.
            Your report can still continue through institutional review.

            **This does not mean your case is closed or that the funds have been recovered.**
            """
        )

    elif hold_state["hold_state"] == "ESCALATED":
        st.info(
            "Your case was escalated to a Human Reviewer — simulated"
        )

        st.markdown(
            """
            **What happens now?**

            A human reviewer would examine the stronger evidence and decide
            whether further action is justified.

            Human review does not mean that fraud has been proven or that
            the money will automatically be returned.
            """
        )


def render_no_hold_review():
    st.warning(
        "We could not authorize a temporary hold automatically."
    )

    st.markdown(
        """
        We did not find the additional independent signal required for
        automatic preservation.

        **This does not mean your report is false.**

        Your report has been sent for institutional review.
        """
    )

    st.markdown("### What happens now?")

    st.markdown(
        """
        - No temporary hold is active.
        - Your report remains under review.
        - Keep your transaction reference and evidence available.
        - In a real case, you should also contact your financial institution immediately.
        - A temporary hold and getting your money back are not the same thing.
        """
    )


def render_too_late():
    st.warning(
        "The fast temporary-preservation window has passed."
    )

    st.markdown(
        """
        This report falls outside the prototype 30-minute eligibility window
        for temporary preservation.

        **The review to try to recover the money can still continue.**
        """
    )

    st.markdown("### What happens now?")

    st.markdown(
        """
        - No temporary hold is active through this fast path.
        - Your report remains active for further review.
        - In a real case, contact your financial institution immediately.
        - Temporary preservation is different from recovering the money.
        """
    )


def main():
    initialize_session_state()

    gemini_api_key = st.secrets.get("GEMINI_API_KEY", "")

    st.title("Ana Fast-Lane")
    st.subheader("Report a fraudulent transfer quickly")

    st.warning(
        "SIMULATED PROTOTYPE — Synthetic data only. "
        "Not connected to Banco de México, SPEI, any real bank, "
        "police, or any real recipient account."
    )

    st.markdown(
        """
        **What this prototype does**

        It checks whether one reported transfer can qualify for a temporary
        simulated preservation action.

        **First, we try to keep the money from moving. This does NOT mean
        you have already recovered your money.**
        """
    )

    st.divider()

    with st.expander("Prototype demo case selector"):
        selected_case = st.selectbox(
            "Choose a synthetic demo case",
            options=list(DEMO_CASES.keys()),
            on_change=reset_hold_state,
        )

    case = DEMO_CASES[selected_case]

    st.markdown("### Your reported transfer")

    reference = st.text_input(
        "Transaction reference",
        value=case["reference"],
        max_chars=50,
        help="In a real case, this would come from your transfer confirmation.",
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
        max_chars=100,
    )

    transfer_age_minutes = st.number_input(
        "Minutes since transfer",
        min_value=0,
        value=int(case["transfer_age_minutes"]),
        step=1,
    )

    narrative = st.text_area(
        "Tell us what happened",
        value="Me engañaron para hacer esta transferencia.",
        max_chars=1000,
        help="A short explanation is enough for this prototype.",
    )

    screenshot = st.file_uploader(
        "Upload evidence",
        type=["png", "jpg", "jpeg"],
        help=(
            "Upload a screenshot of the transfer confirmation, conversation, "
            "or other evidence related to this specific transfer."
        ),
    )

    if screenshot is not None:
        st.success("Evidence received.")

    if st.button(
        "Report fraud & check preservation",
        type="primary",
        use_container_width=True,
    ):
        if not reference.strip():
            st.error("Transaction reference is required.")
            return

        if amount <= 0:
            st.error("Amount must be positive.")
            return

        if not recipient.strip():
            st.error("Recipient is required.")
            return

        if not narrative.strip():
            st.error("Please briefly explain what happened.")
            return

        if screenshot is None:
            st.error("Please upload evidence before continuing.")
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
            if not gemini_api_key:
                st.error(
                    "The evidence service is temporarily unavailable. "
                    "No automatic hold was authorized."
                )
                return

            evidence_result = structure_evidence(
                api_key=gemini_api_key,
                image_bytes=screenshot.getvalue(),
                image_mime_type=screenshot.type,
                narrative=narrative,
                reported_amount=amount,
                reported_reference=reference,
                reported_recipient=recipient,
            )

            st.session_state.evidence_result = evidence_result

            if evidence_result["ai_status"] != "structured":
                st.warning(
                    "The evidence service is temporarily unavailable. "
                    "No automatic hold was authorized."
                )

            st.session_state.decision_result = (
                run_preservation_decision(
                    reference=reference,
                    reported_amount=amount,
                    transaction_verified=True,
                    timely=True,
                    evidence_consistent=evidence_result[
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
            st.error(
                "We could not verify this transaction. "
                "Please review the transaction details and try again."
            )

        elif decision == "NO_AUTOMATIC_HOLD":
            st.warning(
                "We could not authorize a temporary hold automatically."
            )

            st.markdown(
                """
                Your report has been sent for institutional review.

                **This does not mean your report is false.**

                In a real case, you should also contact your financial
                institution immediately.
                """
            )

    st.divider()

    with st.expander("Prototype rules"):
        st.caption(
            "30-minute eligibility window · "
            "15-minute simulated hold · "
            "reported transaction only"
        )


if __name__ == "__main__":
    main()

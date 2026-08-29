from verification import (
    check_timeliness,
    verify_and_check_timeliness,
    verify_transaction,
)


def test_case_1_transaction_verifies():
    result = verify_transaction(
        reference="SPEI-48392",
        amount=18500,
        recipient="Cuenta terminada en 2714",
    )

    assert result["transaction_verified"] is True
    assert result["reason"] == "transaction_verified"


def test_case_2_transaction_verifies():
    result = verify_transaction(
        reference="SPEI-58417",
        amount=12400,
        recipient="Cuenta terminada en 6408",
    )

    assert result["transaction_verified"] is True


def test_case_3_transaction_verifies():
    result = verify_transaction(
        reference="SPEI-73105",
        amount=22600,
        recipient="Cuenta terminada en 9032",
    )

    assert result["transaction_verified"] is True


def test_transaction_mismatch_blocks_verification():
    result = verify_transaction(
        reference="SPEI-48392",
        amount=99999,
        recipient="Cuenta terminada en 2714",
    )

    assert result["transaction_verified"] is False
    assert result["reason"] == "transaction_cannot_be_verified"


def test_unknown_reference_blocks_verification():
    result = verify_transaction(
        reference="SPEI-DOES-NOT-EXIST",
        amount=18500,
        recipient="Cuenta terminada en 2714",
    )

    assert result["transaction_verified"] is False
    assert result["reason"] == "transaction_not_found"


def test_30_minutes_is_timely():
    result = check_timeliness(30)

    assert result["timely"] is True
    assert result["reason"] == "within_window"


def test_more_than_30_minutes_is_not_timely():
    result = check_timeliness(30.01)

    assert result["timely"] is False
    assert result["reason"] == "outside_window"


def test_case_1_is_verified_and_timely():
    result = verify_and_check_timeliness(
        reference="SPEI-48392",
        amount=18500,
        recipient="Cuenta terminada en 2714",
        transfer_age_minutes=12,
    )

    assert result["transaction_verified"] is True
    assert result["timely"] is True
    assert result["outcome"] == "Transaction verified · report is timely"


def test_case_2_is_verified_and_timely():
    result = verify_and_check_timeliness(
        reference="SPEI-58417",
        amount=12400,
        recipient="Cuenta terminada en 6408",
        transfer_age_minutes=8,
    )

    assert result["transaction_verified"] is True
    assert result["timely"] is True


def test_case_3_is_verified_but_too_late():
    result = verify_and_check_timeliness(
        reference="SPEI-73105",
        amount=22600,
        recipient="Cuenta terminada en 9032",
        transfer_age_minutes=47,
    )

    assert result["transaction_verified"] is True
    assert result["timely"] is False
    assert result["outcome"] == "Preservation unavailable · restitution review continues"


def test_failed_verification_stops_before_timeliness():
    result = verify_and_check_timeliness(
        reference="SPEI-48392",
        amount=1,
        recipient="Cuenta terminada en 2714",
        transfer_age_minutes=12,
    )

    assert result["transaction_verified"] is False
    assert result["timeliness_checked"] is False
    assert result["outcome"] == "Stop: transaction cannot be verified"

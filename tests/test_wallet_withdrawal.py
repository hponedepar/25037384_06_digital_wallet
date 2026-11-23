import pytest

from src.wallet_withdrawal import withdraw


# Requirement 3.1.1 - Subtract amount_cents from balance_cents.
# Requirement 3.1.2 - Withdrawing the exact balance is allowed and returns zero.
@pytest.mark.parametrize(
    ("balance_cents", "amount_cents", "expected_balance"),
    [
        (1000, 500, 500),  # typical withdrawal
        (100, 70, 30),  # exact subtraction check: 100 - 70 must be 30
        (5000, 1234, 3766),  # exact subtraction with irregular values
        (1000, 1, 999),  # smallest valid amount
        (1000, 999, 1),  # one cent below the balance
        # DEFECT D1: the next 2 cases fail - wallet_withdrawal.py line 9 uses >=
        # instead of >, so the exact balance raises ValueError instead of returning 0
        (1000, 1000, 0),  # exact balance returns zero
        (1, 1, 0),  # smallest balance, exact withdrawal
    ],
)
def test_withdraw_valid_amount_returns_remaining_balance(
    balance_cents, amount_cents, expected_balance
):
    # Act
    result = withdraw(balance_cents, amount_cents)

    # Assert
    assert result == expected_balance
    assert type(result) is int


# Requirement 3.1.2 - A zero or negative amount, negative balance,
# or withdrawal above the balance raises ValueError.
@pytest.mark.parametrize(
    ("balance_cents", "amount_cents"),
    [
        (1000, 0),  # zero amount
        (1000, -1),  # negative amount
        (-1, 1),  # negative balance
        (1000, 1001),  # one cent above the balance
        (0, 1),  # zero balance cannot cover any withdrawal
    ],
)
def test_withdraw_out_of_range_value_raises_value_error(balance_cents, amount_cents):
    # Act and Assert
    with pytest.raises(ValueError):
        withdraw(balance_cents, amount_cents)


# General Requirements 2.2 and 2.3 - Inputs must be int (bool is not valid),
# otherwise TypeError is raised.
@pytest.mark.parametrize(
    ("balance_cents", "amount_cents"),
    [
        (1000.0, 100),  # balance is a float
        ("1000", 100),  # balance is a string
        (None, 100),  # balance is None
        (True, 100),  # balance is a bool
        (1000, 100.5),  # amount is a float
        (1000, "100"),  # amount is a string
        (1000, None),  # amount is None
        (1000, True),  # amount is a bool
        (1000, False),  # amount is False (rejected even though Python treats it as 0)
        (-1.5, 100),  # confirms type validation happens before the negative-balance check
        (1000, -1.5),  # confirms type validation happens before the negative-amount check
    ],
)
def test_withdraw_invalid_type_raises_type_error(balance_cents, amount_cents):
    # Act and Assert
    with pytest.raises(TypeError):
        withdraw(balance_cents, amount_cents)

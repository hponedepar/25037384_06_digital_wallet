import pytest

from src.wallet_affordability import can_afford


# Requirement 3.2.1 - Affordable when balance_cents >= price_cents.
# Requirement 3.2.2 - A zero price is affordable, including when the balance is zero.
# Output - Must return the actual bool True (the integer 1 is not acceptable).
# DEFECT D2: all 5 cases fail - wallet_affordability.py line 9 returns int(...),
# so the result is 1 instead of True
@pytest.mark.parametrize(
    ("balance_cents", "price_cents"),
    [
        (1000, 500),  # balance greater than price
        (1000, 1000),  # balance equal to price
        (1000, 999),  # price one cent below balance
        (1000, 0),  # zero price is affordable
        (0, 0),  # zero price with zero balance
    ],
)
def test_can_afford_balance_covers_price_returns_true(balance_cents, price_cents):
    # Act
    result = can_afford(balance_cents, price_cents)

    # Assert
    assert result is True


# Requirement 3.2.2 - A lower balance cannot cover the price.
# Output - Must return the actual bool False (the integer 0 is not acceptable).
# DEFECT D2: all 3 cases fail - wallet_affordability.py line 9 returns int(...),
# so the result is 0 instead of False
@pytest.mark.parametrize(
    ("balance_cents", "price_cents"),
    [
        (999, 1000),  # balance one cent below price
        (0, 1),  # zero balance, smallest price
        (500, 1000),  # balance lower than price
    ],
)
def test_can_afford_balance_below_price_returns_false(balance_cents, price_cents):
    # Act
    result = can_afford(balance_cents, price_cents)

    # Assert
    assert result is False


# General Requirement 2.4 - Both values must be nonnegative, otherwise ValueError.
@pytest.mark.parametrize(
    ("balance_cents", "price_cents"),
    [
        (-1, 0),  # negative balance
        (0, -1),  # negative price
        (-1, -1),  # both inputs negative
    ],
)
def test_can_afford_negative_value_raises_value_error(balance_cents, price_cents):
    # Act and Assert
    with pytest.raises(ValueError):
        can_afford(balance_cents, price_cents)


# General Requirements 2.2 and 2.3 - Inputs must be int (bool is not valid),
# otherwise TypeError is raised.
@pytest.mark.parametrize(
    ("balance_cents", "price_cents"),
    [
        (1000.0, 100),  # balance is a float
        ("1000", 100),  # balance is a string
        (None, 100),  # balance is None
        (True, 0),  # balance is a bool
        (1000, 100.5),  # price is a float
        (1000, "100"),  # price is a string
        (1000, None),  # price is None
        (1000, False),  # price is a bool
        (-1.5, 100),  # confirms type validation happens before the negative-balance check
        (1000, -1.5),  # confirms type validation happens before the negative-price check
    ],
)
def test_can_afford_invalid_type_raises_type_error(balance_cents, price_cents):
    # Act and Assert
    with pytest.raises(TypeError):
        can_afford(balance_cents, price_cents)

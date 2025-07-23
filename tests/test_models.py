import pytest
from pydantic import ValidationError
from datetime import datetime

from dsp2_client.models.account import Account
from dsp2_client.models.balance import Balance
from dsp2_client.models.identity import Identity
from dsp2_client.models.transaction import Transaction

# --------- Account ---------
def test_account_valid():
    acc = Account(
        id="acct_Ms99YLcC2LETpC4KKK7VcjPY",
        type="CARD",
        usage="PRIV",
        iban="FR1420041010050500013M04406",
        name="Compte Carte",
        currency="USD"
    )
    assert acc.id.startswith("acct_")
    assert acc.type == "CARD"

def test_account_invalid_missing_id():
    with pytest.raises(ValidationError):
        Account(
            type="CARD",
            usage="PRIV"
        )

# --------- Balance ---------
def test_balance_valid():
    bal = Balance(
        id="blnc_YUUO26FOwggqOMvyhsr9ojzA",
        name="Main Balance",
        amount=2500.50,
        currency="EUR",
        type="CLBD"
    )
    assert isinstance(bal.amount, float)
    assert bal.currency == "EUR"

def test_balance_negative_amount():
    bal = Balance(
        id="blnc_YUUO26FOwggqOMvyhsr9ojzA",
        amount=-100.0,
        currency="EUR"
    )
    assert bal.amount == -100.0

# --------- Identity ---------
def test_identity_valid():
    user = Identity(
        id="user_TLMLiOYdrPdO7YYuuLdK9Dvw",
        prefix="MIST",
        first_name="Maurice",
        last_name="Dupuis",
        date_of_birth="1970-05-06"
    )
    assert user.first_name == "Maurice"
    assert user.date_of_birth == "1970-05-06"

def test_identity_invalid_missing_fields():
    with pytest.raises(ValidationError):
        Identity(id="x", first_name="X", last_name=None)

# --------- Transaction ---------
def test_transaction_valid():
    tx = Transaction(
        id="tran_tzotgyExrpHajnVJTyRrxqUj",
        label="Payment at Supermarket",
        amount=45.10,
        crdt_dbit_indicator="DBIT",
        status="BOOK",
        currency="EUR",
        date_operation=datetime(2025, 7, 23, 9, 16, 48, 293000),
        date_processed=datetime(2025, 7, 23, 9, 17, 10, 100000)
    )
    assert tx.amount > 0
    assert tx.status in ("BOOK", "PENDING", "INFO")

def test_transaction_invalid_missing_id():
    with pytest.raises(ValidationError):
        Transaction(
            label="T",
            amount=5.0
        )

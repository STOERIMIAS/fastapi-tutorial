import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(800)

@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (7, 1, 8),
    (12, 4, 16)
])

def test_add(num1, num2, expected):
    assert add(num1, num2) == expected

def test_subtract():
    assert subtract(9, 4) == 5

def test_multiply():
    assert multiply(9, 4) == 36

def test_divide():
    assert divide(9, 9) == 1

def test_BankAccount_set_initial_amount(bank_account):
    assert bank_account.balance == 800

def test_BankAccount_defluat_amaount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_BankAccount_withdraw(bank_account):
    bank_account.withdraw(50)
    assert bank_account.balance == 750

def test_BankAccount_deposit(bank_account):
    bank_account.deposit(50)
    assert bank_account.balance == 850

def test_BankAccount_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 2) == 880

import pytest
from app.services.bank_service import BankService
from app.models import Account, Transaction, Customer
from app.database import get_db

def test_deposit_operation(app):
    """Test deposit increases balance and creates transaction record."""
    with app.app_context():
        with get_db() as db:
            acc = db.query(Account).filter_by(account_id=101).first()
            initial_bal = float(acc.balance)

        res = BankService.deposit(account_id=101, amount=1500.00, description="Test Deposit")
        assert res['success'] is True
        assert res['new_balance'] == initial_bal + 1500.00

        with get_db() as db:
            tx = db.query(Transaction).filter_by(transaction_id=res['transaction_id']).first()
            assert tx is not None
            assert tx.transaction_type == 'Deposit'
            assert float(tx.amount) == 1500.00

def test_withdrawal_operation(app):
    """Test withdrawal decreases balance and creates transaction record."""
    with app.app_context():
        res = BankService.withdraw(account_id=101, amount=500.00, description="Test Withdrawal")
        assert res['success'] is True

        with get_db() as db:
            tx = db.query(Transaction).filter_by(transaction_id=res['transaction_id']).first()
            assert tx is not None
            assert tx.transaction_type == 'Withdrawal'
            assert float(tx.amount) == 500.00

def test_withdrawal_insufficient_funds_rejected(app):
    """Test overdraft rejection when balance is insufficient."""
    with app.app_context():
        with pytest.raises(ValueError, match="Insufficient funds"):
            BankService.withdraw(account_id=101, amount=99999999.00)

def test_atomic_transfer_operation(app):
    """Test atomic fund transfer debits source and credits destination."""
    with app.app_context():
        with get_db() as db:
            src = db.query(Account).filter_by(account_id=101).first()
            tgt = db.query(Account).filter_by(account_id=103).first()
            src_initial = float(src.balance)
            tgt_initial = float(tgt.balance)

        res = BankService.transfer(
            source_account_id=101,
            target_account_id=103,
            amount=2000.00,
            description="Inter-account test transfer"
        )
        assert res['success'] is True
        assert res['source_new_balance'] == src_initial - 2000.00
        assert res['target_new_balance'] == tgt_initial + 2000.00

def test_atomic_transfer_insufficient_funds_rollback(app):
    """Test transfer failure if balance insufficient, preserving both balances."""
    with app.app_context():
        with get_db() as db:
            src = db.query(Account).filter_by(account_id=103).first()
            tgt = db.query(Account).filter_by(account_id=101).first()
            src_bal = float(src.balance)
            tgt_bal = float(tgt.balance)

        with pytest.raises(ValueError, match="Insufficient funds"):
            BankService.transfer(
                source_account_id=103,
                target_account_id=101,
                amount=99999999.00
            )

        # Check balances were untouched
        with get_db() as db:
            src_after = db.query(Account).filter_by(account_id=103).first()
            tgt_after = db.query(Account).filter_by(account_id=101).first()
            assert float(src_after.balance) == src_bal
            assert float(tgt_after.balance) == tgt_bal

def test_customer_creation_duplicate_email_rejected(app):
    """Test email uniqueness constraint."""
    with app.app_context():
        with pytest.raises(ValueError, match="already exists"):
            BankService.create_customer(
                name="Duplicate User",
                email="priya.sharma@example.com", # already in sample data
                phone="9999999999",
                address="Hyderabad"
            )

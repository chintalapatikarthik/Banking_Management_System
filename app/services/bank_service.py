from decimal import Decimal
from datetime import date, datetime
from app.database import get_db, execute_raw_sql
from app.models import Customer, Account, Transaction, Loan, Employee, Branch, User

class BankService:
    """Core banking operations and business logic with transaction integrity."""

    @staticmethod
    def get_dashboard_summary():
        """Retrieve aggregated KPI counts for dashboard cards."""
        with get_db() as db:
            total_customers = db.query(Customer).count()
            total_accounts = db.query(Account).count()
            total_balance = sum(float(a.balance) for a in db.query(Account).all())
            total_transactions = db.query(Transaction).count()
            total_loan_amount = sum(float(l.loan_amount) for l in db.query(Loan).all())
            total_employees = db.query(Employee).count()
            total_branches = db.query(Branch).count()

            return {
                'total_customers': total_customers,
                'total_accounts': total_accounts,
                'total_balance': total_balance,
                'total_transactions': total_transactions,
                'total_loan_amount': total_loan_amount,
                'total_employees': total_employees,
                'total_branches': total_branches
            }

    @staticmethod
    def deposit(account_id, amount, description=None):
        """
        Deposit funds into an account atomically.
        Increases balance and records transaction.
        """
        amount = Decimal(str(amount))
        if amount <= 0:
            raise ValueError("Deposit amount must be strictly greater than zero.")

        with get_db() as db:
            account = db.query(Account).filter_by(account_id=account_id).with_for_update().first()
            if not account:
                raise ValueError(f"Account ID #{account_id} not found.")
            if account.account_status != 'Active':
                raise ValueError(f"Account ID #{account_id} is {account.account_status} and cannot receive deposits.")

            account.balance = Decimal(str(account.balance)) + amount
            
            tx = Transaction(
                account_id=account_id,
                transaction_type='Deposit',
                amount=amount,
                transaction_date=date.today(),
                description=description or 'Cash / Online Deposit'
            )
            db.add(tx)
            db.commit()
            return {
                'success': True,
                'account_id': account.account_id,
                'new_balance': float(account.balance),
                'transaction_id': tx.transaction_id
            }

    @staticmethod
    def withdraw(account_id, amount, description=None):
        """
        Withdraw funds from an account atomically.
        Validates sufficient balance, decreases balance, records transaction.
        """
        amount = Decimal(str(amount))
        if amount <= 0:
            raise ValueError("Withdrawal amount must be strictly greater than zero.")

        with get_db() as db:
            account = db.query(Account).filter_by(account_id=account_id).with_for_update().first()
            if not account:
                raise ValueError(f"Account ID #{account_id} not found.")
            if account.account_status != 'Active':
                raise ValueError(f"Account ID #{account_id} is {account.account_status} and cannot process withdrawals.")

            current_balance = Decimal(str(account.balance))
            if current_balance < amount:
                raise ValueError(f"Insufficient funds! Available balance: ₹{current_balance:,.2f}, Requested: ₹{amount:,.2f}")

            account.balance = current_balance - amount
            
            tx = Transaction(
                account_id=account_id,
                transaction_type='Withdrawal',
                amount=amount,
                transaction_date=date.today(),
                description=description or 'Cash / ATM Withdrawal'
            )
            db.add(tx)
            db.commit()
            return {
                'success': True,
                'account_id': account.account_id,
                'new_balance': float(account.balance),
                'transaction_id': tx.transaction_id
            }

    @staticmethod
    def transfer(source_account_id, target_account_id, amount, description=None):
        """
        Transfer funds between two accounts using an atomic database transaction.
        Debits source account, credits target account, creates twin transaction records.
        """
        if source_account_id == target_account_id:
            raise ValueError("Source and destination accounts must be different.")

        amount = Decimal(str(amount))
        if amount <= 0:
            raise ValueError("Transfer amount must be strictly greater than zero.")

        with get_db() as db:
            source = db.query(Account).filter_by(account_id=source_account_id).with_for_update().first()
            target = db.query(Account).filter_by(account_id=target_account_id).with_for_update().first()

            if not source:
                raise ValueError(f"Source account #{source_account_id} not found.")
            if not target:
                raise ValueError(f"Target account #{target_account_id} not found.")
            if source.account_status != 'Active':
                raise ValueError(f"Source account #{source_account_id} is not Active.")
            if target.account_status != 'Active':
                raise ValueError(f"Target account #{target_account_id} is not Active.")

            src_balance = Decimal(str(source.balance))
            if src_balance < amount:
                raise ValueError(f"Insufficient funds in sender account! Available: ₹{src_balance:,.2f}, Requested: ₹{amount:,.2f}")

            # Execute Atomic Balance Updates
            source.balance = src_balance - amount
            target.balance = Decimal(str(target.balance)) + amount

            desc_src = description or f"Transfer to A/C #{target_account_id}"
            desc_tgt = description or f"Transfer from A/C #{source_account_id}"

            tx_debit = Transaction(
                account_id=source_account_id,
                transaction_type='Transfer Debit',
                amount=amount,
                transaction_date=date.today(),
                description=desc_src
            )
            tx_credit = Transaction(
                account_id=target_account_id,
                transaction_type='Transfer Credit',
                amount=amount,
                transaction_date=date.today(),
                description=desc_tgt
            )

            db.add(tx_debit)
            db.add(tx_credit)
            db.commit()

            return {
                'success': True,
                'source_account_id': source.account_id,
                'source_new_balance': float(source.balance),
                'target_account_id': target.account_id,
                'target_new_balance': float(target.balance),
                'debit_transaction_id': tx_debit.transaction_id,
                'credit_transaction_id': tx_credit.transaction_id
            }

    @staticmethod
    def create_customer(name, email, phone, address, registration_date=None):
        """Create a new customer record."""
        with get_db() as db:
            existing = db.query(Customer).filter_by(email=email).first()
            if existing:
                raise ValueError(f"A customer with email '{email}' already exists.")

            cust = Customer(
                name=name.strip(),
                email=email.strip().lower(),
                phone=phone.strip() if phone else None,
                address=address.strip() if address else None,
                registration_date=registration_date or date.today()
            )
            db.add(cust)
            db.commit()
            db.refresh(cust)
            return cust.to_dict()

    @staticmethod
    def create_account(customer_id, branch_id, account_type, initial_deposit=0.0):
        """Create a new bank account with optional initial deposit."""
        init_amount = Decimal(str(initial_deposit or 0.0))
        if init_amount < 0:
            raise ValueError("Initial deposit cannot be negative.")

        with get_db() as db:
            cust = db.query(Customer).filter_by(customer_id=customer_id).first()
            if not cust:
                raise ValueError(f"Customer #{customer_id} does not exist.")

            account = Account(
                customer_id=customer_id,
                branch_id=branch_id if branch_id else None,
                account_type=account_type,
                balance=init_amount,
                opening_date=date.today(),
                account_status='Active'
            )
            db.add(account)
            db.commit()
            db.refresh(account)

            if init_amount > 0:
                tx = Transaction(
                    account_id=account.account_id,
                    transaction_type='Deposit',
                    amount=init_amount,
                    transaction_date=date.today(),
                    description='Initial account opening deposit'
                )
                db.add(tx)
                db.commit()

            return account.to_dict()

    @staticmethod
    def create_loan(customer_id, loan_amount, interest_rate, loan_date=None):
        """Disburse a new loan to a customer."""
        amount = Decimal(str(loan_amount))
        rate = Decimal(str(interest_rate))
        if amount <= 0:
            raise ValueError("Loan amount must be positive.")
        if rate <= 0:
            raise ValueError("Interest rate must be positive.")

        with get_db() as db:
            cust = db.query(Customer).filter_by(customer_id=customer_id).first()
            if not cust:
                raise ValueError(f"Customer #{customer_id} does not exist.")

            loan = Loan(
                customer_id=customer_id,
                loan_amount=amount,
                interest_rate=rate,
                loan_date=loan_date or date.today()
            )
            db.add(loan)
            db.commit()
            db.refresh(loan)
            return loan.to_dict()

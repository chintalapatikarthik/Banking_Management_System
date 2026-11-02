from datetime import datetime, date
from decimal import Decimal
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import (
    Column, Integer, String, Numeric, Date, DateTime, 
    ForeignKey, Boolean, CheckConstraint, Index
)
from sqlalchemy.orm import relationship
from app.database import Base

class Branch(Base):
    __tablename__ = 'branches'

    branch_id = Column(Integer, primary_key=True, autoincrement=True)
    branch_name = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    accounts = relationship("Account", back_populates="branch", cascade="all, delete-orphan")
    employees = relationship("Employee", back_populates="branch")

    def to_dict(self):
        return {
            'branch_id': self.branch_id,
            'branch_name': self.branch_name,
            'location': self.location,
            'total_accounts': len(self.accounts),
            'total_employees': len(self.employees),
            'total_deposits': sum(float(a.balance) for a in self.accounts)
        }

class Customer(Base):
    __tablename__ = 'customers'

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(15), nullable=True)
    address = Column(String(255), nullable=True)
    registration_date = Column(Date, nullable=False, default=date.today)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    accounts = relationship("Account", back_populates="customer", cascade="all, delete-orphan")
    loans = relationship("Loan", back_populates="customer", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'customer_id': self.customer_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'registration_date': self.registration_date.strftime('%Y-%m-%d') if self.registration_date else '',
            'accounts_count': len(self.accounts),
            'loans_count': len(self.loans),
            'total_balance': sum(float(a.balance) for a in self.accounts)
        }

class Account(Base):
    __tablename__ = 'accounts'

    account_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id', ondelete='CASCADE'), nullable=False)
    branch_id = Column(Integer, ForeignKey('branches.branch_id', ondelete='SET NULL'), nullable=True)
    account_type = Column(String(50), nullable=False) # 'Savings', 'Current'
    balance = Column(Numeric(12, 2), nullable=False, default=Decimal('0.00'))
    opening_date = Column(Date, nullable=False, default=date.today)
    account_status = Column(String(20), nullable=False, default='Active') # 'Active', 'Inactive'
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint('balance >= 0', name='chk_positive_balance'),
    )

    # Relationships
    customer = relationship("Customer", back_populates="accounts")
    branch = relationship("Branch", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account", cascade="all, delete-orphan", order_by="desc(Transaction.transaction_id)")

    def to_dict(self):
        return {
            'account_id': self.account_id,
            'customer_id': self.customer_id,
            'customer_name': self.customer.name if self.customer else 'N/A',
            'branch_id': self.branch_id,
            'branch_name': self.branch.branch_name if self.branch else 'Unassigned',
            'account_type': self.account_type,
            'balance': float(self.balance),
            'opening_date': self.opening_date.strftime('%Y-%m-%d') if self.opening_date else '',
            'account_status': self.account_status
        }

class Transaction(Base):
    __tablename__ = 'transactions'

    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('accounts.account_id', ondelete='CASCADE'), nullable=False)
    transaction_type = Column(String(20), nullable=False) # 'Deposit', 'Withdrawal', 'Transfer Debit', 'Transfer Credit'
    amount = Column(Numeric(10, 2), nullable=False)
    transaction_date = Column(Date, nullable=False, default=date.today)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint('amount > 0', name='chk_positive_transaction_amount'),
    )

    # Relationships
    account = relationship("Account", back_populates="transactions")

    def to_dict(self):
        return {
            'transaction_id': self.transaction_id,
            'account_id': self.account_id,
            'customer_name': self.account.customer.name if self.account and self.account.customer else 'N/A',
            'transaction_type': self.transaction_type,
            'amount': float(self.amount),
            'transaction_date': self.transaction_date.strftime('%Y-%m-%d') if self.transaction_date else '',
            'description': self.description or ''
        }

class Loan(Base):
    __tablename__ = 'loans'

    loan_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id', ondelete='CASCADE'), nullable=False)
    loan_amount = Column(Numeric(12, 2), nullable=False)
    interest_rate = Column(Numeric(5, 2), nullable=False)
    loan_date = Column(Date, nullable=False, default=date.today)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint('loan_amount > 0', name='chk_positive_loan_amount'),
    )

    # Relationships
    customer = relationship("Customer", back_populates="loans")

    def to_dict(self):
        return {
            'loan_id': self.loan_id,
            'customer_id': self.customer_id,
            'customer_name': self.customer.name if self.customer else 'N/A',
            'loan_amount': float(self.loan_amount),
            'interest_rate': float(self.interest_rate),
            'loan_date': self.loan_date.strftime('%Y-%m-%d') if self.loan_date else ''
        }

class Employee(Base):
    __tablename__ = 'employees'

    employee_id = Column(Integer, primary_key=True, autoincrement=True)
    employee_name = Column(String(100), nullable=False)
    position = Column(String(50), nullable=False)
    salary = Column(Numeric(10, 2), nullable=False)
    joining_date = Column(Date, nullable=False, default=date.today)
    branch_id = Column(Integer, ForeignKey('branches.branch_id', ondelete='SET NULL'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    branch = relationship("Branch", back_populates="employees")
    user = relationship("User", back_populates="employee", uselist=False)

    def to_dict(self):
        return {
            'employee_id': self.employee_id,
            'employee_name': self.employee_name,
            'position': self.position,
            'salary': float(self.salary),
            'joining_date': self.joining_date.strftime('%Y-%m-%d') if self.joining_date else '',
            'branch_id': self.branch_id,
            'branch_name': self.branch.branch_name if self.branch else 'Unassigned'
        }

class User(Base, UserMixin):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default='employee') # 'admin' or 'employee'
    employee_id = Column(Integer, ForeignKey('employees.employee_id', ondelete='SET NULL'), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    employee = relationship("Employee", back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.user_id)

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_employee(self):
        return self.role in ('employee', 'admin')

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'employee_id': self.employee_id,
            'is_active': self.is_active
        }

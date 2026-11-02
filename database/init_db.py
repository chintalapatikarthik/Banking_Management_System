import os
import sys
from datetime import datetime, date
from decimal import Decimal

# Add parent directory to path so imports work when executed directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import engine, Base, get_db
from app.models import Branch, Customer, Account, Transaction, Loan, Employee, User
from app.config import Config
from sqlalchemy import text

def create_views(db):
    """Create database views for analysis, compatible with MySQL and SQLite."""
    views_sql = [
        # 1. Customer Accounts View
        """
        CREATE VIEW IF NOT EXISTS v_customer_accounts AS
        SELECT 
            c.customer_id,
            c.name AS customer_name,
            c.email,
            c.phone,
            c.address,
            a.account_id,
            a.account_type,
            a.balance,
            a.account_status,
            a.opening_date,
            b.branch_name,
            b.location AS branch_location
        FROM customers c
        JOIN accounts a ON c.customer_id = a.customer_id
        LEFT JOIN branches b ON a.branch_id = b.branch_id;
        """,
        # 2. Transaction Details View
        """
        CREATE VIEW IF NOT EXISTS v_transaction_details AS
        SELECT 
            t.transaction_id,
            t.transaction_date,
            t.transaction_type,
            t.amount,
            t.description,
            a.account_id,
            a.account_type,
            c.customer_id,
            c.name AS customer_name,
            b.branch_name
        FROM transactions t
        JOIN accounts a ON t.account_id = a.account_id
        JOIN customers c ON a.customer_id = c.customer_id
        LEFT JOIN branches b ON a.branch_id = b.branch_id;
        """,
        # 3. Loan Details with Customers View
        """
        CREATE VIEW IF NOT EXISTS v_customer_loans AS
        SELECT 
            l.loan_id,
            l.loan_amount,
            l.interest_rate,
            l.loan_date,
            c.customer_id,
            c.name AS customer_name,
            c.email,
            c.phone,
            c.address
        FROM loans l
        JOIN customers c ON l.customer_id = c.customer_id;
        """,
        # 4. Total Balance per Customer View
        """
        CREATE VIEW IF NOT EXISTS v_customer_total_balance AS
        SELECT 
            c.customer_id,
            c.name AS customer_name,
            c.email,
            COUNT(a.account_id) AS total_accounts,
            COALESCE(SUM(a.balance), 0.00) AS total_balance
        FROM customers c
        LEFT JOIN accounts a ON c.customer_id = a.customer_id
        GROUP BY c.customer_id, c.name, c.email;
        """,
        # 5. High Value Transactions View (Transactions >= 25000)
        """
        CREATE VIEW IF NOT EXISTS v_high_value_transactions AS
        SELECT 
            t.transaction_id,
            t.account_id,
            c.name AS customer_name,
            t.transaction_type,
            t.amount,
            t.transaction_date,
            t.description
        FROM transactions t
        JOIN accounts a ON t.account_id = a.account_id
        JOIN customers c ON a.customer_id = c.customer_id
        WHERE t.amount >= 25000.00;
        """
    ]

    for v_sql in views_sql:
        try:
            # Handle MySQL CREATE OR REPLACE vs SQLite CREATE VIEW IF NOT EXISTS
            if 'mysql' in str(engine.url):
                v_sql = v_sql.replace('CREATE VIEW IF NOT EXISTS', 'CREATE OR REPLACE VIEW')
            db.execute(text(v_sql))
            db.commit()
        except Exception as e:
            print(f"Notice: view creation warning: {e}")
            db.rollback()

def create_procedures(db):
    """Create MySQL stored procedures from procedures.sql if running on MySQL."""
    if 'mysql' not in str(engine.url):
        return

    procedures_path = os.path.join(os.path.dirname(__file__), 'procedures.sql')
    if not os.path.exists(procedures_path):
        return

    try:
        with open(procedures_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split on $$ delimiter to handle multiple DELIMITER $$ blocks
        blocks = content.split('$$')
        for block in blocks:
            sql = block.strip()
            if not sql or sql.startswith('DELIMITER'):
                continue
            sql = sql.replace('DELIMITER ;', '').strip()
            if sql:
                try:
                    db.execute(text(sql))
                    db.commit()
                except Exception as e:
                    print(f"Notice: stored procedure creation notice: {e}")
                    db.rollback()
        print("[OK] MySQL Stored Procedures registered successfully.")
    except Exception as e:
        print(f"Notice: could not load procedures.sql: {e}")

def seed_sample_data(db):
    """Seed initial sample data idempotently if tables are empty."""
    # 1. Branches
    if db.query(Branch).count() == 0:
        branches = [
            Branch(branch_id=1, branch_name='Hyderabad Main Branch', location='Hyderabad'),
            Branch(branch_id=2, branch_name='Banjara Hills Branch', location='Hyderabad'),
            Branch(branch_id=3, branch_name='Bangalore Central', location='Bangalore'),
            Branch(branch_id=4, branch_name='Mumbai Fort Branch', location='Mumbai'),
            Branch(branch_id=5, branch_name='Connaught Place Branch', location='Delhi'),
            Branch(branch_id=6, branch_name='T Nagar Branch', location='Chennai')
        ]
        db.add_all(branches)
        db.commit()
        print("[OK] Branches seeded successfully.")

    # 2. Customers
    if db.query(Customer).count() == 0:
        customers = [
            Customer(customer_id=101, name='Rahul Sharma', email='rahul.sharma@example.com', phone='9876543210', address='Banjara Hills, Hyderabad', registration_date=date(2021, 3, 15)),
            Customer(customer_id=102, name='Priya Patel', email='priya.patel@example.com', phone='9823456781', address='Koramangala, Bangalore', registration_date=date(2021, 6, 20)),
            Customer(customer_id=103, name='Amit Kumar', email='amit.kumar@example.com', phone='9712345678', address='Hitec City, Hyderabad', registration_date=date(2022, 1, 10)),
            Customer(customer_id=104, name='Sneha Reddy', email='sneha.reddy@example.com', phone='9654321870', address='Jubilee Hills, Hyderabad', registration_date=date(2022, 4, 18)),
            Customer(customer_id=105, name='Vikram Malhotra', email='vikram.m@example.com', phone='9543210987', address='Bandra West, Mumbai', registration_date=date(2022, 8, 5)),
            Customer(customer_id=106, name='Ananya Iyer', email='ananya.iyer@example.com', phone='9432109876', address='Indiranagar, Bangalore', registration_date=date(2023, 2, 14)),
            Customer(customer_id=107, name='Rohan Verma', email='rohan.verma@example.com', phone='9321098765', address='Connaught Place, Delhi', registration_date=date(2023, 5, 22)),
            Customer(customer_id=108, name='Deepika Rao', email='deepika.rao@example.com', phone='9210987654', address='Madhapur, Hyderabad', registration_date=date(2023, 9, 11)),
            Customer(customer_id=109, name='Karthik Subramanian', email='karthik.s@example.com', phone='9109876543', address='T Nagar, Chennai', registration_date=date(2024, 1, 15)),
            Customer(customer_id=110, name='Suresh Raina', email='suresh.raina@example.com', phone='9098765432', address='Alwal, Hyderabad', registration_date=date(2024, 3, 1)),
            Customer(customer_id=111, name='Meera Nair', email='meera.nair@example.com', phone='9988776655', address='Gachibowli, Hyderabad', registration_date=date(2024, 4, 10))
        ]
        db.add_all(customers)
        db.commit()
        print("[OK] Customers seeded successfully.")

    # 3. Accounts
    if db.query(Account).count() == 0:
        accounts = [
            Account(account_id=201, customer_id=101, branch_id=1, account_type='Savings', balance=Decimal('85000.00'), opening_date=date(2021, 3, 16), account_status='Active'),
            Account(account_id=202, customer_id=101, branch_id=1, account_type='Current', balance=Decimal('125000.00'), opening_date=date(2021, 9, 10), account_status='Active'),
            Account(account_id=203, customer_id=102, branch_id=3, account_type='Savings', balance=Decimal('42000.00'), opening_date=date(2021, 6, 22), account_status='Active'),
            Account(account_id=204, customer_id=103, branch_id=1, account_type='Savings', balance=Decimal('62000.00'), opening_date=date(2022, 1, 12), account_status='Active'),
            Account(account_id=205, customer_id=104, branch_id=2, account_type='Savings', balance=Decimal('195000.00'), opening_date=date(2022, 4, 20), account_status='Active'),
            Account(account_id=206, customer_id=105, branch_id=4, account_type='Current', balance=Decimal('310000.00'), opening_date=date(2022, 8, 8), account_status='Active'),
            Account(account_id=207, customer_id=106, branch_id=3, account_type='Savings', balance=Decimal('28000.00'), opening_date=date(2023, 2, 16), account_status='Active'),
            Account(account_id=208, customer_id=107, branch_id=5, account_type='Savings', balance=Decimal('54000.00'), opening_date=date(2023, 5, 25), account_status='Active'),
            Account(account_id=209, customer_id=108, branch_id=2, account_type='Current', balance=Decimal('78000.00'), opening_date=date(2023, 9, 15), account_status='Active'),
            Account(account_id=210, customer_id=109, branch_id=6, account_type='Savings', balance=Decimal('18500.00'), opening_date=date(2024, 1, 18), account_status='Active'),
            Account(account_id=211, customer_id=103, branch_id=2, account_type='Current', balance=Decimal('5000.00'), opening_date=date(2024, 2, 1), account_status='Inactive'),
            Account(account_id=212, customer_id=104, branch_id=1, account_type='Savings', balance=Decimal('15000.00'), opening_date=date(2024, 3, 15), account_status='Active')
        ]
        db.add_all(accounts)
        db.commit()
        print("[OK] Accounts seeded successfully.")

    # 4. Transactions
    if db.query(Transaction).count() == 0:
        transactions = [
            Transaction(transaction_id=301, account_id=201, transaction_type='Deposit', amount=Decimal('20000.00'), transaction_date=date(2024, 1, 5), description='Salary credit'),
            Transaction(transaction_id=302, account_id=201, transaction_type='Withdrawal', amount=Decimal('5000.00'), transaction_date=date(2024, 1, 12), description='ATM withdrawal'),
            Transaction(transaction_id=303, account_id=202, transaction_type='Deposit', amount=Decimal('50000.00'), transaction_date=date(2024, 1, 15), description='Client payment'),
            Transaction(transaction_id=304, account_id=203, transaction_type='Deposit', amount=Decimal('15000.00'), transaction_date=date(2024, 1, 20), description='Cash deposit'),
            Transaction(transaction_id=305, account_id=204, transaction_type='Deposit', amount=Decimal('25000.00'), transaction_date=date(2024, 1, 25), description='Consulting fee'),
            Transaction(transaction_id=306, account_id=205, transaction_type='Deposit', amount=Decimal('80000.00'), transaction_date=date(2024, 2, 2), description='Business revenue'),
            Transaction(transaction_id=307, account_id=205, transaction_type='Withdrawal', amount=Decimal('12000.00'), transaction_date=date(2024, 2, 10), description='Vendor payment'),
            Transaction(transaction_id=308, account_id=206, transaction_type='Deposit', amount=Decimal('100000.00'), transaction_date=date(2024, 2, 15), description='Direct transfer'),
            Transaction(transaction_id=309, account_id=206, transaction_type='Withdrawal', amount=Decimal('25000.00'), transaction_date=date(2024, 2, 22), description='Equipment purchase'),
            Transaction(transaction_id=310, account_id=207, transaction_type='Deposit', amount=Decimal('10000.00'), transaction_date=date(2024, 3, 1), description='Freelance stipend'),
            Transaction(transaction_id=311, account_id=208, transaction_type='Deposit', amount=Decimal('30000.00'), transaction_date=date(2024, 3, 8), description='Quarterly bonus'),
            Transaction(transaction_id=312, account_id=209, transaction_type='Withdrawal', amount=Decimal('15000.00'), transaction_date=date(2024, 3, 14), description='Office supplies'),
            Transaction(transaction_id=313, account_id=201, transaction_type='Deposit', amount=Decimal('35000.00'), transaction_date=date(2024, 3, 20), description='Tax refund'),
            Transaction(transaction_id=314, account_id=202, transaction_type='Withdrawal', amount=Decimal('18000.00'), transaction_date=date(2024, 3, 25), description='Utility bill settlement'),
            Transaction(transaction_id=315, account_id=210, transaction_type='Deposit', amount=Decimal('12000.00'), transaction_date=date(2024, 4, 2), description='Opening deposit'),
            Transaction(transaction_id=316, account_id=205, transaction_type='Deposit', amount=Decimal('45000.00'), transaction_date=date(2024, 4, 10), description='Dividend credit'),
            Transaction(transaction_id=317, account_id=206, transaction_type='Deposit', amount=Decimal('65000.00'), transaction_date=date(2024, 4, 18), description='Retainer fee')
        ]
        db.add_all(transactions)
        db.commit()
        print("[OK] Transactions seeded successfully.")

    # 5. Loans
    if db.query(Loan).count() == 0:
        loans = [
            Loan(loan_id=401, customer_id=101, loan_amount=Decimal('500000.00'), interest_rate=Decimal('8.50'), loan_date=date(2022, 5, 10)),
            Loan(loan_id=402, customer_id=103, loan_amount=Decimal('1200000.00'), interest_rate=Decimal('7.75'), loan_date=date(2022, 11, 20)),
            Loan(loan_id=403, customer_id=104, loan_amount=Decimal('2500000.00'), interest_rate=Decimal('8.25'), loan_date=date(2023, 3, 15)),
            Loan(loan_id=404, customer_id=105, loan_amount=Decimal('3500000.00'), interest_rate=Decimal('9.00'), loan_date=date(2023, 7, 1)),
            Loan(loan_id=405, customer_id=107, loan_amount=Decimal('750000.00'), interest_rate=Decimal('8.80'), loan_date=date(2023, 10, 12)),
            Loan(loan_id=406, customer_id=108, loan_amount=Decimal('450000.00'), interest_rate=Decimal('9.50'), loan_date=date(2024, 2, 28))
        ]
        db.add_all(loans)
        db.commit()
        print("[OK] Loans seeded successfully.")

    # 6. Employees
    if db.query(Employee).count() == 0:
        employees = [
            Employee(employee_id=501, employee_name='Venkatesh Rao', position='Branch Manager', salary=Decimal('95000.00'), joining_date=date(2020, 1, 15), branch_id=1),
            Employee(employee_id=502, employee_name='Lakshmi Narayanan', position='Assistant Manager', salary=Decimal('75000.00'), joining_date=date(2021, 4, 10), branch_id=1),
            Employee(employee_id=503, employee_name='Arjun Reddy', position='Loan Officer', salary=Decimal('58000.00'), joining_date=date(2022, 7, 1), branch_id=2),
            Employee(employee_id=504, employee_name='Divya Krishnan', position='Senior Cashier', salary=Decimal('48000.00'), joining_date=date(2021, 11, 20), branch_id=3),
            Employee(employee_id=505, employee_name='Manish Tiwari', position='Relationship Manager', salary=Decimal('62000.00'), joining_date=date(2023, 1, 15), branch_id=4),
            Employee(employee_id=506, employee_name='Pooja Hegde', position='Loan Officer', salary=Decimal('54000.00'), joining_date=date(2023, 6, 1), branch_id=1),
            Employee(employee_id=507, employee_name='Sanjay Gupta', position='Branch Manager', salary=Decimal('92000.00'), joining_date=date(2023, 9, 10), branch_id=5),
            Employee(employee_id=508, employee_name='Nisha Sharma', position='Customer Service Rep', salary=Decimal('42000.00'), joining_date=date(2024, 2, 1), branch_id=2)
        ]
        db.add_all(employees)
        db.commit()
        print("[OK] Employees seeded successfully.")

    # 7. Default System Users
    admin_user = db.query(User).filter_by(username=Config.DEFAULT_ADMIN_USERNAME).first()
    if not admin_user:
        admin = User(
            username=Config.DEFAULT_ADMIN_USERNAME,
            email=Config.DEFAULT_ADMIN_EMAIL,
            role='admin',
            employee_id=501,
            is_active=True
        )
        admin.set_password(Config.DEFAULT_ADMIN_PASSWORD)
        db.add(admin)
        db.commit()
        print(f"[OK] Default Admin user '{Config.DEFAULT_ADMIN_USERNAME}' created.")

    emp_user = db.query(User).filter_by(username=Config.DEFAULT_EMPLOYEE_USERNAME).first()
    if not emp_user:
        employee = User(
            username=Config.DEFAULT_EMPLOYEE_USERNAME,
            email=Config.DEFAULT_EMPLOYEE_EMAIL,
            role='employee',
            employee_id=503,
            is_active=True
        )
        employee.set_password(Config.DEFAULT_EMPLOYEE_PASSWORD)
        db.add(employee)
        db.commit()
        print(f"[OK] Default Employee user '{Config.DEFAULT_EMPLOYEE_USERNAME}' created.")

def init_database():
    """Complete database setup: creates tables, views, and seeds data."""
    print("="*60)
    print(f"Initializing Banking Management System Database on: {engine.url.drivername}")
    print("="*60)
    
    # Create all tables defined in Base metadata
    Base.metadata.create_all(bind=engine)
    print("[OK] Tables verified/created successfully.")

    with get_db() as db:
        create_views(db)
        create_procedures(db)
        seed_sample_data(db)

    print("[OK] Database initialization complete!")
    print("="*60)

if __name__ == '__main__':
    init_database()

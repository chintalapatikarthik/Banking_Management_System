import os
import sys
from datetime import datetime, date
from decimal import Decimal

# Add parent directory to path so imports work when executed directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import engine, Base, get_db
from app.models import Branch, Customer, Account, Transaction, Loan, Employee, User, QueryHistory
from app.config import Config
from sqlalchemy import text

def create_views(db):
    """Create database views for analysis, compatible with MySQL and SQLite."""
    views_sql = [
        # Q26. View for customer accounts
        """
        CREATE VIEW IF NOT EXISTS vw_customer_accounts AS
        SELECT c.customer_id, c.name AS customer_name, c.email, c.phone,
               a.account_id, a.account_type, a.balance, a.opening_date
        FROM Customers c
        INNER JOIN Accounts a ON c.customer_id = a.customer_id;
        """,
        # Q27. View for transaction details
        """
        CREATE VIEW IF NOT EXISTS vw_transaction_details AS
        SELECT t.transaction_id, t.account_id, c.customer_id,
               c.name AS customer_name, t.transaction_type, t.amount, t.transaction_date
        FROM transactions t
        INNER JOIN Accounts a ON t.account_id = a.account_id
        INNER JOIN Customers c ON a.customer_id = c.customer_id;
        """,
        # Q28. View for loan details with customers
        """
        CREATE VIEW IF NOT EXISTS vw_loan_details_customers AS
        SELECT l.loan_id, c.customer_id, c.name AS customer_name, c.email,
               l.loan_amount, l.interest_rate, l.loan_date
        FROM Loans l
        INNER JOIN Customers c ON l.customer_id = c.customer_id;
        """,
        # Q29. View for total balance per customer
        """
        CREATE VIEW IF NOT EXISTS vw_total_balance_per_customer AS
        SELECT c.customer_id, c.name AS customer_name,
               COALESCE(SUM(a.balance), 0.00) AS total_balance
        FROM Customers c
        LEFT JOIN Accounts a ON c.customer_id = a.customer_id
        GROUP BY c.customer_id, c.name;
        """,
        # Q30. View for high value transactions (amount > 50000)
        """
        CREATE VIEW IF NOT EXISTS vw_high_value_transactions AS
        SELECT transaction_id, account_id, transaction_type, amount, transaction_date
        FROM transactions
        WHERE amount > 50000;
        """,
        # Backwards-compatible aliases with v_ prefix
        "CREATE VIEW IF NOT EXISTS v_customer_accounts AS SELECT * FROM vw_customer_accounts;",
        "CREATE VIEW IF NOT EXISTS v_transaction_details AS SELECT * FROM vw_transaction_details;",
        "CREATE VIEW IF NOT EXISTS v_customer_loans AS SELECT * FROM vw_loan_details_customers;",
        "CREATE VIEW IF NOT EXISTS v_customer_total_balance AS SELECT * FROM vw_total_balance_per_customer;",
        "CREATE VIEW IF NOT EXISTS v_high_value_transactions AS SELECT * FROM vw_high_value_transactions;"
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
            Branch(branch_id=401, branch_name='Madhapur Branch', location='Madhapur, Hyderabad'),
            Branch(branch_id=402, branch_name='Kukatpally Branch', location='Kukatpally, Hyderabad'),
            Branch(branch_id=403, branch_name='Guntur Main Branch', location='Guntur, Andhra Pradesh'),
            Branch(branch_id=404, branch_name='Vijayawada Branch', location='Vijayawada, Andhra Pradesh')
        ]
        db.add_all(branches)
        db.commit()
        print("[OK] Branches seeded successfully.")

    # 2. Customers
    if db.query(Customer).count() == 0:
        customers = [
            Customer(customer_id=1, name='Aarav Reddy', email='aarav.reddy@example.com', phone='9876501001', address='Madhapur, Hyderabad', registration_date=date(2021, 2, 15)),
            Customer(customer_id=2, name='Priya Sharma', email='priya.sharma@example.com', phone='9876501002', address='Kukatpally, Hyderabad', registration_date=date(2022, 6, 10)),
            Customer(customer_id=3, name='Rahul Varma', email='rahul.varma@example.com', phone='9876501003', address='Gachibowli, Hyderabad', registration_date=date(2020, 11, 22)),
            Customer(customer_id=4, name='Sneha Rao', email='sneha.rao@example.com', phone='9876501004', address='Vijayawada, Andhra Pradesh', registration_date=date(2023, 1, 5)),
            Customer(customer_id=5, name='Kiran Kumar', email='kiran.kumar@example.com', phone='9876501005', address='Guntur, Andhra Pradesh', registration_date=date(2021, 8, 19)),
            Customer(customer_id=6, name='Meera Nair', email='meera.nair@example.com', phone='9876501006', address='Miyapur, Hyderabad', registration_date=date(2024, 3, 12)),
            Customer(customer_id=7, name='Arjun Patel', email='arjun.patel@example.com', phone='9876501007', address='Bengaluru, Karnataka', registration_date=date(2022, 9, 30)),
            Customer(customer_id=8, name='Divya Lakshmi', email='divya.lakshmi@example.com', phone='9876501008', address='Secunderabad, Hyderabad', registration_date=date(2020, 4, 17)),
            Customer(customer_id=9, name='Vikram Singh', email='vikram.singh@example.com', phone='9876501009', address='Chennai, Tamil Nadu', registration_date=date(2023, 7, 25)),
            Customer(customer_id=10, name='Ananya Das', email='ananya.das@example.com', phone='9876501010', address='Warangal, Telangana', registration_date=date(2024, 5, 8))
        ]
        db.add_all(customers)
        db.commit()
        print("[OK] Customers seeded successfully.")

    # 3. Accounts
    if db.query(Account).count() == 0:
        accounts = [
            Account(account_id=101, customer_id=1, branch_id=401, account_type='Savings', balance=Decimal('85000.00'), opening_date=date(2021, 2, 20), account_status='Active'),
            Account(account_id=102, customer_id=1, branch_id=401, account_type='Current', balance=Decimal('150000.00'), opening_date=date(2022, 1, 15), account_status='Active'),
            Account(account_id=103, customer_id=2, branch_id=402, account_type='Savings', balance=Decimal('42000.00'), opening_date=date(2022, 6, 15), account_status='Active'),
            Account(account_id=104, customer_id=3, branch_id=401, account_type='Savings', balance=Decimal('67500.00'), opening_date=date(2020, 12, 1), account_status='Active'),
            Account(account_id=105, customer_id=3, branch_id=401, account_type='Current', balance=Decimal('210000.00'), opening_date=date(2021, 5, 10), account_status='Active'),
            Account(account_id=106, customer_id=4, branch_id=404, account_type='Savings', balance=Decimal('18000.00'), opening_date=date(2023, 1, 10), account_status='Active'),
            Account(account_id=107, customer_id=5, branch_id=403, account_type='Savings', balance=Decimal('52000.00'), opening_date=date(2021, 8, 25), account_status='Active'),
            Account(account_id=108, customer_id=6, branch_id=402, account_type='Savings', balance=Decimal('9500.00'), opening_date=date(2024, 3, 15), account_status='Inactive'),
            Account(account_id=109, customer_id=7, branch_id=401, account_type='Current', balance=Decimal('125000.00'), opening_date=date(2022, 10, 5), account_status='Active'),
            Account(account_id=110, customer_id=8, branch_id=401, account_type='Savings', balance=Decimal('73000.00'), opening_date=date(2020, 4, 25), account_status='Active'),
            Account(account_id=111, customer_id=8, branch_id=401, account_type='Current', balance=Decimal('35000.00'), opening_date=date(2021, 7, 12), account_status='Active'),
            Account(account_id=112, customer_id=9, branch_id=401, account_type='Savings', balance=Decimal('61000.00'), opening_date=date(2023, 8, 1), account_status='Inactive')
        ]
        db.add_all(accounts)
        db.commit()
        print("[OK] Accounts seeded successfully.")

    # 4. Transactions
    if db.query(Transaction).count() == 0:
        transactions = [
            Transaction(transaction_id=1001, account_id=101, transaction_type='Deposit', amount=Decimal('20000.00'), transaction_date=date(2024, 1, 5), description='Cash deposit'),
            Transaction(transaction_id=1002, account_id=101, transaction_type='Withdrawal', amount=Decimal('5000.00'), transaction_date=date(2024, 1, 12), description='ATM withdrawal'),
            Transaction(transaction_id=1003, account_id=101, transaction_type='Deposit', amount=Decimal('15000.00'), transaction_date=date(2024, 2, 3), description='Account transfer deposit'),
            Transaction(transaction_id=1004, account_id=102, transaction_type='Deposit', amount=Decimal('50000.00'), transaction_date=date(2024, 1, 8), description='Client payment'),
            Transaction(transaction_id=1005, account_id=102, transaction_type='Withdrawal', amount=Decimal('12000.00'), transaction_date=date(2024, 2, 14), description='Vendor payment'),
            Transaction(transaction_id=1006, account_id=102, transaction_type='Transfer', amount=Decimal('25000.00'), transaction_date=date(2024, 3, 2), description='Funds transfer'),
            Transaction(transaction_id=1007, account_id=103, transaction_type='Deposit', amount=Decimal('8000.00'), transaction_date=date(2024, 1, 20), description='Cash deposit'),
            Transaction(transaction_id=1008, account_id=103, transaction_type='Withdrawal', amount=Decimal('3000.00'), transaction_date=date(2024, 2, 18), description='ATM withdrawal'),
            Transaction(transaction_id=1009, account_id=104, transaction_type='Deposit', amount=Decimal('30000.00'), transaction_date=date(2024, 1, 11), description='Salary credit'),
            Transaction(transaction_id=1010, account_id=104, transaction_type='Withdrawal', amount=Decimal('7000.00'), transaction_date=date(2024, 3, 10), description='Online payment'),
            Transaction(transaction_id=1011, account_id=105, transaction_type='Deposit', amount=Decimal('75000.00'), transaction_date=date(2024, 1, 16), description='Business revenue'),
            Transaction(transaction_id=1012, account_id=105, transaction_type='Transfer', amount=Decimal('20000.00'), transaction_date=date(2024, 2, 21), description='Supplier settlement'),
            Transaction(transaction_id=1013, account_id=105, transaction_type='Withdrawal', amount=Decimal('15000.00'), transaction_date=date(2024, 3, 19), description='Equipment purchase'),
            Transaction(transaction_id=1014, account_id=106, transaction_type='Deposit', amount=Decimal('6000.00'), transaction_date=date(2024, 2, 2), description='Cash deposit'),
            Transaction(transaction_id=1015, account_id=107, transaction_type='Deposit', amount=Decimal('18000.00'), transaction_date=date(2024, 1, 25), description='Cash deposit'),
            Transaction(transaction_id=1016, account_id=107, transaction_type='Withdrawal', amount=Decimal('4000.00'), transaction_date=date(2024, 2, 27), description='ATM withdrawal'),
            Transaction(transaction_id=1017, account_id=109, transaction_type='Deposit', amount=Decimal('40000.00'), transaction_date=date(2024, 1, 9), description='Direct deposit'),
            Transaction(transaction_id=1018, account_id=109, transaction_type='Transfer', amount=Decimal('10000.00'), transaction_date=date(2024, 3, 5), description='Transfer payment'),
            Transaction(transaction_id=1019, account_id=110, transaction_type='Deposit', amount=Decimal('22000.00'), transaction_date=date(2024, 1, 13), description='Dividend deposit'),
            Transaction(transaction_id=1020, account_id=110, transaction_type='Withdrawal', amount=Decimal('9000.00'), transaction_date=date(2024, 2, 16), description='Branch withdrawal'),
            Transaction(transaction_id=1021, account_id=111, transaction_type='Deposit', amount=Decimal('12000.00'), transaction_date=date(2024, 1, 30), description='Cash deposit'),
            Transaction(transaction_id=1022, account_id=111, transaction_type='Withdrawal', amount=Decimal('2500.00'), transaction_date=date(2024, 3, 12), description='ATM withdrawal'),
            Transaction(transaction_id=1023, account_id=101, transaction_type='Transfer', amount=Decimal('7500.00'), transaction_date=date(2024, 4, 4), description='Account transfer'),
            Transaction(transaction_id=1024, account_id=105, transaction_type='Deposit', amount=Decimal('35000.00'), transaction_date=date(2024, 4, 15), description='Retainer deposit')
        ]
        db.add_all(transactions)
        db.commit()
        print("[OK] Transactions seeded successfully.")

    # 5. Loans
    if db.query(Loan).count() == 0:
        loans = [
            Loan(loan_id=201, customer_id=1, loan_amount=Decimal('500000.00'), interest_rate=Decimal('8.50'), loan_date=date(2022, 3, 10)),
            Loan(loan_id=202, customer_id=2, loan_amount=Decimal('250000.00'), interest_rate=Decimal('9.00'), loan_date=date(2023, 6, 18)),
            Loan(loan_id=203, customer_id=3, loan_amount=Decimal('1200000.00'), interest_rate=Decimal('7.75'), loan_date=date(2021, 9, 5)),
            Loan(loan_id=204, customer_id=5, loan_amount=Decimal('400000.00'), interest_rate=Decimal('8.25'), loan_date=date(2022, 11, 22)),
            Loan(loan_id=205, customer_id=7, loan_amount=Decimal('850000.00'), interest_rate=Decimal('8.00'), loan_date=date(2023, 2, 14)),
            Loan(loan_id=206, customer_id=8, loan_amount=Decimal('150000.00'), interest_rate=Decimal('9.25'), loan_date=date(2024, 1, 9))
        ]
        db.add_all(loans)
        db.commit()
        print("[OK] Loans seeded successfully.")

    # 6. Employees
    if db.query(Employee).count() == 0:
        employees = [
            Employee(employee_id=301, employee_name='Suresh Babu', position='Branch Manager', salary=Decimal('85000.00'), joining_date=date(2020, 4, 15), branch_id=401),
            Employee(employee_id=302, employee_name='Nisha Gupta', position='Accountant', salary=Decimal('52000.00'), joining_date=date(2021, 7, 1), branch_id=401),
            Employee(employee_id=303, employee_name='Ramesh Naidu', position='Cashier', salary=Decimal('38000.00'), joining_date=date(2022, 11, 10), branch_id=402),
            Employee(employee_id=304, employee_name='Pooja Menon', position='Loan Officer', salary=Decimal('61000.00'), joining_date=date(2023, 2, 20), branch_id=403),
            Employee(employee_id=305, employee_name='Imran Khan', position='Customer Support', salary=Decimal('42000.00'), joining_date=date(2024, 1, 8), branch_id=402),
            Employee(employee_id=306, employee_name='Kavya Reddy', position='Operations Lead', salary=Decimal('70000.00'), joining_date=date(2021, 12, 5), branch_id=404)
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
            employee_id=301,
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
            employee_id=303,
            is_active=True
        )
        employee.set_password(Config.DEFAULT_EMPLOYEE_PASSWORD)
        db.add(employee)
        db.commit()
        print(f"[OK] Default Employee user '{Config.DEFAULT_EMPLOYEE_USERNAME}' created.")

def clear_all_tables(db):
    """Truncate/clear all tables for clean reseeding."""
    table_names = ['query_history', 'transactions', 'loans', 'accounts', 'users', 'employees', 'branches', 'customers']
    # If SQLite, disable foreign key checks temporarily
    is_sqlite = 'sqlite' in str(engine.url)
    if is_sqlite:
        db.execute(text("PRAGMA foreign_keys = OFF;"))
    else:
        db.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
    
    for tbl in table_names:
        try:
            db.execute(text(f"DELETE FROM {tbl};"))
        except Exception as e:
            print(f"Notice: clearing {tbl}: {e}")
    
    if is_sqlite:
        db.execute(text("PRAGMA foreign_keys = ON;"))
    else:
        db.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
    db.commit()
    print("[OK] All tables cleared successfully.")

def init_database(reset=False):
    """Complete database setup: creates tables, views, and seeds data."""
    print("="*60)
    print(f"Initializing Banking Management System Database on: {engine.url.drivername}")
    print("="*60)
    
    # Create all tables defined in Base metadata
    Base.metadata.create_all(bind=engine)
    print("[OK] Tables verified/created successfully.")

    with get_db() as db:
        if reset:
            clear_all_tables(db)
        create_views(db)
        create_procedures(db)
        seed_sample_data(db)

    print("[OK] Database initialization complete!")
    print("="*60)

if __name__ == '__main__':
    reset = '--reset' in sys.argv
    init_database(reset=reset)

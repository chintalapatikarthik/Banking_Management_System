# 🏦 Banking Management System
### *Enterprise Full-Stack Python & SQL Web Application*

[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12-blue?logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Framework-Flask%203.1-black?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Database](https://img.shields.io/badge/SQL%20Database-MySQL%208.x%20%2F%20SQLite-00758F?logo=mysql&logoColor=white)](https://mysql.com)
[![Testing](https://img.shields.io/badge/Tests-22%20Passed%20(100%25)-success?logo=pytest&logoColor=white)](https://pytest.org)
[![UI](https://img.shields.io/badge/Frontend-Bootstrap%205%20%2B%20Chart.js-7952B3?logo=bootstrap&logoColor=white)](https://getbootstrap.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

An enterprise-grade, responsive, database-driven Banking Management Web Application engineered with Python, Flask, SQLAlchemy ORM, raw SQL analytics, Bootstrap 5, and Chart.js.

Built for administrators, branch managers, and banking officers to oversee customer onboarding, multi-tier account portfolios, atomic financial transactions (deposits, withdrawals, inter-account transfers), loan disbursements, employee allocations, branch operations, and a dedicated **SQL Query Lab** executing all 41 canonical database questions from `Banking_Management_System.sql`.

---

## 📑 Table of Contents
1. [Key Features & Highlights](#-key-features--highlights)
2. [Technology Stack](#-technology-stack)
3. [System Architecture & Directory Structure](#-system-architecture--directory-structure)
4. [Database Design & Schema](#-database-design--schema)
5. [Canonical 41 SQL Questions Curriculum](#-canonical-41-sql-questions-curriculum)
6. [Dedicated SQL Learning & Execution Modules](#-dedicated-sql-learning--execution-modules)
7. [RESTful SQL API Endpoints](#-restful-sql-api-endpoints)
8. [Security & Role-Based Access Control](#-security--role-based-access-control)
9. [Getting Started (Local Installation)](#-getting-started-local-installation)
10. [Automated Testing Suite (22/22 Tests Passing)](#-automated-testing-suite)
11. [Public Deployment Guide](#-public-deployment-guide)
12. [Default Demo Credentials](#-default-demo-credentials)

---

## 🌟 Key Features & Highlights

- **Executive Banking Dashboard**:
  - 7 Real-time KPI Cards: Total Customers, Accounts, Total Deposits, Transaction Logs, Loan Liabilities, Employees, and Branches.
  - 6 Interactive Chart.js Visualizations: Monthly Transaction Activity, Deposit vs. Withdrawal Ratio, Account Types Distribution, Customer Acquisition Trends, Branch-wise Balance, and Top Loan Portfolio.
- **Customer Lifecycle Management**:
  - Full CRUD operations with search by name/ID, location filtering, and dedicated profile view displaying all linked accounts, transaction statements, and credit facilities.
- **Account Portfolio**:
  - Open Savings & Current accounts with optional opening deposits.
  - Filter by account type, active/inactive status, and real-time status toggling.
- **Financial Transactions Engine**:
  - **Deposit**: Real-time balance crediting with instant calculation preview.
  - **Withdrawal**: Overdraft detection preventing negative account balances.
  - **Atomic Fund Transfer**: Executes debits and credits in an isolated ACID database transaction (`COMMIT`/`ROLLBACK`).
- **Credit & Loan Management**:
  - Disburse new loans, track interest rates, aggregate total portfolio liabilities, and rank largest borrowers.
- **Human Resources & Branches**:
  - Staff onboarding, salary management, branch assignment, and branch liquidity tracking.
- **Interactive SQL Query Lab (`/sql-lab`)**:
  - Interactive workbench executing all **41 canonical SQL questions** directly against the live database engine.
  - Syntax-highlighted code editor, Copy SQL, Reset Query, View Explanation, and Reset Sample Data.
  - Category selector filter pills, instant keyword search, and Question cards (Q1 to Q41).
  - Dynamic execution metrics (latency in milliseconds, rows returned, status code, database engine).
- **Dedicated SQL Views Module (`/sql-views`)**:
  - Showcases all 5 predefined database views (`vw_customer_accounts`, `vw_transaction_details`, `vw_loan_details_customers`, `vw_total_balance_per_customer`, `vw_high_value_transactions`).
  - View results button, DDL definition copy, and responsive data tables.
- **Dedicated Stored Procedures Module (`/stored-procedures`)**:
  - Interactive workbench for all 5 enterprise stored procedures (`sp_insert_new_customer`, `sp_update_account_balance`, `sp_display_account_transactions`, `sp_calculate_total_bank_balance`, `sp_list_customer_accounts`).
  - Input parameter forms with validation and real-time `CALL ...` statement preview.
- **Reports & Analytics with Chart.js (`/reports`)**:
  - Interactive visual reporting implementing all 6 analytical reports with Chart.js:
    1. Top 5 customers with highest balance (Horizontal Bar Chart)
    2. Most active customers (Bar Chart)
    3. Monthly transaction report (Multi-line Chart: Deposits, Withdrawals, Transfers)
    4. Branch with highest deposits (Bar Chart)
    5. Customer transaction analysis (Grouped Bar Chart)
    6. Highest loan customers (Bar Chart)
  - 1-click downloadable CSV exports for all reports.
- **Query Execution History (`/sql-history`)**:
  - Persistent database audit log recording every query execution, duration in ms, row count, user, and status.

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Backend** | Python 3.11 / 3.12, Flask 3.1, Werkzeug (Password Hashing), Flask-Login (Session Security) |
| **Database** | MySQL 8.x (Cloud / Enterprise) & SQLite (Portable Development / Testing) |
| **ORM & SQL** | SQLAlchemy 2.0 (ORM Models & Raw SQL Engine), PyMySQL Driver |
| **Frontend** | HTML5 Semantic, CSS3 (Slate & Indigo Modern Fintech Theme), JavaScript (ES6+) |
| **UI Framework** | Bootstrap 5.3, Bootstrap Icons, Google Fonts (Outfit & Inter) |
| **Data Visuals** | Chart.js 4.4 (Bar, Doughnut, Polar, Line, and Horizontal Bar charts) |
| **Testing** | Pytest 9.2 (22 Unit, Integration, and SQL Assertion tests) |
| **Production WSGI**| Gunicorn 26.2 |
| **Cloud Deployment**| Render, Railway, Vercel |

---

## 🏛️ System Architecture & Directory Structure

```
SqlProject/
├── app/
│   ├── __init__.py               # Flask application factory, Jinja filters, context processors
│   ├── config.py                 # Environment configuration & database URLs
│   ├── database.py               # Engine, thread-safe session, and raw SQL executor
│   ├── models.py                 # SQLAlchemy ORM models (Branch, Customer, Account, QueryHistory, etc.)
│   ├── auth.py                   # Flask-Login configuration & @admin_required decorators
│   ├── routes/
│   │   ├── auth_routes.py        # Login & logout handling
│   │   ├── dashboard_routes.py   # Overview dashboard & navigation shortcuts (/sql-lab, /sql-views, etc.)
│   │   ├── customer_routes.py    # Customer CRUD & profile views
│   │   ├── account_routes.py     # Account lifecycle & status toggles
│   │   ├── transaction_routes.py # Deposit, withdrawal, and atomic transfer
│   │   ├── loan_routes.py        # Loan disbursements & portfolio
│   │   ├── employee_routes.py    # Staff & officer directory
│   │   ├── branch_routes.py      # Branch network management
│   │   ├── sql_ops_routes.py     # SQL Query Lab, Views, Stored Procedures, and History views
│   │   ├── sql_api_routes.py     # Dedicated RESTful API endpoints (/api/sql/execute, etc.)
│   │   └── report_routes.py      # Executive reporting with CSV downloads
│   ├── services/
│   │   ├── bank_service.py       # Atomic business logic & financial validations
│   │   ├── analytics_service.py  # Real-time SQL aggregations for Chart.js
│   │   └── sql_queries.py        # Registry & execution engine for all 41 SQL questions
│   ├── static/
│   │   ├── css/style.css         # Modern fintech design system
│   │   └── js/
│   │       ├── main.js           # UI interactions, real-time clock, balance calculations
│   │       └── charts.js         # Chart.js initialization & dynamic fetching
│   └── templates/                # Jinja2 responsive templates
│       ├── base.html             # Master layout with left sidebar & topbar
│       ├── login.html            # Sign-in portal with 1-click demo presets
│       ├── dashboard.html        # Executive analytics dashboard
│       ├── customers/            # Customer list, form, and view
│       ├── accounts/             # Account list, form, and view
│       ├── transactions/         # Ledger, deposit, withdraw, transfer
│       ├── loans/                # Portfolio list & form
│       ├── employees/            # Staff directory & form
│       ├── branches/             # Branch network & form
│       ├── sql_operations/       # SQL Query Lab modules
│       │   ├── index.html        # Interactive SQL Query Lab (Q1 - Q41)
│       │   ├── views.html        # Dedicated SQL Views module (Q26 - Q30)
│       │   ├── procedures.html   # Dedicated Stored Procedures Workbench (Q31 - Q35)
│       │   └── history.html      # Query Execution Audit Log
│       └── reports/              # 6 analytical reports with Chart.js visualizations
├── database/
│   ├── schema.sql                # MySQL 8.x DDL schema script
│   ├── sample_data.sql           # Canonical Indian banking dataset (10 customers, 12 accounts, etc.)
│   ├── views.sql                 # 5 SQL view definitions
│   ├── procedures.sql            # MySQL stored procedures definitions
│   └── init_db.py                # Idempotent database initializer & --reset CLI
├── tests/
│   ├── conftest.py               # Pytest test fixtures & automatic database reset hooks
│   ├── test_auth.py              # Authentication & role authorization tests
│   ├── test_banking_ops.py       # Financial transactions & ACID integrity tests
│   └── test_sql_queries.py       # All 41 SQL questions & API endpoints assertion tests
├── scripts/
│   └── verify_live_server.py     # Live server integration test runner
├── requirements.txt              # Production Python dependencies
├── run.py                        # Application entry point
└── README.md                     # Comprehensive system documentation
```

---

## 🗄️ Database Design & Schema

The relational database architecture models realistic core banking operations with strict referential integrity:

### Core Tables
1. **`branches`**: `branch_id` (PK), `branch_name`, `location`, `created_at`
2. **`customers`**: `customer_id` (PK), `name`, `email` (UNIQUE), `phone`, `address`, `registration_date`
3. **`accounts`**: `account_id` (PK), `customer_id` (FK -> customers), `branch_id` (FK -> branches), `account_type` ('Savings' / 'Current'), `balance` (DECIMAL(12,2) with CHECK >= 0), `opening_date`, `account_status` ('Active' / 'Inactive')
4. **`transactions`**: `transaction_id` (PK), `account_id` (FK -> accounts), `transaction_type` ('Deposit', 'Withdrawal', 'Transfer'), `amount` (DECIMAL(10,2) with CHECK > 0), `transaction_date`, `description`
5. **`loans`**: `loan_id` (PK), `customer_id` (FK -> customers), `loan_amount` (DECIMAL(12,2)), `interest_rate` (DECIMAL(5,2)), `loan_date`
6. **`employees`**: `employee_id` (PK), `employee_name`, `position`, `salary` (DECIMAL(10,2)), `joining_date`, `branch_id` (FK -> branches)
7. **`users`**: `user_id` (PK), `username` (UNIQUE), `email` (UNIQUE), `password_hash`, `role` ('admin' / 'employee'), `employee_id` (FK -> employees), `is_active`
8. **`query_history`**: `history_id` (PK), `user_id` (FK -> users), `username`, `question_id`, `query_key`, `query_title`, `category`, `sql_text`, `status`, `execution_time_ms`, `row_count`, `error_message`, `executed_at`

---

## 📊 Canonical 41 SQL Questions Curriculum

All 41 questions from `Banking_Management_System.sql` are integrated into the system:

### 1. Basic Queries (Q1 – Q4)
- **Q1**: Display accounts with balance greater than 50000.  
  `SELECT * FROM Accounts WHERE balance > 50000;`
- **Q2**: Show all customers from Hyderabad.  
  `SELECT * FROM Customers WHERE address LIKE '%Hyderabad%';`
- **Q3**: List savings accounts.  
  `SELECT * FROM Accounts WHERE account_type = 'Savings';`
- **Q4**: Display employees joined after 2022.  
  `SELECT * FROM Employees WHERE joining_date >= '2023-01-01';`

### 2. Joins (Q5 – Q10)
- **Q5**: Show customer name with their accounts.  
  `SELECT c.customer_id, c.name AS customer_name, a.account_id, a.account_type, a.balance, a.opening_date FROM Customers c INNER JOIN Accounts a ON c.customer_id = a.customer_id;`
- **Q6**: Display account with transaction details.  
  `SELECT a.account_id, a.account_type, a.balance, t.transaction_id, t.transaction_type, t.amount, t.transaction_date FROM Accounts a INNER JOIN Transactions t ON a.account_id = t.account_id;`
- **Q7**: Show loan details with customer information.  
  `SELECT l.loan_id, c.customer_id, c.name AS customer_name, l.loan_amount, l.interest_rate, l.loan_date FROM Loans l INNER JOIN Customers c ON l.customer_id = c.customer_id;`
- **Q8**: Assign branch to employees & verify schema.  
  `ALTER TABLE employees ADD COLUMN branch_id INT; ... SELECT e.employee_id, e.employee_name, e.branch_id, b.branch_name FROM Employees e LEFT JOIN Branches b ON e.branch_id = b.branch_id;`
- **Q9**: List employees with their branch.  
  `SELECT e.employee_id, e.employee_name, e.position, b.branch_id, b.branch_name, b.location FROM Employees e INNER JOIN Branches b ON e.branch_id = b.branch_id;`
- **Q10**: Show customers with their transactions.  
  `SELECT c.customer_id, c.name AS customer_name, a.account_id, t.transaction_id, t.transaction_type, t.amount, t.transaction_date FROM Customers c INNER JOIN Accounts a ON c.customer_id = a.customer_id INNER JOIN Transactions t ON a.account_id = t.account_id;`

### 3. Aggregate Functions (Q11 – Q15)
- **Q11**: Count total customers.  
  `SELECT COUNT(*) AS total_customers FROM Customers;`
- **Q12**: Find average account balance.  
  `SELECT ROUND(AVG(balance), 2) AS average_account_balance FROM Accounts;`
- **Q13**: Calculate total loan amount.  
  `SELECT SUM(loan_amount) AS total_loan_amount FROM Loans;`
- **Q14**: Count total transactions.  
  `SELECT COUNT(*) AS total_transactions FROM Transactions;`
- **Q15**: Find highest account balance.  
  `SELECT MAX(balance) AS highest_account_balance FROM Accounts;`

### 4. Subqueries (Q16 – Q20)
- **Q16**: Find customers who have no accounts.  
  `SELECT c.* FROM Customers c WHERE NOT EXISTS (SELECT 1 FROM Accounts a WHERE a.customer_id = c.customer_id);`
- **Q17**: Find accounts with no transactions.  
  `SELECT a.* FROM Accounts a WHERE NOT EXISTS (SELECT 1 FROM Transactions t WHERE t.account_id = a.account_id);`
- **Q18**: Show accounts with balance greater than average.  
  `SELECT * FROM Accounts WHERE balance > (SELECT AVG(balance) FROM Accounts);`
- **Q19**: Find customers with loan amount above average.  
  `SELECT c.customer_id, c.name AS customer_name, l.loan_id, l.loan_amount FROM Customers c INNER JOIN Loans l ON c.customer_id = l.customer_id WHERE l.loan_amount > (SELECT AVG(loan_amount) FROM Loans);`
- **Q20**: Show transactions above average amount.  
  `SELECT * FROM Transactions WHERE amount > (SELECT AVG(amount) FROM Transactions);`

### 5. Updates & Deletes (Q21 – Q25)
- **Q21**: Update account balance.  
  `UPDATE Accounts SET balance = 90000.00 WHERE account_id = 101;`
- **Q22**: Change customer email.  
  `UPDATE Customers SET email = 'aarav.updated@example.com' WHERE customer_id = 1;`
- **Q23**: Update branch location.  
  `UPDATE Branches SET location = 'Hitech City, Hyderabad' WHERE branch_id = 401;`
- **Q24**: Delete inactive accounts.  
  `DELETE FROM Accounts WHERE account_status = 'Inactive';`
- **Q25**: Delete customers with no accounts.  
  `DELETE FROM Customers WHERE NOT EXISTS (SELECT 1 FROM Accounts a WHERE a.customer_id = Customers.customer_id) AND NOT EXISTS (SELECT 1 FROM Loans l WHERE l.customer_id = Customers.customer_id);`

### 6. Views (Q26 – Q30)
- **Q26**: Customer Accounts View (`vw_customer_accounts`).  
  `SELECT * FROM vw_customer_accounts;`
- **Q27**: Transaction Details View (`vw_transaction_details`).  
  `SELECT * FROM vw_transaction_details;`
- **Q28**: Loan Details with Customers View (`vw_loan_details_customers`).  
  `SELECT * FROM vw_loan_details_customers;`
- **Q29**: Total Balance per Customer View (`vw_total_balance_per_customer`).  
  `SELECT * FROM vw_total_balance_per_customer;`
- **Q30**: High Value Transactions View (`vw_high_value_transactions`).  
  `SELECT * FROM vw_high_value_transactions;`

### 7. Stored Procedures (Q31 – Q35)
- **Q31**: Insert New Customer (`sp_insert_new_customer`).  
  `CALL sp_insert_new_customer(11, 'Ravi Teja', 'ravi.teja@example.com', '9876501011', 'Guntur, Andhra Pradesh', '2024-06-01');`
- **Q32**: Update Account Balance (`sp_update_account_balance`).  
  `CALL sp_update_account_balance(101, 95000.00);`
- **Q33**: Display Transactions of an Account (`sp_display_account_transactions`).  
  `CALL sp_display_account_transactions(101);`
- **Q34**: Calculate Total Bank Balance (`sp_calculate_total_bank_balance`).  
  `CALL sp_calculate_total_bank_balance();`
- **Q35**: List Accounts of a Customer (`sp_list_customer_accounts`).  
  `CALL sp_list_customer_accounts(1);`

### 8. Reports / Analysis (Q36 – Q41)
- **Q36**: Top 5 customers with highest balance.  
  `SELECT c.customer_id, c.name, SUM(a.balance) FROM Customers c JOIN Accounts a GROUP BY c.customer_id ORDER BY 3 DESC LIMIT 5;`
- **Q37**: Most active customers.  
  `SELECT c.customer_id, c.name, COUNT(t.transaction_id) FROM Customers c JOIN Accounts a JOIN Transactions t GROUP BY c.customer_id ORDER BY 3 DESC LIMIT 10;`
- **Q38**: Monthly transaction report.  
  `SELECT SUBSTR(transaction_date, 1, 7) AS month_year, COUNT(*), SUM(amount), SUM(CASE WHEN transaction_type = 'Deposit' THEN amount ELSE 0 END) AS total_deposits ... FROM Transactions GROUP BY 1;`
- **Q39**: Branch with highest deposits.  
  `SELECT b.branch_id, b.branch_name, SUM(t.amount) AS total_deposits FROM Branches b JOIN Accounts a JOIN Transactions t WHERE t.transaction_type = 'Deposit' GROUP BY b.branch_id ORDER BY 3 DESC LIMIT 1;`
- **Q40**: Customer transaction analysis.  
  `SELECT c.customer_id, c.name, COUNT(t.transaction_id), SUM(CASE WHEN transaction_type = 'Deposit' THEN amount ELSE 0 END) ... FROM Customers c LEFT JOIN Accounts a LEFT JOIN Transactions t GROUP BY c.customer_id;`
- **Q41**: Highest loan customers.  
  `SELECT c.customer_id, c.name, SUM(l.loan_amount) FROM Customers c JOIN Loans l GROUP BY c.customer_id ORDER BY 3 DESC LIMIT 5;`

---

## 🌐 RESTful SQL API Endpoints

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/sql/questions` | List metadata for all 41 questions (ID, title, category, description, SQL) | Yes |
| `GET` | `/api/sql/categories` | Return 8 SQL categories with question counts and icons | Yes |
| `POST` | `/api/sql/execute` | Execute approved query or custom SQL with validation & logging | Yes |
| `GET` | `/api/sql/history` | Return recent execution logs (filter by category & status) | Yes |
| `POST` | `/api/sql/clear-history`| Clear execution audit logs | Admin Only |
| `POST` | `/api/sql/reset-sample-data` | Restore database to canonical sample dataset | Yes |

---

## 🔒 Security & Role-Based Access Control

- **Role-Based Execution Policies**:
  - `SELECT` queries, Views, and Reports can be run by all authenticated users.
  - `UPDATE` and `DELETE` operations are restricted to Administrators.
- **Destructive Command Blocking**:
  - `DROP`, `TRUNCATE`, and `ALTER` (destructive) statements are blocked in custom execution.
- **Audit Logging**:
  - All query executions, durations, affected row counts, and error states are recorded in `query_history`.
- **Database Transaction Management**:
  - All modifications execute inside atomic transaction blocks (`commit=True` / `rollback`).

---

## 🚀 Getting Started (Local Installation)

### 1. Clone & Setup Virtual Environment
```bash
git clone <repository-url>
cd SqlProject

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1    # On Windows
# source .venv/bin/activate     # On Linux / macOS
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Initialize Database & Canonical Sample Data
```bash
python database/init_db.py --reset
```

### 4. Run Flask Server
```bash
python run.py
```
Open **`http://127.0.0.1:5000`** in your browser.

---

## 🧪 Automated Testing Suite

The application includes an extensive automated test suite covering unit tests, integration tests, stored procedures, views, API endpoints, and ACID transactions:

```bash
python -m pytest -v
```

### Test Results (22/22 Tests Passing)
```
tests/test_auth.py::test_login_page_renders PASSED
tests/test_auth.py::test_admin_login_success PASSED
tests/test_auth.py::test_employee_login_success PASSED
tests/test_auth.py::test_invalid_password_rejected PASSED
tests/test_auth.py::test_logout PASSED
tests/test_banking_ops.py::test_deposit_operation PASSED
tests/test_banking_ops.py::test_withdrawal_operation PASSED
tests/test_banking_ops.py::test_withdrawal_insufficient_funds_rejected PASSED
tests/test_banking_ops.py::test_atomic_transfer_operation PASSED
tests/test_banking_ops.py::test_atomic_transfer_insufficient_funds_rollback PASSED
tests/test_banking_ops.py::test_customer_creation_duplicate_email_rejected PASSED
tests/test_sql_queries.py::test_all_registered_sql_queries PASSED (Q1 - Q41)
tests/test_sql_queries.py::test_subqueries_edge_cases PASSED
tests/test_sql_queries.py::test_views_execution PASSED
tests/test_sql_queries.py::test_custom_query_runner_success PASSED
tests/test_sql_queries.py::test_custom_query_destructive_statement_blocked PASSED
tests/test_sql_queries.py::test_stored_procedures_queries PASSED
tests/test_sql_queries.py::test_custom_console_procedure_call PASSED
tests/test_sql_queries.py::test_procedures_web_routes PASSED
tests/test_sql_queries.py::test_updates_and_deletes_queries PASSED
tests/test_sql_queries.py::test_sql_api_endpoints PASSED
tests/test_sql_queries.py::test_navigation_and_pages PASSED

====================== 22 passed in 4.61s ======================
```

### Run Live Server Verification Script
```bash
python scripts/verify_live_server.py
```

---

## 🔑 Default Demo Credentials

| Role | Username | Password | Linked Employee | Permissions |
| :--- | :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `Admin@123` | Suresh Babu (ID: 301) | Full System Access, DML Operations, HR & Branches |
| **Bank Employee** | `employee` | `Employee@123` | Ramesh Naidu (ID: 303) | Customer Onboarding, Transactions, Reports, Queries |

---

## 📄 License
This project is licensed under the MIT License.

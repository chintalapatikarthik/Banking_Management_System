# 🏦 Banking Management System
### *Full-Stack Python & SQL Web Application*

[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12-blue?logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Framework-Flask%203.1-black?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Database](https://img.shields.io/badge/SQL%20Database-MySQL%208.x%20%2F%20SQLite-00758F?logo=mysql&logoColor=white)](https://mysql.com)
[![Testing](https://img.shields.io/badge/Tests-20%20Passed%20(100%25)-success?logo=pytest&logoColor=white)](https://pytest.org)
[![UI](https://img.shields.io/badge/Frontend-Bootstrap%205%20%2B%20Chart.js-7952B3?logo=bootstrap&logoColor=white)](https://getbootstrap.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

An enterprise-grade, responsive, database-driven Banking Management Web Application engineered with Python, Flask, SQLAlchemy ORM, raw SQL analytics, Bootstrap 5, and Chart.js.

Built for administrators, branch managers, and banking officers to oversee customer onboarding, multi-tier account portfolios, atomic financial transactions (deposits, withdrawals, inter-account transfers), loan disbursements, employee allocations, branch operations, and SQL analytics.

---

## 📑 Table of Contents
1. [Key Features & Highlights](#-key-features--highlights)
2. [Technology Stack](#-technology-stack)
3. [System Architecture & Directory Structure](#-system-architecture--directory-structure)
4. [Database Design & Schema](#-database-design--schema)
5. [SQL Operations & Analytics Registry (36+ Exercises across 8 Categories)](#-sql-operations--analytics-registry)
6. [Security & Role-Based Access Control](#-security--role-based-access-control)
7. [Getting Started (Local Installation)](#-getting-started-local-installation)
8. [Automated Testing Suite](#-automated-testing-suite)
9. [Public Deployment Guide](#-public-deployment-guide)
10. [Default Demo Credentials](#-default-demo-credentials)

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
- **Interactive SQL Operations Explorer**:
  - Live query runner for all 36+ SQL operations across 8 curriculum categories: Basic Queries, Joins, Aggregates, Subqueries, Database Views, Stored Procedures, Updates & Deletes, and Analytical Reports.
  - Full integration of all 5 enterprise MySQL 8.x stored procedures (`sp_customer_accounts`, `sp_account_transactions`, `sp_calculate_total_balance`, `sp_update_balance`, `sp_insert_customer`) with interactive parameter forms and DDL definition inspection directly in the SQL Operations catalog.
  - Interactive DML operations (UPDATE & DELETE) with live database commit and record verification tables.
  - Execution speed benchmarks in milliseconds, rows count indicator, raw SQL syntax preview, DDL/CALL toggle, and dynamic data tables.
  - **Custom Safe SQL Console**: Allows authorized users to write and execute custom `SELECT`, `CALL sp_...`, `UPDATE`, and `DELETE` queries.
- **Executive Reporting & Export**:
  - 6 tabbed analytical reports with 1-click downloadable CSV exports.

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Backend** | Python 3.11+, Flask 3.1, Werkzeug (Password Hashing), Flask-Login (Session Security) |
| **Database** | MySQL 8.x (Cloud / Enterprise) & SQLite (Portable Development / Testing) |
| **ORM & SQL** | SQLAlchemy 2.0 (ORM Models & Raw SQL Engine), PyMySQL Driver |
| **Frontend** | HTML5 Semantic, CSS3 (Modern Glassmorphic Slate & Indigo Theme), JavaScript (ES6+) |
| **UI Framework** | Bootstrap 5.3, Bootstrap Icons, Google Fonts (Outfit & Inter) |
| **Data Visuals** | Chart.js 4.4 (Bar, Doughnut, Polar, Line, and Horizontal Bar charts) |
| **Testing** | Pytest 9.2 (Unit, Integration, and SQL Assertion tests) |
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
│   ├── models.py                 # SQLAlchemy ORM models (Branch, Customer, Account, etc.)
│   ├── auth.py                   # Flask-Login configuration & @admin_required decorators
│   ├── routes/
│   │   ├── auth_routes.py        # Login & logout handling
│   │   ├── dashboard_routes.py   # Overview dashboard & /api/charts data endpoint
│   │   ├── customer_routes.py    # Customer CRUD & profile views
│   │   ├── account_routes.py     # Account lifecycle & status toggles
│   │   ├── transaction_routes.py # Deposit, withdrawal, and atomic transfer
│   │   ├── loan_routes.py        # Loan disbursements & portfolio
│   │   ├── employee_routes.py    # Staff & officer directory (admin restricted)
│   │   ├── branch_routes.py      # Branch network management
│   │   ├── sql_ops_routes.py     # Interactive SQL exercises & custom console API
│   │   └── report_routes.py      # Executive reporting & CSV downloads
│   ├── services/
│   │   ├── bank_service.py       # Atomic business logic & financial validations
│   │   ├── analytics_service.py  # Real-time SQL aggregations for Chart.js
│   │   └── sql_queries.py        # Complete registry of all 25+ SQL operations
│   ├── static/
│   │   ├── css/style.css         # Modern fintech design system
│   │   └── js/
│   │       ├── main.js           # UI interactions, real-time clock, balance calculations
│   │       └── charts.js         # Chart.js initialization & dynamic fetching
│   └── templates/                # Jinja2 responsive templates
│       ├── base.html             # Master layout with sidebar & topbar
│       ├── login.html            # Sign-in portal with 1-click demo presets
│       ├── dashboard.html        # Executive analytics dashboard
│       ├── customers/            # Customer list, form, and view
│       ├── accounts/             # Account list, form, and view
│       ├── transactions/         # Ledger, deposit, withdraw, transfer
│       ├── loans/                # Portfolio list & form
│       ├── employees/            # Staff directory & form
│       ├── branches/             # Branch network & form
│       ├── sql_operations/       # Interactive SQL learning platform & procedures workbench
│       │   ├── index.html        # Categorized SQL exercise catalog
│       │   └── procedures.html   # Dedicated Stored Procedures Workbench
│       └── reports/              # 6 analytical reports with CSV export
├── database/
│   ├── schema.sql                # MySQL 8.x DDL schema script
│   ├── sample_data.sql           # Realistic Indian banking dataset
│   ├── views.sql                 # 5 SQL view definitions
│   ├── procedures.sql            # MySQL stored procedures
│   └── init_db.py                # Idempotent cross-platform database initializer
├── tests/
│   ├── conftest.py               # Pytest in-memory database fixture
│   ├── test_auth.py              # Authentication & role authorization tests
│   ├── test_banking_ops.py       # Financial transactions & ACID integrity tests
│   └── test_sql_queries.py       # All 25+ SQL exercises & security runner tests
├── scripts/
│   └── verify_live_server.py     # Live server integration test runner
├── .env.example                  # Environment configuration template
├── .gitignore                    # Git ignore specifications
├── Procfile                      # Gunicorn WSGI process configuration
├── render.yaml                   # Infrastructure-as-code for Render deployment
├── vercel.json                   # Serverless WSGI specification for Vercel
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
4. **`transactions`**: `transaction_id` (PK), `account_id` (FK -> accounts), `transaction_type` ('Deposit', 'Withdrawal', 'Transfer Debit', 'Transfer Credit'), `amount` (DECIMAL(10,2) with CHECK > 0), `transaction_date`, `description`
5. **`loans`**: `loan_id` (PK), `customer_id` (FK -> customers), `loan_amount` (DECIMAL(12,2)), `interest_rate` (DECIMAL(5,2)), `loan_date`
6. **`employees`**: `employee_id` (PK), `employee_name`, `position`, `salary` (DECIMAL(10,2)), `joining_date`, `branch_id` (FK -> branches)
7. **`users`**: `user_id` (PK), `username` (UNIQUE), `email` (UNIQUE), `password_hash`, `role` ('admin' / 'employee'), `employee_id` (FK -> employees), `is_active`

### Database Views
- `v_customer_accounts`: Consolidates customer profiles with active account balances and assigned branch details.
- `v_transaction_details`: Joins transactions, account parameters, and customer identity.
- `v_customer_loans`: Credit liabilities and interest rates mapped to borrower contact details.
- `v_customer_total_balance`: Grouped customer net liquidity and account count.
- `v_high_value_transactions`: High-value financial transactions (>= ₹25,000).

### Stored Procedures
- `sp_insert_customer`: Atomic customer insertion returning generated primary key.
- `sp_update_balance`: Balance updater with negative balance prevention.
- `sp_account_transactions`: Chronological ledger fetch for an account.
- `sp_calculate_total_balance`: Aggregate liquidity calculator.
- `sp_customer_accounts`: List accounts held by a customer.

---

## 📊 SQL Operations & Analytics Registry

The dedicated **SQL Operations & Analytics** module in the web application executes real database queries dynamically:

### 1. Basic Queries
- `basic_1`: Accounts with balance greater than ₹50,000.
- `basic_2`: Customers residing in Hyderabad (`WHERE address LIKE '%Hyderabad%'`).
- `basic_3`: List all Savings accounts.
- `basic_4`: Employees who joined after 2022 (`WHERE joining_date > '2022-12-31'`).

### 2. Joins
- `join_1`: Customer names with their accounts (`INNER JOIN accounts`).
- `join_2`: Accounts with transaction details (`INNER JOIN transactions`).
- `join_3`: Loan details with customer information (`INNER JOIN customers`).
- `join_4`: Employees with their branches (`LEFT JOIN branches`).
- `join_5`: Multi-table join connecting Customers, Accounts, and Transactions.

### 3. Aggregate Functions
- `agg_1`: Count total registered customers (`COUNT(*)`).
- `agg_2`: Average account balance, minimum and maximum balance (`AVG()`, `ROUND()`).
- `agg_3`: Total bank loan portfolio disbursed (`SUM(loan_amount)`).
- `agg_4`: Total transactions grouped by transaction type.
- `agg_5`: Identify account holding the highest balance (`WHERE balance = (SELECT MAX(balance)...)`).

### 4. Subqueries
- `subquery_1`: Customers who hold no bank accounts (`WHERE customer_id NOT IN (...)`).
- `subquery_2`: Accounts with zero recorded transactions (`WHERE NOT EXISTS (...)`).
- `subquery_3`: Accounts with balance above bank-wide average.
- `subquery_4`: Customers with loan amounts above average.
- `subquery_5`: Transactions exceeding average transaction volume.

### 5. Views
- `view_1`: Query `v_customer_accounts`.
- `view_2`: Query `v_transaction_details`.
- `view_3`: Query `v_customer_loans`.
- `view_4`: Query `v_customer_total_balance`.
- `view_5`: Query `v_high_value_transactions`.

### 6. Stored Procedures
- `proc_1`: Customer Accounts (`sp_customer_accounts`) - retrieves all accounts, balances, and branch details held by a specific customer.
- `proc_2`: Account Transactions (`sp_account_transactions`) - chronological transaction ledger statement for an account.
- `proc_3`: Calculate Total Bank Balance (`sp_calculate_total_balance`) - aggregate liquidity across all accounts via OUT parameter.
- `proc_4`: Update Account Balance (`sp_update_balance`) - updates balance with negative balance exception handling (`SIGNAL SQLSTATE '45000'`).
- `proc_5`: Insert New Customer (`sp_insert_customer`) - atomic customer registration returning the generated customer ID.

### 7. Updates & Deletes (DML)
- `update_1`: Update account balance (`UPDATE accounts SET balance = 95000.00 WHERE account_id = 201`).
- `update_2`: Change customer email (`UPDATE customers SET email = 'rahul.sharma.new@example.com' WHERE customer_id = 101`).
- `update_3`: Update branch location (`UPDATE branches SET location = 'Cyberabad, Hyderabad' WHERE branch_id = 1`).
- `delete_1`: Delete inactive accounts (`DELETE FROM accounts WHERE account_status = 'Inactive'`).
- `delete_2`: Delete customers with no accounts (`DELETE FROM customers WHERE customer_id NOT IN (...)`).

### 8. Reports & Analytics
- `report_1`: Top 5 customers ranked by aggregate balance.
- `report_2`: Most active customers by transaction count and volume.
- `report_3`: Monthly transaction volume breakdown by month and type.
- `report_4`: Branches ranked by total deposit volume.
- `report_5`: Customer credit vs. debit monetary analysis.
- `report_6`: Customers with highest loan liabilities.

---

## 🔒 Security & Role-Based Access Control

- **Password Hashing**: High-entropy `scrypt` hashing via Werkzeug security.
- **Session Management**: Secure HTTP-only cookies with configurable session expiration.
- **Role-Based Authorization**:
  - `Admin`: Full access to customer CRUD, account modifications, employee onboarding/deletion, branch management, and all analytics.
  - `Employee`: Access to customer directory, registrations, account view, transaction recording (deposit, withdrawal, transfer), and reports.
- **ACID Financial Integrity**:
  - All balance changes execute within database transaction scopes.
  - Overdrafts and negative balances are prevented at both the application and database check-constraint levels.
- **Read-Only Custom SQL Console**:
  - Custom SQL input parses statement prefixes and restricts execution strictly to read-only queries (`SELECT`, `WITH`, `EXPLAIN`).

---

## 🚀 Getting Started (Local Installation)

### Prerequisites
- Python 3.11+ installed (`python --version`)
- Git installed (`git --version`)

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/banking-management-system.git
cd banking-management-system
```

### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
*(Default settings automatically use SQLite for instant zero-configuration development)*

### 5. Initialize the Database
```bash
python database/init_db.py
```

### 6. Run the Application
```bash
python run.py
```
Open your browser and navigate to:
👉 **`http://127.0.0.1:5000`**

---

## 🧪 Automated Testing Suite

The application includes a comprehensive test suite covering authentication, ACID transactions, overdraft protection, and all 25+ SQL exercises:

```bash
# Run pytest with summary
pytest -v
```

**Test Coverage Summary:**
- `tests/test_auth.py`: Login, session management, employee access, admin privilege verification.
- `tests/test_banking_ops.py`: Deposits, withdrawals, overdraft rejections, atomic transfers, rollback validation, and customer unique constraints.
- `tests/test_sql_queries.py`: All 25+ registered SQL exercises, view assertions, subqueries, and custom query security validation.

---

## 🌐 Public Deployment Guide

The application is pre-configured for 1-click cloud deployment.

### Option A: Render (Recommended)
1. Fork or push this repository to your GitHub account.
2. Sign in to [Render](https://render.com).
3. Click **New +** -> **Web Service** -> Connect your GitHub repository.
4. Set the following parameters:
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && python database/init_db.py`
   - **Start Command**: `gunicorn run:app`
5. Add the following Environment Variables in the Render dashboard:
   - `SECRET_KEY`: *(Generate a random 32-character string)*
   - `FLASK_ENV`: `production`
   - `DATABASE_URL`: *(Leave blank for persistent SQLite, or supply your managed MySQL URL: `mysql+pymysql://user:pass@host:3306/dbname`)*
6. Click **Deploy Web Service**. Your application will be live at `https://your-app-name.onrender.com`.

### Option B: Railway
1. Sign in to [Railway](https://railway.app).
2. Click **New Project** -> **Deploy from GitHub repo**.
3. (Optional) Add a **MySQL** plugin service to provision an instant managed MySQL database.
4. Set `DATABASE_URL` to `${{MySQL.MYSQL_URL}}`.
5. Railway automatically detects `Procfile` and deploys using Gunicorn.

### Option C: Vercel
1. The included `vercel.json` provides serverless deployment capability.
2. Deploy directly via `vercel --prod` or connect the GitHub repository in the Vercel dashboard.

---

## 🔑 Default Demo Credentials

Use these credentials to explore the live application:

| Role | Username | Password | Permissions |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `Admin@123` | Full access across all 10 modules, staff & branch editing, destructive operations |
| **Bank Employee** | `employee` | `Employee@123` | Customer registration, transaction recording, account management, reports |

*(You can also click the 1-Click Demo Fill buttons directly on the Login page)*

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).

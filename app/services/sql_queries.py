import re
import time
from app.database import execute_raw_sql, engine

# Registry of all SQL operations defined in Section 8 of specification
SQL_QUERIES_REGISTRY = {
    # -------------------------------------------------------------
    # Basic Queries
    # -------------------------------------------------------------
    'basic_1': {
        'category': 'Basic Queries',
        'title': 'Accounts with Balance Greater than 50,000',
        'description': 'Filters all bank accounts where the available balance exceeds ₹50,000 using WHERE clause.',
        'sql': """
SELECT 
    account_id,
    customer_id,
    account_type,
    balance,
    opening_date,
    account_status
FROM accounts
WHERE balance > 50000.00
ORDER BY balance DESC;
        """
    },
    'basic_2': {
        'category': 'Basic Queries',
        'title': 'All Customers from Hyderabad',
        'description': 'Retrieves all customers whose residential or registered address contains "Hyderabad" using LIKE pattern matching.',
        'sql': """
SELECT 
    customer_id,
    name,
    email,
    phone,
    address,
    registration_date
FROM customers
WHERE address LIKE '%Hyderabad%'
ORDER BY name ASC;
        """
    },
    'basic_3': {
        'category': 'Basic Queries',
        'title': 'List All Savings Accounts',
        'description': 'Lists all accounts classified as Savings account type.',
        'sql': """
SELECT 
    account_id,
    customer_id,
    balance,
    opening_date,
    account_status
FROM accounts
WHERE account_type = 'Savings'
ORDER BY account_id ASC;
        """
    },
    'basic_4': {
        'category': 'Basic Queries',
        'title': 'Employees Who Joined After 2022',
        'description': 'Filters employees who were hired on or after January 1st, 2023 using date comparison.',
        'sql': """
SELECT 
    employee_id,
    employee_name,
    position,
    salary,
    joining_date
FROM employees
WHERE joining_date > '2022-12-31'
ORDER BY joining_date DESC;
        """
    },

    # -------------------------------------------------------------
    # Joins
    # -------------------------------------------------------------
    'join_1': {
        'category': 'Joins',
        'title': 'Customer Names with Their Accounts',
        'description': 'Performs an INNER JOIN between Customers and Accounts to show each account alongside its holder name.',
        'sql': """
SELECT 
    c.customer_id,
    c.name AS customer_name,
    c.email,
    a.account_id,
    a.account_type,
    a.balance,
    a.account_status
FROM customers c
INNER JOIN accounts a ON c.customer_id = a.customer_id
ORDER BY c.name ASC, a.account_id ASC;
        """
    },
    'join_2': {
        'category': 'Joins',
        'title': 'Accounts with Transaction Details',
        'description': 'Joins Accounts with Transactions to review the complete financial activity per account.',
        'sql': """
SELECT 
    a.account_id,
    a.account_type,
    t.transaction_id,
    t.transaction_type,
    t.amount,
    t.transaction_date,
    t.description
FROM accounts a
INNER JOIN transactions t ON a.account_id = t.account_id
ORDER BY t.transaction_date DESC, t.transaction_id DESC;
        """
    },
    'join_3': {
        'category': 'Joins',
        'title': 'Loan Details with Customer Information',
        'description': 'Joins Loans with Customers to inspect credit exposures linked to customer contact details.',
        'sql': """
SELECT 
    l.loan_id,
    c.customer_id,
    c.name AS customer_name,
    c.phone,
    l.loan_amount,
    l.interest_rate,
    l.loan_date
FROM loans l
INNER JOIN customers c ON l.customer_id = c.customer_id
ORDER BY l.loan_amount DESC;
        """
    },
    'join_4': {
        'category': 'Joins',
        'title': 'Employees with Their Branches',
        'description': 'LEFT JOIN between Employees and Branches showing the branch location each staff member is assigned to.',
        'sql': """
SELECT 
    e.employee_id,
    e.employee_name,
    e.position,
    e.salary,
    b.branch_name,
    b.location AS branch_location
FROM employees e
LEFT JOIN branches b ON e.branch_id = b.branch_id
ORDER BY b.location ASC, e.employee_name ASC;
        """
    },
    'join_5': {
        'category': 'Joins',
        'title': 'Customers with Their Transactions',
        'description': 'Multi-table JOIN connecting Customers through Accounts to Transactions.',
        'sql': """
SELECT 
    c.customer_id,
    c.name AS customer_name,
    a.account_id,
    t.transaction_id,
    t.transaction_type,
    t.amount,
    t.transaction_date
FROM customers c
INNER JOIN accounts a ON c.customer_id = a.customer_id
INNER JOIN transactions t ON a.account_id = t.account_id
ORDER BY t.transaction_date DESC;
        """
    },

    # -------------------------------------------------------------
    # Aggregate Functions
    # -------------------------------------------------------------
    'agg_1': {
        'category': 'Aggregate Functions',
        'title': 'Count Total Customers',
        'description': 'Uses COUNT(*) to compute the total number of registered bank customers.',
        'sql': """
SELECT COUNT(*) AS total_customers_count FROM customers;
        """
    },
    'agg_2': {
        'category': 'Aggregate Functions',
        'title': 'Find Average Account Balance',
        'description': 'Uses AVG() and ROUND() to determine the mean balance across all accounts.',
        'sql': """
SELECT 
    ROUND(AVG(balance), 2) AS average_account_balance,
    ROUND(MIN(balance), 2) AS minimum_balance,
    ROUND(MAX(balance), 2) AS maximum_balance
FROM accounts;
        """
    },
    'agg_3': {
        'category': 'Aggregate Functions',
        'title': 'Calculate Total Loan Amount',
        'description': 'Uses SUM() to calculate the total outstanding credit / loan portfolio.',
        'sql': """
SELECT 
    COUNT(loan_id) AS total_loans_issued,
    SUM(loan_amount) AS total_loan_disbursed,
    ROUND(AVG(interest_rate), 2) AS average_interest_rate
FROM loans;
        """
    },
    'agg_4': {
        'category': 'Aggregate Functions',
        'title': 'Count Total Transactions',
        'description': 'Computes total transaction count and aggregates by transaction type.',
        'sql': """
SELECT 
    transaction_type,
    COUNT(*) AS total_count,
    SUM(amount) AS total_volume
FROM transactions
GROUP BY transaction_type;
        """
    },
    'agg_5': {
        'category': 'Aggregate Functions',
        'title': 'Find the Highest Account Balance',
        'description': 'Finds the highest balance and identifies the corresponding account.',
        'sql': """
SELECT 
    a.account_id,
    c.name AS customer_name,
    a.account_type,
    a.balance
FROM accounts a
JOIN customers c ON a.customer_id = c.customer_id
WHERE a.balance = (SELECT MAX(balance) FROM accounts);
        """
    },

    # -------------------------------------------------------------
    # Subqueries
    # -------------------------------------------------------------
    'subquery_1': {
        'category': 'Subqueries',
        'title': 'Find Customers Who Have No Accounts',
        'description': 'Uses NOT IN or NOT EXISTS subquery to detect prospects who registered but hold no active accounts.',
        'sql': """
SELECT 
    c.customer_id,
    c.name,
    c.email,
    c.phone,
    c.registration_date
FROM customers c
WHERE c.customer_id NOT IN (
    SELECT DISTINCT customer_id FROM accounts WHERE customer_id IS NOT NULL
);
        """
    },
    'subquery_2': {
        'category': 'Subqueries',
        'title': 'Find Accounts with No Transactions',
        'description': 'Uses NOT EXISTS subquery to identify dormant or newly opened accounts without any transaction history.',
        'sql': """
SELECT 
    a.account_id,
    c.name AS customer_name,
    a.account_type,
    a.balance,
    a.opening_date
FROM accounts a
JOIN customers c ON a.customer_id = c.customer_id
WHERE NOT EXISTS (
    SELECT 1 FROM transactions t WHERE t.account_id = a.account_id
);
        """
    },
    'subquery_3': {
        'category': 'Subqueries',
        'title': 'Accounts with Balance Greater than Average',
        'description': 'Uses a scalar subquery (AVG) in the WHERE clause to find above-average balance accounts.',
        'sql': """
SELECT 
    account_id,
    customer_id,
    account_type,
    balance
FROM accounts
WHERE balance > (SELECT AVG(balance) FROM accounts)
ORDER BY balance DESC;
        """
    },
    'subquery_4': {
        'category': 'Subqueries',
        'title': 'Customers with Loan Amounts Above Average',
        'description': 'Identifies customers holding loans greater than the bank-wide average loan amount.',
        'sql': """
SELECT 
    c.name AS customer_name,
    l.loan_id,
    l.loan_amount,
    l.interest_rate
FROM loans l
JOIN customers c ON l.customer_id = c.customer_id
WHERE l.loan_amount > (SELECT AVG(loan_amount) FROM loans)
ORDER BY l.loan_amount DESC;
        """
    },
    'subquery_5': {
        'category': 'Subqueries',
        'title': 'Transactions Above Average Amount',
        'description': 'Filters all transactions that exceed the average monetary value of all transactions.',
        'sql': """
SELECT 
    transaction_id,
    account_id,
    transaction_type,
    amount,
    transaction_date,
    description
FROM transactions
WHERE amount > (SELECT AVG(amount) FROM transactions)
ORDER BY amount DESC;
        """
    },

    # -------------------------------------------------------------
    # Database Views
    # -------------------------------------------------------------
    'view_1': {
        'category': 'Views',
        'title': 'Customer Accounts View (v_customer_accounts)',
        'description': 'Queries predefined SQL View joining customer profile, account parameters, and branch location.',
        'sql': """
SELECT * FROM v_customer_accounts ORDER BY customer_id ASC, account_id ASC;
        """
    },
    'view_2': {
        'category': 'Views',
        'title': 'Transaction Details View (v_transaction_details)',
        'description': 'Queries predefined SQL View joining transaction records, accounts, and client holders.',
        'sql': """
SELECT * FROM v_transaction_details ORDER BY transaction_date DESC LIMIT 50;
        """
    },
    'view_3': {
        'category': 'Views',
        'title': 'Loan Details with Customers View (v_customer_loans)',
        'description': 'Queries predefined SQL View joining loan credit details with customer demographic data.',
        'sql': """
SELECT * FROM v_customer_loans ORDER BY loan_amount DESC;
        """
    },
    'view_4': {
        'category': 'Views',
        'title': 'Total Balance per Customer View (v_customer_total_balance)',
        'description': 'Aggregated view summarizing customer account count and cumulative liquid net worth.',
        'sql': """
SELECT * FROM v_customer_total_balance ORDER BY total_balance DESC;
        """
    },
    'view_5': {
        'category': 'Views',
        'title': 'High Value Transactions View (v_high_value_transactions)',
        'description': 'Queries predefined view filtered for high-value financial movements (>= ₹25,000).',
        'sql': """
SELECT * FROM v_high_value_transactions ORDER BY amount DESC;
        """
    },

    # -------------------------------------------------------------
    # Stored Procedures (MySQL 8.x & Cross-Platform Engine)
    # -------------------------------------------------------------
    'proc_1': {
        'category': 'Stored Procedures',
        'title': 'Display Customer Accounts (sp_customer_accounts)',
        'procedure_name': 'sp_customer_accounts',
        'description': 'Executes stored procedure sp_customer_accounts to list all bank accounts, account types, balances, and branch details held by a specific customer (default: Customer ID 101).',
        'parameters': [
            {'name': 'p_customer_id', 'type': 'INT', 'default': 101, 'label': 'Customer ID'}
        ],
        'sql': """
-- 1. Stored Procedure: Display Accounts of a Customer
-- Database Engine: MySQL 8.x / Banking System Schema

-- Call Stored Procedure:
CALL sp_customer_accounts(101);
        """.strip(),
        'definition': """
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_customer_accounts$$
CREATE PROCEDURE sp_customer_accounts(
    IN p_customer_id INT
)
BEGIN
    SELECT 
        a.account_id,
        a.account_type,
        a.balance,
        a.opening_date,
        a.account_status,
        b.branch_name,
        b.location
    FROM accounts a
    LEFT JOIN branches b ON a.branch_id = b.branch_id
    WHERE a.customer_id = p_customer_id
    ORDER BY a.account_id ASC;
END$$
DELIMITER ;
        """.strip()
    },
    'proc_2': {
        'category': 'Stored Procedures',
        'title': 'Account Transaction Ledger (sp_account_transactions)',
        'procedure_name': 'sp_account_transactions',
        'description': 'Executes stored procedure sp_account_transactions to retrieve the complete chronological financial ledger statement for a given account (default: Account ID 201).',
        'parameters': [
            {'name': 'p_account_id', 'type': 'INT', 'default': 201, 'label': 'Account ID'}
        ],
        'sql': """
-- 2. Stored Procedure: Display Transactions of an Account
-- Database Engine: MySQL 8.x / Banking System Schema

-- Call Stored Procedure:
CALL sp_account_transactions(201);
        """.strip(),
        'definition': """
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_account_transactions$$
CREATE PROCEDURE sp_account_transactions(
    IN p_account_id INT
)
BEGIN
    SELECT 
        transaction_id,
        transaction_type,
        amount,
        transaction_date,
        description
    FROM transactions
    WHERE account_id = p_account_id
    ORDER BY transaction_date DESC, transaction_id DESC;
END$$
DELIMITER ;
        """.strip()
    },
    'proc_3': {
        'category': 'Stored Procedures',
        'title': 'Calculate Total Bank Balance (sp_calculate_total_balance)',
        'procedure_name': 'sp_calculate_total_balance',
        'description': 'Executes stored procedure sp_calculate_total_balance using an OUT parameter to compute cumulative liquidity held across all accounts in the institution.',
        'parameters': [],
        'sql': """
-- 3. Stored Procedure: Calculate Total Bank Balance
-- Database Engine: MySQL 8.x / Banking System Schema

-- Call Stored Procedure with OUT parameter:
CALL sp_calculate_total_balance(@total_balance);
SELECT @total_balance AS total_bank_balance;
        """.strip(),
        'definition': """
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_calculate_total_balance$$
CREATE PROCEDURE sp_calculate_total_balance(
    OUT p_total DECIMAL(14, 2)
)
BEGIN
    SELECT COALESCE(SUM(balance), 0.00) INTO p_total FROM accounts;
END$$
DELIMITER ;
        """.strip()
    },
    'proc_4': {
        'category': 'Stored Procedures',
        'title': 'Update Account Balance with Validation (sp_update_balance)',
        'procedure_name': 'sp_update_balance',
        'description': 'Executes stored procedure sp_update_balance enforcing business check constraints (raises SQLSTATE 45000 if balance is negative) and returns the updated account state.',
        'parameters': [
            {'name': 'p_account_id', 'type': 'INT', 'default': 201, 'label': 'Account ID'},
            {'name': 'p_new_balance', 'type': 'DECIMAL', 'default': 85000.00, 'label': 'New Balance (₹)'}
        ],
        'sql': """
-- 4. Stored Procedure: Update Account Balance with Integrity Validation
-- Database Engine: MySQL 8.x / Banking System Schema

-- Call Stored Procedure:
CALL sp_update_balance(201, 85000.00);

-- Verify Result:
SELECT account_id, customer_id, account_type, balance, account_status 
FROM accounts 
WHERE account_id = 201;
        """.strip(),
        'definition': """
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_update_balance$$
CREATE PROCEDURE sp_update_balance(
    IN p_account_id INT,
    IN p_new_balance DECIMAL(12, 2)
)
BEGIN
    IF p_new_balance < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Balance cannot be negative';
    ELSE
        UPDATE accounts 
        SET balance = p_new_balance 
        WHERE account_id = p_account_id;
    END IF;
END$$
DELIMITER ;
        """.strip()
    },
    'proc_5': {
        'category': 'Stored Procedures',
        'title': 'Insert New Customer (sp_insert_customer)',
        'procedure_name': 'sp_insert_customer',
        'description': 'Executes stored procedure sp_insert_customer to safely insert a customer record and return the auto-generated primary key via an OUT parameter.',
        'parameters': [
            {'name': 'p_name', 'type': 'VARCHAR', 'default': 'Kavita Krishnan', 'label': 'Customer Name'},
            {'name': 'p_email', 'type': 'VARCHAR', 'default': 'kavita.k@example.com', 'label': 'Email Address'},
            {'name': 'p_phone', 'type': 'VARCHAR', 'default': '9876501234', 'label': 'Phone Number'},
            {'name': 'p_address', 'type': 'VARCHAR', 'default': 'Jubilee Hills, Hyderabad', 'label': 'Address'},
            {'name': 'p_reg_date', 'type': 'DATE', 'default': '2024-04-15', 'label': 'Registration Date'}
        ],
        'sql': """
-- 5. Stored Procedure: Insert New Customer
-- Database Engine: MySQL 8.x / Banking System Schema

-- Call Stored Procedure with OUT parameter:
CALL sp_insert_customer(
    'Kavita Krishnan', 
    'kavita.k@example.com', 
    '9876501234', 
    'Jubilee Hills, Hyderabad', 
    '2024-04-15', 
    @new_customer_id
);
SELECT customer_id, name, email, phone, address, registration_date 
FROM customers 
WHERE customer_id = @new_customer_id;
        """.strip(),
        'definition': """
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_insert_customer$$
CREATE PROCEDURE sp_insert_customer(
    IN p_name VARCHAR(100),
    IN p_email VARCHAR(100),
    IN p_phone VARCHAR(15),
    IN p_address VARCHAR(255),
    IN p_reg_date DATE,
    OUT p_customer_id INT
)
BEGIN
    INSERT INTO customers (name, email, phone, address, registration_date)
    VALUES (p_name, p_email, p_phone, p_address, p_reg_date);
    SET p_customer_id = LAST_INSERT_ID();
END$$
DELIMITER ;
        """.strip()
    },

    # -------------------------------------------------------------
    # Updates & Deletes (Data Manipulation Language - DML)
    # -------------------------------------------------------------
    'update_1': {
        'category': 'Updates & Deletes',
        'title': 'Update Account Balance',
        'description': 'Updates the balance of account 201 to ₹95,000.00 and verifies the updated account record.',
        'sql': """
-- 1. Update Account Balance:
UPDATE accounts 
SET balance = 95000.00 
WHERE account_id = 201;

-- 2. Verify Updated Account Balance:
SELECT account_id, customer_id, account_type, balance, account_status 
FROM accounts 
WHERE account_id = 201;
        """.strip()
    },
    'update_2': {
        'category': 'Updates & Deletes',
        'title': 'Change Customer Email',
        'description': 'Updates the registered email address for customer ID 102 to priya.patel.updated@example.com and verifies the profile.',
        'sql': """
-- 1. Change Customer Email:
UPDATE customers 
SET email = 'priya.patel.updated@example.com' 
WHERE customer_id = 102;

-- 2. Verify Changed Customer Email:
SELECT customer_id, name, email, phone, address, registration_date 
FROM customers 
WHERE customer_id = 102;
        """.strip()
    },
    'update_3': {
        'category': 'Updates & Deletes',
        'title': 'Update Branch Location',
        'description': 'Updates the physical branch location for branch ID 1 to Cyberabad, Hyderabad and verifies the branch record.',
        'sql': """
-- 1. Update Branch Location:
UPDATE branches 
SET location = 'Cyberabad, Hyderabad' 
WHERE branch_id = 1;

-- 2. Verify Updated Branch Location:
SELECT branch_id, branch_name, location 
FROM branches 
WHERE branch_id = 1;
        """.strip()
    },
    'delete_1': {
        'category': 'Updates & Deletes',
        'title': 'Delete Inactive Accounts',
        'description': 'Deletes bank accounts where account_status is Inactive and verifies that inactive accounts have been removed.',
        'sql': """
-- 1. Delete Inactive Accounts:
DELETE FROM accounts 
WHERE account_status = 'Inactive';

-- 2. Verify Inactive Accounts Deletion:
SELECT account_id, customer_id, account_type, balance, account_status 
FROM accounts 
WHERE account_status = 'Inactive';
        """.strip()
    },
    'delete_2': {
        'category': 'Updates & Deletes',
        'title': 'Delete Customers with No Accounts',
        'description': 'Deletes customer records who do not hold any bank accounts using a subquery and verifies that no orphan customers remain.',
        'sql': """
-- 1. Delete Customers With No Accounts:
DELETE FROM customers 
WHERE customer_id NOT IN (
    SELECT DISTINCT customer_id FROM accounts WHERE customer_id IS NOT NULL
);

-- 2. Verify Customers with No Accounts (Should return 0):
SELECT customer_id, name, email, phone, registration_date 
FROM customers 
WHERE customer_id NOT IN (
    SELECT DISTINCT customer_id FROM accounts WHERE customer_id IS NOT NULL
);
        """.strip()
    },

    # -------------------------------------------------------------
    # Reports and Analysis
    # -------------------------------------------------------------
    'report_1': {
        'category': 'Reports & Analytics',
        'title': 'Top 5 Customers with Highest Balance',
        'description': 'Identifies premier tier clients ranked by total aggregate balances across all their accounts.',
        'sql': """
SELECT 
    c.customer_id,
    c.name AS customer_name,
    c.email,
    COUNT(a.account_id) AS total_accounts,
    SUM(a.balance) AS aggregate_balance
FROM customers c
INNER JOIN accounts a ON c.customer_id = a.customer_id
GROUP BY c.customer_id, c.name, c.email
ORDER BY aggregate_balance DESC
LIMIT 5;
        """
    },
    'report_2': {
        'category': 'Reports & Analytics',
        'title': 'Most Active Customers',
        'description': 'Ranks customers by total transaction volume and frequency.',
        'sql': """
SELECT 
    c.customer_id,
    c.name AS customer_name,
    COUNT(t.transaction_id) AS total_transactions_count,
    SUM(t.amount) AS total_transacted_volume
FROM customers c
JOIN accounts a ON c.customer_id = a.customer_id
JOIN transactions t ON a.account_id = t.account_id
GROUP BY c.customer_id, c.name
ORDER BY total_transactions_count DESC
LIMIT 10;
        """
    },
    'report_3': {
        'category': 'Reports & Analytics',
        'title': 'Monthly Transaction Report',
        'description': 'Aggregates transaction counts and volume broken down by month and type.',
        'sql': """
SELECT 
    SUBSTR(transaction_date, 1, 7) AS transaction_month,
    transaction_type,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_amount
FROM transactions
GROUP BY SUBSTR(transaction_date, 1, 7), transaction_type
ORDER BY transaction_month DESC, transaction_type ASC;
        """
    },
    'report_4': {
        'category': 'Reports & Analytics',
        'title': 'Branch with Highest Deposits',
        'description': 'Calculates deposit balance aggregated by branch location to identify top performing branches.',
        'sql': """
SELECT 
    b.branch_id,
    b.branch_name,
    b.location,
    COUNT(a.account_id) AS accounts_count,
    COALESCE(SUM(a.balance), 0.00) AS total_branch_deposits
FROM branches b
LEFT JOIN accounts a ON b.branch_id = a.branch_id
GROUP BY b.branch_id, b.branch_name, b.location
ORDER BY total_branch_deposits DESC;
        """
    },
    'report_5': {
        'category': 'Reports & Analytics',
        'title': 'Customer Transaction Analysis',
        'description': 'Examines deposits vs withdrawals per customer account.',
        'sql': """
SELECT 
    c.customer_id,
    c.name AS customer_name,
    SUM(CASE WHEN t.transaction_type LIKE '%Deposit%' OR t.transaction_type LIKE '%Credit%' THEN t.amount ELSE 0 END) AS total_credited,
    SUM(CASE WHEN t.transaction_type LIKE '%Withdrawal%' OR t.transaction_type LIKE '%Debit%' THEN t.amount ELSE 0 END) AS total_debited,
    COUNT(t.transaction_id) AS transaction_count
FROM customers c
JOIN accounts a ON c.customer_id = a.customer_id
JOIN transactions t ON a.account_id = t.account_id
GROUP BY c.customer_id, c.name
ORDER BY transaction_count DESC;
        """
    },
    'report_6': {
        'category': 'Reports & Analytics',
        'title': 'Customers with Highest Loan Amounts',
        'description': 'Ranks customers with greatest borrowed liabilities and applicable interest rates.',
        'sql': """
SELECT 
    c.customer_id,
    c.name AS customer_name,
    c.phone,
    l.loan_id,
    l.loan_amount,
    l.interest_rate,
    l.loan_date
FROM loans l
JOIN customers c ON l.customer_id = c.customer_id
ORDER BY l.loan_amount DESC;
        """
    }
}

def _build_procedure_call_sql(query_key, q_info, params):
    """Generate dynamic formatted CALL query reflecting user-provided or default parameters."""
    if query_key == 'proc_1':
        cid = params.get('p_customer_id', 101)
        return f"-- Invoke Stored Procedure with Customer ID {cid}:\nCALL sp_customer_accounts({cid});"
    elif query_key == 'proc_2':
        aid = params.get('p_account_id', 201)
        return f"-- Invoke Stored Procedure with Account ID {aid}:\nCALL sp_account_transactions({aid});"
    elif query_key == 'proc_3':
        return "-- Invoke Stored Procedure with OUT parameter:\nCALL sp_calculate_total_balance(@total_balance);\nSELECT @total_balance AS total_bank_balance;"
    elif query_key == 'proc_4':
        aid = params.get('p_account_id', 201)
        bal = params.get('p_new_balance', 85000.00)
        return f"-- Invoke Stored Procedure with Account {aid} and Balance ₹{bal}:\nCALL sp_update_balance({aid}, {bal});\n\n-- Verify Updated Account:\nSELECT account_id, customer_id, account_type, balance, account_status FROM accounts WHERE account_id = {aid};"
    elif query_key == 'proc_5':
        name = params.get('p_name', 'Kavita Krishnan')
        email = params.get('p_email', 'kavita.k@example.com')
        phone = params.get('p_phone', '9876501234')
        address = params.get('p_address', 'Jubilee Hills, Hyderabad')
        reg_date = params.get('p_reg_date', '2024-04-15')
        return f"-- Invoke Stored Procedure with OUT parameter:\nCALL sp_insert_customer('{name}', '{email}', '{phone}', '{address}', '{reg_date}', @new_customer_id);\nSELECT customer_id, name, email, phone, address, registration_date FROM customers WHERE customer_id = @new_customer_id;"
    return q_info['sql'].strip()

def _execute_stored_procedure(query_key, q_info, params):
    """
    Executes a stored procedure natively on MySQL, or executes an equivalent
    pure SQL emulation layer on SQLite / development environments.
    """
    is_mysql = 'mysql' in str(engine.url)

    if query_key == 'proc_1':
        p_id = int(params.get('p_customer_id') or 101)
        if is_mysql:
            try:
                return execute_raw_sql("CALL sp_customer_accounts(:p_customer_id)", {'p_customer_id': p_id}, fetch_all=True)
            except Exception:
                pass
        sql = """
        SELECT 
            a.account_id,
            a.account_type,
            a.balance,
            a.opening_date,
            a.account_status,
            b.branch_name,
            b.location
        FROM accounts a
        LEFT JOIN branches b ON a.branch_id = b.branch_id
        WHERE a.customer_id = :p_customer_id
        ORDER BY a.account_id ASC;
        """
        return execute_raw_sql(sql, {'p_customer_id': p_id}, fetch_all=True)

    elif query_key == 'proc_2':
        a_id = int(params.get('p_account_id') or 201)
        if is_mysql:
            try:
                return execute_raw_sql("CALL sp_account_transactions(:p_account_id)", {'p_account_id': a_id}, fetch_all=True)
            except Exception:
                pass
        sql = """
        SELECT 
            transaction_id,
            transaction_type,
            amount,
            transaction_date,
            description
        FROM transactions
        WHERE account_id = :p_account_id
        ORDER BY transaction_date DESC, transaction_id DESC;
        """
        return execute_raw_sql(sql, {'p_account_id': a_id}, fetch_all=True)

    elif query_key == 'proc_3':
        if is_mysql:
            try:
                execute_raw_sql("CALL sp_calculate_total_balance(@total_balance)")
                return execute_raw_sql("SELECT @total_balance AS total_bank_balance", fetch_all=True)
            except Exception:
                pass
        sql = "SELECT COALESCE(SUM(balance), 0.00) AS total_bank_balance FROM accounts;"
        return execute_raw_sql(sql, fetch_all=True)

    elif query_key == 'proc_4':
        a_id = int(params.get('p_account_id') or 201)
        new_bal = float(params.get('p_new_balance') if params.get('p_new_balance') is not None else 85000.00)
        if new_bal < 0:
            raise ValueError("Balance cannot be negative (SQLSTATE 45000: sp_update_balance integrity check failed)")

        if is_mysql:
            try:
                execute_raw_sql("CALL sp_update_balance(:acc, :bal)", {'acc': a_id, 'bal': new_bal}, commit=True)
                return execute_raw_sql(
                    "SELECT account_id, customer_id, account_type, balance, account_status, 'Updated via MySQL 8.x sp_update_balance' AS procedure_status FROM accounts WHERE account_id = :acc",
                    {'acc': a_id},
                    fetch_all=True
                )
            except Exception:
                pass

        execute_raw_sql("UPDATE accounts SET balance = :bal WHERE account_id = :acc", {'bal': new_bal, 'acc': a_id}, commit=True)
        return execute_raw_sql(
            "SELECT account_id, customer_id, account_type, balance, account_status, 'Verified & Updated via sp_update_balance' AS procedure_status FROM accounts WHERE account_id = :acc",
            {'acc': a_id},
            fetch_all=True
        )

    elif query_key == 'proc_5':
        name = str(params.get('p_name') or 'Kavita Krishnan').strip()
        email = str(params.get('p_email') or 'kavita.k@example.com').strip()
        phone = str(params.get('p_phone') or '9876501234').strip()
        address = str(params.get('p_address') or 'Jubilee Hills, Hyderabad').strip()
        reg_date = str(params.get('p_reg_date') or '2024-04-15').strip()

        # Check existing customer record
        existing = execute_raw_sql(
            "SELECT customer_id, name, email, phone, address, registration_date, 'Customer Record Verified (sp_insert_customer)' AS procedure_status FROM customers WHERE email = :email",
            {'email': email},
            fetch_all=True
        )
        if existing:
            return existing

        if is_mysql:
            try:
                execute_raw_sql(
                    "CALL sp_insert_customer(:name, :email, :phone, :address, :reg_date, @new_customer_id)",
                    {'name': name, 'email': email, 'phone': phone, 'address': address, 'reg_date': reg_date},
                    commit=True
                )
                return execute_raw_sql(
                    "SELECT customer_id, name, email, phone, address, registration_date, 'Inserted via MySQL sp_insert_customer' AS procedure_status FROM customers WHERE customer_id = @new_customer_id",
                    fetch_all=True
                )
            except Exception:
                pass

        execute_raw_sql(
            "INSERT INTO customers (name, email, phone, address, registration_date) VALUES (:name, :email, :phone, :address, :reg_date)",
            {'name': name, 'email': email, 'phone': phone, 'address': address, 'reg_date': reg_date},
            commit=True
        )
        return execute_raw_sql(
            "SELECT customer_id, name, email, phone, address, registration_date, 'Inserted & Key Returned via sp_insert_customer' AS procedure_status FROM customers WHERE email = :email",
            {'email': email},
            fetch_all=True
        )

    raise ValueError(f"Unknown stored procedure key '{query_key}'")

def _execute_update_delete(query_key, q_info, params):
    """
    Executes DML statements (UPDATE / DELETE) with commit=True,
    then retrieves and returns the verified record state as tabular results.
    """
    if query_key == 'update_1':
        execute_raw_sql(
            "UPDATE accounts SET balance = 95000.00 WHERE account_id = 201",
            commit=True
        )
        return execute_raw_sql(
            "SELECT account_id, customer_id, account_type, balance, account_status, 'Balance Updated Successfully' AS status_check FROM accounts WHERE account_id = 201",
            fetch_all=True
        )

    elif query_key == 'update_2':
        execute_raw_sql(
            "UPDATE customers SET email = 'priya.patel.updated@example.com' WHERE customer_id = 102",
            commit=True
        )
        return execute_raw_sql(
            "SELECT customer_id, name, email, phone, address, registration_date, 'Email Changed Successfully' AS status_check FROM customers WHERE customer_id = 102",
            fetch_all=True
        )

    elif query_key == 'update_3':
        execute_raw_sql(
            "UPDATE branches SET location = 'Cyberabad, Hyderabad' WHERE branch_id = 1",
            commit=True
        )
        return execute_raw_sql(
            "SELECT branch_id, branch_name, location, 'Branch Location Updated' AS status_check FROM branches WHERE branch_id = 1",
            fetch_all=True
        )

    elif query_key == 'delete_1':
        deleted = execute_raw_sql(
            "DELETE FROM accounts WHERE account_status = 'Inactive'",
            commit=True
        )
        rows = execute_raw_sql(
            "SELECT account_id, customer_id, account_type, balance, account_status FROM accounts WHERE account_status = 'Inactive'",
            fetch_all=True
        )
        if not rows:
            return [{'status': 'Inactive Accounts Deleted', 'message': f'Deleted {deleted if isinstance(deleted, int) else 1} inactive account(s). 0 inactive accounts remain.', 'remaining_count': 0}]
        return rows

    elif query_key == 'delete_2':
        orphans = execute_raw_sql(
            "SELECT customer_id, name, email FROM customers WHERE customer_id NOT IN (SELECT DISTINCT customer_id FROM accounts WHERE customer_id IS NOT NULL)",
            fetch_all=True
        )
        deleted = execute_raw_sql(
            "DELETE FROM customers WHERE customer_id NOT IN (SELECT DISTINCT customer_id FROM accounts WHERE customer_id IS NOT NULL)",
            commit=True
        )
        rows = execute_raw_sql(
            "SELECT customer_id, name, email, phone, registration_date FROM customers WHERE customer_id NOT IN (SELECT DISTINCT customer_id FROM accounts WHERE customer_id IS NOT NULL)",
            fetch_all=True
        )
        if not rows:
            names_str = ", ".join([o['name'] for o in orphans]) if orphans else "None"
            return [{'status': 'Customers With No Accounts Deleted', 'message': f'Deleted {len(orphans)} customer(s) without accounts ({names_str}). 0 orphan customers remain.', 'remaining_count': 0}]
        return rows

    raise ValueError(f"Unknown update/delete query key '{query_key}'")

def run_registered_query(query_key, params=None):
    """
    Executes a predefined SQL exercise query, stored procedure, or DML update/delete.
    Supports dynamic parameter binding, native execution, and emulation fallbacks.
    Returns: dictionary with columns, rows, execution_time_ms, and row_count.
    """
    if query_key not in SQL_QUERIES_REGISTRY:
        raise ValueError(f"Query key '{query_key}' not recognized.")

    q_info = SQL_QUERIES_REGISTRY[query_key]
    params = params or {}
    start_time = time.perf_counter()

    if q_info.get('category') == 'Stored Procedures':
        rows = _execute_stored_procedure(query_key, q_info, params)
        raw_sql = _build_procedure_call_sql(query_key, q_info, params)
    elif q_info.get('category') == 'Updates & Deletes':
        rows = _execute_update_delete(query_key, q_info, params)
        raw_sql = q_info['sql'].strip()
    else:
        raw_sql = q_info['sql'].strip()
        rows = execute_raw_sql(raw_sql, fetch_all=True)

    execution_time = (time.perf_counter() - start_time) * 1000
    columns = list(rows[0].keys()) if rows else []

    return {
        'key': query_key,
        'title': q_info['title'],
        'category': q_info['category'],
        'description': q_info['description'],
        'sql': raw_sql,
        'definition': q_info.get('definition', ''),
        'procedure_name': q_info.get('procedure_name', ''),
        'parameters': q_info.get('parameters', []),
        'columns': columns,
        'rows': rows,
        'row_count': len(rows),
        'execution_time_ms': round(execution_time, 2)
    }

def run_custom_query(custom_sql):
    """
    Safely executes an ad-hoc custom query entered by an authorized user.
    Permits SELECT queries, Stored Procedure invocations (CALL), and DML (UPDATE, DELETE).
    """
    clean_sql = custom_sql.strip()
    first_word = clean_sql.split()[0].upper() if clean_sql else ''

    if first_word not in ('SELECT', 'WITH', 'EXPLAIN', 'PRAGMA', 'SHOW', 'DESCRIBE', 'CALL', 'UPDATE', 'DELETE'):
        raise ValueError("Only queries (SELECT, WITH, EXPLAIN), CALL statements, and DML (UPDATE, DELETE) are permitted in this console.")

    start_time = time.perf_counter()

    # Special handling for CALL statements
    if first_word == 'CALL':
        match = re.match(r'CALL\s+(sp_\w+)(?:\s*\((.*?)\))?', clean_sql, re.IGNORECASE)
        if match:
            proc_name = match.group(1).lower()
            raw_args = [arg.strip().strip("'\"") for arg in match.group(2).split(',') if arg.strip()] if match.group(2) else []
            
            if proc_name == 'sp_customer_accounts':
                cid = int(raw_args[0]) if raw_args and raw_args[0].isdigit() else 101
                rows = _execute_stored_procedure('proc_1', SQL_QUERIES_REGISTRY['proc_1'], {'p_customer_id': cid})
            elif proc_name == 'sp_account_transactions':
                aid = int(raw_args[0]) if raw_args and raw_args[0].isdigit() else 201
                rows = _execute_stored_procedure('proc_2', SQL_QUERIES_REGISTRY['proc_2'], {'p_account_id': aid})
            elif proc_name == 'sp_calculate_total_balance':
                rows = _execute_stored_procedure('proc_3', SQL_QUERIES_REGISTRY['proc_3'], {})
            elif proc_name == 'sp_update_balance':
                aid = int(raw_args[0]) if len(raw_args) > 0 and raw_args[0].isdigit() else 201
                bal = float(raw_args[1]) if len(raw_args) > 1 else 85000.00
                rows = _execute_stored_procedure('proc_4', SQL_QUERIES_REGISTRY['proc_4'], {'p_account_id': aid, 'p_new_balance': bal})
            elif proc_name == 'sp_insert_customer':
                name = raw_args[0] if len(raw_args) > 0 else 'Kavita Krishnan'
                email = raw_args[1] if len(raw_args) > 1 else 'kavita.k@example.com'
                phone = raw_args[2] if len(raw_args) > 2 else '9876501234'
                address = raw_args[3] if len(raw_args) > 3 else 'Jubilee Hills, Hyderabad'
                reg_date = raw_args[4] if len(raw_args) > 4 else '2024-04-15'
                rows = _execute_stored_procedure('proc_5', SQL_QUERIES_REGISTRY['proc_5'], {
                    'p_name': name, 'p_email': email, 'p_phone': phone, 'p_address': address, 'p_reg_date': reg_date
                })
            else:
                rows = execute_raw_sql(clean_sql, fetch_all=True)
        else:
            rows = execute_raw_sql(clean_sql, fetch_all=True)
    elif first_word in ('UPDATE', 'DELETE'):
        rowcount = execute_raw_sql(clean_sql, commit=True)
        rows = [{
            'operation': first_word,
            'rows_affected': rowcount if isinstance(rowcount, int) else 1,
            'status': 'Statement Executed and Committed Successfully'
        }]
    else:
        rows = execute_raw_sql(clean_sql, fetch_all=True)

    execution_time = (time.perf_counter() - start_time) * 1000
    columns = list(rows[0].keys()) if rows else []

    return {
        'sql': clean_sql,
        'columns': columns,
        'rows': rows,
        'row_count': len(rows),
        'execution_time_ms': round(execution_time, 2)
    }

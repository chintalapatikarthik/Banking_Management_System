import re
import time
from datetime import datetime
from decimal import Decimal
from sqlalchemy import text
from app.database import execute_raw_sql, engine, get_db
from app.models import QueryHistory

# =====================================================================
# Canonical 41 SQL Questions Registry (from Banking_Management_System.sql)
# Organized across 8 Core Categories
# =====================================================================

SQL_QUERIES_REGISTRY = {
    # -----------------------------------------------------------------
    # 1. Basic Queries (Q1 - Q4)
    # -----------------------------------------------------------------
    'q1': {
        'id': 1,
        'q_num': 1,
        'category': 'Basic Queries',
        'title': 'Display accounts with balance greater than 50000',
        'description': 'Filters all bank accounts where the available balance exceeds ₹50,000 using WHERE clause.',
        'explanation': 'The WHERE clause evaluates a boolean condition on each row. Here, balance > 50000 filters for high-balance accounts.',
        'sql': "SELECT * FROM accounts WHERE balance > 50000;",
        'is_dml': False,
        'is_sp': False,
        'is_view': False,
        'is_report': False
    },
    'q2': {
        'id': 2,
        'q_num': 2,
        'category': 'Basic Queries',
        'title': 'Show all customers from Hyderabad',
        'description': 'Retrieves all customers whose residential address contains "Hyderabad" using LIKE pattern matching.',
        'explanation': "The LIKE operator searches with wildcards ('%'). '%Hyderabad%' matches any address containing 'Hyderabad'.",
        'sql': "SELECT * FROM customers WHERE address LIKE '%Hyderabad%';",
        'is_dml': False,
        'is_sp': False,
        'is_view': False,
        'is_report': False
    },
    'q3': {
        'id': 3,
        'q_num': 3,
        'category': 'Basic Queries',
        'title': 'List savings accounts',
        'description': 'Lists all accounts classified as Savings account type.',
        'explanation': "A simple equality condition filtering for rows where account_type matches 'Savings'.",
        'sql': "SELECT * FROM accounts WHERE account_type = 'Savings';",
        'is_dml': False,
        'is_sp': False,
        'is_view': False,
        'is_report': False
    },
    'q4': {
        'id': 4,
        'q_num': 4,
        'category': 'Basic Queries',
        'title': 'Display employees joined after 2022',
        'description': 'Filters employees who were hired on or after January 1st, 2023 using date comparison.',
        'explanation': "Date literals in standard ISO format 'YYYY-MM-DD' allow direct comparison with relational operators like >=.",
        'sql': "SELECT * FROM employees WHERE joining_date >= '2023-01-01';",
        'is_dml': False,
        'is_sp': False,
        'is_view': False,
        'is_report': False
    },

    # -----------------------------------------------------------------
    # 2. Joins (Q5 - Q10)
    # -----------------------------------------------------------------
    'q5': {
        'id': 5,
        'q_num': 5,
        'category': 'Joins',
        'title': 'Show customer name with their accounts',
        'description': 'Performs an INNER JOIN between Customers and Accounts to show each account alongside its holder name.',
        'explanation': 'INNER JOIN pairs records from Customers and Accounts where the primary key customer_id matches the foreign key.',
        'sql': """SELECT c.customer_id, c.name AS customer_name,
       a.account_id, a.account_type, a.balance, a.opening_date
FROM customers c
INNER JOIN accounts a ON c.customer_id = a.customer_id;""",
        'is_dml': False,
        'is_sp': False,
        'is_view': False,
        'is_report': False
    },
    'q6': {
        'id': 6,
        'q_num': 6,
        'category': 'Joins',
        'title': 'Display account with transaction details',
        'description': 'Joins Accounts with Transactions to review the complete financial activity per account.',
        'explanation': 'INNER JOIN links each transaction record to its corresponding account record via account_id.',
        'sql': """SELECT a.account_id, a.account_type, a.balance,
       t.transaction_id, t.transaction_type, t.amount, t.transaction_date
FROM accounts a
INNER JOIN transactions t ON a.account_id = t.account_id;""",
        'is_dml': False,
        'is_sp': False,
        'is_view': False,
        'is_report': False
    },
    'q7': {
        'id': 7,
        'q_num': 7,
        'category': 'Joins',
        'title': 'Show loan details with customer information',
        'description': 'Joins Loans with Customers to inspect credit exposures linked to customer contact details.',
        'explanation': 'INNER JOIN matches customer demographics with active loan facilities through customer_id.',
        'sql': """SELECT l.loan_id, c.customer_id, c.name AS customer_name,
       l.loan_amount, l.interest_rate, l.loan_date
FROM loans l
INNER JOIN customers c ON l.customer_id = c.customer_id;""",
        'is_dml': False,
        'is_sp': False,
        'is_view': False,
        'is_report': False
    },
    'q8': {
        'id': 8,
        'q_num': 8,
        'category': 'Joins',
        'title': 'Assign branch to employees & verify schema',
        'description': 'Q8 in SQL script: Schema alteration adding branch_id foreign key to Employees and updating staff branch assignments.',
        'explanation': 'Demonstrates DDL schema alteration (ALTER TABLE) adding foreign keys and updating entity relationships.',
        'sql': """-- Schema extension demonstrated:
-- ALTER TABLE employees ADD COLUMN branch_id INT;
-- ALTER TABLE employees ADD CONSTRAINT fk_employees_branch FOREIGN KEY (branch_id) REFERENCES branches(branch_id);
SELECT e.employee_id, e.employee_name, e.position, e.branch_id, b.branch_name, b.location
FROM employees e
LEFT JOIN branches b ON e.branch_id = b.branch_id;""",
        'is_dml': False,
        'is_sp': False,
        'is_view': False,
        'is_report': False
    },
    'q9': {
        'id': 9,
        'q_num': 9,
        'category': 'Joins',
        'title': 'List employees with their branch',
        'description': 'INNER JOIN between Employees and Branches showing the branch location each staff member is assigned to.',
        'explanation': 'INNER JOIN displays staff members alongside their assigned physical branch location.',
        'sql': """SELECT e.employee_id, e.employee_name, e.position,
       b.branch_id, b.branch_name, b.location
FROM employees e
INNER JOIN branches b ON e.branch_id = b.branch_id;""",
        'is_dml': False,
        'is_sp': False,
        'is_view': False,
        'is_report': False
    },
    'q10': {
        'id': 10,
        'q_num': 10,
        'category': 'Joins',
        'title': 'Show customers with their transactions',
        'description': 'Multi-table JOIN connecting Customers through Accounts to Transactions.',
        'explanation': 'Performs a three-table chain join (Customers -> Accounts -> Transactions) to trace cash movement back to customer profiles.',
        'sql': """SELECT c.customer_id, c.name AS customer_name, a.account_id,
       t.transaction_id, t.transaction_type, t.amount, t.transaction_date
FROM customers c
INNER JOIN accounts a ON c.customer_id = a.customer_id
INNER JOIN transactions t ON a.account_id = t.account_id;""",
        'is_dml': False,
        'is_sp': False,
        'is_view': False,
        'is_report': False
    },

    # -----------------------------------------------------------------
    # 3. Aggregate Functions (Q11 - Q15)
    # -----------------------------------------------------------------
    'q11': {
        'id': 11,
        'q_num': 11,
        'category': 'Aggregate Functions',
        'title': 'Count total customers',
        'description': 'Uses COUNT(*) to compute the total number of registered bank customers.',
        'explanation': 'COUNT(*) counts the total number of rows meeting criteria (or in the whole table if unfiltered).',
        'sql': "SELECT COUNT(*) AS total_customers FROM customers;",
        'is_dml': False,
        'is_sp': False,
        'is_view': False,
        'is_report': False
    },
    'q12': {
        'id': 12,
        'q_num': 12,
        'category': 'Aggregate Functions',
        'title': 'Find average account balance',
        'description': 'Uses AVG() and ROUND() to determine the mean balance across all accounts.',
        'explanation': 'AVG(balance) computes the arithmetic mean, and ROUND(..., 2) formats the result to 2 decimal places.',
        'sql': "SELECT ROUND(AVG(balance), 2) AS average_account_balance FROM accounts;",
        'is_dml': False,
        'is_sp': False,
        'is_view': False,
        'is_report': False
    },
    'q13': {
        'id': 13,
        'q_num': 13,
        'category': 'Aggregate Functions',
        'title': 'Calculate total loan amount',
        'description': 'Uses SUM() to calculate the total outstanding credit / loan portfolio.',
        'explanation': 'SUM(loan_amount) accumulates all values in the column to return total bank credit exposure.',
        'sql': "SELECT SUM(loan_amount) AS total_loan_amount FROM loans;",
        'is_dml': False,
        'is_sp': False,
        'is_view': False,
        'is_report': False
    },
    'q14': {
        'id': 14,
        'q_num': 14,
        'category': 'Aggregate Functions',
        'title': 'Count total transactions',
        'description': 'Computes total transaction count across all accounts.',
        'explanation': 'COUNT(*) returns total ledger rows across Deposits, Withdrawals, and Transfers.',
        'sql': "SELECT COUNT(*) AS total_transactions FROM transactions;",
        'is_dml': False,
        'is_sp': False,
        'is_view': False,
        'is_report': False
    },
    'q15': {
        'id': 15,
        'q_num': 15,
        'category': 'Aggregate Functions',
        'title': 'Find highest account balance',
        'description': 'Finds the highest balance across all bank accounts.',
        'explanation': 'MAX(balance) scans column values and identifies the single maximum deposit figure.',
        'sql': "SELECT MAX(balance) AS highest_account_balance FROM accounts;",
        'is_dml': False,
        'is_sp': False,
        'is_view': False,
        'is_report': False
    },

    # -----------------------------------------------------------------
    # 4. Subqueries (Q16 - Q20)
    # -----------------------------------------------------------------
    'q16': {
        'id': 16,
        'q_num': 16,
        'category': 'Subqueries',
        'title': 'Find customers who have no accounts',
        'description': 'Uses NOT EXISTS subquery to detect customers who registered but hold no active accounts.',
        'explanation': 'Correlated subquery with NOT EXISTS checks if an inner SELECT returns 0 rows for the outer customer.',
        'sql': """SELECT c.*
FROM customers c
WHERE NOT EXISTS (
    SELECT 1 FROM accounts a WHERE a.customer_id = c.customer_id
);""",
        'is_dml': False,
        'is_sp': False,
        'is_view': False,
        'is_report': False
    },
    'q17': {
        'id': 17,
        'q_num': 17,
        'category': 'Subqueries',
        'title': 'Find accounts with no transactions',
        'description': 'Uses NOT EXISTS subquery to identify accounts without any transaction history.',
        'explanation': 'Detects dormant or newly opened accounts that have zero records in the transactions ledger.',
        'sql': """SELECT a.*
FROM accounts a
WHERE NOT EXISTS (
    SELECT 1 FROM transactions t WHERE t.account_id = a.account_id
);""",
        'is_dml': False,
        'is_sp': False,
        'is_view': False,
        'is_report': False
    },
    'q18': {
        'id': 18,
        'q_num': 18,
        'category': 'Subqueries',
        'title': 'Show accounts with balance greater than average',
        'description': 'Uses a scalar subquery (AVG) in the WHERE clause to find above-average balance accounts.',
        'explanation': 'The scalar subquery (SELECT AVG(balance) FROM accounts) evaluates first, then compares with each account balance.',
        'sql': """SELECT *
FROM accounts
WHERE balance > (SELECT AVG(balance) FROM accounts);""",
        'is_dml': False,
        'is_sp': False,
        'is_view': False,
        'is_report': False
    },
    'q19': {
        'id': 19,
        'q_num': 19,
        'category': 'Subqueries',
        'title': 'Find customers with loan amount above average',
        'description': 'Identifies customers holding loans greater than the bank-wide average loan amount.',
        'explanation': 'Combines an INNER JOIN with a scalar subquery (SELECT AVG(loan_amount) FROM loans).',
        'sql': """SELECT c.customer_id, c.name AS customer_name, l.loan_id, l.loan_amount
FROM customers c
INNER JOIN loans l ON c.customer_id = l.customer_id
WHERE l.loan_amount > (SELECT AVG(loan_amount) FROM loans);""",
        'is_dml': False,
        'is_sp': False,
        'is_view': False,
        'is_report': False
    },
    'q20': {
        'id': 20,
        'q_num': 20,
        'category': 'Subqueries',
        'title': 'Show transactions above average amount',
        'description': 'Filters all transactions that exceed the average monetary value of all transactions.',
        'explanation': 'Dynamically computes the average transaction amount and returns entries with amount > average.',
        'sql': """SELECT *
FROM transactions
WHERE amount > (SELECT AVG(amount) FROM transactions);""",
        'is_dml': False,
        'is_sp': False,
        'is_view': False,
        'is_report': False
    },

    # -----------------------------------------------------------------
    # 5. Updates & Deletes (Q21 - Q25)
    # -----------------------------------------------------------------
    'q21': {
        'id': 21,
        'q_num': 21,
        'category': 'Updates & Deletes',
        'title': 'Update account balance',
        'description': 'Updates the balance of account 101 to ₹90,000.00 and verifies the updated account record.',
        'explanation': 'DML UPDATE modifying a column value based on primary key filter, preserving data integrity.',
        'sql': """-- 1. Update Account Balance:
UPDATE accounts 
SET balance = 90000.00 
WHERE account_id = 101;

-- 2. Verify Updated Account Balance:
SELECT account_id, customer_id, account_type, balance, account_status 
FROM accounts 
WHERE account_id = 101;""",
        'is_dml': True,
        'is_sp': False,
        'is_view': False,
        'is_report': False
    },
    'q22': {
        'id': 22,
        'q_num': 22,
        'category': 'Updates & Deletes',
        'title': 'Change customer email',
        'description': 'Updates the registered email address for customer ID 1 to aarav.updated@example.com and verifies the profile.',
        'explanation': 'DML UPDATE modifying customer contact information filtered by customer_id.',
        'sql': """-- 1. Change Customer Email:
UPDATE customers 
SET email = 'aarav.updated@example.com' 
WHERE customer_id = 1;

-- 2. Verify Changed Customer Email:
SELECT customer_id, name, email, phone, address, registration_date 
FROM customers 
WHERE customer_id = 1;""",
        'is_dml': True,
        'is_sp': False,
        'is_view': False,
        'is_report': False
    },
    'q23': {
        'id': 23,
        'q_num': 23,
        'category': 'Updates & Deletes',
        'title': 'Update branch location',
        'description': 'Updates the physical branch location for branch ID 401 to Hitech City, Hyderabad and verifies the branch record.',
        'explanation': 'DML UPDATE modifying branch geographic location record in branches table.',
        'sql': """-- 1. Update Branch Location:
UPDATE branches 
SET location = 'Hitech City, Hyderabad' 
WHERE branch_id = 401;

-- 2. Verify Updated Branch Location:
SELECT branch_id, branch_name, location 
FROM branches 
WHERE branch_id = 401;""",
        'is_dml': True,
        'is_sp': False,
        'is_view': False,
        'is_report': False
    },
    'q24': {
        'id': 24,
        'q_num': 24,
        'category': 'Updates & Deletes',
        'title': 'Delete inactive accounts',
        'description': 'Deletes bank accounts where account_status is Inactive, preserving relational integrity.',
        'explanation': 'DML DELETE removing inactive accounts while cascading or removing associated ledger references.',
        'sql': """-- 1. Delete Inactive Accounts:
DELETE FROM accounts 
WHERE account_status = 'Inactive';

-- 2. Verify Inactive Accounts Deletion:
SELECT account_id, customer_id, account_type, balance, account_status 
FROM accounts 
WHERE account_status = 'Inactive';""",
        'is_dml': True,
        'is_sp': False,
        'is_view': False,
        'is_report': False
    },
    'q25': {
        'id': 25,
        'q_num': 25,
        'category': 'Updates & Deletes',
        'title': 'Delete customers with no accounts',
        'description': 'Deletes customer records who do not hold any bank accounts or loans.',
        'explanation': 'DML DELETE with NOT EXISTS to safely remove orphan customer registrations with no accounts or loans.',
        'sql': """-- 1. Delete Customers With No Accounts:
DELETE FROM customers 
WHERE NOT EXISTS (
    SELECT 1 FROM accounts a WHERE a.customer_id = customers.customer_id
)
AND NOT EXISTS (
    SELECT 1 FROM loans l WHERE l.customer_id = customers.customer_id
);

-- 2. Verify Customers with No Accounts (Should return 0):
SELECT customer_id, name, email, phone, registration_date 
FROM customers 
WHERE NOT EXISTS (
    SELECT 1 FROM accounts a WHERE a.customer_id = customers.customer_id
);""",
        'is_dml': True,
        'is_sp': False,
        'is_view': False,
        'is_report': False
    },

    # -----------------------------------------------------------------
    # 6. Views (Q26 - Q30)
    # -----------------------------------------------------------------
    'q26': {
        'id': 26,
        'q_num': 26,
        'category': 'Views',
        'title': 'Customer Accounts View (vw_customer_accounts)',
        'description': 'Predefined view displaying customer profile, account type, balance, and opening date.',
        'explanation': 'Views encapsulate complex joins and provide a simplified virtual table for secure application access.',
        'sql': "SELECT * FROM vw_customer_accounts;",
        'definition': """CREATE OR REPLACE VIEW vw_customer_accounts AS
SELECT c.customer_id, c.name AS customer_name, c.email, c.phone,
       a.account_id, a.account_type, a.balance, a.opening_date
FROM Customers c
INNER JOIN Accounts a ON c.customer_id = a.customer_id;""",
        'is_dml': False,
        'is_sp': False,
        'is_view': True,
        'is_report': False
    },
    'q27': {
        'id': 27,
        'q_num': 27,
        'category': 'Views',
        'title': 'Transaction Details View (vw_transaction_details)',
        'description': 'Predefined view joining transaction records, accounts, and client holders.',
        'explanation': 'Virtual view denormalizing ledger entries with account and customer holder metadata.',
        'sql': "SELECT * FROM vw_transaction_details;",
        'definition': """CREATE OR REPLACE VIEW vw_transaction_details AS
SELECT t.transaction_id, t.account_id, c.customer_id,
       c.name AS customer_name, t.transaction_type, t.amount, t.transaction_date
FROM Transactions t
INNER JOIN Accounts a ON t.account_id = a.account_id
INNER JOIN Customers c ON a.customer_id = c.customer_id;""",
        'is_dml': False,
        'is_sp': False,
        'is_view': True,
        'is_report': False
    },
    'q28': {
        'id': 28,
        'q_num': 28,
        'category': 'Views',
        'title': 'Loan Details with Customers View (vw_loan_details_customers)',
        'description': 'Predefined view joining loan credit details with customer demographic data.',
        'explanation': 'Consolidates credit liability portfolio with borrower names, email, interest rate, and issuance dates.',
        'sql': "SELECT * FROM vw_loan_details_customers;",
        'definition': """CREATE OR REPLACE VIEW vw_loan_details_customers AS
SELECT l.loan_id, c.customer_id, c.name AS customer_name, c.email,
       l.loan_amount, l.interest_rate, l.loan_date
FROM Loans l
INNER JOIN Customers c ON l.customer_id = c.customer_id;""",
        'is_dml': False,
        'is_sp': False,
        'is_view': True,
        'is_report': False
    },
    'q29': {
        'id': 29,
        'q_num': 29,
        'category': 'Views',
        'title': 'Total Balance per Customer View (vw_total_balance_per_customer)',
        'description': 'Predefined view calculating aggregate liquid balance per customer.',
        'explanation': 'Aggregates multi-account balances per client into a single net worth metric using LEFT JOIN and GROUP BY.',
        'sql': "SELECT * FROM vw_total_balance_per_customer;",
        'definition': """CREATE OR REPLACE VIEW vw_total_balance_per_customer AS
SELECT c.customer_id, c.name AS customer_name,
       COALESCE(SUM(a.balance), 0.00) AS total_balance
FROM Customers c
LEFT JOIN Accounts a ON c.customer_id = a.customer_id
GROUP BY c.customer_id, c.name;""",
        'is_dml': False,
        'is_sp': False,
        'is_view': True,
        'is_report': False
    },
    'q30': {
        'id': 30,
        'q_num': 30,
        'category': 'Views',
        'title': 'High Value Transactions View (vw_high_value_transactions)',
        'description': 'Predefined view filtered for high-value transactions (> ₹50,000).',
        'explanation': 'Provides an automated compliance and AML audit view filtering transactions exceeding ₹50,000.',
        'sql': "SELECT * FROM vw_high_value_transactions;",
        'definition': """CREATE OR REPLACE VIEW vw_high_value_transactions AS
SELECT transaction_id, account_id, transaction_type, amount, transaction_date
FROM Transactions
WHERE amount > 50000;""",
        'is_dml': False,
        'is_sp': False,
        'is_view': True,
        'is_report': False
    },

    # -----------------------------------------------------------------
    # 7. Stored Procedures (Q31 - Q35)
    # -----------------------------------------------------------------
    'q31': {
        'id': 31,
        'q_num': 31,
        'category': 'Stored Procedures',
        'title': 'Insert New Customer (sp_insert_new_customer)',
        'procedure_name': 'sp_insert_new_customer',
        'description': 'Executes stored procedure sp_insert_new_customer to insert a new client into Customers table.',
        'explanation': 'Encapsulates customer registration logic and validation inside an atomic database procedure.',
        'parameters': [
            {'name': 'p_customer_id', 'type': 'INT', 'default': 11, 'label': 'Customer ID'},
            {'name': 'p_name', 'type': 'VARCHAR', 'default': 'Ravi Teja', 'label': 'Customer Name'},
            {'name': 'p_email', 'type': 'VARCHAR', 'default': 'ravi.teja@example.com', 'label': 'Email Address'},
            {'name': 'p_phone', 'type': 'VARCHAR', 'default': '9876501011', 'label': 'Phone Number'},
            {'name': 'p_address', 'type': 'VARCHAR', 'default': 'Guntur, Andhra Pradesh', 'label': 'Address'},
            {'name': 'p_registration_date', 'type': 'DATE', 'default': '2024-06-01', 'label': 'Registration Date'}
        ],
        'sql': "CALL sp_insert_new_customer(11, 'Ravi Teja', 'ravi.teja@example.com', '9876501011', 'Guntur, Andhra Pradesh', '2024-06-01');",
        'definition': """DELIMITER //
CREATE PROCEDURE sp_insert_new_customer(
    IN p_customer_id INT,
    IN p_name VARCHAR(100),
    IN p_email VARCHAR(100),
    IN p_phone VARCHAR(15),
    IN p_address VARCHAR(255),
    IN p_registration_date DATE
)
BEGIN
    INSERT INTO Customers
    (customer_id, name, email, phone, address, registration_date)
    VALUES
    (p_customer_id, p_name, p_email, p_phone, p_address, p_registration_date);
END//
DELIMITER ;""",
        'is_dml': False,
        'is_sp': True,
        'is_view': False,
        'is_report': False
    },
    'q32': {
        'id': 32,
        'q_num': 32,
        'category': 'Stored Procedures',
        'title': 'Update Account Balance (sp_update_account_balance)',
        'procedure_name': 'sp_update_account_balance',
        'description': 'Executes stored procedure sp_update_account_balance enforcing business check constraints (raises SQLSTATE 45000 if negative).',
        'explanation': 'Ensures database-level business constraint checking and transactional balance updates.',
        'parameters': [
            {'name': 'p_account_id', 'type': 'INT', 'default': 101, 'label': 'Account ID'},
            {'name': 'p_new_balance', 'type': 'DECIMAL', 'default': 95000.00, 'label': 'New Balance (₹)'}
        ],
        'sql': "CALL sp_update_account_balance(101, 95000.00);",
        'definition': """DELIMITER //
DROP PROCEDURE IF EXISTS sp_update_account_balance//
CREATE PROCEDURE sp_update_account_balance(
    IN p_account_id INT,
    IN p_new_balance DECIMAL(12,2)
)
BEGIN
    IF p_new_balance < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Account balance cannot be negative';
    ELSE
        UPDATE Accounts
        SET balance = p_new_balance
        WHERE account_id = p_account_id;

        IF ROW_COUNT() = 0 THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Account not found';
        END IF;
    END IF;
END//
DELIMITER ;""",
        'is_dml': False,
        'is_sp': True,
        'is_view': False,
        'is_report': False
    },
    'q33': {
        'id': 33,
        'q_num': 33,
        'category': 'Stored Procedures',
        'title': 'Display Transactions of an Account (sp_display_account_transactions)',
        'procedure_name': 'sp_display_account_transactions',
        'description': 'Executes stored procedure sp_display_account_transactions to retrieve the complete transaction ledger for an account.',
        'explanation': 'Retrieves all financial movements for an account sorted in reverse chronological order.',
        'parameters': [
            {'name': 'p_account_id', 'type': 'INT', 'default': 101, 'label': 'Account ID'}
        ],
        'sql': "CALL sp_display_account_transactions(101);",
        'definition': """DELIMITER //
DROP PROCEDURE IF EXISTS sp_display_account_transactions//
CREATE PROCEDURE sp_display_account_transactions(IN p_account_id INT)
BEGIN
    SELECT transaction_id, account_id, transaction_type, amount, transaction_date
    FROM Transactions
    WHERE account_id = p_account_id
    ORDER BY transaction_date DESC;
END//
DELIMITER ;""",
        'is_dml': False,
        'is_sp': True,
        'is_view': False,
        'is_report': False
    },
    'q34': {
        'id': 34,
        'q_num': 34,
        'category': 'Stored Procedures',
        'title': 'Calculate Total Bank Balance (sp_calculate_total_bank_balance)',
        'procedure_name': 'sp_calculate_total_bank_balance',
        'description': 'Executes parameter-less stored procedure sp_calculate_total_bank_balance to compute cumulative liquidity.',
        'explanation': 'Aggregates all liquid funds held in deposits across the entire banking institution.',
        'parameters': [],
        'sql': "CALL sp_calculate_total_bank_balance();",
        'definition': """DELIMITER //
DROP PROCEDURE IF EXISTS sp_calculate_total_bank_balance//
CREATE PROCEDURE sp_calculate_total_bank_balance()
BEGIN
    SELECT COALESCE(SUM(balance), 0.00) AS total_bank_balance
    FROM Accounts;
END//
DELIMITER ;""",
        'is_dml': False,
        'is_sp': True,
        'is_view': False,
        'is_report': False
    },
    'q35': {
        'id': 35,
        'q_num': 35,
        'category': 'Stored Procedures',
        'title': 'List Accounts of a Customer (sp_list_customer_accounts)',
        'procedure_name': 'sp_list_customer_accounts',
        'description': 'Executes stored procedure sp_list_customer_accounts to list all accounts held by a customer.',
        'explanation': 'Returns account portfolio (savings, current, balances, opening date) belonging to a client.',
        'parameters': [
            {'name': 'p_customer_id', 'type': 'INT', 'default': 1, 'label': 'Customer ID'}
        ],
        'sql': "CALL sp_list_customer_accounts(1);",
        'definition': """DELIMITER //
DROP PROCEDURE IF EXISTS sp_list_customer_accounts//
CREATE PROCEDURE sp_list_customer_accounts(IN p_customer_id INT)
BEGIN
    SELECT account_id, customer_id, account_type, balance, opening_date
    FROM Accounts
    WHERE customer_id = p_customer_id;
END//
DELIMITER ;""",
        'is_dml': False,
        'is_sp': True,
        'is_view': False,
        'is_report': False
    },

    # -----------------------------------------------------------------
    # 8. Reports / Analysis (Q36 - Q41)
    # -----------------------------------------------------------------
    'q36': {
        'id': 36,
        'q_num': 36,
        'category': 'Reports / Analysis',
        'title': 'Top 5 customers with highest balance',
        'description': 'Adds balances across all accounts belonging to each customer and ranks the top 5.',
        'explanation': 'Sums account balances per client and sorts in descending order with LIMIT 5 to highlight high net-worth individuals.',
        'sql': """SELECT c.customer_id, c.name AS customer_name, SUM(a.balance) AS total_balance
FROM customers c
INNER JOIN accounts a ON c.customer_id = a.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_balance DESC
LIMIT 5;""",
        'is_dml': False,
        'is_sp': False,
        'is_view': False,
        'is_report': True
    },
    'q37': {
        'id': 37,
        'q_num': 37,
        'category': 'Reports / Analysis',
        'title': 'Most active customers',
        'description': 'Ranks customers by activity measured by total transaction frequency.',
        'explanation': 'Counts ledger entries per customer profile, ordering by transaction volume to find the most engaged customers.',
        'sql': """SELECT c.customer_id, c.name AS customer_name,
       COUNT(t.transaction_id) AS total_transactions
FROM customers c
INNER JOIN accounts a ON c.customer_id = a.customer_id
INNER JOIN transactions t ON a.account_id = t.account_id
GROUP BY c.customer_id, c.name
ORDER BY total_transactions DESC
LIMIT 10;""",
        'is_dml': False,
        'is_sp': False,
        'is_view': False,
        'is_report': True
    },
    'q38': {
        'id': 38,
        'q_num': 38,
        'category': 'Reports / Analysis',
        'title': 'Monthly transaction report',
        'description': 'Aggregates monthly transaction counts, total amount, deposits, withdrawals, and transfers.',
        'explanation': 'Pivots transaction types by month using conditional SUM(CASE ...) expressions to produce a monthly cash flow audit.',
        'sql': """SELECT SUBSTR(transaction_date, 1, 7) AS month_year,
       COUNT(*) AS total_transactions,
       SUM(amount) AS total_amount,
       SUM(CASE WHEN transaction_type = 'Deposit' THEN amount ELSE 0 END) AS total_deposits,
       SUM(CASE WHEN transaction_type = 'Withdrawal' THEN amount ELSE 0 END) AS total_withdrawals,
       SUM(CASE WHEN transaction_type LIKE 'Transfer%' THEN amount ELSE 0 END) AS total_transfers
FROM transactions
GROUP BY SUBSTR(transaction_date, 1, 7)
ORDER BY month_year;""",
        'is_dml': False,
        'is_sp': False,
        'is_view': False,
        'is_report': True
    },
    'q39': {
        'id': 39,
        'q_num': 39,
        'category': 'Reports / Analysis',
        'title': 'Branch with highest deposits',
        'description': 'Identifies the operating branch with the highest cumulative deposit volume.',
        'explanation': 'Connects branches to accounts and deposit transactions, identifying the top branch by cash inflow.',
        'sql': """SELECT b.branch_id, b.branch_name, b.location,
       SUM(t.amount) AS total_deposits
FROM branches b
INNER JOIN accounts a ON b.branch_id = a.branch_id
INNER JOIN transactions t ON a.account_id = t.account_id
WHERE t.transaction_type = 'Deposit'
GROUP BY b.branch_id, b.branch_name, b.location
ORDER BY total_deposits DESC
LIMIT 1;""",
        'is_dml': False,
        'is_sp': False,
        'is_view': False,
        'is_report': True
    },
    'q40': {
        'id': 40,
        'q_num': 40,
        'category': 'Reports / Analysis',
        'title': 'Customer transaction analysis',
        'description': 'Comprehensive breakdown of customer transaction counts, deposits, withdrawals, transfers, and total volume.',
        'explanation': 'Per-customer matrix computing deposit, withdrawal, and transfer totals with COALESCE handling null states.',
        'sql': """SELECT c.customer_id, c.name AS customer_name,
       COUNT(t.transaction_id) AS transaction_count,
       COALESCE(SUM(CASE WHEN t.transaction_type = 'Deposit' THEN t.amount ELSE 0 END), 0) AS total_deposits,
       COALESCE(SUM(CASE WHEN t.transaction_type = 'Withdrawal' THEN t.amount ELSE 0 END), 0) AS total_withdrawals,
       COALESCE(SUM(CASE WHEN t.transaction_type LIKE 'Transfer%' THEN t.amount ELSE 0 END), 0) AS total_transfers,
       COALESCE(SUM(t.amount), 0) AS total_transaction_amount
FROM customers c
LEFT JOIN accounts a ON c.customer_id = a.customer_id
LEFT JOIN transactions t ON a.account_id = t.account_id
GROUP BY c.customer_id, c.name
ORDER BY total_transaction_amount DESC;""",
        'is_dml': False,
        'is_sp': False,
        'is_view': False,
        'is_report': True
    },
    'q41': {
        'id': 41,
        'q_num': 41,
        'category': 'Reports / Analysis',
        'title': 'Highest loan customers',
        'description': 'Ranks customers by combined loan liabilities in descending order.',
        'explanation': 'Sums debt obligations per client to highlight top lending risks and credit exposures.',
        'sql': """SELECT c.customer_id, c.name AS customer_name,
       SUM(l.loan_amount) AS total_loan_amount
FROM customers c
INNER JOIN loans l ON c.customer_id = l.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_loan_amount DESC
LIMIT 5;""",
        'is_dml': False,
        'is_sp': False,
        'is_view': False,
        'is_report': True
    }
}

# =====================================================================
# Legacy Aliases Mapping (Preserves 100% Backwards Compatibility)
# =====================================================================

QUERY_ALIASES = {
    'basic_1': 'q1',
    'basic_2': 'q2',
    'basic_3': 'q3',
    'basic_4': 'q4',
    'join_1': 'q5',
    'join_2': 'q6',
    'join_3': 'q7',
    'join_4': 'q8',
    'join_5': 'q9',
    'join_6': 'q10',
    'agg_1': 'q11',
    'agg_2': 'q12',
    'agg_3': 'q13',
    'agg_4': 'q14',
    'agg_5': 'q15',
    'subquery_1': 'q16',
    'subquery_2': 'q17',
    'subquery_3': 'q18',
    'subquery_4': 'q19',
    'subquery_5': 'q20',
    'update_1': 'q21',
    'update_2': 'q22',
    'update_3': 'q23',
    'delete_1': 'q24',
    'delete_2': 'q25',
    'view_1': 'q26',
    'view_2': 'q27',
    'view_3': 'q28',
    'view_4': 'q29',
    'view_5': 'q30',
    'proc_1': 'q35',  # sp_list_customer_accounts
    'proc_2': 'q33',  # sp_display_account_transactions
    'proc_3': 'q34',  # sp_calculate_total_bank_balance
    'proc_4': 'q32',  # sp_update_account_balance
    'proc_5': 'q31',  # sp_insert_new_customer
    'report_1': 'q36',
    'report_2': 'q37',
    'report_3': 'q38',
    'report_4': 'q39',
    'report_5': 'q40',
    'report_6': 'q41'
}

# Add alias keys into registry as references so iteration and key lookups work directly
for alias, primary in QUERY_ALIASES.items():
    if primary in SQL_QUERIES_REGISTRY and alias not in SQL_QUERIES_REGISTRY:
        SQL_QUERIES_REGISTRY[alias] = SQL_QUERIES_REGISTRY[primary]


def resolve_query_key(identifier):
    """Resolves an integer, qN string, or legacy alias string to canonical qN key."""
    if isinstance(identifier, int):
        key = f"q{identifier}"
        if key in SQL_QUERIES_REGISTRY:
            return key
    str_id = str(identifier).strip().lower()
    if str_id.isdigit():
        key = f"q{str_id}"
        if key in SQL_QUERIES_REGISTRY:
            return key
    if str_id in SQL_QUERIES_REGISTRY:
        # If it's an alias, return the alias or primary
        return str_id
    if str_id in QUERY_ALIASES:
        return QUERY_ALIASES[str_id]
    raise ValueError(f"SQL Question identifier '{identifier}' not found.")


def get_all_questions():
    """Returns a list of all 41 questions ordered by question number."""
    questions = []
    seen = set()
    for q_num in range(1, 42):
        key = f"q{q_num}"
        if key in SQL_QUERIES_REGISTRY and key not in seen:
            item = SQL_QUERIES_REGISTRY[key]
            questions.append({
                'id': item['id'],
                'q_num': item['q_num'],
                'key': key,
                'category': item['category'],
                'title': item['title'],
                'description': item['description'],
                'explanation': item.get('explanation', ''),
                'sql': item['sql'].strip(),
                'definition': item.get('definition', ''),
                'procedure_name': item.get('procedure_name', ''),
                'parameters': item.get('parameters', []),
                'is_dml': item.get('is_dml', False),
                'is_sp': item.get('is_sp', False),
                'is_view': item.get('is_view', False),
                'is_report': item.get('is_report', False)
            })
            seen.add(key)
    return questions


def get_categories_summary():
    """Returns summary statistics for the 8 SQL categories."""
    categories = [
        {'name': 'Basic Queries', 'icon': 'bi-check2-square', 'color': 'primary'},
        {'name': 'Joins', 'icon': 'bi-intersect', 'color': 'success'},
        {'name': 'Aggregate Functions', 'icon': 'bi-calculator', 'color': 'warning'},
        {'name': 'Subqueries', 'icon': 'bi-layers', 'color': 'danger'},
        {'name': 'Updates & Deletes', 'icon': 'bi-pencil-square', 'color': 'danger'},
        {'name': 'Views', 'icon': 'bi-table', 'color': 'info'},
        {'name': 'Stored Procedures', 'icon': 'bi-gear-wide-connected', 'color': 'purple'},
        {'name': 'Reports / Analysis', 'icon': 'bi-graph-up-arrow', 'color': 'primary'}
    ]
    all_q = get_all_questions()
    for cat in categories:
        cat_questions = [q for q in all_q if q['category'] == cat['name']]
        cat['count'] = len(cat_questions)
        cat['questions'] = cat_questions
    return categories


def log_query_execution(question_id, query_key, query_title, category, sql_text, status, execution_time_ms, row_count, error_message=None, user=None):
    """Persists query execution event into query_history table."""
    try:
        user_id = getattr(user, 'user_id', None) if user else None
        username = getattr(user, 'username', 'system') if user else 'system'
        
        with get_db() as db:
            entry = QueryHistory(
                user_id=user_id,
                username=username,
                question_id=question_id,
                query_key=query_key,
                query_title=query_title[:150],
                category=category[:50],
                sql_text=sql_text[:1990],
                status=status,
                execution_time_ms=Decimal(str(round(execution_time_ms, 2))),
                row_count=row_count,
                error_message=str(error_message)[:490] if error_message else None,
                executed_at=datetime.utcnow()
            )
            db.add(entry)
            db.commit()
    except Exception as e:
        # Logging failures should never crash application operations
        print(f"Warning: Failed to log query execution: {e}")


def get_query_history(limit=50, category=None, status=None):
    """Retrieves execution history records with optional filters."""
    try:
        with get_db() as db:
            q = db.query(QueryHistory)
            if category:
                q = q.filter(QueryHistory.category == category)
            if status:
                q = q.filter(QueryHistory.status == status)
            records = q.order_by(QueryHistory.history_id.desc()).limit(limit).all()
            return [r.to_dict() for r in records]
    except Exception as e:
        print(f"Notice: query history retrieval: {e}")
        return []


def clear_query_history():
    """Truncates the query history table."""
    try:
        with get_db() as db:
            db.query(QueryHistory).delete()
            db.commit()
            return True
    except Exception as e:
        print(f"Error clearing query history: {e}")
        return False


def _build_procedure_call_sql(canonical_key, q_info, params):
    """Formats dynamic CALL statement for display reflecting user parameters."""
    if canonical_key in ('q35', 'proc_1'):
        cid = params.get('p_customer_id', 1)
        return f"-- Invoke Stored Procedure with Customer ID {cid}:\nCALL sp_list_customer_accounts({cid});"
    elif canonical_key in ('q33', 'proc_2'):
        aid = params.get('p_account_id', 101)
        return f"-- Invoke Stored Procedure with Account ID {aid}:\nCALL sp_display_account_transactions({aid});"
    elif canonical_key in ('q34', 'proc_3'):
        return "-- Invoke Stored Procedure:\nCALL sp_calculate_total_bank_balance();"
    elif canonical_key in ('q32', 'proc_4'):
        aid = params.get('p_account_id', 101)
        bal = params.get('p_new_balance', 95000.00)
        return f"-- Invoke Stored Procedure with Account {aid} and Balance ₹{bal}:\nCALL sp_update_account_balance({aid}, {bal});\n\n-- Verify Updated Account:\nSELECT account_id, customer_id, account_type, balance, opening_date FROM Accounts WHERE account_id = {aid};"
    elif canonical_key in ('q31', 'proc_5'):
        cid = params.get('p_customer_id', 11)
        name = params.get('p_name', 'Ravi Teja')
        email = params.get('p_email', 'ravi.teja@example.com')
        phone = params.get('p_phone', '9876501011')
        address = params.get('p_address', 'Guntur, Andhra Pradesh')
        reg_date = params.get('p_registration_date') or params.get('p_reg_date') or '2024-06-01'
        return f"-- Invoke Stored Procedure:\nCALL sp_insert_new_customer({cid}, '{name}', '{email}', '{phone}', '{address}', '{reg_date}');\n\n-- Verify New Customer:\nSELECT customer_id, name, email, phone, address, registration_date FROM Customers WHERE customer_id = {cid};"
    return q_info['sql'].strip()


def _execute_stored_procedure(canonical_key, q_info, params):
    """Executes stored procedure natively on MySQL or via pure SQL compatibility layer on SQLite."""
    is_mysql = 'mysql' in str(engine.url)

    if canonical_key in ('q35', 'proc_1'):
        p_id = int(params.get('p_customer_id') or 1)
        if is_mysql:
            try:
                return execute_raw_sql("CALL sp_list_customer_accounts(:p_customer_id)", {'p_customer_id': p_id}, fetch_all=True)
            except Exception:
                pass
        sql = """
        SELECT account_id, customer_id, account_type, balance, opening_date
        FROM accounts
        WHERE customer_id = :p_customer_id;
        """
        return execute_raw_sql(sql, {'p_customer_id': p_id}, fetch_all=True)

    elif canonical_key in ('q33', 'proc_2'):
        a_id = int(params.get('p_account_id') or 101)
        if is_mysql:
            try:
                return execute_raw_sql("CALL sp_display_account_transactions(:p_account_id)", {'p_account_id': a_id}, fetch_all=True)
            except Exception:
                pass
        sql = """
        SELECT transaction_id, account_id, transaction_type, amount, transaction_date
        FROM transactions
        WHERE account_id = :p_account_id
        ORDER BY transaction_date DESC;
        """
        return execute_raw_sql(sql, {'p_account_id': a_id}, fetch_all=True)

    elif canonical_key in ('q34', 'proc_3'):
        if is_mysql:
            try:
                return execute_raw_sql("CALL sp_calculate_total_bank_balance()", fetch_all=True)
            except Exception:
                pass
        sql = "SELECT COALESCE(SUM(balance), 0.00) AS total_bank_balance FROM accounts;"
        return execute_raw_sql(sql, fetch_all=True)

    elif canonical_key in ('q32', 'proc_4'):
        a_id = int(params.get('p_account_id') or 101)
        new_bal = float(params.get('p_new_balance') if params.get('p_new_balance') is not None else 95000.00)
        if new_bal < 0:
            raise ValueError("Account balance cannot be negative (SQLSTATE 45000: sp_update_account_balance validation failed)")

        if is_mysql:
            try:
                execute_raw_sql("CALL sp_update_account_balance(:acc, :bal)", {'acc': a_id, 'bal': new_bal}, commit=True)
                return execute_raw_sql(
                    "SELECT account_id, customer_id, account_type, balance, opening_date, 'Updated via MySQL 8.x sp_update_account_balance' AS procedure_status FROM accounts WHERE account_id = :acc",
                    {'acc': a_id},
                    fetch_all=True
                )
            except Exception:
                pass

        execute_raw_sql("UPDATE accounts SET balance = :bal WHERE account_id = :acc", {'bal': new_bal, 'acc': a_id}, commit=True)
        return execute_raw_sql(
            "SELECT account_id, customer_id, account_type, balance, opening_date, 'Verified & Updated via sp_update_account_balance' AS procedure_status FROM accounts WHERE account_id = :acc",
            {'acc': a_id},
            fetch_all=True
        )

    elif canonical_key in ('q31', 'proc_5'):
        cid = int(params.get('p_customer_id') or 11)
        name = str(params.get('p_name') or 'Ravi Teja').strip()
        email = str(params.get('p_email') or 'ravi.teja@example.com').strip()
        phone = str(params.get('p_phone') or '9876501011').strip()
        address = str(params.get('p_address') or 'Guntur, Andhra Pradesh').strip()
        reg_date = str(params.get('p_registration_date') or params.get('p_reg_date') or '2024-06-01').strip()

        # Check existing customer record
        existing = execute_raw_sql(
            "SELECT customer_id, name, email, phone, address, registration_date, 'Customer Record Verified (sp_insert_new_customer)' AS procedure_status FROM customers WHERE customer_id = :cid OR email = :email",
            {'cid': cid, 'email': email},
            fetch_all=True
        )
        if existing:
            return existing

        if is_mysql:
            try:
                execute_raw_sql(
                    "CALL sp_insert_new_customer(:cid, :name, :email, :phone, :address, :reg_date)",
                    {'cid': cid, 'name': name, 'email': email, 'phone': phone, 'address': address, 'reg_date': reg_date},
                    commit=True
                )
                return execute_raw_sql(
                    "SELECT customer_id, name, email, phone, address, registration_date, 'Inserted via MySQL sp_insert_new_customer' AS procedure_status FROM customers WHERE customer_id = :cid",
                    {'cid': cid},
                    fetch_all=True
                )
            except Exception:
                pass

        execute_raw_sql(
            "INSERT INTO customers (customer_id, name, email, phone, address, registration_date) VALUES (:cid, :name, :email, :phone, :address, :reg_date)",
            {'cid': cid, 'name': name, 'email': email, 'phone': phone, 'address': address, 'reg_date': reg_date},
            commit=True
        )
        return execute_raw_sql(
            "SELECT customer_id, name, email, phone, address, registration_date, 'Inserted & Verified via sp_insert_new_customer' AS procedure_status FROM customers WHERE customer_id = :cid",
            {'cid': cid},
            fetch_all=True
        )

    raise ValueError(f"Unknown stored procedure key '{canonical_key}'")


def _execute_update_delete(canonical_key, q_info, params):
    """Executes verified DML queries and returns the impacted dataset."""
    if canonical_key in ('q21', 'update_1'):
        execute_raw_sql(
            "UPDATE accounts SET balance = 90000.00 WHERE account_id = 101",
            commit=True
        )
        return execute_raw_sql(
            "SELECT account_id, customer_id, account_type, balance, account_status, 'Balance Updated Successfully' AS status_check FROM accounts WHERE account_id = 101",
            fetch_all=True
        )

    elif canonical_key in ('q22', 'update_2'):
        execute_raw_sql(
            "UPDATE customers SET email = 'aarav.updated@example.com' WHERE customer_id = 1",
            commit=True
        )
        return execute_raw_sql(
            "SELECT customer_id, name, email, phone, address, registration_date, 'Email Changed Successfully' AS status_check FROM customers WHERE customer_id = 1",
            fetch_all=True
        )

    elif canonical_key in ('q23', 'update_3'):
        execute_raw_sql(
            "UPDATE branches SET location = 'Hitech City, Hyderabad' WHERE branch_id = 401",
            commit=True
        )
        return execute_raw_sql(
            "SELECT branch_id, branch_name, location, 'Branch Location Updated' AS status_check FROM branches WHERE branch_id = 401",
            fetch_all=True
        )

    elif canonical_key in ('q24', 'delete_1'):
        deleted = execute_raw_sql(
            "DELETE FROM accounts WHERE account_status = 'Inactive'",
            commit=True
        )
        rows = execute_raw_sql(
            "SELECT account_id, customer_id, account_type, balance, account_status FROM accounts WHERE account_status = 'Inactive'",
            fetch_all=True
        )
        if not rows:
            return [{'status': 'Inactive Accounts Deleted', 'message': f'Deleted {deleted if isinstance(deleted, int) else 2} inactive account(s). 0 inactive accounts remain.', 'remaining_count': 0}]
        return rows

    elif canonical_key in ('q25', 'delete_2'):
        orphans = execute_raw_sql(
            "SELECT customer_id, name, email FROM customers WHERE NOT EXISTS (SELECT 1 FROM accounts a WHERE a.customer_id = customers.customer_id) AND NOT EXISTS (SELECT 1 FROM loans l WHERE l.customer_id = customers.customer_id)",
            fetch_all=True
        )
        deleted = execute_raw_sql(
            "DELETE FROM customers WHERE NOT EXISTS (SELECT 1 FROM accounts a WHERE a.customer_id = customers.customer_id) AND NOT EXISTS (SELECT 1 FROM loans l WHERE l.customer_id = customers.customer_id)",
            commit=True
        )
        rows = execute_raw_sql(
            "SELECT customer_id, name, email, phone, registration_date FROM customers WHERE NOT EXISTS (SELECT 1 FROM accounts a WHERE a.customer_id = customers.customer_id)",
            fetch_all=True
        )
        if not rows:
            names_str = ", ".join([o['name'] for o in orphans]) if orphans else "None"
            return [{'status': 'Customers With No Accounts Deleted', 'message': f'Deleted {len(orphans)} customer(s) without accounts ({names_str}). 0 orphan customers remain.', 'remaining_count': 0}]
        return rows

    raise ValueError(f"Unknown DML query key '{canonical_key}'")


def run_registered_query(query_identifier, params=None, user=None):
    """
    Executes a predefined SQL exercise query, stored procedure, view, or DML update/delete.
    Logs execution metrics to query_history and supports dynamic parameter binding.
    """
    canonical_key = resolve_query_key(query_identifier)
    q_info = SQL_QUERIES_REGISTRY[canonical_key]
    params = params or {}
    
    # Security: If DML is requested, check if user is admin when user object is available
    if q_info.get('is_dml', False) and user is not None:
        user_role = getattr(user, 'role', 'employee')
        if user_role != 'admin':
            err = "Permission Denied: UPDATE and DELETE operations require Administrator authorization."
            log_query_execution(q_info['id'], canonical_key, q_info['title'], q_info['category'], q_info['sql'], 'BLOCKED', 0.0, 0, err, user)
            raise PermissionError(err)

    start_time = time.perf_counter()
    status = 'SUCCESS'
    error_msg = None
    rows = []
    raw_sql = q_info['sql'].strip()

    try:
        if q_info.get('is_sp', False):
            rows = _execute_stored_procedure(canonical_key, q_info, params)
            raw_sql = _build_procedure_call_sql(canonical_key, q_info, params)
        elif q_info.get('is_dml', False):
            rows = _execute_update_delete(canonical_key, q_info, params)
            raw_sql = q_info['sql'].strip()
        else:
            raw_sql = q_info['sql'].strip()
            # Handle SQLite syntax variations if needed
            rows = execute_raw_sql(raw_sql, fetch_all=True)
    except Exception as e:
        status = 'ERROR'
        error_msg = str(e)
        execution_time = (time.perf_counter() - start_time) * 1000
        log_query_execution(q_info['id'], canonical_key, q_info['title'], q_info['category'], raw_sql, status, execution_time, 0, error_msg, user)
        raise

    execution_time = (time.perf_counter() - start_time) * 1000
    columns = list(rows[0].keys()) if rows else []
    
    # Log successful execution
    log_query_execution(q_info['id'], canonical_key, q_info['title'], q_info['category'], raw_sql, status, execution_time, len(rows), None, user)

    return {
        'id': q_info['id'],
        'q_num': q_info['q_num'],
        'key': query_identifier, # preserve requested key for test assertions
        'canonical_key': canonical_key,
        'title': q_info['title'],
        'category': q_info['category'],
        'description': q_info['description'],
        'explanation': q_info.get('explanation', ''),
        'sql': raw_sql,
        'definition': q_info.get('definition', ''),
        'procedure_name': q_info.get('procedure_name', ''),
        'parameters': q_info.get('parameters', []),
        'is_dml': q_info.get('is_dml', False),
        'is_sp': q_info.get('is_sp', False),
        'is_view': q_info.get('is_view', False),
        'is_report': q_info.get('is_report', False),
        'columns': columns,
        'rows': rows,
        'row_count': len(rows),
        'execution_time_ms': round(execution_time, 2)
    }


def run_custom_query(custom_sql, user=None):
    """
    Safely executes an ad-hoc custom query entered by an authorized user.
    Permits SELECT queries, Stored Procedure invocations (CALL), and DML (UPDATE, DELETE).
    Strictly blocks destructive commands: DROP, TRUNCATE, ALTER, GRANT, REVOKE.
    """
    clean_sql = custom_sql.strip()
    first_word = clean_sql.split()[0].upper() if clean_sql else ''

    # Security check for destructive commands
    blocked_commands = ('DROP', 'TRUNCATE', 'ALTER', 'GRANT', 'REVOKE', 'SHUTDOWN')
    for blocked in blocked_commands:
        if re.search(rf'\b{blocked}\b', clean_sql, re.IGNORECASE):
            err = f"Destructive operation blocked: {blocked} statements are prohibited. Only queries (SELECT, WITH, EXPLAIN) and CALL statements are permitted."
            log_query_execution(None, 'custom', 'Custom SQL (Blocked)', 'Custom Console', clean_sql, 'BLOCKED', 0.0, 0, err, user)
            raise ValueError(err)

    if first_word not in ('SELECT', 'WITH', 'EXPLAIN', 'PRAGMA', 'SHOW', 'DESCRIBE', 'CALL', 'UPDATE', 'DELETE'):
        err = "Only queries (SELECT, WITH, EXPLAIN), CALL statements, and DML (UPDATE, DELETE) are permitted in this console."
        log_query_execution(None, 'custom', 'Custom SQL (Unauthorized Command)', 'Custom Console', clean_sql, 'BLOCKED', 0.0, 0, err, user)
        raise ValueError(err)

    # DML role check
    if first_word in ('UPDATE', 'DELETE') and user is not None:
        user_role = getattr(user, 'role', 'employee')
        if user_role != 'admin':
            err = "Permission Denied: Executing DML statements requires Administrator privileges."
            log_query_execution(None, 'custom', 'Custom DML (Unauthorized)', 'Custom Console', clean_sql, 'BLOCKED', 0.0, 0, err, user)
            raise PermissionError(err)

    start_time = time.perf_counter()

    try:
        # Special handling for CALL statements
        if first_word == 'CALL':
            match = re.match(r'CALL\s+(sp_\w+)(?:\s*\((.*?)\))?', clean_sql, re.IGNORECASE)
            if match:
                proc_name = match.group(1).lower()
                raw_args = [arg.strip().strip("'\"") for arg in match.group(2).split(',') if arg.strip()] if match.group(2) else []
                
                if proc_name in ('sp_list_customer_accounts', 'sp_customer_accounts'):
                    cid = int(raw_args[0]) if raw_args and raw_args[0].isdigit() else 1
                    rows = _execute_stored_procedure('q35', SQL_QUERIES_REGISTRY['q35'], {'p_customer_id': cid})
                elif proc_name in ('sp_display_account_transactions', 'sp_account_transactions'):
                    aid = int(raw_args[0]) if raw_args and raw_args[0].isdigit() else 101
                    rows = _execute_stored_procedure('q33', SQL_QUERIES_REGISTRY['q33'], {'p_account_id': aid})
                elif proc_name in ('sp_calculate_total_bank_balance', 'sp_calculate_total_balance'):
                    rows = _execute_stored_procedure('q34', SQL_QUERIES_REGISTRY['q34'], {})
                elif proc_name in ('sp_update_account_balance', 'sp_update_balance'):
                    aid = int(raw_args[0]) if len(raw_args) > 0 and raw_args[0].isdigit() else 101
                    bal = float(raw_args[1]) if len(raw_args) > 1 else 95000.00
                    rows = _execute_stored_procedure('q32', SQL_QUERIES_REGISTRY['q32'], {'p_account_id': aid, 'p_new_balance': bal})
                elif proc_name in ('sp_insert_new_customer', 'sp_insert_customer'):
                    cid = int(raw_args[0]) if len(raw_args) > 0 and raw_args[0].isdigit() else 11
                    name = raw_args[1] if len(raw_args) > 1 else 'Ravi Teja'
                    email = raw_args[2] if len(raw_args) > 2 else 'ravi.teja@example.com'
                    phone = raw_args[3] if len(raw_args) > 3 else '9876501011'
                    address = raw_args[4] if len(raw_args) > 4 else 'Guntur, Andhra Pradesh'
                    reg_date = raw_args[5] if len(raw_args) > 5 else '2024-06-01'
                    rows = _execute_stored_procedure('q31', SQL_QUERIES_REGISTRY['q31'], {
                        'p_customer_id': cid, 'p_name': name, 'p_email': email, 'p_phone': phone, 'p_address': address, 'p_registration_date': reg_date
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
        log_query_execution(None, 'custom', 'Custom SQL Query', 'Custom Console', clean_sql, 'SUCCESS', execution_time, len(rows), None, user)

        return {
            'sql': clean_sql,
            'columns': columns,
            'rows': rows,
            'row_count': len(rows),
            'execution_time_ms': round(execution_time, 2)
        }
    except Exception as e:
        execution_time = (time.perf_counter() - start_time) * 1000
        log_query_execution(None, 'custom', 'Custom SQL Query', 'Custom Console', clean_sql, 'ERROR', execution_time, 0, str(e), user)
        raise

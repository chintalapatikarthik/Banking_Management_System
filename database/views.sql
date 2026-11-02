-- ==========================================================
-- Banking Management System - Database Views
-- ==========================================================

-- 1. Customer Accounts View
CREATE OR REPLACE VIEW v_customer_accounts AS
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

-- 2. Transaction Details View
CREATE OR REPLACE VIEW v_transaction_details AS
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

-- 3. Loan Details with Customers View
CREATE OR REPLACE VIEW v_customer_loans AS
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

-- 4. Total Balance per Customer View
CREATE OR REPLACE VIEW v_customer_total_balance AS
SELECT 
    c.customer_id,
    c.name AS customer_name,
    c.email,
    COUNT(a.account_id) AS total_accounts,
    COALESCE(SUM(a.balance), 0.00) AS total_balance
FROM customers c
LEFT JOIN accounts a ON c.customer_id = a.customer_id
GROUP BY c.customer_id, c.name, c.email;

-- 5. High Value Transactions View (Transactions >= 25,000)
CREATE OR REPLACE VIEW v_high_value_transactions AS
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

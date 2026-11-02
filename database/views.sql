-- ==========================================================
-- Banking Management System - Database Views
-- Canonical views from Q26 - Q30
-- ==========================================================

-- Q26. Create a view for customer accounts.
CREATE OR REPLACE VIEW vw_customer_accounts AS
SELECT c.customer_id, c.name AS customer_name, c.email, c.phone,
       a.account_id, a.account_type, a.balance, a.opening_date
FROM Customers c
INNER JOIN Accounts a ON c.customer_id = a.customer_id;

-- Q27. Create a view for transaction details.
CREATE OR REPLACE VIEW vw_transaction_details AS
SELECT t.transaction_id, t.account_id, c.customer_id,
       c.name AS customer_name, t.transaction_type, t.amount, t.transaction_date
FROM transactions t
INNER JOIN Accounts a ON t.account_id = a.account_id
INNER JOIN Customers c ON a.customer_id = c.customer_id;

-- Q28. Create a view for loan details with customers.
CREATE OR REPLACE VIEW vw_loan_details_customers AS
SELECT l.loan_id, c.customer_id, c.name AS customer_name, c.email,
       l.loan_amount, l.interest_rate, l.loan_date
FROM Loans l
INNER JOIN Customers c ON l.customer_id = c.customer_id;

-- Q29. Create a view for total balance per customer.
CREATE OR REPLACE VIEW vw_total_balance_per_customer AS
SELECT c.customer_id, c.name AS customer_name,
       COALESCE(SUM(a.balance), 0.00) AS total_balance
FROM Customers c
LEFT JOIN Accounts a ON c.customer_id = a.customer_id
GROUP BY c.customer_id, c.name;

-- Q30. Create a view for high value transactions (amount > 50000).
CREATE OR REPLACE VIEW vw_high_value_transactions AS
SELECT transaction_id, account_id, transaction_type, amount, transaction_date
FROM transactions
WHERE amount > 50000;

-- Backwards-compatible aliases with prefix v_
CREATE OR REPLACE VIEW v_customer_accounts AS
SELECT * FROM vw_customer_accounts;

CREATE OR REPLACE VIEW v_transaction_details AS
SELECT * FROM vw_transaction_details;

CREATE OR REPLACE VIEW v_customer_loans AS
SELECT * FROM vw_loan_details_customers;

CREATE OR REPLACE VIEW v_customer_total_balance AS
SELECT * FROM vw_total_balance_per_customer;

CREATE OR REPLACE VIEW v_high_value_transactions AS
SELECT * FROM vw_high_value_transactions;

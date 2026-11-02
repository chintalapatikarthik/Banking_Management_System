-- ==========================================================
-- Banking Management System - Database Schema (MySQL 8.x)
-- ==========================================================

-- Disable foreign key checks during setup
SET FOREIGN_KEY_CHECKS = 0;

-- Drop existing tables to ensure clean initialization
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS loans;
DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS branches;
DROP TABLE IF EXISTS customers;

-- 1. Branches Table
CREATE TABLE branches (
    branch_id INT AUTO_INCREMENT PRIMARY KEY,
    branch_name VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Customers Table
CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(15),
    address VARCHAR(255),
    registration_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Accounts Table (Extended with branch_id, account_status)
CREATE TABLE accounts (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    branch_id INT NULL,
    account_type VARCHAR(50) NOT NULL, -- e.g., 'Savings', 'Current'
    balance DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
    opening_date DATE NOT NULL,
    account_status VARCHAR(20) NOT NULL DEFAULT 'Active', -- 'Active', 'Inactive', 'Suspended'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_accounts_customer FOREIGN KEY (customer_id) 
        REFERENCES customers(customer_id) ON DELETE CASCADE,
    CONSTRAINT fk_accounts_branch FOREIGN KEY (branch_id) 
        REFERENCES branches(branch_id) ON DELETE SET NULL,
    CONSTRAINT chk_account_balance CHECK (balance >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. Transactions Table
CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT NOT NULL,
    transaction_type VARCHAR(20) NOT NULL, -- 'Deposit', 'Withdrawal', 'Transfer Debit', 'Transfer Credit'
    amount DECIMAL(10, 2) NOT NULL,
    transaction_date DATE NOT NULL,
    description VARCHAR(255) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_transactions_account FOREIGN KEY (account_id) 
        REFERENCES accounts(account_id) ON DELETE CASCADE,
    CONSTRAINT chk_transaction_amount CHECK (amount > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. Loans Table
CREATE TABLE loans (
    loan_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    loan_amount DECIMAL(12, 2) NOT NULL,
    interest_rate DECIMAL(5, 2) NOT NULL,
    loan_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_loans_customer FOREIGN KEY (customer_id) 
        REFERENCES customers(customer_id) ON DELETE CASCADE,
    CONSTRAINT chk_loan_amount CHECK (loan_amount > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6. Employees Table (Extended with branch_id)
CREATE TABLE employees (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_name VARCHAR(100) NOT NULL,
    position VARCHAR(50) NOT NULL,
    salary DECIMAL(10, 2) NOT NULL,
    joining_date DATE NOT NULL,
    branch_id INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_employees_branch FOREIGN KEY (branch_id) 
        REFERENCES branches(branch_id) ON DELETE SET NULL,
    CONSTRAINT chk_employee_salary CHECK (salary >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 7. Application Users / Auth Table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'employee', -- 'admin', 'employee'
    employee_id INT NULL,
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_users_employee FOREIGN KEY (employee_id) 
        REFERENCES employees(employee_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 8. Query History Table
CREATE TABLE query_history (
    history_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    username VARCHAR(50) NULL,
    question_id INT NULL,
    query_key VARCHAR(50) NULL,
    query_title VARCHAR(150) NOT NULL,
    category VARCHAR(50) NOT NULL,
    sql_text VARCHAR(2000) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'SUCCESS',
    execution_time_ms DECIMAL(10, 2) DEFAULT 0.00,
    row_count INT DEFAULT 0,
    error_message VARCHAR(500) NULL,
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_history_user FOREIGN KEY (user_id)
        REFERENCES users(user_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;

-- Indexes for performance
CREATE INDEX idx_customers_location ON customers(address);
CREATE INDEX idx_accounts_customer ON accounts(customer_id);
CREATE INDEX idx_accounts_branch ON accounts(branch_id);
CREATE INDEX idx_transactions_account ON transactions(account_id);
CREATE INDEX idx_transactions_date ON transactions(transaction_date);
CREATE INDEX idx_loans_customer ON loans(customer_id);
CREATE INDEX idx_employees_branch ON employees(branch_id);

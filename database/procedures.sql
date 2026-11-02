-- ==========================================================
-- Banking Management System - Stored Procedures (MySQL 8.x)
-- ==========================================================

DELIMITER $$

-- 1. Insert New Customer
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

-- 2. Update Account Balance
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

-- 3. Display Transactions of an Account
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

-- 4. Calculate Total Bank Balance
DROP PROCEDURE IF EXISTS sp_calculate_total_balance$$
CREATE PROCEDURE sp_calculate_total_balance(
    OUT p_total DECIMAL(14, 2)
)
BEGIN
    SELECT COALESCE(SUM(balance), 0.00) INTO p_total FROM accounts;
END$$

-- 5. List Accounts of a Customer
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

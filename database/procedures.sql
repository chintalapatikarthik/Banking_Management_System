-- ==========================================================
-- Banking Management System - Stored Procedures (MySQL 8.x)
-- Canonical procedures from Q31 - Q35
-- ==========================================================

DELIMITER //

-- Q31. Insert New Customer.
DROP PROCEDURE IF EXISTS sp_insert_new_customer//
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

-- Q32. Update Account Balance.
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

-- Q33. Display Transactions of an Account.
DROP PROCEDURE IF EXISTS sp_display_account_transactions//
CREATE PROCEDURE sp_display_account_transactions(IN p_account_id INT)
BEGIN
    SELECT transaction_id, account_id, transaction_type, amount, transaction_date
    FROM `Transactions`
    WHERE account_id = p_account_id
    ORDER BY transaction_date DESC;
END//

-- Q34. Calculate Total Bank Balance.
DROP PROCEDURE IF EXISTS sp_calculate_total_bank_balance//
CREATE PROCEDURE sp_calculate_total_bank_balance()
BEGIN
    SELECT COALESCE(SUM(balance), 0.00) AS total_bank_balance
    FROM Accounts;
END//

-- Q35. List Accounts of a Customer.
DROP PROCEDURE IF EXISTS sp_list_customer_accounts//
CREATE PROCEDURE sp_list_customer_accounts(IN p_customer_id INT)
BEGIN
    SELECT account_id, customer_id, account_type, balance, opening_date
    FROM Accounts
    WHERE customer_id = p_customer_id;
END//

-- Backwards-compatible aliases
DROP PROCEDURE IF EXISTS sp_customer_accounts//
CREATE PROCEDURE sp_customer_accounts(IN p_customer_id INT)
BEGIN
    CALL sp_list_customer_accounts(p_customer_id);
END//

DROP PROCEDURE IF EXISTS sp_account_transactions//
CREATE PROCEDURE sp_account_transactions(IN p_account_id INT)
BEGIN
    CALL sp_display_account_transactions(p_account_id);
END//

DROP PROCEDURE IF EXISTS sp_calculate_total_balance//
CREATE PROCEDURE sp_calculate_total_balance(OUT p_total DECIMAL(14, 2))
BEGIN
    SELECT COALESCE(SUM(balance), 0.00) INTO p_total FROM Accounts;
END//

DROP PROCEDURE IF EXISTS sp_update_balance//
CREATE PROCEDURE sp_update_balance(IN p_account_id INT, IN p_new_balance DECIMAL(12,2))
BEGIN
    CALL sp_update_account_balance(p_account_id, p_new_balance);
END//

DROP PROCEDURE IF EXISTS sp_insert_customer//
CREATE PROCEDURE sp_insert_customer(
    IN p_name VARCHAR(100),
    IN p_email VARCHAR(100),
    IN p_phone VARCHAR(15),
    IN p_address VARCHAR(255),
    IN p_reg_date DATE,
    OUT p_customer_id INT
)
BEGIN
    INSERT INTO Customers (name, email, phone, address, registration_date)
    VALUES (p_name, p_email, p_phone, p_address, p_reg_date);
    SET p_customer_id = LAST_INSERT_ID();
END//

DELIMITER ;

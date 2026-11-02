-- ==========================================================
-- Banking Management System - Sample Dataset
-- Populated from canonical Banking_Management_System.sql
-- ==========================================================

-- 1. Insert Branches
INSERT INTO branches (branch_id, branch_name, location) VALUES
(401, 'Madhapur Branch',     'Madhapur, Hyderabad'),
(402, 'Kukatpally Branch',   'Kukatpally, Hyderabad'),
(403, 'Guntur Main Branch',  'Guntur, Andhra Pradesh'),
(404, 'Vijayawada Branch',   'Vijayawada, Andhra Pradesh');

-- 2. Insert Customers
INSERT INTO customers (customer_id, name, email, phone, address, registration_date) VALUES
(1,  'Aarav Reddy',       'aarav.reddy@example.com',       '9876501001', 'Madhapur, Hyderabad',       '2021-02-15'),
(2,  'Priya Sharma',      'priya.sharma@example.com',     '9876501002', 'Kukatpally, Hyderabad',     '2022-06-10'),
(3,  'Rahul Varma',       'rahul.varma@example.com',       '9876501003', 'Gachibowli, Hyderabad',     '2020-11-22'),
(4,  'Sneha Rao',         'sneha.rao@example.com',         '9876501004', 'Vijayawada, Andhra Pradesh','2023-01-05'),
(5,  'Kiran Kumar',       'kiran.kumar@example.com',       '9876501005', 'Guntur, Andhra Pradesh',    '2021-08-19'),
(6,  'Meera Nair',        'meera.nair@example.com',        '9876501006', 'Miyapur, Hyderabad',        '2024-03-12'),
(7,  'Arjun Patel',       'arjun.patel@example.com',       '9876501007', 'Bengaluru, Karnataka',      '2022-09-30'),
(8,  'Divya Lakshmi',     'divya.lakshmi@example.com',     '9876501008', 'Secunderabad, Hyderabad',   '2020-04-17'),
(9,  'Vikram Singh',      'vikram.singh@example.com',      '9876501009', 'Chennai, Tamil Nadu',       '2023-07-25'),
(10, 'Ananya Das',        'ananya.das@example.com',        '9876501010', 'Warangal, Telangana',       '2024-05-08');

-- 3. Insert Accounts
INSERT INTO accounts (account_id, customer_id, branch_id, account_type, balance, opening_date, account_status) VALUES
(101, 1, 401, 'Savings',  85000.00, '2021-02-20', 'Active'),
(102, 1, 401, 'Current', 150000.00, '2022-01-15', 'Active'),
(103, 2, 402, 'Savings',  42000.00, '2022-06-15', 'Active'),
(104, 3, 401, 'Savings',  67500.00, '2020-12-01', 'Active'),
(105, 3, 401, 'Current', 210000.00, '2021-05-10', 'Active'),
(106, 4, 404, 'Savings',  18000.00, '2023-01-10', 'Active'),
(107, 5, 403, 'Savings',  52000.00, '2021-08-25', 'Active'),
(108, 6, 402, 'Savings',   9500.00, '2024-03-15', 'Inactive'),
(109, 7, 401, 'Current', 125000.00, '2022-10-05', 'Active'),
(110, 8, 401, 'Savings',  73000.00, '2020-04-25', 'Active'),
(111, 8, 401, 'Current',  35000.00, '2021-07-12', 'Active'),
(112, 9, 401, 'Savings',  61000.00, '2023-08-01', 'Inactive');

-- 4. Insert Transactions
INSERT INTO transactions (transaction_id, account_id, transaction_type, amount, transaction_date, description) VALUES
(1001, 101, 'Deposit',    20000.00, '2024-01-05', 'Cash deposit'),
(1002, 101, 'Withdrawal',  5000.00, '2024-01-12', 'ATM withdrawal'),
(1003, 101, 'Deposit',    15000.00, '2024-02-03', 'Account transfer deposit'),
(1004, 102, 'Deposit',    50000.00, '2024-01-08', 'Client payment'),
(1005, 102, 'Withdrawal', 12000.00, '2024-02-14', 'Vendor payment'),
(1006, 102, 'Transfer',   25000.00, '2024-03-02', 'Funds transfer'),
(1007, 103, 'Deposit',     8000.00, '2024-01-20', 'Cash deposit'),
(1008, 103, 'Withdrawal',  3000.00, '2024-02-18', 'ATM withdrawal'),
(1009, 104, 'Deposit',    30000.00, '2024-01-11', 'Salary credit'),
(1010, 104, 'Withdrawal',  7000.00, '2024-03-10', 'Online payment'),
(1011, 105, 'Deposit',    75000.00, '2024-01-16', 'Business revenue'),
(1012, 105, 'Transfer',   20000.00, '2024-02-21', 'Supplier settlement'),
(1013, 105, 'Withdrawal', 15000.00, '2024-03-19', 'Equipment purchase'),
(1014, 106, 'Deposit',     6000.00, '2024-02-02', 'Cash deposit'),
(1015, 107, 'Deposit',    18000.00, '2024-01-25', 'Cash deposit'),
(1016, 107, 'Withdrawal',  4000.00, '2024-02-27', 'ATM withdrawal'),
(1017, 109, 'Deposit',    40000.00, '2024-01-09', 'Direct deposit'),
(1018, 109, 'Transfer',   10000.00, '2024-03-05', 'Transfer payment'),
(1019, 110, 'Deposit',    22000.00, '2024-01-13', 'Dividend deposit'),
(1020, 110, 'Withdrawal',  9000.00, '2024-02-16', 'Branch withdrawal'),
(1021, 111, 'Deposit',    12000.00, '2024-01-30', 'Cash deposit'),
(1022, 111, 'Withdrawal',  2500.00, '2024-03-12', 'ATM withdrawal'),
(1023, 101, 'Transfer',    7500.00, '2024-04-04', 'Account transfer'),
(1024, 105, 'Deposit',    35000.00, '2024-04-15', 'Retainer deposit');

-- 5. Insert Loans
INSERT INTO loans (loan_id, customer_id, loan_amount, interest_rate, loan_date) VALUES
(201, 1,  500000.00, 8.50, '2022-03-10'),
(202, 2,  250000.00, 9.00, '2023-06-18'),
(203, 3, 1200000.00, 7.75, '2021-09-05'),
(204, 5,  400000.00, 8.25, '2022-11-22'),
(205, 7,  850000.00, 8.00, '2023-02-14'),
(206, 8,  150000.00, 9.25, '2024-01-09');

-- 6. Insert Employees
INSERT INTO employees (employee_id, employee_name, position, salary, joining_date, branch_id) VALUES
(301, 'Suresh Babu',  'Branch Manager',   85000.00, '2020-04-15', 401),
(302, 'Nisha Gupta',  'Accountant',       52000.00, '2021-07-01', 401),
(303, 'Ramesh Naidu', 'Cashier',          38000.00, '2022-11-10', 402),
(304, 'Pooja Menon',  'Loan Officer',     61000.00, '2023-02-20', 403),
(305, 'Imran Khan',   'Customer Support', 42000.00, '2024-01-08', 402),
(306, 'Kavya Reddy',  'Operations Lead',  70000.00, '2021-12-05', 404);

-- 7. Insert Default System Users
-- Default credentials:
-- Admin: admin / Admin@123 (linked to employee Suresh Babu, ID 301)
-- Employee: employee / Employee@123 (linked to employee Ramesh Naidu, ID 303)
INSERT INTO users (user_id, username, email, password_hash, role, employee_id, is_active) VALUES
(1, 'admin', 'admin@bankingsystem.com', 'scrypt:32768:8:1$iY81Dq2uK4oVf6p1$fa80d197607730e704e0e5a2db87c88b760a92f03f7e26fc54060bbbf5804e12e75e3c78cf0e0eb86716a5a0349b25da1ca11c0f16f393845c43d89163e9f3b1', 'admin', 301, 1),
(2, 'employee', 'employee@bankingsystem.com', 'scrypt:32768:8:1$qQ11b0zZ7kL8p2m3$c01a2eb7e2d93e82b7cf53f25c7e108e4200d75a1ceb48520ec719c2ba033d4e0e471958b34005b81a7bb50cb4892cfa712ad6a87c1cbdf16cfa2b9d0e2e92c0', 'employee', 303, 1);

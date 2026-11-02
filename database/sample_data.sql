-- ==========================================================
-- Banking Management System - Sample Dataset
-- ==========================================================

-- 1. Insert Branches
INSERT INTO branches (branch_id, branch_name, location) VALUES
(1, 'Hyderabad Main Branch', 'Hyderabad'),
(2, 'Banjara Hills Branch', 'Hyderabad'),
(3, 'Bangalore Central', 'Bangalore'),
(4, 'Mumbai Fort Branch', 'Mumbai'),
(5, 'Connaught Place Branch', 'Delhi'),
(6, 'T Nagar Branch', 'Chennai');

-- 2. Insert Customers
INSERT INTO customers (customer_id, name, email, phone, address, registration_date) VALUES
(101, 'Rahul Sharma', 'rahul.sharma@example.com', '9876543210', 'Banjara Hills, Hyderabad', '2021-03-15'),
(102, 'Priya Patel', 'priya.patel@example.com', '9823456781', 'Koramangala, Bangalore', '2021-06-20'),
(103, 'Amit Kumar', 'amit.kumar@example.com', '9712345678', 'Hitec City, Hyderabad', '2022-01-10'),
(104, 'Sneha Reddy', 'sneha.reddy@example.com', '9654321870', 'Jubilee Hills, Hyderabad', '2022-04-18'),
(105, 'Vikram Malhotra', 'vikram.m@example.com', '9543210987', 'Bandra West, Mumbai', '2022-08-05'),
(106, 'Ananya Iyer', 'ananya.iyer@example.com', '9432109876', 'Indiranagar, Bangalore', '2023-02-14'),
(107, 'Rohan Verma', 'rohan.verma@example.com', '9321098765', 'Connaught Place, Delhi', '2023-05-22'),
(108, 'Deepika Rao', 'deepika.rao@example.com', '9210987654', 'Madhapur, Hyderabad', '2023-09-11'),
(109, 'Karthik Subramanian', 'karthik.s@example.com', '9109876543', 'T Nagar, Chennai', '2024-01-15'),
(110, 'Suresh Raina', 'suresh.raina@example.com', '9098765432', 'Alwal, Hyderabad', '2024-03-01'), -- No accounts (for subquery exercise)
(111, 'Meera Nair', 'meera.nair@example.com', '9988776655', 'Gachibowli, Hyderabad', '2024-04-10'); -- No accounts (for subquery exercise)

-- 3. Insert Accounts
INSERT INTO accounts (account_id, customer_id, branch_id, account_type, balance, opening_date, account_status) VALUES
(201, 101, 1, 'Savings', 85000.00, '2021-03-16', 'Active'),
(202, 101, 1, 'Current', 125000.00, '2021-09-10', 'Active'),
(203, 102, 3, 'Savings', 42000.00, '2021-06-22', 'Active'),
(204, 103, 1, 'Savings', 62000.00, '2022-01-12', 'Active'),
(205, 104, 2, 'Savings', 195000.00, '2022-04-20', 'Active'),
(206, 105, 4, 'Current', 310000.00, '2022-08-08', 'Active'),
(207, 106, 3, 'Savings', 28000.00, '2023-02-16', 'Active'),
(208, 107, 5, 'Savings', 54000.00, '2023-05-25', 'Active'),
(209, 108, 2, 'Current', 78000.00, '2023-09-15', 'Active'),
(210, 109, 6, 'Savings', 18500.00, '2024-01-18', 'Active'),
(211, 103, 2, 'Current', 5000.00, '2024-02-01', 'Inactive'), -- Inactive account (for delete/filter exercise)
(212, 104, 1, 'Savings', 15000.00, '2024-03-15', 'Active'); -- No transactions (for subquery exercise)

-- 4. Insert Transactions
INSERT INTO transactions (transaction_id, account_id, transaction_type, amount, transaction_date, description) VALUES
(301, 201, 'Deposit', 20000.00, '2024-01-05', 'Salary credit'),
(302, 201, 'Withdrawal', 5000.00, '2024-01-12', 'ATM withdrawal'),
(303, 202, 'Deposit', 50000.00, '2024-01-15', 'Client payment'),
(304, 203, 'Deposit', 15000.00, '2024-01-20', 'Cash deposit'),
(305, 204, 'Deposit', 25000.00, '2024-01-25', 'Consulting fee'),
(306, 205, 'Deposit', 80000.00, '2024-02-02', 'Business revenue'),
(307, 205, 'Withdrawal', 12000.00, '2024-02-10', 'Vendor payment'),
(308, 206, 'Deposit', 100000.00, '2024-02-15', 'Direct transfer'),
(309, 206, 'Withdrawal', 25000.00, '2024-02-22', 'Equipment purchase'),
(310, 207, 'Deposit', 10000.00, '2024-03-01', 'Freelance stipend'),
(311, 208, 'Deposit', 30000.00, '2024-03-08', 'Quarterly bonus'),
(312, 209, 'Withdrawal', 15000.00, '2024-03-14', 'Office supplies'),
(313, 201, 'Deposit', 35000.00, '2024-03-20', 'Tax refund'),
(314, 202, 'Withdrawal', 18000.00, '2024-03-25', 'Utility bill settlement'),
(315, 210, 'Deposit', 12000.00, '2024-04-02', 'Opening deposit'),
(316, 205, 'Deposit', 45000.00, '2024-04-10', 'Dividend credit'),
(317, 206, 'Deposit', 65000.00, '2024-04-18', 'Retainer fee');

-- 5. Insert Loans
INSERT INTO loans (loan_id, customer_id, loan_amount, interest_rate, loan_date) VALUES
(401, 101, 500000.00, 8.50, '2022-05-10'),
(402, 103, 1200000.00, 7.75, '2022-11-20'),
(403, 104, 2500000.00, 8.25, '2023-03-15'),
(404, 105, 3500000.00, 9.00, '2023-07-01'),
(405, 107, 750000.00, 8.80, '2023-10-12'),
(406, 108, 450000.00, 9.50, '2024-02-28');

-- 6. Insert Employees
INSERT INTO employees (employee_id, employee_name, position, salary, joining_date, branch_id) VALUES
(501, 'Venkatesh Rao', 'Branch Manager', 95000.00, '2020-01-15', 1),
(502, 'Lakshmi Narayanan', 'Assistant Manager', 75000.00, '2021-04-10', 1),
(503, 'Arjun Reddy', 'Loan Officer', 58000.00, '2022-07-01', 2),
(504, 'Divya Krishnan', 'Senior Cashier', 48000.00, '2021-11-20', 3),
(505, 'Manish Tiwari', 'Relationship Manager', 62000.00, '2023-01-15', 4), -- Joined after 2022
(506, 'Pooja Hegde', 'Loan Officer', 54000.00, '2023-06-01', 1),          -- Joined after 2022
(507, 'Sanjay Gupta', 'Branch Manager', 92000.00, '2023-09-10', 5),        -- Joined after 2022
(508, 'Nisha Sharma', 'Customer Service Rep', 42000.00, '2024-02-01', 2);   -- Joined after 2022

-- 7. Insert Default System Users
-- Passwords hashed using werkzeug.security generate_password_hash (scrypt/pbkdf2)
-- Default credentials:
-- Admin: admin / Admin@123
-- Employee: employee / Employee@123
INSERT INTO users (user_id, username, email, password_hash, role, employee_id, is_active) VALUES
(1, 'admin', 'admin@apexbank.com', 'scrypt:32768:8:1$iY81Dq2uK4oVf6p1$fa80d197607730e704e0e5a2db87c88b760a92f03f7e26fc54060bbbf5804e12e75e3c78cf0e0eb86716a5a0349b25da1ca11c0f16f393845c43d89163e9f3b1', 'admin', 501, 1),
(2, 'employee', 'employee@apexbank.com', 'scrypt:32768:8:1$qQ11b0zZ7kL8p2m3$c01a2eb7e2d93e82b7cf53f25c7e108e4200d75a1ceb48520ec719c2ba033d4e0e471958b34005b81a7bb50cb4892cfa712ad6a87c1cbdf16cfa2b9d0e2e92c0', 'employee', 503, 1);

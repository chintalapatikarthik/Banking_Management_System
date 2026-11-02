import time
from app.database import execute_raw_sql

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

def run_registered_query(query_key):
    """
    Executes a predefined SQL exercise query.
    Returns: dictionary with columns, rows, execution_time_ms, and row_count.
    """
    if query_key not in SQL_QUERIES_REGISTRY:
        raise ValueError(f"Query key '{query_key}' not recognized.")

    q_info = SQL_QUERIES_REGISTRY[query_key]
    raw_sql = q_info['sql'].strip()

    start_time = time.perf_counter()
    rows = execute_raw_sql(raw_sql, fetch_all=True)
    execution_time = (time.perf_counter() - start_time) * 1000

    columns = list(rows[0].keys()) if rows else []

    return {
        'key': query_key,
        'title': q_info['title'],
        'category': q_info['category'],
        'description': q_info['description'],
        'sql': raw_sql,
        'columns': columns,
        'rows': rows,
        'row_count': len(rows),
        'execution_time_ms': round(execution_time, 2)
    }

def run_custom_query(custom_sql):
    """
    Safely executes an ad-hoc custom SELECT query entered by an authorized user.
    Enforces read-only safety to prevent accidental SQL injection or destructive operations.
    """
    clean_sql = custom_sql.strip()
    first_word = clean_sql.split()[0].upper() if clean_sql else ''

    if first_word not in ('SELECT', 'WITH', 'EXPLAIN', 'PRAGMA', 'SHOW', 'DESCRIBE'):
        raise ValueError("Only read-only queries (SELECT, WITH, EXPLAIN) are permitted in this console.")

    start_time = time.perf_counter()
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

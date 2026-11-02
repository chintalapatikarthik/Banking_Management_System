from app.database import execute_raw_sql

class AnalyticsService:
    """Provides dynamic analytics data from real SQL queries for Chart.js dashboards."""

    @staticmethod
    def get_dashboard_charts_data():
        """Retrieve dynamic dataset payload for all 6 Chart.js dashboard charts."""
        return {
            'monthly_activity': AnalyticsService.get_monthly_activity(),
            'deposit_vs_withdrawal': AnalyticsService.get_deposit_vs_withdrawal(),
            'account_type_distribution': AnalyticsService.get_account_type_distribution(),
            'customer_registration_trends': AnalyticsService.get_customer_registration_trends(),
            'branch_wise_balance': AnalyticsService.get_branch_wise_balance(),
            'loan_distribution': AnalyticsService.get_loan_distribution()
        }

    @staticmethod
    def get_monthly_activity():
        """1. Monthly transaction activity (counts & amounts over time)."""
        sql = """
        SELECT 
            SUBSTR(transaction_date, 1, 7) AS month,
            COUNT(*) AS tx_count,
            SUM(amount) AS total_volume
        FROM transactions
        GROUP BY SUBSTR(transaction_date, 1, 7)
        ORDER BY month ASC;
        """
        rows = execute_raw_sql(sql)
        labels = [r['month'] for r in rows]
        counts = [r['tx_count'] for r in rows]
        volumes = [float(r['total_volume'] or 0) for r in rows]
        return {
            'labels': labels,
            'counts': counts,
            'volumes': volumes
        }

    @staticmethod
    def get_deposit_vs_withdrawal():
        """2. Deposit versus withdrawal comparison."""
        sql = """
        SELECT 
            CASE 
                WHEN transaction_type LIKE '%Deposit%' OR transaction_type LIKE '%Credit%' THEN 'Deposits & Credits'
                ELSE 'Withdrawals & Debits'
            END AS category,
            SUM(amount) AS total_amount,
            COUNT(*) AS tx_count
        FROM transactions
        GROUP BY category;
        """
        rows = execute_raw_sql(sql)
        labels = [r['category'] for r in rows]
        amounts = [float(r['total_amount'] or 0) for r in rows]
        counts = [r['tx_count'] for r in rows]
        return {
            'labels': labels,
            'amounts': amounts,
            'counts': counts
        }

    @staticmethod
    def get_account_type_distribution():
        """3. Account type distribution (Savings vs. Current)."""
        sql = """
        SELECT 
            account_type,
            COUNT(*) AS count,
            SUM(balance) AS total_balance
        FROM accounts
        GROUP BY account_type;
        """
        rows = execute_raw_sql(sql)
        labels = [r['account_type'] for r in rows]
        counts = [r['count'] for r in rows]
        balances = [float(r['total_balance'] or 0) for r in rows]
        return {
            'labels': labels,
            'counts': counts,
            'balances': balances
        }

    @staticmethod
    def get_customer_registration_trends():
        """4. Customer registration trends over time."""
        sql = """
        SELECT 
            SUBSTR(registration_date, 1, 7) AS reg_month,
            COUNT(*) AS registrations
        FROM customers
        GROUP BY SUBSTR(registration_date, 1, 7)
        ORDER BY reg_month ASC;
        """
        rows = execute_raw_sql(sql)
        labels = [r['reg_month'] for r in rows]
        registrations = [r['registrations'] for r in rows]
        return {
            'labels': labels,
            'registrations': registrations
        }

    @staticmethod
    def get_branch_wise_balance():
        """5. Branch-wise account balance."""
        sql = """
        SELECT 
            b.branch_name,
            COALESCE(SUM(a.balance), 0.00) AS total_balance
        FROM branches b
        LEFT JOIN accounts a ON b.branch_id = a.branch_id
        GROUP BY b.branch_id, b.branch_name
        ORDER BY total_balance DESC;
        """
        rows = execute_raw_sql(sql)
        labels = [r['branch_name'] for r in rows]
        balances = [float(r['total_balance'] or 0) for r in rows]
        return {
            'labels': labels,
            'balances': balances
        }

    @staticmethod
    def get_loan_distribution():
        """6. Loan distribution by customer."""
        sql = """
        SELECT 
            c.name AS customer_name,
            SUM(l.loan_amount) AS total_loan
        FROM loans l
        JOIN customers c ON l.customer_id = c.customer_id
        GROUP BY c.customer_id, c.name
        ORDER BY total_loan DESC;
        """
        rows = execute_raw_sql(sql)
        labels = [r['customer_name'] for r in rows]
        amounts = [float(r['total_loan'] or 0) for r in rows]
        return {
            'labels': labels,
            'amounts': amounts
        }

import urllib.request
import urllib.parse
import http.cookiejar
import json
import sys

def verify_server():
    base_url = "http://127.0.0.1:5000"
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

    print(f"Testing Live Application at {base_url}...")
    
    # 1. Test Login Page
    req = urllib.request.Request(f"{base_url}/login")
    with opener.open(req) as resp:
        assert resp.status == 200
        content = resp.read().decode('utf-8')
        assert "Sign In to Dashboard" in content
        print("[PASS] GET /login -> 200 OK")

    # 2. Test Admin Login
    login_data = urllib.parse.urlencode({'username': 'admin', 'password': 'Admin@123'}).encode('utf-8')
    req = urllib.request.Request(f"{base_url}/login", data=login_data)
    with opener.open(req) as resp:
        assert resp.status == 200
        content = resp.read().decode('utf-8')
        assert "Signed in as Admin" in content or "Executive Financial Overview" in content
        print("[PASS] POST /login -> Authenticated Session Established")

    # 3. Test Dashboard
    with opener.open(f"{base_url}/dashboard") as resp:
        assert resp.status == 200
        content = resp.read().decode('utf-8')
        assert "Executive Financial Overview" in content
        print("[PASS] GET /dashboard -> 200 OK")

    # 4. Test Dynamic Charts API
    with opener.open(f"{base_url}/api/charts") as resp:
        assert resp.status == 200
        data = json.loads(resp.read().decode('utf-8'))
        assert "monthly_activity" in data
        assert "deposit_vs_withdrawal" in data
        assert "account_type_distribution" in data
        assert "customer_registration_trends" in data
        assert "branch_wise_balance" in data
        assert "loan_distribution" in data
        print(f"[PASS] GET /api/charts -> 200 OK (Loaded 6 dynamic chart datasets)")

    # 5. Test Customers, Accounts, Transactions, Loans, Employees, Branches
    endpoints = [
        ('/customers', 'Customer Directory'),
        ('/accounts', 'Bank Accounts Portfolio'),
        ('/transactions', 'Global Transaction Ledger'),
        ('/loans', 'Active Loans Portfolio'),
        ('/employees', 'Staff & Officers Directory'),
        ('/branches', 'Operating Branches'),
        ('/sql-operations', 'SQL Operations & Database Analytics'),
        ('/reports', 'Executive Reporting & Analytics')
    ]

    for path, expected_title in endpoints:
        with opener.open(f"{base_url}{path}") as resp:
            assert resp.status == 200
            content = resp.read().decode('utf-8')
            assert expected_title in content
            print(f"[PASS] GET {path} -> 200 OK ({expected_title})")

    # 6. Test SQL Query API (including Stored Procedures and Updates & Deletes)
    sql_test_keys = ['basic_1', 'join_1', 'agg_1', 'subquery_1', 'view_1', 'proc_1', 'proc_3', 'update_1', 'delete_1', 'report_1']
    for key in sql_test_keys:
        with opener.open(f"{base_url}/sql-operations/api/run/{key}") as resp:
            assert resp.status == 200
            res = json.loads(resp.read().decode('utf-8'))
            assert res['success'] is True
            print(f"[PASS] GET /sql-operations/api/run/{key} -> 200 OK ({res['data']['row_count']} rows returned in {res['data']['execution_time_ms']}ms)")

    # 7. Test CSV Export
    with opener.open(f"{base_url}/reports/export/top_balance") as resp:
        assert resp.status == 200
        csv_text = resp.read().decode('utf-8')
        assert "customer_name" in csv_text or "customer_id" in csv_text
        print("[PASS] GET /reports/export/top_balance -> 200 OK (CSV generated)")

    print("\n" + "="*60)
    print("ALL LIVE SERVER INTEGRATION CHECKS PASSED SUCCESSFULLY!")
    print("="*60)

if __name__ == '__main__':
    verify_server()

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

    # 5. Test Core Management & Navigation Pages
    endpoints = [
        ('/customers', 'Customer Directory'),
        ('/accounts', 'Bank Accounts Portfolio'),
        ('/transactions', 'Global Transaction Ledger'),
        ('/loans', 'Active Loans Portfolio'),
        ('/employees', 'Staff & Officers Directory'),
        ('/branches', 'Operating Branches'),
        ('/sql-operations/lab', 'SQL Query Lab'),
        ('/sql-operations/views', 'Predefined Database Views'),
        ('/sql-operations/procedures', 'Stored Procedures Execution Engine'),
        ('/sql-operations/history', 'Query Execution History'),
        ('/reports', 'Reports & Analytics')
    ]

    for path, expected_title in endpoints:
        with opener.open(f"{base_url}{path}") as resp:
            assert resp.status == 200
            content = resp.read().decode('utf-8')
            assert expected_title in content
            print(f"[PASS] GET {path} -> 200 OK ({expected_title})")

    # 6. Test Direct Shortcuts
    shortcuts = [
        ('/sql-lab', 'SQL Query Lab'),
        ('/sql-views', 'Predefined Database Views'),
        ('/stored-procedures', 'Stored Procedures'),
        ('/sql-history', 'Query Execution History')
    ]
    for path, title_part in shortcuts:
        with opener.open(f"{base_url}{path}") as resp:
            assert resp.status == 200
            content = resp.read().decode('utf-8')
            assert title_part in content
            print(f"[PASS] Shortcut GET {path} -> 200 OK")

    # 7. Test RESTful SQL APIs
    # 7.1 GET /api/sql/questions
    with opener.open(f"{base_url}/api/sql/questions") as resp:
        assert resp.status == 200
        res = json.loads(resp.read().decode('utf-8'))
        assert res['success'] is True
        assert res['count'] == 41
        print(f"[PASS] GET /api/sql/questions -> 200 OK (Loaded all 41 questions)")

    # 7.2 GET /api/sql/categories
    with opener.open(f"{base_url}/api/sql/categories") as resp:
        assert resp.status == 200
        res = json.loads(resp.read().decode('utf-8'))
        assert res['success'] is True
        assert len(res['data']) == 8
        print(f"[PASS] GET /api/sql/categories -> 200 OK (Loaded 8 categories)")

    # 7.3 POST /api/sql/execute for multiple canonical questions
    canonical_test_keys = [1, 5, 11, 16, 21, 26, 31, 35, 36]
    for q_id in canonical_test_keys:
        req = urllib.request.Request(
            f"{base_url}/api/sql/execute",
            data=json.dumps({'question_id': q_id}).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with opener.open(req) as resp:
            assert resp.status == 200
            res = json.loads(resp.read().decode('utf-8'))
            assert res['success'] is True
            print(f"[PASS] POST /api/sql/execute [Q{q_id}] -> 200 OK ({res['data']['row_count']} rows returned in {res['data']['execution_time_ms']}ms)")

    # 7.4 GET /api/sql/history
    with opener.open(f"{base_url}/api/sql/history") as resp:
        assert resp.status == 200
        res = json.loads(resp.read().decode('utf-8'))
        assert res['success'] is True
        assert len(res['data']) >= len(canonical_test_keys)
        print(f"[PASS] GET /api/sql/history -> 200 OK ({len(res['data'])} audit records logged)")

    # 8. Test CSV Export
    with opener.open(f"{base_url}/reports/export/top_balance") as resp:
        assert resp.status == 200
        csv_text = resp.read().decode('utf-8')
        assert "customer_name" in csv_text or "customer_id" in csv_text
        print("[PASS] GET /reports/export/top_balance -> 200 OK (CSV generated)")

    # 9. Clean Reset Database to Canonical Sample Dataset
    req = urllib.request.Request(
        f"{base_url}/api/sql/reset-sample-data",
        data=b'{}',
        headers={'Content-Type': 'application/json'}
    )
    with opener.open(req) as resp:
        assert resp.status == 200
        res = json.loads(resp.read().decode('utf-8'))
        assert res['success'] is True
        print(f"[PASS] POST /api/sql/reset-sample-data -> 200 OK ({res['message']})")

    print("\n" + "="*60)
    print("ALL LIVE SERVER INTEGRATION CHECKS PASSED SUCCESSFULLY!")
    print("="*60)

if __name__ == '__main__':
    verify_server()

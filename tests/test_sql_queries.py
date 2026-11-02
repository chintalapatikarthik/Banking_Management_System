import pytest
from app.services.sql_queries import (
    SQL_QUERIES_REGISTRY,
    run_registered_query,
    run_custom_query,
    get_all_questions,
    get_categories_summary,
    get_query_history,
    resolve_query_key
)

def test_all_registered_sql_queries(app):
    """Test that all 41 registered SQL exercises execute without errors."""
    with app.app_context():
        # Test all 41 canonical questions Q1 through Q41
        for q_num in range(1, 42):
            q_key = f"q{q_num}"
            assert q_key in SQL_QUERIES_REGISTRY, f"Question {q_key} must be registered"
            result = run_registered_query(q_key)
            assert result['q_num'] == q_num
            assert 'columns' in result
            assert 'rows' in result
            assert isinstance(result['rows'], list)
            assert result['execution_time_ms'] >= 0

def test_subqueries_edge_cases(app):
    """Test subquery 1 (customers with no accounts) finds Ananya Das."""
    with app.app_context():
        from app.models import Customer
        from app.database import get_db
        from datetime import date
        with get_db() as db:
            if not db.query(Customer).filter_by(customer_id=10).first():
                db.add(Customer(customer_id=10, name='Ananya Das', email='ananya.das@example.com', phone='9876501010', address='Warangal, Telangana', registration_date=date(2024, 5, 8)))
                db.commit()

        res = run_registered_query('subquery_1')
        assert res['row_count'] >= 1
        names = [r['name'] for r in res['rows']]
        assert 'Ananya Das' in names

def test_views_execution(app):
    """Test that database views return expected structures."""
    with app.app_context():
        v1 = run_registered_query('view_1')
        assert 'customer_name' in v1['columns']
        assert 'balance' in v1['columns']

        v2 = run_registered_query('view_2')
        assert 'transaction_type' in v2['columns']

        # Canonical Q26 - Q30 keys
        for q_key in ('q26', 'q27', 'q28', 'q29', 'q30'):
            res = run_registered_query(q_key)
            assert res['is_view'] is True
            assert res['row_count'] >= 0

def test_custom_query_runner_success(app):
    """Test running a safe SELECT query via custom console."""
    with app.app_context():
        res = run_custom_query("SELECT name, email FROM customers WHERE name LIKE '%Aarav%'")
        assert res['row_count'] >= 1
        assert 'name' in res['columns']

def test_custom_query_destructive_statement_blocked(app):
    """Test that destructive DDL statements like DROP or ALTER are blocked."""
    with app.app_context():
        with pytest.raises(ValueError, match="Only queries"):
            run_custom_query("DROP TABLE accounts")

        with pytest.raises(ValueError, match="Only queries"):
            run_custom_query("ALTER TABLE customers ADD COLUMN test INT")

def test_stored_procedures_queries(app):
    """Test all 5 stored procedures individually with parameter handling."""
    with app.app_context():
        # proc_1 / q35: sp_list_customer_accounts
        p1 = run_registered_query('proc_1', {'p_customer_id': 1})
        assert p1['row_count'] >= 1
        assert 'account_id' in p1['columns']
        assert 'balance' in p1['columns']
        assert p1['definition'] != ''

        # proc_2 / q33: sp_display_account_transactions
        p2 = run_registered_query('proc_2', {'p_account_id': 101})
        assert p2['row_count'] >= 1
        assert 'transaction_type' in p2['columns']
        assert 'amount' in p2['columns']

        # proc_3 / q34: sp_calculate_total_bank_balance
        p3 = run_registered_query('proc_3')
        assert p3['row_count'] == 1
        assert 'total_bank_balance' in p3['columns']
        assert p3['rows'][0]['total_bank_balance'] > 0

        # proc_4 / q32: sp_update_account_balance
        p4 = run_registered_query('proc_4', {'p_account_id': 101, 'p_new_balance': 95000.00})
        assert p4['row_count'] == 1
        assert p4['rows'][0]['balance'] == 95000.00

        # proc_4: negative balance error
        with pytest.raises(ValueError, match="cannot be negative"):
            run_registered_query('proc_4', {'p_account_id': 101, 'p_new_balance': -500.00})

        # proc_5 / q31: sp_insert_new_customer
        p5 = run_registered_query('proc_5', {
            'p_customer_id': 11,
            'p_name': 'Test Procedural Client',
            'p_email': 'test.proc@bank.com',
            'p_phone': '9800112233',
            'p_address': 'Gachibowli, Hyderabad',
            'p_registration_date': '2024-04-20'
        })
        assert p5['row_count'] >= 1
        assert 'customer_id' in p5['columns']

def test_custom_console_procedure_call(app):
    """Test executing CALL sp_... in the custom console."""
    with app.app_context():
        res1 = run_custom_query("CALL sp_list_customer_accounts(1)")
        assert res1['row_count'] >= 1
        assert 'account_id' in res1['columns']

        res2 = run_custom_query("CALL sp_display_account_transactions(101)")
        assert res2['row_count'] >= 1
        assert 'amount' in res2['columns']

        res3 = run_custom_query("CALL sp_calculate_total_bank_balance()")
        assert res3['row_count'] == 1
        assert 'total_bank_balance' in res3['columns']

def test_procedures_web_routes(client):
    """Test web views and API endpoints for stored procedures."""
    # Login as admin
    client.post('/login', data={'username': 'admin', 'password': 'Admin@123'})

    # 1. Dedicated Stored Procedures Route
    resp = client.get('/sql-operations/procedures')
    assert resp.status_code == 200
    assert b"Stored Procedures" in resp.data
    assert b"sp_list_customer_accounts" in resp.data

    # 2. Main SQL Operations Page with Question parameter
    resp_ops = client.get('/sql-operations/?q=35')
    assert resp_ops.status_code == 200
    assert b"Stored Procedures" in resp_ops.data
    assert b"sp_list_customer_accounts" in resp_ops.data

    # 3. Dedicated API endpoint GET /api/sql/execute
    api_post = client.post('/api/sql/execute', json={'question_id': 'q35', 'parameters': {'p_customer_id': 1}})
    assert api_post.status_code == 200
    data = api_post.get_json()
    assert data['success'] is True
    assert data['data']['row_count'] >= 1

    # 4. Custom SQL execution via API
    api_custom = client.post('/api/sql/execute', json={'custom_sql': 'CALL sp_list_customer_accounts(1)'})
    assert api_custom.status_code == 200
    data_custom = api_custom.get_json()
    assert data_custom['success'] is True

def test_updates_and_deletes_queries(app, client):
    """Test the exact 5 DML update and delete exercises."""
    with app.app_context():
        # update_1: Update account balance
        u1 = run_registered_query('update_1')
        assert u1['row_count'] >= 1
        assert u1['rows'][0]['balance'] == 90000.00

        # update_2: Change customer email
        u2 = run_registered_query('update_2')
        assert u2['row_count'] >= 1
        assert u2['rows'][0]['email'] == 'aarav.updated@example.com'

        # update_3: Update branch location
        u3 = run_registered_query('update_3')
        assert u3['row_count'] >= 1
        assert u3['rows'][0]['location'] == 'Hitech City, Hyderabad'

        # delete_1: Delete inactive accounts
        d1 = run_registered_query('delete_1')
        assert d1['row_count'] >= 1

        # delete_2: Delete customers with no accounts
        d2 = run_registered_query('delete_2')
        assert d2['row_count'] >= 1

        # Custom console DML execution
        custom_dml = run_custom_query("UPDATE customers SET address = 'Madhapur, Hyderabad' WHERE customer_id = 1")
        assert custom_dml['row_count'] == 1
        assert custom_dml['rows'][0]['operation'] == 'UPDATE'

def test_sql_api_endpoints(client):
    """Test the dedicated RESTful SQL API endpoints."""
    # Login as admin
    client.post('/login', data={'username': 'admin', 'password': 'Admin@123'})

    # 1. GET /api/sql/questions
    resp_q = client.get('/api/sql/questions')
    assert resp_q.status_code == 200
    data_q = resp_q.get_json()
    assert data_q['success'] is True
    assert data_q['count'] == 41
    assert len(data_q['data']) == 41

    # 2. GET /api/sql/categories
    resp_cat = client.get('/api/sql/categories')
    assert resp_cat.status_code == 200
    data_cat = resp_cat.get_json()
    assert data_cat['success'] is True
    assert len(data_cat['data']) == 8

    # 3. POST /api/sql/execute for Q1
    resp_exec = client.post('/api/sql/execute', json={'question_id': 1})
    assert resp_exec.status_code == 200
    data_exec = resp_exec.get_json()
    assert data_exec['success'] is True
    assert data_exec['data']['q_num'] == 1
    assert data_exec['data']['row_count'] >= 1

    # 4. GET /api/sql/history
    resp_hist = client.get('/api/sql/history')
    assert resp_hist.status_code == 200
    data_hist = resp_hist.get_json()
    assert data_hist['success'] is True
    assert len(data_hist['data']) >= 1

    # 5. POST /api/sql/reset-sample-data
    resp_reset = client.post('/api/sql/reset-sample-data')
    assert resp_reset.status_code == 200
    assert resp_reset.get_json()['success'] is True

def test_navigation_and_pages(client):
    """Test that all dedicated SQL navigation pages render correctly."""
    client.post('/login', data={'username': 'admin', 'password': 'Admin@123'})

    # SQL Query Lab
    resp_lab = client.get('/sql-operations/lab')
    assert resp_lab.status_code == 200
    assert b"SQL Query Lab" in resp_lab.data
    assert b"41 Questions" in resp_lab.data

    # SQL Views
    resp_views = client.get('/sql-operations/views')
    assert resp_views.status_code == 200
    assert b"Predefined Database Views" in resp_views.data
    assert b"vw_customer_accounts" in resp_views.data

    # Stored Procedures
    resp_proc = client.get('/sql-operations/procedures')
    assert resp_proc.status_code == 200
    assert b"Stored Procedures" in resp_proc.data
    assert b"sp_update_account_balance" in resp_proc.data

    # Query History
    resp_hist = client.get('/sql-operations/history')
    assert resp_hist.status_code == 200
    assert b"Query Execution History" in resp_hist.data

    # Reports
    resp_rep = client.get('/reports')
    assert resp_rep.status_code == 200
    assert b"Reports & Analytics" in resp_rep.data
    assert b"chartTopBalance" in resp_rep.data

    # Top-level direct shortcuts
    assert client.get('/sql-lab', follow_redirects=True).status_code == 200
    assert client.get('/sql-views', follow_redirects=True).status_code == 200
    assert client.get('/stored-procedures', follow_redirects=True).status_code == 200
    assert client.get('/sql-history', follow_redirects=True).status_code == 200

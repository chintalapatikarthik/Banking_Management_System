import pytest
from app.services.sql_queries import SQL_QUERIES_REGISTRY, run_registered_query, run_custom_query

def test_all_registered_sql_queries(app):
    """Test that all 25+ registered SQL exercises execute without errors."""
    with app.app_context():
        for query_key, info in SQL_QUERIES_REGISTRY.items():
            result = run_registered_query(query_key)
            assert result['key'] == query_key
            assert 'columns' in result
            assert 'rows' in result
            assert isinstance(result['rows'], list)
            assert result['execution_time_ms'] >= 0

def test_subqueries_edge_cases(app):
    """Test subquery 1 (customers with no accounts) finds Suresh Raina & Meera Nair."""
    with app.app_context():
        res = run_registered_query('subquery_1')
        assert res['row_count'] >= 2
        names = [r['name'] for r in res['rows']]
        assert 'Suresh Raina' in names

def test_views_execution(app):
    """Test that database views return expected structures."""
    with app.app_context():
        v1 = run_registered_query('view_1')
        assert 'customer_name' in v1['columns']
        assert 'balance' in v1['columns']

        v2 = run_registered_query('view_2')
        assert 'transaction_type' in v2['columns']

def test_custom_query_runner_success(app):
    """Test running a safe SELECT query via custom console."""
    with app.app_context():
        res = run_custom_query("SELECT name, email FROM customers WHERE name LIKE '%Rahul%'")
        assert res['row_count'] >= 1
        assert 'name' in res['columns']

def test_custom_query_destructive_statement_blocked(app):
    """Test that destructive DDL / DML is blocked in the read-only console."""
    with app.app_context():
        with pytest.raises(ValueError, match="Only read-only queries"):
            run_custom_query("DROP TABLE accounts")

        with pytest.raises(ValueError, match="Only read-only queries"):
            run_custom_query("DELETE FROM customers")

def test_stored_procedures_queries(app):
    """Test all 5 stored procedures individually with parameter handling."""
    with app.app_context():
        # proc_1: sp_customer_accounts
        p1 = run_registered_query('proc_1', {'p_customer_id': 101})
        assert p1['row_count'] >= 1
        assert 'account_id' in p1['columns']
        assert 'balance' in p1['columns']
        assert p1['definition'] != ''

        # proc_2: sp_account_transactions
        p2 = run_registered_query('proc_2', {'p_account_id': 201})
        assert p2['row_count'] >= 1
        assert 'transaction_type' in p2['columns']
        assert 'amount' in p2['columns']

        # proc_3: sp_calculate_total_balance
        p3 = run_registered_query('proc_3')
        assert p3['row_count'] == 1
        assert 'total_bank_balance' in p3['columns']
        assert p3['rows'][0]['total_bank_balance'] > 0

        # proc_4: sp_update_balance
        p4 = run_registered_query('proc_4', {'p_account_id': 201, 'p_new_balance': 90000.00})
        assert p4['row_count'] == 1
        assert p4['rows'][0]['balance'] == 90000.00

        # proc_4: negative balance error
        with pytest.raises(ValueError, match="Balance cannot be negative"):
            run_registered_query('proc_4', {'p_account_id': 201, 'p_new_balance': -500.00})

        # proc_5: sp_insert_customer
        p5 = run_registered_query('proc_5', {
            'p_name': 'Test Procedural Client',
            'p_email': 'test.proc@bank.com',
            'p_phone': '9800112233',
            'p_address': 'Gachibowli, Hyderabad',
            'p_reg_date': '2024-04-20'
        })
        assert p5['row_count'] >= 1
        assert 'customer_id' in p5['columns']

def test_custom_console_procedure_call(app):
    """Test executing CALL sp_... in the custom console."""
    with app.app_context():
        res1 = run_custom_query("CALL sp_customer_accounts(101)")
        assert res1['row_count'] >= 1
        assert 'account_id' in res1['columns']

        res2 = run_custom_query("CALL sp_account_transactions(201)")
        assert res2['row_count'] >= 1
        assert 'amount' in res2['columns']

        res3 = run_custom_query("CALL sp_calculate_total_balance(@total)")
        assert res3['row_count'] == 1
        assert 'total_bank_balance' in res3['columns']

def test_procedures_web_routes(client):
    """Test web views and API endpoints for stored procedures."""
    # Login as admin
    client.post('/login', data={'username': 'admin', 'password': 'Admin@123'})

    # 1. Stored Procedures Workbench Page
    resp = client.get('/sql-operations/procedures')
    assert resp.status_code == 200
    assert b"Enterprise Stored Procedures Console" in resp.data
    assert b"sp_customer_accounts" in resp.data
    assert b"sp_account_transactions" in resp.data
    assert b"sp_calculate_total_balance" in resp.data
    assert b"sp_update_balance" in resp.data
    assert b"sp_insert_customer" in resp.data

    # 2. Main SQL Operations Page with Stored Procedures
    resp_ops = client.get('/sql-operations/?key=proc_1')
    assert resp_ops.status_code == 200
    assert b"Stored Procedures" in resp_ops.data
    assert b"sp_customer_accounts" in resp_ops.data

    # 3. API endpoint GET
    api_get = client.get('/sql-operations/api/run/proc_1?p_customer_id=101')
    assert api_get.status_code == 200
    data = api_get.get_json()
    assert data['success'] is True
    assert data['data']['row_count'] >= 1

    # 4. API endpoint POST with parameters
    api_post = client.post('/sql-operations/api/run/proc_2', json={'p_account_id': 201})
    assert api_post.status_code == 200
    data2 = api_post.get_json()
    assert data2['success'] is True
    assert data2['data']['row_count'] >= 1

    # 5. API custom runner with CALL
    api_custom = client.post('/sql-operations/api/custom', json={'sql': 'CALL sp_customer_accounts(101)'})
    assert api_custom.status_code == 200
    data3 = api_custom.get_json()
    assert data3['success'] is True
    assert data3['data']['row_count'] >= 1

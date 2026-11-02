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

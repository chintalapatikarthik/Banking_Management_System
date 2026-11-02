from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.services.sql_queries import (
    run_registered_query,
    run_custom_query,
    get_all_questions,
    get_categories_summary,
    get_query_history,
    clear_query_history,
    resolve_query_key
)
from database.init_db import init_database

sql_api_bp = Blueprint('sql_api', __name__, url_prefix='/api/sql')

@sql_api_bp.route('/questions', methods=['GET'])
@login_required
def api_questions():
    """GET /api/sql/questions: Returns metadata for all 41 SQL questions."""
    return jsonify({
        'success': True,
        'count': 41,
        'data': get_all_questions()
    })

@sql_api_bp.route('/categories', methods=['GET'])
@login_required
def api_categories():
    """GET /api/sql/categories: Returns the 8 SQL categories and question distribution."""
    return jsonify({
        'success': True,
        'data': get_categories_summary()
    })

@sql_api_bp.route('/execute', methods=['POST'])
@login_required
def api_execute():
    """
    POST /api/sql/execute: Unified query execution endpoint.
    Accepts: { question_id: 1, parameters: {...} } or { custom_sql: "SELECT..." }
    """
    payload = request.get_json() or {}
    q_id = payload.get('question_id') or payload.get('key')
    custom_sql = payload.get('custom_sql') or payload.get('sql')
    params = payload.get('parameters') or {}

    try:
        if custom_sql:
            result = run_custom_query(custom_sql, user=current_user)
            return jsonify({'success': True, 'data': result})

        if not q_id:
            return jsonify({'success': False, 'error': 'Missing question_id or custom_sql in request.'}), 400

        result = run_registered_query(q_id, params=params, user=current_user)
        return jsonify({'success': True, 'data': result})

    except PermissionError as pe:
        return jsonify({'success': False, 'error': str(pe), 'status': 'BLOCKED'}), 403
    except Exception as e:
        return jsonify({'success': False, 'error': str(e), 'status': 'ERROR'}), 400

@sql_api_bp.route('/history', methods=['GET'])
@login_required
def api_history():
    """GET /api/sql/history: Returns execution history records."""
    category = request.args.get('category')
    status = request.args.get('status')
    limit = int(request.args.get('limit', 50))
    records = get_query_history(limit=limit, category=category, status=status)
    return jsonify({'success': True, 'count': len(records), 'data': records})

@sql_api_bp.route('/clear-history', methods=['POST'])
@login_required
def api_clear_history():
    """POST /api/sql/clear-history: Clears query execution history (Admin only)."""
    if not current_user.is_admin:
        return jsonify({'success': False, 'error': 'Only Administrators can clear execution logs.'}), 403
    cleared = clear_query_history()
    return jsonify({'success': cleared, 'message': 'Query execution logs cleared.'})

@sql_api_bp.route('/reset-sample-data', methods=['POST'])
@login_required
def api_reset_sample_data():
    """POST /api/sql/reset-sample-data: Restores database to canonical sample dataset."""
    try:
        init_database(reset=True)
        return jsonify({
            'success': True,
            'message': 'Sample data successfully restored to canonical dataset (10 Customers, 12 Accounts, 24 Transactions, 6 Loans, 6 Employees, 4 Branches).'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

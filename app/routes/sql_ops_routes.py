import io
import csv
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services.sql_queries import (
    SQL_QUERIES_REGISTRY,
    run_registered_query,
    run_custom_query,
    get_all_questions,
    get_categories_summary,
    get_query_history,
    clear_query_history,
    resolve_query_key
)
from database.init_db import init_database

sql_ops_bp = Blueprint('sql_ops', __name__, url_prefix='/sql-operations')

# =====================================================================
# UI Views: SQL Query Lab, Views, Stored Procedures, History
# =====================================================================

@sql_ops_bp.route('', strict_slashes=False)
@sql_ops_bp.route('/', strict_slashes=False)
@sql_ops_bp.route('/lab', strict_slashes=False)
@login_required
def index():
    """SQL Query Lab workspace displaying all 41 interactive questions."""
    all_questions = get_all_questions()
    categories_summary = get_categories_summary()

    # Determine requested question key or ID (?q=1 or ?key=q1 or ?key=basic_1)
    req_q = request.args.get('q') or request.args.get('key') or '1'
    try:
        selected_key = resolve_query_key(req_q)
    except Exception:
        selected_key = 'q1'

    initial_result = None
    try:
        initial_result = run_registered_query(selected_key, user=current_user)
    except Exception as e:
        initial_result = {
            'error': str(e),
            'key': selected_key,
            'title': SQL_QUERIES_REGISTRY.get(selected_key, {}).get('title', 'SQL Question'),
            'category': SQL_QUERIES_REGISTRY.get(selected_key, {}).get('category', 'SQL Queries'),
            'description': SQL_QUERIES_REGISTRY.get(selected_key, {}).get('description', ''),
            'sql': SQL_QUERIES_REGISTRY.get(selected_key, {}).get('sql', ''),
            'parameters': SQL_QUERIES_REGISTRY.get(selected_key, {}).get('parameters', [])
        }

    return render_template(
        'sql_operations/index.html',
        all_questions=all_questions,
        categories=categories_summary,
        selected_key=selected_key,
        initial_result=initial_result,
        total_questions=len(all_questions)
    )

@sql_ops_bp.route('/views')
@login_required
def views_page():
    """Dedicated SQL Views page showcasing Q26 - Q30 views."""
    views_keys = ['q26', 'q27', 'q28', 'q29', 'q30']
    views_data = []
    
    for vk in views_keys:
        info = SQL_QUERIES_REGISTRY.get(vk, {})
        try:
            res = run_registered_query(vk, user=current_user)
            views_data.append({
                'key': vk,
                'q_num': info.get('q_num'),
                'title': info.get('title'),
                'description': info.get('description'),
                'explanation': info.get('explanation'),
                'definition': info.get('definition', ''),
                'sql': info.get('sql', '').strip(),
                'columns': res.get('columns', []),
                'rows': res.get('rows', []),
                'row_count': res.get('row_count', 0),
                'execution_time_ms': res.get('execution_time_ms', 0.0)
            })
        except Exception as e:
            views_data.append({
                'key': vk,
                'q_num': info.get('q_num'),
                'title': info.get('title'),
                'description': info.get('description'),
                'explanation': info.get('explanation'),
                'definition': info.get('definition', ''),
                'sql': info.get('sql', '').strip(),
                'error': str(e),
                'columns': [],
                'rows': [],
                'row_count': 0,
                'execution_time_ms': 0.0
            })

    return render_template('sql_operations/views.html', views=views_data)

@sql_ops_bp.route('/procedures')
@login_required
def procedures_page():
    """Dedicated Stored Procedures page showcasing Q31 - Q35 procedures."""
    proc_keys = ['q31', 'q32', 'q33', 'q34', 'q35']
    procedures = []
    
    for pk in proc_keys:
        info = SQL_QUERIES_REGISTRY.get(pk, {})
        procedures.append({
            'key': pk,
            'q_num': info.get('q_num'),
            'procedure_name': info.get('procedure_name', ''),
            'title': info.get('title'),
            'description': info.get('description'),
            'explanation': info.get('explanation'),
            'parameters': info.get('parameters', []),
            'sql': info.get('sql', '').strip(),
            'definition': info.get('definition', '')
        })

    # Execute default procedure (Q35 / sp_list_customer_accounts) for initial view
    default_result = None
    try:
        default_result = run_registered_query('q35', params={'p_customer_id': 1}, user=current_user)
    except Exception as e:
        default_result = {'error': str(e)}

    return render_template(
        'sql_operations/procedures.html',
        procedures=procedures,
        initial_result=default_result,
        selected_key='q35'
    )

@sql_ops_bp.route('/history')
@login_required
def history_page():
    """Inspection interface for historical query executions."""
    category_filter = request.args.get('category')
    status_filter = request.args.get('status')
    history_records = get_query_history(limit=100, category=category_filter, status=status_filter)
    categories = get_categories_summary()

    return render_template(
        'sql_operations/history.html',
        history=history_records,
        categories=categories,
        selected_category=category_filter,
        selected_status=status_filter
    )


# =====================================================================
# RESTful API Endpoints (Section 5 Requirements)
# =====================================================================

@sql_ops_bp.route('/api/questions', methods=['GET'])
@login_required
def api_get_questions():
    """Returns metadata for all 41 SQL questions."""
    return jsonify({
        'success': True,
        'count': 41,
        'data': get_all_questions()
    })

@sql_ops_bp.route('/api/categories', methods=['GET'])
@login_required
def api_get_categories():
    """Returns the 8 SQL categories and question distribution."""
    return jsonify({
        'success': True,
        'data': get_categories_summary()
    })

@sql_ops_bp.route('/api/execute', methods=['POST'])
@login_required
def api_execute():
    """
    Unified query execution endpoint.
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

@sql_ops_bp.route('/api/run/<query_key>', methods=['GET', 'POST'])
@login_required
def api_run_query_legacy(query_key):
    """Backwards-compatible execution endpoint supporting GET and POST."""
    try:
        params = {}
        if request.method == 'POST':
            params = request.get_json() or {}
        elif request.args:
            params = request.args.to_dict()

        result = run_registered_query(query_key, params=params, user=current_user)
        return jsonify({'success': True, 'data': result})
    except PermissionError as pe:
        return jsonify({'success': False, 'error': str(pe)}), 403
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@sql_ops_bp.route('/api/custom', methods=['POST'])
@login_required
def api_run_custom_legacy():
    """Backwards-compatible custom query runner endpoint."""
    data = request.get_json() or {}
    custom_sql = data.get('sql', '').strip()
    if not custom_sql:
        return jsonify({'success': False, 'error': 'SQL query string cannot be empty.'}), 400

    try:
        result = run_custom_query(custom_sql, user=current_user)
        return jsonify({'success': True, 'data': result})
    except PermissionError as pe:
        return jsonify({'success': False, 'error': str(pe)}), 403
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@sql_ops_bp.route('/api/history', methods=['GET'])
@login_required
def api_get_history():
    """Returns execution history records."""
    category = request.args.get('category')
    status = request.args.get('status')
    limit = int(request.args.get('limit', 50))
    records = get_query_history(limit=limit, category=category, status=status)
    return jsonify({'success': True, 'count': len(records), 'data': records})

@sql_ops_bp.route('/api/clear-history', methods=['POST'])
@login_required
def api_clear_history():
    """Clears query execution history (Admin only)."""
    if not current_user.is_admin:
        return jsonify({'success': False, 'error': 'Only Administrators can clear execution logs.'}), 403
    cleared = clear_query_history()
    return jsonify({'success': cleared, 'message': 'Query execution logs cleared.'})

@sql_ops_bp.route('/api/reset-sample-data', methods=['POST'])
@login_required
def api_reset_sample_data():
    """Restores database to canonical sample dataset."""
    try:
        init_database(reset=True)
        return jsonify({
            'success': True,
            'message': 'Sample data successfully restored to canonical dataset (10 Customers, 12 Accounts, 24 Transactions, 6 Loans, 6 Employees, 4 Branches).'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

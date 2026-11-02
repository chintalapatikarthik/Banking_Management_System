from flask import Blueprint, render_template, request, jsonify, flash
from flask_login import login_required
from app.services.sql_queries import SQL_QUERIES_REGISTRY, run_registered_query, run_custom_query

sql_ops_bp = Blueprint('sql_ops', __name__, url_prefix='/sql-operations')

@sql_ops_bp.route('/')
@login_required
def index():
    # Group registry items by category
    categories = {}
    for key, item in SQL_QUERIES_REGISTRY.items():
        cat = item['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append({
            'key': key,
            'title': item['title'],
            'description': item['description'],
            'sql': item['sql'].strip()
        })

    # Default to running basic_1 for initial view
    initial_result = None
    try:
        initial_result = run_registered_query('basic_1')
    except Exception as e:
        initial_result = {'error': str(e)}

    return render_template('sql_operations/index.html', 
                           categories=categories, 
                           initial_result=initial_result,
                           total_queries=len(SQL_QUERIES_REGISTRY))

@sql_ops_bp.route('/api/run/<query_key>')
@login_required
def api_run_query(query_key):
    try:
        result = run_registered_query(query_key)
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@sql_ops_bp.route('/api/custom', methods=['POST'])
@login_required
def api_run_custom():
    data = request.get_json() or {}
    custom_sql = data.get('sql', '').strip()

    if not custom_sql:
        return jsonify({'success': False, 'error': 'SQL query string cannot be empty.'}), 400

    try:
        result = run_custom_query(custom_sql)
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

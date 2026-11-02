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
            'sql': item['sql'].strip(),
            'definition': item.get('definition', ''),
            'procedure_name': item.get('procedure_name', ''),
            'parameters': item.get('parameters', [])
        })

    # Allow query parameter to select active key (e.g., ?key=proc_1)
    selected_key = request.args.get('key', 'basic_1')
    if selected_key not in SQL_QUERIES_REGISTRY:
        selected_key = 'basic_1'

    initial_result = None
    try:
        initial_result = run_registered_query(selected_key)
    except Exception as e:
        initial_result = {'error': str(e)}

    return render_template('sql_operations/index.html', 
                           categories=categories, 
                           initial_result=initial_result,
                           initial_key=selected_key,
                           total_queries=len(SQL_QUERIES_REGISTRY))

@sql_ops_bp.route('/procedures')
@login_required
def procedures():
    """Dedicated interactive workbench for MySQL 8.x Stored Procedures."""
    procedure_items = {k: v for k, v in SQL_QUERIES_REGISTRY.items() if v.get('category') == 'Stored Procedures'}
    
    selected_key = request.args.get('key', 'proc_1')
    if selected_key not in procedure_items:
        selected_key = 'proc_1'

    initial_result = None
    try:
        initial_result = run_registered_query(selected_key)
    except Exception as e:
        initial_result = {'error': str(e)}

    return render_template('sql_operations/procedures.html', 
                           procedures=procedure_items, 
                           selected_key=selected_key,
                           initial_result=initial_result)

@sql_ops_bp.route('/api/run/<query_key>', methods=['GET', 'POST'])
@login_required
def api_run_query(query_key):
    try:
        params = {}
        if request.method == 'POST':
            params = request.get_json() or {}
        elif request.args:
            params = request.args.to_dict()

        result = run_registered_query(query_key, params=params)
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

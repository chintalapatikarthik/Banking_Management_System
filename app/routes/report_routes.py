import io
import csv
from flask import Blueprint, render_template, request, Response
from flask_login import login_required
from app.services.sql_queries import run_registered_query

report_bp = Blueprint('report', __name__, url_prefix='/reports')

@report_bp.route('', strict_slashes=False)
@report_bp.route('/', strict_slashes=False)
@login_required
def index():
    active_tab = request.args.get('tab', 'top_balance')

    reports = {
        'top_balance': run_registered_query('report_1'),
        'active_customers': run_registered_query('report_2'),
        'monthly_transactions': run_registered_query('report_3'),
        'branch_deposits': run_registered_query('report_4'),
        'tx_analysis': run_registered_query('report_5'),
        'high_loans': run_registered_query('report_6')
    }

    return render_template('reports/index.html', reports=reports, active_tab=active_tab)

@report_bp.route('/export/<report_key>')
@login_required
def export_csv(report_key):
    key_mapping = {
        'top_balance': 'report_1',
        'active_customers': 'report_2',
        'monthly_transactions': 'report_3',
        'branch_deposits': 'report_4',
        'tx_analysis': 'report_5',
        'high_loans': 'report_6'
    }

    actual_key = key_mapping.get(report_key, 'report_1')
    result = run_registered_query(actual_key)

    output = io.StringIO()
    writer = csv.writer(output)

    if result['columns']:
        writer.writerow(result['columns'])
        for row in result['rows']:
            writer.writerow([row.get(col, '') for col in result['columns']])

    csv_data = output.getvalue()
    filename = f"{report_key}_report.csv"

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename={filename}"}
    )

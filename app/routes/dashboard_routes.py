from flask import Blueprint, render_template, jsonify, redirect, url_for
from flask_login import login_required, current_user
from app.services.bank_service import BankService
from app.services.analytics_service import AnalyticsService

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    return redirect(url_for('auth.login'))

@dashboard_bp.route('/dashboard')
@login_required
def index():
    summary = BankService.get_dashboard_summary()
    return render_template('dashboard.html', summary=summary)

@dashboard_bp.route('/api/charts')
@login_required
def api_charts():
    charts_data = AnalyticsService.get_dashboard_charts_data()
    return jsonify(charts_data)

# Top-level direct shortcuts
@dashboard_bp.route('/sql-lab')
@login_required
def sql_lab_shortcut():
    return redirect(url_for('sql_ops.index'))

@dashboard_bp.route('/sql-views')
@login_required
def sql_views_shortcut():
    return redirect(url_for('sql_ops.views_page'))

@dashboard_bp.route('/stored-procedures')
@login_required
def stored_procedures_shortcut():
    return redirect(url_for('sql_ops.procedures_page'))

@dashboard_bp.route('/sql-history')
@login_required
def sql_history_shortcut():
    return redirect(url_for('sql_ops.history_page'))


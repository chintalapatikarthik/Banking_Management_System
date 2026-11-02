from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from app.services.bank_service import BankService
from app.services.analytics_service import AnalyticsService

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def home():
    return render_template('dashboard.html')

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

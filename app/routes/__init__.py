from app.routes.auth_routes import auth_bp
from app.routes.dashboard_routes import dashboard_bp
from app.routes.customer_routes import customer_bp
from app.routes.account_routes import account_bp
from app.routes.transaction_routes import transaction_bp
from app.routes.loan_routes import loan_bp
from app.routes.employee_routes import employee_bp
from app.routes.branch_routes import branch_bp
from app.routes.sql_ops_routes import sql_ops_bp
from app.routes.sql_api_routes import sql_api_bp
from app.routes.report_routes import report_bp

def register_blueprints(app):
    """Registers all application blueprint modules."""
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(account_bp)
    app.register_blueprint(transaction_bp)
    app.register_blueprint(loan_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(branch_bp)
    app.register_blueprint(sql_ops_bp)
    app.register_blueprint(sql_api_bp)
    app.register_blueprint(report_bp)

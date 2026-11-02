import os
from flask import Flask, render_template
from app.config import Config
from app.auth import login_manager
from app.routes import register_blueprints
from app.database import engine, Base
from database.init_db import init_database

def create_app(config_class=Config):
    """Application factory for Banking Management System."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Authentication
    login_manager.init_app(app)

    # Register Blueprints
    register_blueprints(app)

    # Custom Jinja filters
    @app.template_filter('currency')
    def currency_filter(value):
        try:
            val = float(value or 0)
            return f"₹{val:,.2f}"
        except (ValueError, TypeError):
            return f"₹{value}"

    @app.template_filter('format_date')
    def format_date_filter(value):
        if not value:
            return ''
        if isinstance(value, str):
            return value
        return value.strftime('%b %d, %Y')

    # Context processors for global template variables
    @app.context_processor
    def inject_globals():
        return {
            'bank_name': Config.BANK_NAME,
            'bank_tagline': Config.BANK_TAGLINE,
            'app_version': Config.APP_VERSION
        }

    # Custom error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html', error=str(e)), 500

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('403.html'), 403

    # Ensure database is initialized
    with app.app_context():
        try:
            init_database()
        except Exception as e:
            app.logger.warning(f"Database auto-init warning: {e}")

    return app

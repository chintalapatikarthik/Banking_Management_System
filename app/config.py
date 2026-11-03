import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base application configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'banking-management-system-secret-key-92817293')
    
    # Database URL
    raw_db_url = os.environ.get('DATABASE_URL', '').strip()
    if not raw_db_url:
        mysql_user = os.environ.get('MYSQL_USER')
        mysql_pwd = os.environ.get('MYSQL_PASSWORD')
        if mysql_user and mysql_pwd:
            import urllib.parse
            mysql_host = os.environ.get('MYSQL_HOST', '127.0.0.1')
            mysql_port = os.environ.get('MYSQL_PORT', '3306')
            mysql_db = os.environ.get('MYSQL_DATABASE', 'banking_management_system')
            raw_db_url = f"mysql+pymysql://{mysql_user}:{urllib.parse.quote_plus(mysql_pwd)}@{mysql_host}:{mysql_port}/{mysql_db}"
        else:
            raw_db_url = 'sqlite:///banking.db'
    
    # Fix for Heroku/Render postgres or mysql dialect if needed
    if raw_db_url.startswith('postgres://'):
        raw_db_url = raw_db_url.replace('postgres://', 'postgresql://', 1)
    elif raw_db_url.startswith('mysql://'):
        raw_db_url = raw_db_url.replace('mysql://', 'mysql+pymysql://', 1)
        
    SQLALCHEMY_DATABASE_URI = raw_db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 280,
        'pool_pre_ping': True,
    } if 'sqlite' not in raw_db_url else {}
    
    # Session Security
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    
    # Default Administrative & Staff Credentials
    DEFAULT_ADMIN_USERNAME = os.environ.get('DEFAULT_ADMIN_USERNAME', 'admin')
    DEFAULT_ADMIN_PASSWORD = os.environ.get('DEFAULT_ADMIN_PASSWORD', 'Admin@123')
    DEFAULT_ADMIN_EMAIL = os.environ.get('DEFAULT_ADMIN_EMAIL', 'admin@bankingsystem.com')
    
    DEFAULT_EMPLOYEE_USERNAME = os.environ.get('DEFAULT_EMPLOYEE_USERNAME', 'employee')
    DEFAULT_EMPLOYEE_PASSWORD = os.environ.get('DEFAULT_EMPLOYEE_PASSWORD', 'Employee@123')
    DEFAULT_EMPLOYEE_EMAIL = os.environ.get('DEFAULT_EMPLOYEE_EMAIL', 'employee@bankingsystem.com')
    
    # Bank Identity
    BANK_NAME = "Banking Management System"
    BANK_TAGLINE = "Full-Stack Python & SQL Web Application"
    APP_VERSION = "2.4.0"

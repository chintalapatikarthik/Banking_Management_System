from functools import wraps
from flask import redirect, url_for, flash, abort
from flask_login import LoginManager, current_user
from app.models import User
from app.database import get_db

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    with get_db() as db:
        user = db.query(User).filter_by(user_id=int(user_id)).first()
        if user:
            # Expunge to use across request outside context
            db.expunge(user)
        return user

def admin_required(f):
    """Decorator ensuring that only users with role 'admin' can access the route."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        if current_user.role != 'admin':
            flash("Administrator privileges required to access this resource.", "danger")
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function

def employee_required(f):
    """Decorator ensuring that logged-in users with role 'employee' or 'admin' can access."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

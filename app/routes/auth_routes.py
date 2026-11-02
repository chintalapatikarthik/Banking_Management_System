from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app.database import get_db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = bool(request.form.get('remember'))

        if not username or not password:
            flash("Please provide both username and password.", "danger")
            return render_template('login.html', username=username)

        with get_db() as db:
            user = db.query(User).filter((User.username == username) | (User.email == username)).first()
            if user and user.check_password(password):
                if not user.is_active:
                    flash("Your account has been deactivated. Please contact an administrator.", "warning")
                    return render_template('login.html', username=username)

                # Detach/expunge before login_user
                db.expunge(user)
                login_user(user, remember=remember)
                flash(f"Welcome back, {user.username}! Signed in as {user.role.title()}.", "success")
                next_page = request.args.get('next')
                return redirect(next_page or url_for('dashboard.index'))
            else:
                flash("Invalid username or password. Please try again.", "danger")

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been successfully logged out.", "info")
    return redirect(url_for('auth.login'))

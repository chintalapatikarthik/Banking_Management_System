from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import Branch, Employee, Account
from app.database import get_db
from app.auth import admin_required

branch_bp = Blueprint('branch', __name__, url_prefix='/branches')

@branch_bp.route('/')
@login_required
def list_branches():
    search = request.args.get('search', '').strip()

    with get_db() as db:
        query = db.query(Branch)
        if search:
            query = query.filter((Branch.branch_name.ilike(f'%{search}%')) | (Branch.location.ilike(f'%{search}%')))

        branches = query.order_by(Branch.branch_id.asc()).all()
        branch_list = [b.to_dict() for b in branches]

    return render_template('branches/list.html', branches=branch_list, search=search)

@branch_bp.route('/new', methods=['GET', 'POST'])
@login_required
@admin_required
def create_branch():
    if request.method == 'POST':
        name = request.form.get('branch_name', '').strip()
        location = request.form.get('location', '').strip()

        if not name or not location:
            flash("Branch Name and Location are required.", "danger")
            return render_template('branches/form.html', action='new', branch=request.form)

        with get_db() as db:
            branch = Branch(branch_name=name, location=location)
            db.add(branch)
            db.commit()
            flash(f"Branch '{name}' created successfully in {location}!", "success")
            return redirect(url_for('branch.list_branches'))

    return render_template('branches/form.html', action='new', branch={})

@branch_bp.route('/<int:branch_id>')
@login_required
def view_branch(branch_id):
    with get_db() as db:
        branch = db.query(Branch).filter_by(branch_id=branch_id).first()
        if not branch:
            flash("Branch not found.", "danger")
            return redirect(url_for('branch.list_branches'))

        b_data = branch.to_dict()
        employees = [e.to_dict() for e in branch.employees]
        accounts = [a.to_dict() for a in branch.accounts]

    return render_template('branches/view.html', branch=b_data, employees=employees, accounts=accounts)

@branch_bp.route('/<int:branch_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_branch(branch_id):
    with get_db() as db:
        branch = db.query(Branch).filter_by(branch_id=branch_id).first()
        if not branch:
            flash("Branch not found.", "danger")
            return redirect(url_for('branch.list_branches'))

        if request.method == 'POST':
            name = request.form.get('branch_name', '').strip()
            location = request.form.get('location', '').strip()

            if not name or not location:
                flash("Branch Name and Location are required.", "danger")
                return render_template('branches/form.html', action='edit', branch=request.form)

            branch.branch_name = name
            branch.location = location
            db.commit()
            flash(f"Branch #{branch_id} updated.", "success")
            return redirect(url_for('branch.view_branch', branch_id=branch_id))

        b_dict = branch.to_dict()

    return render_template('branches/form.html', action='edit', branch=b_dict)

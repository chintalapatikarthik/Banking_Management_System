from decimal import Decimal
from datetime import datetime, date
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import Employee, Branch
from app.database import get_db
from app.auth import admin_required

employee_bp = Blueprint('employee', __name__, url_prefix='/employees')

@employee_bp.route('/')
@login_required
def list_employees():
    search = request.args.get('search', '').strip()
    position = request.args.get('position', '').strip()
    branch_id = request.args.get('branch_id', type=int)

    with get_db() as db:
        query = db.query(Employee).outerjoin(Branch)

        if search:
            if search.isdigit():
                query = query.filter(Employee.employee_id == int(search))
            else:
                query = query.filter(Employee.employee_name.ilike(f'%{search}%'))

        if position:
            query = query.filter(Employee.position == position)

        if branch_id:
            query = query.filter(Employee.branch_id == branch_id)

        employees = query.order_by(Employee.employee_id.asc()).all()
        emp_list = [e.to_dict() for e in employees]

        # Filter choices
        positions = sorted(list({e.position for e in db.query(Employee).all()}))
        branches = db.query(Branch).order_by(Branch.branch_name).all()
        branch_choices = [{'id': b.branch_id, 'name': b.branch_name} for b in branches]

    return render_template('employees/list.html', 
                           employees=emp_list, 
                           positions=positions, 
                           branches=branch_choices,
                           search=search, 
                           selected_position=position, 
                           selected_branch=branch_id)

@employee_bp.route('/new', methods=['GET', 'POST'])
@login_required
@admin_required
def create_employee():
    with get_db() as db:
        branches = db.query(Branch).order_by(Branch.branch_name).all()
        branch_choices = [{'id': b.branch_id, 'name': b.branch_name} for b in branches]

    if request.method == 'POST':
        name = request.form.get('employee_name', '').strip()
        position = request.form.get('position', '').strip()
        salary = request.form.get('salary', type=float)
        branch_id = request.form.get('branch_id', type=int)
        joining_date_str = request.form.get('joining_date', '')

        if not name or not position or not salary:
            flash("Employee Name, Position, and Salary are required.", "danger")
            return render_template('employees/form.html', action='new', branches=branch_choices, employee=request.form)

        try:
            joining_date = datetime.strptime(joining_date_str, '%Y-%m-%d').date() if joining_date_str else date.today()
        except ValueError:
            joining_date = date.today()

        with get_db() as db:
            emp = Employee(
                employee_name=name,
                position=position,
                salary=Decimal(str(salary)),
                joining_date=joining_date,
                branch_id=branch_id if branch_id else None
            )
            db.add(emp)
            db.commit()
            flash(f"Employee '{name}' (ID: {emp.employee_id}) onboarded successfully!", "success")
            return redirect(url_for('employee.list_employees'))

    return render_template('employees/form.html', action='new', branches=branch_choices, employee={'joining_date': date.today().strftime('%Y-%m-%d')})

@employee_bp.route('/<int:employee_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_employee(employee_id):
    with get_db() as db:
        emp = db.query(Employee).filter_by(employee_id=employee_id).first()
        if not emp:
            flash("Employee not found.", "danger")
            return redirect(url_for('employee.list_employees'))

        branches = db.query(Branch).order_by(Branch.branch_name).all()
        branch_choices = [{'id': b.branch_id, 'name': b.branch_name} for b in branches]

        if request.method == 'POST':
            name = request.form.get('employee_name', '').strip()
            position = request.form.get('position', '').strip()
            salary = request.form.get('salary', type=float)
            branch_id = request.form.get('branch_id', type=int)

            if not name or not position or not salary:
                flash("Employee Name, Position, and Salary are required.", "danger")
                return render_template('employees/form.html', action='edit', branches=branch_choices, employee=request.form)

            emp.employee_name = name
            emp.position = position
            emp.salary = Decimal(str(salary))
            emp.branch_id = branch_id if branch_id else None
            db.commit()
            flash(f"Employee #{employee_id} updated successfully.", "success")
            return redirect(url_for('employee.list_employees'))

        emp_dict = emp.to_dict()

    return render_template('employees/form.html', action='edit', branches=branch_choices, employee=emp_dict)

@employee_bp.route('/<int:employee_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_employee(employee_id):
    with get_db() as db:
        emp = db.query(Employee).filter_by(employee_id=employee_id).first()
        if not emp:
            flash("Employee not found.", "danger")
            return redirect(url_for('employee.list_employees'))

        name = emp.employee_name
        db.delete(emp)
        db.commit()
        flash(f"Employee #{employee_id} ({name}) removed.", "success")

    return redirect(url_for('employee.list_employees'))

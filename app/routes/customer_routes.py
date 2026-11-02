from datetime import datetime, date
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import Customer, Account, Loan
from app.database import get_db
from app.auth import admin_required

customer_bp = Blueprint('customer', __name__, url_prefix='/customers')

@customer_bp.route('/')
@login_required
def list_customers():
    search = request.args.get('search', '').strip()
    location = request.args.get('location', '').strip()

    with get_db() as db:
        query = db.query(Customer)
        if search:
            if search.isdigit():
                query = query.filter((Customer.customer_id == int(search)) | (Customer.name.ilike(f'%{search}%')))
            else:
                query = query.filter(Customer.name.ilike(f'%{search}%'))
        if location:
            query = query.filter(Customer.address.ilike(f'%{location}%'))

        customers = query.order_by(Customer.customer_id.desc()).all()
        # Extract unique cities for filter dropdown
        all_custs = db.query(Customer.address).all()
        cities = sorted(list({addr[0].split(',')[-1].strip() for addr in all_custs if addr[0]}))

        cust_list = [c.to_dict() for c in customers]

    return render_template('customers/list.html', customers=cust_list, search=search, location=location, cities=cities)

@customer_bp.route('/new', methods=['GET', 'POST'])
@login_required
def create_customer():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()
        reg_date_str = request.form.get('registration_date', '')

        if not name or not email:
            flash("Customer Name and Email are mandatory.", "danger")
            return render_template('customers/form.html', action='new', customer=request.form)

        try:
            reg_date = datetime.strptime(reg_date_str, '%Y-%m-%d').date() if reg_date_str else date.today()
        except ValueError:
            reg_date = date.today()

        with get_db() as db:
            if db.query(Customer).filter_by(email=email).first():
                flash(f"A customer with email '{email}' already exists.", "danger")
                return render_template('customers/form.html', action='new', customer=request.form)

            cust = Customer(
                name=name,
                email=email,
                phone=phone or None,
                address=address or None,
                registration_date=reg_date
            )
            db.add(cust)
            db.commit()
            flash(f"Customer '{name}' (ID: {cust.customer_id}) registered successfully!", "success")
            return redirect(url_for('customer.view_customer', customer_id=cust.customer_id))

    return render_template('customers/form.html', action='new', customer={'registration_date': date.today().strftime('%Y-%m-%d')})

@customer_bp.route('/<int:customer_id>')
@login_required
def view_customer(customer_id):
    with get_db() as db:
        customer = db.query(Customer).filter_by(customer_id=customer_id).first()
        if not customer:
            flash("Customer not found.", "danger")
            return redirect(url_for('customer.list_customers'))

        cust_data = customer.to_dict()
        accounts = [a.to_dict() for a in customer.accounts]
        loans = [l.to_dict() for l in customer.loans]

    return render_template('customers/view.html', customer=cust_data, accounts=accounts, loans=loans)

@customer_bp.route('/<int:customer_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_customer(customer_id):
    with get_db() as db:
        customer = db.query(Customer).filter_by(customer_id=customer_id).first()
        if not customer:
            flash("Customer not found.", "danger")
            return redirect(url_for('customer.list_customers'))

        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip().lower()
            phone = request.form.get('phone', '').strip()
            address = request.form.get('address', '').strip()

            if not name or not email:
                flash("Customer Name and Email are mandatory.", "danger")
                return render_template('customers/form.html', action='edit', customer=request.form)

            # Check email uniqueness against other customers
            existing = db.query(Customer).filter(Customer.email == email, Customer.customer_id != customer_id).first()
            if existing:
                flash(f"Another customer with email '{email}' already exists.", "danger")
                return render_template('customers/form.html', action='edit', customer=request.form)

            customer.name = name
            customer.email = email
            customer.phone = phone or None
            customer.address = address or None
            db.commit()
            flash(f"Customer #{customer_id} updated successfully.", "success")
            return redirect(url_for('customer.view_customer', customer_id=customer_id))

        cust_dict = customer.to_dict()

    return render_template('customers/form.html', action='edit', customer=cust_dict)

@customer_bp.route('/<int:customer_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_customer(customer_id):
    with get_db() as db:
        customer = db.query(Customer).filter_by(customer_id=customer_id).first()
        if not customer:
            flash("Customer not found.", "danger")
            return redirect(url_for('customer.list_customers'))

        # Check if customer has positive balance in any accounts
        for acc in customer.accounts:
            if acc.balance > 0:
                flash(f"Cannot delete Customer #{customer_id}: Account #{acc.account_id} still holds a balance of ₹{acc.balance:,.2f}.", "danger")
                return redirect(url_for('customer.view_customer', customer_id=customer_id))

        name = customer.name
        db.delete(customer)
        db.commit()
        flash(f"Customer #{customer_id} ({name}) has been permanently deleted.", "success")
        return redirect(url_for('customer.list_customers'))

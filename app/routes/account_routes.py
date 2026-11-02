from decimal import Decimal
from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import Account, Customer, Branch, Transaction
from app.database import get_db
from app.services.bank_service import BankService

account_bp = Blueprint('account', __name__, url_prefix='/accounts')

@account_bp.route('/')
@login_required
def list_accounts():
    search = request.args.get('search', '').strip()
    account_type = request.args.get('account_type', '').strip()
    account_status = request.args.get('account_status', '').strip()

    with get_db() as db:
        query = db.query(Account)
        if search:
            if search.isdigit():
                query = query.filter((Account.account_id == int(search)) | (Account.customer_id == int(search)))
            else:
                query = query.join(Customer).filter(Customer.name.ilike(f'%{search}%'))
        if account_type:
            query = query.filter(Account.account_type == account_type)
        if account_status:
            query = query.filter(Account.account_status == account_status)

        accounts = query.order_by(Account.account_id.desc()).all()
        acc_list = [a.to_dict() for a in accounts]

    return render_template('accounts/list.html', 
                           accounts=acc_list, 
                           search=search, 
                           account_type=account_type, 
                           account_status=account_status)

@account_bp.route('/new', methods=['GET', 'POST'])
@login_required
def create_account():
    with get_db() as db:
        customers = db.query(Customer).order_by(Customer.name).all()
        branches = db.query(Branch).order_by(Branch.branch_name).all()
        cust_choices = [{'id': c.customer_id, 'name': c.name, 'email': c.email} for c in customers]
        branch_choices = [{'id': b.branch_id, 'name': b.branch_name, 'location': b.location} for b in branches]

    if request.method == 'POST':
        customer_id = request.form.get('customer_id', type=int)
        branch_id = request.form.get('branch_id', type=int)
        account_type = request.form.get('account_type', 'Savings')
        initial_deposit = request.form.get('initial_deposit', 0.0, type=float)

        if not customer_id:
            flash("Please select a customer for the account.", "danger")
            return render_template('accounts/form.html', customers=cust_choices, branches=branch_choices)

        try:
            acc_data = BankService.create_account(
                customer_id=customer_id,
                branch_id=branch_id,
                account_type=account_type,
                initial_deposit=initial_deposit
            )
            flash(f"Account #{acc_data['account_id']} ({account_type}) opened successfully with initial balance ₹{initial_deposit:,.2f}.", "success")
            return redirect(url_for('account.view_account', account_id=acc_data['account_id']))
        except Exception as e:
            flash(f"Failed to create account: {str(e)}", "danger")

    return render_template('accounts/form.html', customers=cust_choices, branches=branch_choices)

@account_bp.route('/<int:account_id>')
@login_required
def view_account(account_id):
    with get_db() as db:
        account = db.query(Account).filter_by(account_id=account_id).first()
        if not account:
            flash("Account not found.", "danger")
            return redirect(url_for('account.list_accounts'))

        acc_data = account.to_dict()
        transactions = [t.to_dict() for t in account.transactions]
        customer = account.customer.to_dict() if account.customer else None

    return render_template('accounts/view.html', account=acc_data, transactions=transactions, customer=customer)

@account_bp.route('/<int:account_id>/toggle-status', methods=['POST'])
@login_required
def toggle_status(account_id):
    with get_db() as db:
        account = db.query(Account).filter_by(account_id=account_id).first()
        if not account:
            flash("Account not found.", "danger")
            return redirect(url_for('account.list_accounts'))

        new_status = 'Inactive' if account.account_status == 'Active' else 'Active'
        account.account_status = new_status
        db.commit()
        flash(f"Account #{account_id} status updated to '{new_status}'.", "info")

    return redirect(request.referrer or url_for('account.view_account', account_id=account_id))

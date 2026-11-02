from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import Transaction, Account, Customer
from app.database import get_db
from app.services.bank_service import BankService

transaction_bp = Blueprint('transaction', __name__, url_prefix='/transactions')

@transaction_bp.route('/')
@login_required
def list_transactions():
    search = request.args.get('search', '').strip()
    tx_type = request.args.get('transaction_type', '').strip()
    start_date = request.args.get('start_date', '').strip()
    end_date = request.args.get('end_date', '').strip()

    with get_db() as db:
        query = db.query(Transaction).join(Account).join(Customer)

        if search:
            if search.isdigit():
                query = query.filter((Transaction.transaction_id == int(search)) | (Transaction.account_id == int(search)))
            else:
                query = query.filter(Customer.name.ilike(f'%{search}%'))

        if tx_type:
            query = query.filter(Transaction.transaction_type == tx_type)

        if start_date:
            query = query.filter(Transaction.transaction_date >= start_date)

        if end_date:
            query = query.filter(Transaction.transaction_date <= end_date)

        transactions = query.order_by(Transaction.transaction_date.desc(), Transaction.transaction_id.desc()).all()
        tx_list = [t.to_dict() for t in transactions]

    return render_template('transactions/list.html', 
                           transactions=tx_list,
                           search=search,
                           tx_type=tx_type,
                           start_date=start_date,
                           end_date=end_date)

@transaction_bp.route('/deposit', methods=['GET', 'POST'])
@login_required
def deposit():
    with get_db() as db:
        accounts = db.query(Account).filter_by(account_status='Active').order_by(Account.account_id).all()
        acc_choices = [a.to_dict() for a in accounts]

    prefill_acc = request.args.get('account_id', type=int)

    if request.method == 'POST':
        account_id = request.form.get('account_id', type=int)
        amount = request.form.get('amount', type=float)
        description = request.form.get('description', '').strip()

        if not account_id or not amount:
            flash("Account and Amount are required.", "danger")
            return render_template('transactions/deposit.html', accounts=acc_choices, prefill_acc=prefill_acc)

        try:
            res = BankService.deposit(account_id, amount, description)
            flash(f"Deposit successful! ₹{amount:,.2f} credited to Account #{account_id}. New Balance: ₹{res['new_balance']:,.2f}.", "success")
            return redirect(url_for('account.view_account', account_id=account_id))
        except Exception as e:
            flash(f"Deposit failed: {str(e)}", "danger")

    return render_template('transactions/deposit.html', accounts=acc_choices, prefill_acc=prefill_acc)

@transaction_bp.route('/withdraw', methods=['GET', 'POST'])
@login_required
def withdraw():
    with get_db() as db:
        accounts = db.query(Account).filter_by(account_status='Active').order_by(Account.account_id).all()
        acc_choices = [a.to_dict() for a in accounts]

    prefill_acc = request.args.get('account_id', type=int)

    if request.method == 'POST':
        account_id = request.form.get('account_id', type=int)
        amount = request.form.get('amount', type=float)
        description = request.form.get('description', '').strip()

        if not account_id or not amount:
            flash("Account and Amount are required.", "danger")
            return render_template('transactions/withdraw.html', accounts=acc_choices, prefill_acc=prefill_acc)

        try:
            res = BankService.withdraw(account_id, amount, description)
            flash(f"Withdrawal successful! ₹{amount:,.2f} debited from Account #{account_id}. New Balance: ₹{res['new_balance']:,.2f}.", "success")
            return redirect(url_for('account.view_account', account_id=account_id))
        except Exception as e:
            flash(f"Withdrawal failed: {str(e)}", "danger")

    return render_template('transactions/withdraw.html', accounts=acc_choices, prefill_acc=prefill_acc)

@transaction_bp.route('/transfer', methods=['GET', 'POST'])
@login_required
def transfer():
    with get_db() as db:
        accounts = db.query(Account).filter_by(account_status='Active').order_by(Account.account_id).all()
        acc_choices = [a.to_dict() for a in accounts]

    prefill_src = request.args.get('source_id', type=int)

    if request.method == 'POST':
        source_id = request.form.get('source_account_id', type=int)
        target_id = request.form.get('target_account_id', type=int)
        amount = request.form.get('amount', type=float)
        description = request.form.get('description', '').strip()

        if not source_id or not target_id or not amount:
            flash("Source account, Destination account, and Amount are all required.", "danger")
            return render_template('transactions/transfer.html', accounts=acc_choices, prefill_src=prefill_src)

        try:
            res = BankService.transfer(source_id, target_id, amount, description)
            flash(f"Atomic Transfer of ₹{amount:,.2f} from Account #{source_id} to Account #{target_id} completed successfully!", "success")
            return redirect(url_for('account.view_account', account_id=source_id))
        except Exception as e:
            flash(f"Transfer failed: {str(e)}", "danger")

    return render_template('transactions/transfer.html', accounts=acc_choices, prefill_src=prefill_src)

from decimal import Decimal
from datetime import datetime, date
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import Loan, Customer
from app.database import get_db
from app.services.bank_service import BankService

loan_bp = Blueprint('loan', __name__, url_prefix='/loans')

@loan_bp.route('/')
@login_required
def list_loans():
    search = request.args.get('search', '').strip()
    start_date = request.args.get('start_date', '').strip()
    end_date = request.args.get('end_date', '').strip()

    with get_db() as db:
        query = db.query(Loan).join(Customer)

        if search:
            if search.isdigit():
                query = query.filter((Loan.loan_id == int(search)) | (Loan.customer_id == int(search)))
            else:
                query = query.filter(Customer.name.ilike(f'%{search}%'))

        if start_date:
            query = query.filter(Loan.loan_date >= start_date)
        if end_date:
            query = query.filter(Loan.loan_date <= end_date)

        loans = query.order_by(Loan.loan_amount.desc()).all()
        loan_list = [l.to_dict() for l in loans]

        total_amount = sum(l['loan_amount'] for l in loan_list)
        avg_interest = (sum(l['interest_rate'] for l in loan_list) / len(loan_list)) if loan_list else 0.0

    return render_template('loans/list.html', 
                           loans=loan_list, 
                           total_amount=total_amount,
                           avg_interest=round(avg_interest, 2),
                           search=search, 
                           start_date=start_date, 
                           end_date=end_date)

@loan_bp.route('/new', methods=['GET', 'POST'])
@login_required
def create_loan():
    with get_db() as db:
        customers = db.query(Customer).order_by(Customer.name).all()
        cust_choices = [c.to_dict() for c in customers]

    if request.method == 'POST':
        customer_id = request.form.get('customer_id', type=int)
        loan_amount = request.form.get('loan_amount', type=float)
        interest_rate = request.form.get('interest_rate', type=float)
        loan_date_str = request.form.get('loan_date', '')

        if not customer_id or not loan_amount or not interest_rate:
            flash("All fields are required.", "danger")
            return render_template('loans/form.html', customers=cust_choices, loan=request.form)

        try:
            loan_date = datetime.strptime(loan_date_str, '%Y-%m-%d').date() if loan_date_str else date.today()
        except ValueError:
            loan_date = date.today()

        try:
            loan = BankService.create_loan(customer_id, loan_amount, interest_rate, loan_date)
            flash(f"Loan #{loan['loan_id']} for ₹{loan_amount:,.2f} at {interest_rate}% interest disbursed successfully!", "success")
            return redirect(url_for('loan.list_loans'))
        except Exception as e:
            flash(f"Error disbursing loan: {str(e)}", "danger")

    return render_template('loans/form.html', customers=cust_choices, loan={'loan_date': date.today().strftime('%Y-%m-%d'), 'interest_rate': 8.5})

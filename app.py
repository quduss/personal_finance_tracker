from flask import Flask, render_template, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm, LoginForm, TransactionForm
from flask_login import LoginManager, logout_user, login_user, login_required, current_user
from models import db
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
from models import User, Transaction

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/')
def home():
    return "Welcome to Personal Finance Tracker!"

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))

        except IntegrityError:
            db.session.rollback()
            flash('Username or email already exists. Please choose a different one.', 'danger')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/add_transaction', methods=['GET', 'POST'])
@login_required
def add_transaction():
    form = TransactionForm()
    if form.validate_on_submit():
        new_transaction = Transaction(
            amount=form.amount.data,
            description=form.description.data,
            transaction_type=form.transaction_type.data,
            category=form.category.data,
            user_id=current_user.id
        )
        db.session.add(new_transaction)
        db.session.commit()
        flash('Transaction added successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_transaction.html', form=form)

@app.route('/transactions')
@login_required
def transactions():
    # Get all transactions for the current logged-in user
    user_transactions = Transaction.query.filter_by(user_id=current_user.id).all()

    return render_template('transactions.html', transactions=user_transactions)

@app.route('/edit_transaction/<int:transaction_id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)

    # Ensure the user can only edit their own transactions
    if transaction.user_id != current_user.id:
        flash('You are not authorized to edit this transaction', 'danger')
        return redirect(url_for('transactions'))

    form = TransactionForm(obj=transaction)

    if form.validate_on_submit():
        transaction.amount = form.amount.data
        transaction.description = form.description.data
        transaction.transaction_type = form.transaction_type.data
        transaction.category = form.category.data  # if category is implemented
        #transaction.date = form.date.data  # if allowing date editing

        db.session.commit()
        flash('Transaction updated successfully!', 'success')
        return redirect(url_for('transactions'))

    return render_template('edit_transaction.html', form=form, transaction=transaction)

@app.route('/delete_transaction/<int:transaction_id>', methods=['GET', 'POST'])
@login_required
def delete_transaction(transaction_id):
    # Get the transaction by ID and ensure it belongs to the current user
    transaction = Transaction.query.filter_by(id=transaction_id, user_id=current_user.id).first()
    
    if transaction:
        db.session.delete(transaction)
        db.session.commit()
        flash('Transaction has been deleted successfully!', 'success')
    else:
        flash('Transaction not found or unauthorized action.', 'danger')
    
    return redirect(url_for('transactions'))


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

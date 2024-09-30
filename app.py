from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager
from models import db, User

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return "Welcome to Personal Finance Tracker!"

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
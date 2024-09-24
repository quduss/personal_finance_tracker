from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to Personal Finance Tracker!"

if __name__ == '__main__':
    app.run(debug=True)
# flask_paralympics/routes.py

from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/hello/<name>')
def hello(name):
    return f"你好 {name}，欢迎来到 Paralympics App!"

from flask import request

@main.route('/welcome', methods=['GET', 'POST'])
def welcome():
    if request.method == 'POST':
        name = request.form['username']
        return render_template('hello.html', name=name)
    return render_template('form.html')
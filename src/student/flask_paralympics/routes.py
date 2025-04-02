from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/hello/<name>')
def hello(name):
    return render_template('hello.html', name=name)

@main.route('/welcome', methods=['GET', 'POST'])
def welcome():
    from flask import request, redirect, url_for, session
    if request.method == 'POST':
        name = request.form['username']
        return redirect(url_for('main.hello', name=name))
    return render_template('form.html')

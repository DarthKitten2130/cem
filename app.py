from flask import Flask
from flask import render_template, request, redirect, url_for
from sql import *

app = Flask(__name__)


@app.route('/')
def home():
    create_table()
    return render_template('index.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    create_table()
    if request.method == 'POST':
        id = request.form['id']
        password = request.form['password']

        user = get_user(id)
        if user and user[5] == password:
            return redirect(url_for('home'))
        else:
            return render_template('signin.html', error='Invalid credentials')

    return render_template('signin.html')


@app.route('/createaccount', methods=['GET', 'POST'])
def create_account():
    create_table()
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        branch = request.form['branch']
        password = request.form['password']

        insert_user(id, name, email, phone, branch, password)

        return redirect(url_for('home'))

    return render_template('createaccount.html')


if __name__ == '__main__':
    app.run(debug=True)

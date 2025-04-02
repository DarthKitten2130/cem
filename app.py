from flask import Flask, render_template, request, redirect, url_for, session, templating
from sql import *

app = Flask(__name__)
app.secret_key = 'ROOT'


@app.route('/')
def home():
    create_table()
    return render_template('index.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    alert_message = ""
    if request.method == 'POST':
        match account_verification(request.form['id'],
                                   request.form['password']):

            case 'doesNotExist':
                alert_message = "Sorry, your account does not exist, please create one."

            case 'wrongPassword':
                alert_message = "The password you entered is incorrect, please try again."

            case 'verified':
                session['id'] = request.form['id']
                session['password'] = request.form['password']
                return redirect('/')

    return templating.render_template("signin.html", message=alert_message)


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

        return redirect(url_for('signin'))

    return render_template('createaccount.html')


@app.route('/logout')
def logout():
    session.pop('id', None)
    session.pop('password', None)
    return redirect('/')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    create_table()
    user = get_user(session['id'])
    return render_template('profile.html', user=user)


@app.route('/events', methods=['GET', 'POST'])
def events():
    create_table()
    events = get_events()
    return render_template('events.html', events=events)


@app.route('events/<eventid>', methods=['GET', 'POST'])
def event(eventid):
    create_table()
    insert_reg(eventid, session['id'])
    event = get_event(eventid)
    return render_template('desc.html', event=event, eventid=eventid)


if __name__ == '__main__':
    app.run(debug=True)

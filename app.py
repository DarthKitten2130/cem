from flask import Flask, render_template, request, redirect, url_for, session, templating
from sql import *

app = Flask(__name__)
app.secret_key = 'ROOT'


@app.route('/')
def home():
    name = ""
    create_table()
    if 'id' in session:
        try:
            x = get_user(session['id'])
            name = x[1]
            session['dept'] = x[4]
            session['phone'] = x[3]
        except TypeError:
            pass
    session['name'] = name
    return render_template('index.html', name=name)


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


@app.route('/signout')
def signout():
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


@app.route('/events/<eventid>', methods=['GET', 'POST'])
def event(eventid):
    create_table()
    insert_reg(eventid, session['id'])
    event = get_event(eventid)
    return render_template('desc.html', event=event, eventid=eventid)


@app.route('/createevent', methods=['GET', 'POST'])
def create_event():
    create_table()
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        time = request.form['time']
        location = request.form['location']
        desc = request.form['description']
        eventtype = request.form['type']
        image = request.files['image']
        image.save('static/images/' + image.filename)
        insert_event(name, date, time, location, desc,
                     session['dept'], eventtype, session['phone'], f"images/{image.filename}")

        return redirect(url_for('events'))

    return render_template('createevent.html')


@app.route('/events/<eventid>/register', methods=['GET', 'POST'])
def register(eventid):
    insert_reg(eventid, session['id'])
    print(get_reg("1"))
    return render_template('reg.html')


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, session
from sql import *

app = Flask(__name__)
app.secret_key = 'ROOT'


@app.route('/')
def home():
    create_table()
    return render_template('home.html')


@app.route('/carshow')
def carshow():
    return render_template('carshow.html')


@app.route('/mng-ev')
def mng_ev():
    return render_template('mng-ev.html')


@app.route('/Hellskitchen')
def hellskitchen():
    return render_template('Hellskitchen.html')


@app.route('/wrkshp')
def wrkshp():
    return render_template('wrkshp.html')


@app.route('/tech-ev')
def tech_ev():
    return render_template('tech-ev.html')


@app.route('/Sponsor')
def sponsor():
    return render_template('Sponsor.html')


@app.route('/Team')
def team():
    return render_template('Team.html')


@app.route('/contact-us', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        id = session['id']
        message = request.form['message']
        insert_feedback(id, message)

    return render_template('contact-us.html')


@app.route('/SignIn', methods=['GET', 'POST'])
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

    return render_template("SignIn.html", message=alert_message)


@app.route('/CreateAcc', methods=['GET', 'POST'])
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

        return redirect('/SignIn')

    return render_template('CreateAcc.html')


@app.route('/event/<event_id>', methods=['GET', 'POST'])
def event(event_id):
    insert_reg(event_id, session['id'])

    return render_template('reg.html', event=event)


@app.route('/signout')
def signout():
    session.pop('id', None)
    session.pop('password', None)
    return redirect('/')


@app.route('/profile')
def profile():
    if 'id' in session:
        user = get_user(session['id'])
        return render_template('profile.html', user=user)
    else:
        return render_template('profile.html', user=None)


@app.route('/events')
def events():
    if 'id' in session:
        events = get_reg(session['id'])
        print(events)
        return render_template('events.html', events=events)
    else:
        return render_template('events.html', events=get_events())


if __name__ == '__main__':
    app.run(debug=True)

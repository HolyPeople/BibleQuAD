from flask import Flask, render_template, session, redirect, url_for, request
import secrets
import datetime

app = Flask(__name__)
app.secret_key = secrets.token_hex(64)


@app.route('/')
def index():
    if 'account' in session:
        return session['account'] + "login <a href='/logout'> logout </a>"
    return "Not login <a href='/login'>login </a>"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login-1.html',
                               authenticity_token=secrets.token_hex(16),
                               timestamp=int(datetime.datetime.now().timestamp()))
    else:
        account = request.form['account']
        password = request.form['password']
        authenticity_token = request.form['authenticity_token']
        timestamp = request.form['timestamp']
        print(account, password, authenticity_token, timestamp, "is Login")
        session['account'] = account
        return redirect(url_for('index'))
    pass


@app.route('/logout')
def logout():
    session.pop('account', None)
    return redirect(url_for("index"))


@app.route('/submit')
def submit():
    return render_template('submit.html', id_=1, outLine="우주창조", paragraph="여기에 문단이 들어갑니다.")


if __name__ == '__main__':
    app.run()

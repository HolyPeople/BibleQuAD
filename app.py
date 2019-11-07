from flask import Flask, render_template, session, redirect, url_for, request
import datetime
import bcrypt
from Model.AESCipher import AESCipher
from Service import Registeration

app = Flask(__name__)
key = open('.secret').readline()
aes = AESCipher(key)


@app.route('/')
def index():
    if 'account' in session:
        return session['account'] + "login <a href='/logout'> logout </a>"
    return "Not login <a href='/login'>login </a>"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login-1.html',
                               authenticity_token="",
                               timestamp=int(datetime.datetime.now().timestamp()))
    else:
        account = request.form['account']
        password = request.form['password']
        timestamp = request.form['timestamp']
        print(account, password, timestamp, "is Login")
        session['account'] = account
        return redirect(url_for('index'))
    pass


@app.route('/session')
def sessionControl():
    account = request.form['account']
    password = request.form['password']
    timestamp = request.form['timestamp']


@app.route('/logout')
def logout():
    session.pop('account', None)
    return redirect(url_for("index"))


@app.route('/submit')
def submit():
    return render_template('submit.html', id_=1, outLine="우주창조", paragraph="여기에 문단이 들어갑니다.")


@app.route('/join', methods=['POST'])
def join():
    name = aes.encrypt(request.form['name'])
    account = aes.encrypt(request.form['account'])
    password = bcrypt.hashpw(request.form['account'].encode('UTF-8'), bcrypt.gensalt()).hex()
    return Registeration.register(name, account, password)


if __name__ == '__main__':
    app.run()

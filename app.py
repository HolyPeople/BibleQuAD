from flask import Flask, render_template, session, redirect, url_for, request
import datetime
from Model.AESCipher import AESCipher
from Service import Auth

app = Flask(__name__)
app.secret_key = b'$2b$12$s62qTZXKnIAJxiTjw9QUcu'
key = open('.secret').readline()
aes = AESCipher(key)


@app.route('/')
def index():
    if 'uuid' in session:
        return session['uuid'] + " login <a href='/logout'> logout </a>"
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
        user = Auth.login(aes.encrypt(account), password)
        if user is None:
            return '가입하지 않은 아이디이거나, 잘못된 비밀번호입니다.'
        else:
            session['uuid'] = user.uuid
            return redirect(url_for('index'))


@app.route('/session')
def sessionControl():
    account = request.form['account']
    password = request.form['password']
    timestamp = request.form['timestamp']


@app.route('/logout')
def logout():
    session.pop('uuid', None)
    return redirect(url_for("index"))


# TODO: link to submit page
@app.route('/submit')
def submit():
    return render_template('submit.html', id_="창세기 1장 1절", outLine="우주창조", paragraph='''1 태초에 하나님이 천지를 창조하셨다.
2 땅이 혼돈하고 공허하며, 어둠이 깊음 위에 있고, 하나님의 영은 물 위에 움직이고 계셨다.
3 하나님이 말씀하시기를 "빛이 생겨라" 하시니, 빛이 생겼다.
4 그 빛이 하나님 보시기에 좋았다. 하나님이 빛과 어둠을 나누셔서,
5 빛을 낮이라고 하시고, 어둠을 밤이라고 하셨다. 저녁이 되고 아침이 되니, 하루가 지났다.
6 하나님이 말씀하시기를 "물 한가운데 창공이 생겨, 물과 물 사이가 갈라져라" 하셨다.''')


# TODO: link to registration page
@app.route('/join', methods=['POST'])
def join():
    name = request.form['name']
    account = request.form['account']
    password = request.form['password']
    return Auth.register(aes.encrypt(name), aes.encrypt(account), password)


if __name__ == '__main__':
    app.run()

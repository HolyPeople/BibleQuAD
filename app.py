from flask import Flask, render_template, session, redirect, url_for, request
import datetime
from Model.AESCipher import AESCipher
from Service import Auth
from Service import Bible

app = Flask(__name__)
app.templates_auto_reload = True
app.secret_key = b'$2b$12$s62qTZXKnIAJxiTjw9QUcu'
key = open('.secret').readline()
aes = AESCipher(key)


@app.route('/')
def index():
    if 'uuid' in session:
        return session['uuid'] + " login <a href='/logout'> logout </a>"
    return render_template('main.html')


@app.route('/description')
def description():
    return render_template('description.html')


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


@app.route('/submit')
def submit():
    return render_template('submit-10.html', data=Bible.getChapter())


@app.route('/join', methods=['POST'])
def join():
    name = request.form['name']
    account = request.form['account']
    password = request.form['password']
    return Auth.register(aes.encrypt(name), aes.encrypt(account), password)


@app.route('/auth-query', methods=['POST'])
def query():
    _key = request.form['key']
    _value = request.form['value']
    result = False
    if _key == 'name':
        result = Auth.is_exist(name=aes.encrypt(_value))
    elif _key == 'account':
        result = Auth.is_exist(account=aes.encrypt(_value))
    return {'result': result}


@app.route('/submit/paragraph')
def getParagraph():
    book = request.args['book']
    chapter = request.args['chapter']
    verse = request.args['verse']
    return Bible.getParagraph(book, chapter, verse)


if __name__ == '__main__':
    app.run()

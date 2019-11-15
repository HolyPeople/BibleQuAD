from flask import Flask, render_template, session, redirect, url_for, request, abort
import re, json
from Model.AESCipher import AESCipher
from Service import Auth, Bible, QATest, QASubmit

app = Flask(__name__)
app.templates_auto_reload = True
app.secret_key = b'$2b$12$s62qTZXKnIAJxiTjw9QUcu'
key = open('.secret').readline()
api_key = open('.apiKey').readline()
aes = AESCipher(key)


@app.route('/')
def index():
    if 'uuid' in session:
        return render_template('main.html', data={'uuid': session['uuid']}, btn='submit', n_qa=0)
    return render_template('main.html', data={'uuid': None}, btn='login', n_qa=0)

@app.route('/login')
def login():
    if 'uuid' in session:
        return redirect(url_for('index'))
    return render_template('login-1.html')


@app.route('/test')
def test():
    if 'uuid' in session:
        return render_template('test.html', bible=Bible.getChapter(), data={'uuid': session['uuid']})
    else:
        return redirect(url_for('login'))


@app.route('/test/answer')
def answer():
    paragraph = request.args['paragraph']
    question = request.args['question']
    return QATest.getQuery(accessKey=api_key, passage=paragraph, question=question)


@app.route('/session', methods=['POST', 'GET'])
def sessionControl():
    if 'uuid' in session:
        return redirect(url_for('index'))
    if request.method == 'GET':
        return redirect(url_for('login'))
    else:
        account = request.form['account']
        password = request.form['password']
        user = None
        if re.compile(r'^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$').match(
                account):
            user = Auth.loginByEmail(aes.encrypt(account), password)
        else:
            user = Auth.loginByUserName(aes.encrypt(account), password)

        if user is None:
            return render_template('login-1.html', validate='invalid')
        else:
            session['uuid'] = user.uuid
            return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('uuid', None)
    return redirect(url_for("index"))


@app.route('/submit')
def submit():
    if 'uuid' not in session:
        return redirect(url_for('login'))
    return render_template('submit-10.html', bible=Bible.getChapter(), data={'uuid': session['uuid']}, qa_list=None)


@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        name = request.form['name']
        account = request.form['account']
        password = request.form['password']
        if Auth.register(aes.encrypt(name), aes.encrypt(account), password) == 'SUCCESS':
            return redirect(url_for("index"))


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


@app.route('/submit/qa', methods=['GET', 'POST'])
def getQas():
    if 'uuid' not in session:
        return abort(403)
    if request.method == 'GET':
        paragraph_id = request.args['paragraph_id']
        print(paragraph_id)
        return "qas"
    else:
        return QASubmit.submitQA(json.loads(request.form['json']), session['uuid'])


if __name__ == '__main__':
    app.run()

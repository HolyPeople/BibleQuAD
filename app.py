from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/login')
def login():
    return render_template('login.html', authenticity_token="", timestamp="")


if __name__ == '__main__':
    app.run()

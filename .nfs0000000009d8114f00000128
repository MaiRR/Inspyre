from flask import Flask, render_template

import util.apis

app = Flask(__name__)

@app.route('/')
def index():
    word, definition = util.apis.definition_of_the_day()
    return render_template(
        'index.html',
        background=util.apis.image_of_the_day(),
        definition=definition,
        word=word,
    )

@app.route('/login')
def login():
    return render_template(
        'login.html',
    )

@app.route('/register')
def register():
    return render_template(
        'register.html',
    )

if __name__ == '__main__':
    app.debug = True
    app.run()


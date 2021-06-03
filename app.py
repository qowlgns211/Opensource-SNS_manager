from logging import debug
import os
from flask import Flask, render_template
from flask import request
from flask import redirect
from models import db
from models import Fcuser

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/info', methods=['GET', 'POST'])
def info():
    return render_template('main.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        userid = request.form.get('userid')
        useremail = request.form.get('useremail')
        password = request.form.get('password')
        re_password = request.form.get('re_password')
        print(password)
        fcuser = Fcuser()
        fcuser.password = password
        fcuser.userid = userid
        fcuser.useremail = useremail
        db.session.add(fcuser)
        db.session.commit()

        return redirect('/')


@app.route('/main')
def main():
    return render_template('main.html')


if __name__ == "__main__":

    basedir = os.path.abspath(os.path.dirname(__file__))
    dbfile = os.path.join(basedir, 'db.sqlite')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    db.app = app
    db.create_all()   #

    app.run(debug=True)

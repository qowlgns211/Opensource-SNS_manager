
from logging import debug
import os
from flask import Flask, render_template
from flask import request
from flask import redirect
from sqlalchemy.sql.elements import Null
from models import db
from models import Fcuser
from flask import session


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        userid = request.form['userid']
        password = request.form.get('password')

        fcuser = Fcuser.query.filter_by(userid=userid).first()
        if fcuser is not None:
            if fcuser.password == password:
                session['userid'] = userid
                return render_template('main.html', id=userid)
            else:
                a = "wrong"
                return render_template('index.html', answer=a)
        else:
            a = "wrong"
            return render_template('index.html', answer=a)


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

    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    db.init_app(app)
    db.app = app
    db.create_all()   #

    app.run(debug=True)

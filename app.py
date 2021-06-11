
from logging import debug
import os
from flask import Flask, render_template
from flask import request
from flask import redirect
from flask.helpers import url_for
from sqlalchemy.sql.elements import Null
from models import db
from models import Fcuser
from models import NContents
from models import DContents
from models import GContents
from flask import session


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        if 'userid' in session:
            userid = session['userid']
            return redirect(url_for('info'))
        return render_template('index.html')
    else:
        userid = request.form['userid']
        password = request.form.get('password')

        fcuser = Fcuser.query.filter_by(userid=userid).first()
        if fcuser is not None:
            if fcuser.password == password:
                session['userid'] = userid
                session['Nid'] = '미연동'
                session['Did'] = '미연동'
                session['Gid'] = '미연동'
                ncontents = NContents.query.filter_by(userid=userid).first()
                if ncontents is not None:
                    session['Nid'] = ncontents.Nid
                dcontents = DContents.query.filter_by(userid=userid).first()
                if dcontents is not None:
                    session['Did'] = dcontents.Did
                gcontents = GContents.query.filter_by(userid=userid).first()
                if gcontents is not None:
                    session['Gid'] = gcontents.Gid
                return render_template('main.html', userid=session['userid'], Nid=session['Nid'], Did=session['Did'], Gid=session['Gid'])
            else:
                a = "wrong"
                return render_template('index.html', answer=a)
        else:
            a = "wrong"
            return render_template('index.html', answer=a)


@app.route('/logout')
def logout():
    session.pop('userid', None)
    return redirect(url_for('index'))


@app.route('/info', methods=['GET', 'POST'])
def info():
    if 'userid' in session:
        return render_template('main.html', userid=session['userid'], Nid=session['Nid'], Did=session['Did'], Gid=session['Gid'])


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


@app.route('/Idinter', methods=['GET', 'POST'])
def Idinter():
    if request.method == 'GET':
        return render_template('Idinter.html', userid=session['userid'])
    else:
        usermailid = request.form.get('userid')
        usermailpw = request.form.get('password')
        usermailtype = request.form.get('type')
        if (usermailtype == 'Naver'):
            ncontents = NContents()
            ncontents.userid = session['userid']
            ncontents.Nid = usermailid
            session['Nid'] = usermailid
            ncontents.Npw = usermailpw
            db.session.add(ncontents)
            db.session.commit()
            return render_template('main.html', userid=session['userid'], Nid=session['Nid'], Did=session['Did'], Gid=session['Gid'])
        elif (usermailtype == 'Daum'):
            dcontents = DContents()
            dcontents.userid = session['userid']
            dcontents.Did = usermailid
            session['Did'] = usermailid
            dcontents.Dpw = usermailpw
            db.session.add(dcontents)
            db.session.commit()
            return render_template('main.html', userid=session['userid'], Nid=session['Nid'], Did=session['Did'], Gid=session['Gid'])
        elif (usermailtype == 'Google'):
            gcontents = GContents()
            gcontents.userid = session['userid']
            gcontents.Gid = usermailid
            session['Gid'] = usermailid
            gcontents.Gpw = usermailpw
            db.session.add(gcontents)
            db.session.commit()
            return render_template('main.html', userid=session['userid'], Gid=session['Gid'])


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
    db.create_all()

    app.run(debug=True)

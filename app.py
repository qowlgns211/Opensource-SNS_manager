
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
from nmail import nmail


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
                    session['Npw'] = ncontents.Npw
                dcontents = DContents.query.filter_by(userid=userid).first()
                if dcontents is not None:
                    session['Did'] = dcontents.Did
                    session['Dpw'] = dcontents.Dpw
                gcontents = GContents.query.filter_by(userid=userid).first()
                if gcontents is not None:
                    session['Gid'] = gcontents.Gid
                    session['Gpw'] = ncontents.Gpw
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
    session.pop('Nid', None)
    session.pop('Npw', None)
    session.pop('Did', None)
    session.pop('Dpw', None)
    session.pop('Gid', None)
    session.pop('Gpw', None)
    return redirect(url_for('index'))


@app.route('/info', methods=['GET', 'POST'])
def info():
    if request.method == 'GET':
        if 'userid' in session:

            return render_template('main.html', userid=session['userid'], Nid=session['Nid'], Did=session['Did'], Gid=session['Gid'])
        else:
            return render_template('main.html')
    else:
        if request.method == 'POST':
            ReplyConents = request.form.get('reply-contents')
            ReplyName = request.form.get('reply-name')
            ReplyEmail = request.form.get('reply-email')
            mailtype = request.form.get('mailtype')
            if mailtype == 'N':
                mailID = session['Nid']
                mailPW = session['Npw']
                mailadress = mailID + '@naver.com'
                nmail(mailID, mailPW, mailadress,
                      ReplyName, ReplyConents, ReplyEmail)
                return redirect(url_for('index'))

            elif mailtype == 'D':
                mailID = session['Did']
                mailPW = session['Dpw']
                return mailID + mailPW + ReplyConents
            else:
                mailID = session['Gid']
                mailPW = session['Gpw']
                return mailID + mailPW + ReplyConents


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
            session['Npw'] = usermailpw
            # Naver(usermailid, usermailpw)
            db.session.add(ncontents)
            db.session.commit()
            return redirect(url_for('info'))
            # return render_template('main.html', userid=session['userid'], Nid=session['Nid'], Did=session['Did'], Gid=session['Gid'])
        elif (usermailtype == 'Daum'):
            dcontents = DContents()
            dcontents.userid = session['userid']
            dcontents.Did = usermailid
            session['Did'] = usermailid
            dcontents.Dpw = usermailpw
            session['Dpw'] = usermailpw
            db.session.add(dcontents)
            db.session.commit()
            return redirect(url_for('info'))
            # return render_template('main.html', userid=session['userid'], Nid=session['Nid'], Did=session['Did'], Gid=session['Gid'])
        else:
            gcontents = GContents()
            gcontents.userid = session['userid']
            gcontents.Gid = usermailid
            session['Gid'] = usermailid
            gcontents.Gpw = usermailpw
            session['Gpw'] = usermailpw
            db.session.add(gcontents)
            db.session.commit()
            return redirect(url_for('info'))
            # return render_template('main.html', userid=session['userid'], Nid=session['Nid'], Did=session['Did'], Gid=session['Gid'])


@app.route('/IdDisinter', methods=['GET', 'POST'])
def IdDisinter():
    if request.method == 'GET':
        return render_template('IdDisinter.html', userid=session['userid'])
    else:
        mailtype_un = request.form.get('mailtype_un')
        if (mailtype_un == 'N'):
            delmail = NContents.query.filter_by(
                userid=session['userid']).first()
            db.session.delete(delmail)
            session.pop('Nid', None)
            session.pop('Npw', None)
            session['Nid'] = '미연동'
            db.session.commit()
            return redirect(url_for('info'))
        elif (mailtype_un == 'D'):
            delmail = DContents.query.filter_by(
                userid=session['userid']).first()
            db.session.delete(delmail)
            session.pop('Did', None)
            session.pop('Dpw', None)
            session['Did'] = '미연동'
            db.session.commit()
            return redirect(url_for('info'))
        elif (mailtype_un == 'G'):
            delmail = GContents.query.filter_by(
                userid=session['userid']).first()
            db.session.delete(delmail)
            session.pop('Gid', None)
            session.pop('Gpw', None)
            session['Gid'] = '미연동'
            db.session.commit()
            return redirect(url_for('info'))


@app.route('/main')
def main():
    return render_template('Idinter.html', userid=session['userid'])


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

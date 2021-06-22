
from logging import debug
import logging
import os
import pathlib
import google.auth.transport.requests
import requests

from flask import Flask, render_template, abort, request, redirect, session
from flask.helpers import url_for
from sqlalchemy.sql.elements import Null
from models import db
from models import Fcuser
from models import NContents, DContents, GContents
from nmail import nmail
from quickstart import quick
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from pip._vendor import cachecontrol



app = Flask(__name__)

app.secret_key = "temp"
SCOPES = ['https://mail.google.com/']

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "733571866823-p3hiu53f9lqgb85h73k2crr3cf5ndtas.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "credentials.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
                             )

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401) # Authorization required
        else:
            return function()

    return wrapper

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
                logging.warning("Login successful")
                session['userid'] = userid
                session['Nid'] = '미연동'
                session['Did'] = '미연동'
                session['Gid'] = '미연동'
                ncontents = NContents.query.filter_by(userid=userid).first()
                if ncontents is not None:
                    logging.warning(ncontents)
                    logging.warning("Get Naver ID")
                    session['Nid'] = ncontents.Nid
                    session['Npw'] = ncontents.Npw
                dcontents = DContents.query.filter_by(userid=userid).first()
                if dcontents is not None:                    
                    logging.warning(dcontents)
                    logging.warning("get Daum ID")
                    session['Did'] = dcontents.Did
                    session['Dpw'] = dcontents.Dpw
                gcontents = GContents.query.filter_by(userid=userid).first()
                if gcontents is not None:
                    logging.warning(gcontents.Gid)
                    logging.warning("get Google ID")
                    session['Gid'] = gcontents.Gid  
                return redirect("/")
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
    session.clear()
    os.remove("token.json")
    return redirect(url_for('index'))


@app.route('/info', methods=['GET', 'POST'])
def info():
    if request.method == 'GET':
        if 'userid' in session:
            logging.warning("info session clear")
            userid = session['userid']
            gcontents = GContents.query.filter_by(userid=userid).first()
            if gcontents is not None:
                logging.warning(gcontents.Gid)
                logging.warning("get Google ID")
                session['Gid'] = gcontents.Gid  
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
                return redirect("/")


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
            logging.warning("G Idinter")
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

##################################Google Login START###############################################

@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500) # State does not match

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    
    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["email"] = id_info.get("email")
    session["email_verified"] = id_info.get("email_verified")


    logging.warning(session["google_id"])
    logging.warning(session["name"])
    logging.warning(session["email"])
    logging.warning(session["email_verified"])

    gcontents = GContents() 
    gcontents.userid = session["userid"]
    gcontents.Gid = session["email"]
    db.session.add(gcontents)
    db.session.commit()
    logging.warning("commit completed")
    logging.warning(gcontents.Gid)

    return redirect("/protected_area")

@app.route("/protected_area")
@login_is_required
def protected_area():
    return redirect("/quickstart")

@app.route("/quickstart")
def quickstart():
    quick()
    return redirect("/")

##################################Google Login END###########################################



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


from logging import debug
import logging
import os
import pathlib
import google.auth.transport.requests
import requests
import pyperclip
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
from mail import googlemail
from daummail import mail
from flask import json

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

N_person = []
N_address = []
N_title = []

D_person = []
D_title = []
D_address = []


Gdic = {}


def Daum(id_input, pwd_input):

    # 각각의 정보 리스트

    # 로그인 하는 과정

    driver = webdriver.Chrome('./chromedriver.exe')
    driver.get('https://mail.daum.net/')
    driver.find_element_by_xpath(
        '//*[@id="daumHead"]/div/div/a[4]/span').click()
    driver.find_element_by_xpath(
        '//*[@id="mArticle"]/div[1]/div/div/div[2]/a[2]').click()
    driver.find_element_by_name('id').send_keys(id_input)
    sleep(0.5)
    driver.find_element_by_name('pw').send_keys(pwd_input)
    sleep(0.5)
    driver.find_element_by_xpath('//*[@id="loginBtn"]').click()
    sleep(0.5)

    # 메일 안의 내용 받아오기

    driver.get('https://mail.daum.net/')
    print(driver.page_source)

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    mails = soup.select('#mailList > div.scroll > div > ul > li')

    for mail in mails:
        Person = mail.select_one('div.info_from > a')['title']
        Title = mail.select_one('div > a > strong').text
        Address = mail.select_one('div.info_subject > a')['href']
        D_person.append(Person)
        D_title.append(Title)
        D_address.append('https://mail.daum.net/' + Address)

    # 드라이버 종료
    driver.quit()


def Naver(id_input, pwd_input):
    # 전체 리스트 변수

    # 옵션 생성
    options = webdriver.ChromeOptions()

    options.add_argument("headless")
    options.add_argument('window-size=1920x1080')
    options.add_argument('disable-gpu')
    options.add_argument("lang=ko_KR")

    # 드라이버 실행시키기
    driver = webdriver.Chrome(
        './chromedriver.exe', options=options)
    sleep(0.5)

    driver.get('https://mail.naver.com')

    # 아이디 패스워드 자동 입력화 부분
    driver.find_element_by_name('id').click()
    pyperclip.copy(id_input)
    driver.find_element_by_name('id').send_keys(Keys.CONTROL, 'v')
    sleep(0.5)
    driver.find_element_by_name('pw').click()
    pyperclip.copy(pwd_input)
    driver.find_element_by_name('pw').send_keys(Keys.CONTROL, 'v')
    sleep(0.5)

    # 로그인 버튼 클릭 자동화
    driver.find_element_by_id('log.login').click()

    # Web 브라우저 받아오기.
    driver.get("https://mail.naver.com/")
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    # 보낸 사람 person, 내용 주솟값 각각의 리스트에 포함.
    mails = soup.select('#list_for_view > ol > li')

    for mail in mails:
        Person = mail.select_one('div > div > a')['title']
        Address = mail.select_one('div > div.subject > a')['href']
        global N_person
        global N_address

        print(Person)
        print(Address)
        N_person.append(Person)
        N_address.append("https://mail.naver.com/" + Address)

    # 메일 제목 title 딕셔너리에 포함.
    maillist = soup.find_all('strong', 'mail_title')

    for b in maillist:
        global N_title
        N_title.append(b.text)

    # 드라이버 종료
    driver.quit()


app = Flask(__name__)

app.secret_key = "temp"
SCOPES = ['https://mail.google.com/']

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "733571866823-p3hiu53f9lqgb85h73k2crr3cf5ndtas.apps.googleusercontent.com"
client_secrets_file = os.path.join(
    pathlib.Path(__file__).parent, "credentials.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
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
                    Naver(session['Nid'], session['Npw'])
                dcontents = DContents.query.filter_by(userid=userid).first()
                if dcontents is not None:
                    logging.warning(dcontents)
                    logging.warning("get Daum ID")
                    session['Did'] = dcontents.Did
                    session['Dpw'] = dcontents.Dpw
                    Daum(session['Did'], session['Dpw'])
                gcontents = GContents.query.filter_by(userid=userid).first()
                if gcontents is not None:
                    logging.warning(gcontents.Gid)
                    logging.warning("get Google ID")
                    session['Gid'] = gcontents.Gid
                return redirect("/info", Ndic=Ndic)
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
    if os.path.isfile("token.json"):
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
            return render_template('main.html', userid=session['userid'], Nid=session['Nid'], Did=session['Did'], N_person=N_person, N_address=N_address, N_title=N_title, Gid=session['Gid'], Gdic=Gdic)
        else:
            return render_template('main.html',  userid=session['userid'], Nid=session['Nid'], Did=session['Did'], N_person=N_person, N_address=N_address, N_title=N_title, Ddic=Ddic)
    else:
        if request.method == 'POST':
            mailtype = request.form.get('mailtype')
            if mailtype == 'N':
                ReplyConents = request.form.get('reply-contents')
                ReplyName = request.form.get('reply-name')
                ReplyEmail = request.form.get('reply-email')

                mailID = session['Nid']
                mailPW = session['Npw']
                mailadress = mailID + '@naver.com'
                nmail(mailID, mailPW, mailadress,
                      ReplyName, ReplyConents, ReplyEmail)
                return redirect(url_for('index'))

            elif mailtype == 'D':
                ReplyConents = request.form.get('reply-contents')
                ReplyName = request.form.get('reply-name')
                ReplyEmail = request.form.get('reply-email')

                mailID = session['Did']
                mailPW = session['Dpw']
                mailadress = mailID + '@daum.com'
                mail(ReplyEmail, mailadress, ReplyName, ReplyConents, mailPW)
                return redirect(url_for('index'))
            else:
                ReplyConents = request.form.get('reply-contents')
                ReplyName = request.form.get('reply-name')
                ReplyEmail = request.form.get('reply-email')

                mailID = session['Gid']
                mailPW = request.form.get('reply-Gpw')
                mailadress = mailID
                googlemail(mailadress, ReplyEmail,
                           ReplyName, ReplyConents, mailPW)
                return redirect(url_for('index'))


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

            Naver(usermailid, usermailpw)
            ncontents = NContents()
            ncontents.userid = session['userid']
            ncontents.Nid = usermailid
            ncontents.Npw = usermailpw
            session['Nid'] = usermailid
            session['Npw'] = usermailpw
            # Naver(usermailid, usermailpw)
            db.session.add(ncontents)
            db.session.commit()

            return redirect(url_for('info'))
            # return render_template('main.html', userid=session['userid'], Nid=session['Nid'], Did=session['Did'], Gid=session['Gid'])
        elif (usermailtype == 'Daum'):
            Daum(usermailid, usermailpw)
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
        abort(500)  # State does not match

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(
        session=cached_session)

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
    global Gdic
    Gdic = quick()
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

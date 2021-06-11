from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Fcuser(db.Model):
    __tablename__ = 'fcuser'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(64))
    userid = db.Column(db.String(32))
    useremail = db.Column(db.String(32))


class NContents(db.Model):
    __tablename__ = 'ncontents'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(32))
    Nid = db.Column(db.String(32))
    Npw = db.Column(db.String(32))


class DContents(db.Model):
    __tablename__ = 'dcontents'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(32))
    Did = db.Column(db.String(32))
    Dpw = db.Column(db.String(32))


class GContents(db.Model):
    __tablename__ = 'gcontents'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(32))
    Gid = db.Column(db.String(32))
    Gpw = db.Column(db.String(32))

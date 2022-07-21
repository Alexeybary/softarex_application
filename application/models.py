from flask_sqlalchemy import SQLAlchemy
from application import login,db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'info_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    password=db.Column(db.String())

    def __init__(self, name,psw):
        self.name = name
        self.password=psw

    def __repr__(self):
        return f"{self.name}"

    def check_password(self, password):
        return self.password == password
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
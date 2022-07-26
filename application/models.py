from flask_sqlalchemy import SQLAlchemy
from application import login,db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'info_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    password=db.Column(db.String())
    count_of_dimension=db.Column(db.Integer,default=0)

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
class Dimension(db.Model):
    __tablename__ ='dimension'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    dimension=db.Column(db.String())
    dimension_name=db.Column(db.String())
    def __int__(self,name,dimension,dimension_name):
        self.name=name
        self.dimension=dimension
        self.dimension_name=dimension_name
    def __repr__(self):
        return f"{self.name}"



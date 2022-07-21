from flask import Flask, Config
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = 'new_password'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:new_password@localhost:5432/flask_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)
login = LoginManager(app)
from application import routes, models
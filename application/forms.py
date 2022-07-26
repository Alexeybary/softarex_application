import csv

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Submit')

class DimensionForm(FlaskForm):
    dimension= StringField('Dimension', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ValidateFile(object):
    def __call__(self, value):
        if value is None:    # do something when None
            return None
class UploadForm(FlaskForm):
    file = FileField('File')
    dimension_name= StringField('Dimension_name', validators=[DataRequired()])
    upload = SubmitField('upload')

class DeleteForm(FlaskForm):
    delete = SubmitField('delete')

class Download_pdf(FlaskForm):
        save_pdf = SubmitField('save_pdf')

class Download_json(FlaskForm):
    save_json=SubmitField('save_json')

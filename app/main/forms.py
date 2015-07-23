from flask.ext.wtf import Form
from wtforms import SubmitField, PasswordField, StringField, BooleanField, SelectField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, regexp


class NameForm(Form):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class UploadForm(Form):
    datafiles = StringField('Upload Files')
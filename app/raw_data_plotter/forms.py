from flask.ext.wtf import Form
from wtforms import SubmitField, PasswordField, StringField, BooleanField, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Email, EqualTo, Regexp, Length, NumberRange


class RawDataForm(Form):

    loggers = QuerySelectField(label='Select A Logger', get_label='serial')
    sensors = QuerySelectField(label='Select A Sensor', get_label='description')
    month = StringField(label='Enter Month') #, validators=[DataRequired(), NumberRange(1, 12,
                                              #                                       message='Enter a value from 1-12')])
    submit = SubmitField('Submit')

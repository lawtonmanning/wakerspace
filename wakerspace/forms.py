import re
from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, InputRequired
from wakerspace.models import Maker

class IDForm(FlaskForm):
    integer = StringField('pincode', [DataRequired()])

    def __init__(self, length):
        super().__init__()
        self.length = length

    def validate_integer(self, integer):
        if len(integer.data) != self.length:
            raise ValidationError("ID must be {} digits long".format(self.length))
        elif re.match(r'[0-9]+', integer.data) is None:
            raise ValidationError("ID must only include numbers")


class MakerForm(FlaskForm):
    first_name = StringField('First Name', [DataRequired()])
    last_name = StringField('Last Name', [DataRequired()])
    classification = SelectField('Classification', [DataRequired()], choices=Maker.Classification.choices())
    year = SelectField('Year', choices=Maker.Year.choices())
    staff = BooleanField('Staff')

class EditMakerForm(FlaskForm):
    in_out = SubmitField('in/out')


class CheckInForm(FlaskForm):
    purpose = SelectField('Purpose', [InputRequired()], coerce=int)
    submit = SubmitField('Check-In')

class TrainingsForm(FlaskForm):
    trainings = SelectField('Training', [DataRequired()], choices=[], coerce=int)
    submit = SubmitField('Submit')

import re
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError

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
    first_name = StringField('First Name')
    last_name = StringField('Last Name')


class EditMakerForm(FlaskForm):
    in_out = SubmitField('in/out')

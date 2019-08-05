from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import ValidationError

class IDForm(FlaskForm):
    integer = IntegerField('pincode')

    def __init__(self, length):
        super().__init__()
        self.length = length

    def validate_integer(self, integer):
        padded = '{{:0{}d}}'.format(self.length)
        if len(padded.format(integer.data)) != self.length:
            raise ValidationError("ID must be {} digits long".format(self.length))


class MakerForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')


class EditMakerForm(FlaskForm):
    in_out = SubmitField('in/out')

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    profile_pic = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png']), DataRequired()])
    submit = SubmitField('Register')

class AddStairsForm(FlaskForm):
    stairs_climbed = IntegerField('Levels Climbed', validators=[DataRequired()])
    submit = SubmitField('Log')

from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import Length,DataRequired,ValidationError
from flask_wtf.file import FileField,FileRequired,FileAllowed
from webapp.models import User


class RegisterForm(FlaskForm):
    fullname = StringField('Fullname',validators=[Length(min=6),DataRequired()])
    position = StringField('Position',validators=[DataRequired()])
    department = StringField('Department',validators=[DataRequired()])
    submit = SubmitField(label="Register")

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField(False)
    submit = SubmitField(label="Login")

class SignupForm(FlaskForm):

    # Flask form will check for any functions that contains validate as prefix
    # We are using .data because it replicates how we access data from a Flask Form
    def validate_username(self,provided_user):
        user = User.query.filter_by(username=provided_user.data).first()

        if user:
            raise ValidationError("Username already exists")

    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField(label="Sign Up")

    
class UploadForm(FlaskForm):
    # pickle = FileField('Pickle', validators=[FileRequired(), FileAllowed(['pkl'], 'Pickle Files only!')])
    new_data = FileField('Data', validators=[FileRequired(), FileAllowed(['csv'])])
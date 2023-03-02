from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField , PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.db_models.User import User

class LoginForm(FlaskForm):
    email = StringField("Email" , [DataRequired(),Email()])
    password = PasswordField("Password" , [DataRequired()])
    remember = BooleanField('Remember')
    submit = SubmitField('Log IN')


class RegistrationForm(FlaskForm):
    name = StringField("Name" , [DataRequired()])
    email = StringField("Email" , [DataRequired()])
    password = PasswordField("Password" , [DataRequired()])
    repeated_password = PasswordField("Repeat password" , [EqualTo('password', "Passwords must match.")])
    submit = SubmitField('Register')

    def check_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is taken')
        
class AddCategoryForm(FlaskForm):
    name = StringField("Name", [DataRequired(),Length(max=50)],)
    submit = SubmitField('Submit')

class AddNoteForm(FlaskForm):
    name = StringField("Name", [DataRequired()])
    text = StringField("Text", [DataRequired()])
    picture = FileField('Add Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post')


class SearchForm(FlaskForm):
    searched = StringField("Searched", [DataRequired()])
    submit = SubmitField('Submit')

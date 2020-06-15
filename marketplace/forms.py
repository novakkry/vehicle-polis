from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from marketplace.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = RadioField('I want to', choices=[('buyer','buy only (buyer)'),('seller','buy and sell (seller)')], default='buyer')
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already used.')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('This email is already registered. Consider logging in.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    remember = BooleanField('Remember Me')

class PostForm(FlaskForm):
    condition = RadioField('Condition', choices=[('New','New'),('Used','Used'),('Salvaged','Salvaged')], default='New')
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=40)])
    make = SelectField('Make',validators=[DataRequired()], choices=[('Alfa Romeo', 'Alfa Romeo'), ('Audi', 'Audi'), ('BMW', 'BMW'), ('Chevrolete', 'Chevrolet'), ('Citroen', 'Citroen'), ('Fiat', 'Fiat'), ('Ford', 'Ford'), ('Honda', 'Honda'), ('Hyundai', 'Hyundai'), ('Kia', 'Kia'), ('Mazda', 'Mazda'), ('Mercedes', 'Mercedes'), ('Mitsubishi', 'Mitsubishi'), ('Nissan', 'Nissan'), ('Opel', 'Opel'), ('Peugeot', 'Peugeot'), ('Renault', 'Renault'), ('Seat', 'Seat'), ('Skoda', 'Skoda'), ('Subaru', 'Subaru'), ('Suzuki', 'Suzuki'), ('Toyota', 'Toyota'), ('Volkswagen', 'Volkswagen'), ('Volvo', 'Volvo')])
    model = StringField('Model', validators=[DataRequired(), Length(min=1, max=20)])
    price = IntegerField('Price', validators=[DataRequired('This field has to be a number and is required.')])
    year = IntegerField('Year', validators=[DataRequired('This field has to be a number and is required.')])
    ODO = IntegerField('ODO (km)', validators=[DataRequired('This field has to be a number with no spaces and is required.')])
    category = SelectField('Category',validators=[DataRequired()], choices=[('Hatchbag', 'Hatchbag'), ('Sedan', 'Sedan'), ('MUV/SUV', 'MUV/SUV'), ('Coupe', 'Coupe'), ('Convertible', 'Convertible'), ('Wagon', 'Wagon'), ('Van', 'Van'), ('Sport', 'Sport')])
    fuel = SelectField('Fuel type',validators=[DataRequired()], choices=[('Gas', 'Gas'), ('Diesel', 'Diesel'), ('Electric', 'Electric')])
    transmission = SelectField('Transmission type',validators=[DataRequired()], choices=[('Automatic', 'Automatic'), ('Manual', 'Manual')])
    quantity = IntegerField('Quantity', validators=[DataRequired('This field has to be a number and is required.')])
    description = TextAreaField('Description')
    picture = FileField('Upload a picture (.png, .jpg)', validators=[FileAllowed(['png', 'jpg'])])
    submit = SubmitField('Post vehicle')
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, TextAreaField, IntegerField, SelectField, DateTimeField,validators
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from marketplace.models import User
from datetime import datetime

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    contact_number = StringField('Contact number', validators=[DataRequired(), Length(min=2, max=20)])
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
    title = StringField('Title of your ad', validators=[DataRequired(), Length(min=3, max=40)])
    make = SelectField('Make',validators=[DataRequired()], choices=[('', 'Select car make'),('Alfa Romeo', 'Alfa Romeo'), ('Audi', 'Audi'), ('BMW', 'BMW'), ('Chevrolete', 'Chevrolet'), ('Citroen', 'Citroen'), ('Fiat', 'Fiat'), ('Ford', 'Ford'), ('Honda', 'Honda'), ('Hyundai', 'Hyundai'), ('Kia', 'Kia'), ('Mazda', 'Mazda'), ('Mercedes', 'Mercedes'), ('Mitsubishi', 'Mitsubishi'), ('Nissan', 'Nissan'), ('Opel', 'Opel'), ('Peugeot', 'Peugeot'), ('Renault', 'Renault'), ('Seat', 'Seat'), ('Skoda', 'Skoda'), ('Subaru', 'Subaru'), ('Suzuki', 'Suzuki'), ('Toyota', 'Toyota'), ('Volkswagen', 'Volkswagen'), ('Volvo', 'Volvo')])
    model = StringField('Model', validators=[DataRequired(), Length(min=1, max=20)])
    price = IntegerField('Price', validators=[DataRequired('This field has to be a number and is required.')])
    year = IntegerField('Year', validators=[DataRequired('This field has to be a number and is required.'), NumberRange(min=1900, max=2020)])
    ODO = IntegerField('ODO (km)', validators=[DataRequired('This field has to be a number with no spaces and is required.')])
    category = SelectField('Category',validators=[DataRequired()], choices=[('', 'Select category'),('Hatchbag', 'Hatchbag'), ('Sedan', 'Sedan'), ('MUV/SUV', 'MUV/SUV'), ('Coupe', 'Coupe'), ('Convertible', 'Convertible'), ('Wagon', 'Wagon'), ('Van', 'Van'), ('Sport', 'Sport')])
    fuel = SelectField('Fuel type',validators=[DataRequired()], choices=[('', 'Select fuel type'),('Gas', 'Gas'), ('Diesel', 'Diesel'), ('Electric', 'Electric')])
    transmission = SelectField('Transmission type',validators=[DataRequired()], choices=[('', 'Select transmission type'),('Automatic', 'Automatic'), ('Manual', 'Manual')])
    quantity = IntegerField('Quantity', validators=[DataRequired('This field has to be a number and is required.')])
    description = TextAreaField('Description')
    picture = FileField('Upload a picture (.png, .jpg)', validators=[FileAllowed(['png', 'jpg'])])
    submit = SubmitField('Post vehicle')

class OrderForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired('This field has to be a positive number and is required.')])
    first_name = StringField('First name', validators=[DataRequired(), Length(min=2, max=40)])
    last_name = StringField('Last name', validators=[DataRequired(), Length(min=2, max=60)])
    company_name = StringField('Company name', validators=[Length(max=100)])
    address1 = StringField('Address 1', validators=[DataRequired(), Length(min=2, max=100)])
    address2 = StringField('Address 2')
    suburb = StringField('Suburb', validators=[DataRequired(), Length(min=2, max=100)])
    city = StringField('City', validators=[DataRequired(), Length(min=2, max=100)])
    state = StringField('State', validators=[DataRequired(), Length(min=2, max=100)])
    country = SelectField('Country',validators=[DataRequired('Please select your country')], choices=[('', 'Select country'),('Australia', 'Australia')])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Length(min=2, max=100), Email()])
    date_posted = DateTimeField('Date and time', default=datetime.now)
    submit = SubmitField('Submit order')

class SearchForm(FlaskForm):
    text = StringField('Search')
    submit = SubmitField('Search')

class ReviewForm(FlaskForm):
    ranking = SelectField('Rate it',validators=[DataRequired()], choices=[('', 'Rate vehicle'),('★★★★★', '★★★★★'),('★★★★☆', '★★★★☆'),('★★★☆☆', '★★★☆☆'),('★★☆☆☆', '★★☆☆☆'),('★☆☆☆☆', '★☆☆☆☆')])
    content = TextAreaField('Description')
    submit = SubmitField('Post review')

class HomeSearchForm(FlaskForm):
    price_from = IntegerField('Price from', [validators.optional()])
    price_to = IntegerField('Price to', [validators.optional()])
    year_from = IntegerField('Year from', [validators.optional()])
    year_to = IntegerField('Year to', [validators.optional()])
    odo_from = IntegerField('ODO (km) min', [validators.optional()])
    odo_to = IntegerField('ODO (km) max', [validators.optional()])
    transmission = SelectField('Transmission type', choices=[('', 'All transmission types'),('Automatic', 'Automatic'), ('Manual', 'Manual')])
    category = SelectField('Category', choices=[('', 'All categories'),('Hatchbag', 'Hatchbag'), ('Sedan', 'Sedan'), ('MUV/SUV', 'MUV/SUV'), ('Coupe', 'Coupe'), ('Convertible', 'Convertible'), ('Wagon', 'Wagon'), ('Van', 'Van'), ('Sport', 'Sport')])
    fuel = SelectField('Fuel type', choices=[('', 'All fuel types'),('Gas', 'Gas'), ('Diesel', 'Diesel'), ('Electric', 'Electric')])
    submit2 = SubmitField('Search vehicles')

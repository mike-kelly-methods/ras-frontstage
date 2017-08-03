"""
This module contains the data model for the application
"""
import logging

import phonenumbers
from flask_wtf import FlaskForm
from phonenumbers.phonenumberutil import NumberParseException
from structlog import wrap_logger
from wtforms import HiddenField, PasswordField, StringField
from wtforms.validators import InputRequired, EqualTo, Length, DataRequired, Email, ValidationError

from frontstage import app

# db = SQLAlchemy()

logger = wrap_logger(logging.getLogger(__name__))


# class User(db.Model):
#     """User model."""
#
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     username = Column(String(100))
#     pwdhash = Column(String())
#     token = Column(String())
#     token_created_on = Column(DateTime)
#     token_duration = Column(Integer)
#     created_on = Column(DateTime, default=datetime.datetime.utcnow)
#
#     def __init__(self, username, password, token, token_created_on, token_duration, id=None):
#         """Init method."""
#         self.id = id
#         self.username = username
#         self.pwdhash = generate_password_hash(password)
#         self.token = token
#         self.token_created_on = token_created_on
#         self.token_duration = token_duration
#
#     def check_password(self, password):
#         """Method to check password validity."""
#         return check_password_hash(self.pwdhash, password)
#
#     def check_password_simple(self, password):
#         """Check password simplicity."""
#         if password == self.pwdhash:
#             logger.debug("Password checks out. Password in {}, password I have: {}".format(password, self.pwdhash))
#             return True
#         return False
#
#
# class UserScope(db.Model):
#     """Userscope model."""
#
#     __tablename__ = 'user_scopes'
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer)
#     scope = Column(String(100))
#     created_on = Column(DateTime, default=datetime.datetime.utcnow)
#
#     def __init__(self, user_id, scope, id=None):
#         """Init method."""
#         self.id = id
#         self.user_id = user_id
#         self.scope = scope


class EnrolmentCodeForm(FlaskForm):
    """
    This is our Register form and part 1 of registration. It's used for the user to pass the 'Activation Code'. The
    activation code will be sent to the party service, in turn get resolved in the 'case service'. If successful we can
    progress with registration. The 'Activation Code' is a string in our case.
    """
    enrolment_code = StringField('Enrolment Code', [InputRequired()])


class RegistrationForm(FlaskForm):
    """
    Registration form.
    This is our Register form and part 3 of registration. It allows the user to pass all details to create an account.
    The form data will be used to create the account on the OAuth2 server and to provide the Case Service with a valid
    account name that is not verified.
    """
    first_name = StringField('First name',
                             validators=[InputRequired("First name is required"),
                                         Length(max=254,
                                                message='Your first name must be less than 254 characters')])
    last_name = StringField('Last name',
                            validators=[InputRequired("Last name is required"),
                                        Length(max=254, message='Your last name must be less than 254 characters')])
    email_address = StringField('Enter your email address',
                                validators=[InputRequired("Email address is required"),
                                            Email(message="Your email should be of the form 'myname@email.com' "),
                                            Length(max=254,
                                                   message='Your email must be less than 254 characters')])
    password = PasswordField('Create a password',
                             validators=[DataRequired("Password is required"),
                                         EqualTo('password_confirm', message=app.config['PASSWORD_MATCH_ERROR_TEXT']),
                                         Length(min=app.config['PASSWORD_MIN_LENGTH'],
                                                max=app.config['PASSWORD_MAX_LENGTH'],
                                                message=app.config['PASSWORD_CRITERIA_ERROR_TEXT'])])
    password_confirm = PasswordField('Re-type your password')
    phone_number = StringField('Enter your phone number',
                               validators=[DataRequired("Phone number is required"),
                                           Length(min=9,
                                                  max=15,
                                                  message="This should be a valid phone number between 9 and 15 digits")],
                               default=None)
    enrolment_code = HiddenField('Enrolment Code')

    def validate_phone_number(form, field):
        try:
            logger.debug("Checking this is a valid GB Number")
            input_number = phonenumbers.parse(field.data, "GB")  # Tell the parser we are looking for a GB number

            if not (phonenumbers.is_possible_number(input_number)):
                raise ValidationError('This should be a valid phone number between 9 and 15 digits')

            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Please use a valid UK number e.g. 01632 496 0018.')
        except NumberParseException:
            logger.debug(" There is a number parse exception in the phonenumber field")
            raise ValidationError('This should be a valid UK number e.g. 01632 496 0018. ')

    def validate_password(form, field):
        password = field.data
        if password.isalnum() or \
            not any(char.isupper() for char in password) or \
                not any(char.isdigit() for char in password):
                    raise ValidationError(app.config['PASSWORD_CRITERIA_ERROR_TEXT'])


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Email Address', [InputRequired("Email Address is required"),
                                             Email("Your email should be of the form 'myname@email.com' ")])
    password = PasswordField('Password', [InputRequired("Password is required")])


class EnrolmentCodeForm(FlaskForm):
    """
    This is our Register form and part 1 of registration. It's used for the user to pass the 'Activation Code'. The
    activation code will be sent to the party service, in turn get resolved in the 'case service'. If successful we can
    progress with registration. The 'Activation Code' is a string in our case.
    """
    enrolment_code = StringField('Enrolment Code', [InputRequired()])


class ForgotPasswordForm(FlaskForm):
    """
    Forgot Password form.
    """
    email_address = StringField('Enter your email address',
                                validators=[InputRequired("Email address is required"),
                                            Email(message="Your email should be of the form 'myname@email.com' "),
                                            Length(max=254,
                                                   message='Your email must be less than 254 characters')])

class ResetPasswordForm(FlaskForm):
    """
    Reset Password form.
    """
    password = PasswordField('New password',
                             validators=[DataRequired("Password is required"),
                                         EqualTo('password_confirm', message=app.config['PASSWORD_MATCH_ERROR_TEXT']),
                                         Length(min=app.config['PASSWORD_MIN_LENGTH'],
                                                max=app.config['PASSWORD_MAX_LENGTH'],
                                                message=app.config['PASSWORD_CRITERIA_ERROR_TEXT'])])
    password_confirm = PasswordField('Re-type new password')
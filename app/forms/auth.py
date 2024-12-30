# Flask modules
from flask_wtf import FlaskForm
from wtforms.validators import ValidationError
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp
from flask import flash
# Local modules
from app.models.user_model import User


class LoginForm(FlaskForm):
    email = StringField(
        "Email address",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "example@email.com"},
    )
    password = PasswordField(
        "Password", validators=[DataRequired()], render_kw={"placeholder": "********"}
    )
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            DataRequired(),
            Length(min=2, max=80),
            Regexp(
                r"^[a-zA-Z0-9_]+$",
                message="Name must contain only letters, numbers, and underscores.",
            ),
        ],
        render_kw={"placeholder": "Display name"},
    )
    email = StringField(
        "Email address",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "example@email.com"},
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8),
        ],
        render_kw={"placeholder": "Enter your password"},
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match"),
        ],
        render_kw={"placeholder": "Confirm your password"},
    )
    submit = SubmitField("Register")

    def validate_email(self, email):
        """
        Validate an email address.

        Parameters:
            email (str): The email address to be validated.

        Raises:
            ValidationError: If the email address is invalid or already registered.

        Returns:
            None
        """
        # Check if email already exists
        existing_user = User.query.filter_by(email=email.data).one_or_none()
        if existing_user:            
            raise ValidationError("Email address already registered.")
        
        # Validate email domain
        email_parts = email.data.split('@')
        if len(email_parts) != 2:
            raise ValidationError("Invalid email format.")
        
        # Basic email format validation
        import re
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email.data):
            raise ValidationError("Invalid email format.")

    def validate_password(self, password):
        """
        Validates a password.

        Parameters:
            self (object): The instance of the class.
            password (str): The password to be validated.

        Raises:
            ValidationError: If the password does not contain at least one letter and one digit.
        """
        if len(password.data) < 6:
            raise ValidationError("Password must be at least 6 characters long.")
        
        if not any(c.isalpha() for c in password.data) or not any(
            c.isdigit() for c in password.data
        ):
            raise ValidationError(
                "Password must contain at least one letter and one digit."
            )
from flask import Blueprint, render_template, redirect, url_for, session, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from password_validator import PasswordValidator
from functools import wraps

import games.authentication.services as services
import games.adapters.repository as repo




authentication_blueprint = Blueprint('authentication_bp', __name__, url_prefix='/authentication')


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'user_name' not in session:
            return redirect(url_for('authentication_bp.login'))

        user = services.get_user(session['user_name'], repo.repo_instance)

        if user is None:
            session.clear()
            return redirect(url_for('authentication_bp.login'))

        return view(**kwargs)
    return wrapped_view


@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    user_name_not_unique = None

    if form.validate_on_submit():
        # Check that the new user name and email are not already in the database. If they are generate a user error.
        try:
            services.add_user(form.user_name.data, form.password.data, repo.repo_instance)
            return redirect(url_for('authentication_bp.login'))
        except services.NameNotUniqueException:
            user_name_not_unique = 'Your user name is already taken - please enter another'

    return render_template(
        'authentication.html',
        title='Register',
        form=form,
        user_name_error_message=user_name_not_unique,
        handler_url=url_for('authentication_bp.register'),
    )

@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user_name_not_recognised = None
    password_does_not_match_user_name = None

    # Check whether the request method is a POST (user submitted form) and whether the form passed validation checks.
    if form.validate_on_submit():
        try:
            user = services.get_user(form.user_name.data, repo.repo_instance)
            if user is None:
                user_name_not_recognised = 'User name not recognised - please enter another'
                return render_template(
                    'authentication.html',
                    title='Login',
                    user_name_error_message=user_name_not_recognised,
                    password_error_message=password_does_not_match_user_name,
                    form=form,
                )
            services.authenticate_user(user['user_name'], form.password.data, repo.repo_instance)

            session.clear()
            session['user_name'] = user['user_name']
            return redirect(url_for('profile_bp.profile', user_name=user['user_name']))

        except services.AuthenticationException:
            password_does_not_match_user_name = 'Incorrect password - please try again'

    return render_template(
        'authentication.html',
        title='Login',
        user_name_error_message=user_name_not_recognised,
        password_error_message=password_does_not_match_user_name,
        form=form,
    )


@authentication_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home_bp.home'))


# Check Validity of Password
class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = u'Your password must have at least 8 characters, contain an upper case letter,\
            a lower case letter and a digit.'
        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema \
            .min(8) \
            .has().uppercase() \
            .has().lowercase() \
            .has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)


# Create Registration Forms
class RegistrationForm(FlaskForm):
    user_name = StringField('Username', [
        DataRequired(message='Your user name is required'),
        Length(min=3, message='Your user name is too short')])
    password = PasswordField('Password', [
        DataRequired(message='Your password is required'),
        PasswordValid()])
    submit = SubmitField('Register')


# Create Login Forms
class LoginForm(FlaskForm):
    user_name = StringField('Username', [
        DataRequired()])
    password = PasswordField('Password', [
        DataRequired()])
    submit = SubmitField('Login')



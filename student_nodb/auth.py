from .form import AddUserForm, LoginForm  #: import user forms
# from importing all neccessary methods for user actions and login.
from .data import init_db, validate_login, add_user_data
#: import all required dependencies from flask.
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
#: security features for password protection using hashing.
from werkzeug.security import check_password_hash, generate_password_hash
#: To add the functool to create login required decorators.
import functools

'''
Created By: Ajay
Date: Febuary 10, 2019

This module is used to authenticate the user and will deal with registering or login to
Application.
Main Processes :
1. Admin can add the user with register view and its templates
2. Login the existing use into the system.
3. Will Also provide functinality to check if user is login or not
4. Logout for the existing user.

We will be registering this blueprints for this app to provide controllers for the app.
'''

#: create blueprint for auth app.
bp = Blueprint('auth', __name__, url_prefix='/auth')


#: Below will be the start of the views. We basically have 3 views: AddUser, Login and logout.
#: login view for auth/login.
@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # validate the user in the database
        if validate_login(username=form.username.data,
                          password=form.password.data):
            #: for login success
            session.clear()
            session['user_id'] = form.username.data
            flash(
                f'Welcome {form.username.data}, You are logged in.',
                'success')

            return redirect(url_for('student.index'))
        else:
            #: for unsuccesful login
            flash(
                f'Login Unsuccessful. Please check Username or Password.',
                'danger')

    return render_template('auth/login.html', title='Admin Login', form=form)

#: check for user logged in using session cookie.
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = 'admin'


#: login
def login_required(view):
    # : functools used here to create it as decorator wrapper
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:  #: if not logged into the session
            return redirect(url_for('auth.login'))  # : redirect to login

        return view(**kwargs)  # : continue the view processing.
    #: return a wrapper for this method as decorator.
    return wrapped_view


#: add user to to user database.
@bp.route('/adduser', methods=('GET', 'POST'))
@login_required
def adduser():
    form = AddUserForm()
    if form.validate_on_submit():
        #: add user to the database of users
        add_user_data(
            username=form.username.data,
            password=generate_password_hash(
                form.password.data))

        flash(f'Account created for {form.username.data}', 'success')
        return redirect(url_for('student.index'))
    return render_template('auth/adduser.html', title='Add User', form=form)

#: logout will clear the session for the user and remove the logged in user
#: It will return the user back to login screen which is the main page.
@bp.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

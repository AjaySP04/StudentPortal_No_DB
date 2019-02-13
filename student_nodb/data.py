import os
import click
from .database.student_data import (
    load_data_student,
    list_data_student,
    add_data_student,
    update_student_detail,
    delete_student,
    search_student)
from .database.user_data import load_data_user, add_user, login_authenticator
from flask.cli import with_appcontext
from flask import current_app, g, flash

'''
 created by : Ajay Singh Parmar
 Date : Febuary 12, 2019
 Description : COntaines all the database functinality for Student_NODB app can be found here.
 - Thus module is written from scratch to simulate the behavior of any database query language.

 - The methods wriiten here will be imported used inside the views to read or update the file database.
'''


# current directory path.
cwd = os.getcwd()

#: file to load user data for initial app on 'flask init_db'
FILE_USERS = os.path.join(
    cwd, 'student_nodb/database/temp/user/user_data_file.txt')

#:Target file where all users added or can be read to authenticate users
TARGET_USER_FILE = os.path.join(
    cwd, 'instance/temp_user_data_file.txt')


#: file to load student data for initial app on 'flask init_db'
FILE_STUDENTS = os.path.join(
    cwd, 'student_nodb/database/temp/student/student_data_file.txt')

#:Target file where all students are added or CRUD operation will be performed.
TARGET_STUDENT_FILE = os.path.join(
    cwd, 'instance/temp_student_data_file.txt')


#: load user data from file to target
def load_user_data():
    load_data_user(FILE_USERS, TARGET_USER_FILE)


#: load user data from file to target
def load_student_data():
    load_data_student(FILE_STUDENTS, TARGET_STUDENT_FILE)


#: initialize the database
def init_db():

    #: load data for user authentications
    load_user_data()

    #: load student data for CRUD operations.
    load_student_data()


#: validate user credentials for login
def validate_login(username='', password=''):
    return login_authenticator(TARGET_USER_FILE, username, password)


#: add user to user's database
def add_user_data(username='test', password='pass'):
    add_user(TARGET_USER_FILE, username, password)


#: ad student to student database.
def add_student_data(name='Test Student', age=18, gender='Male'):
    add_data_student(TARGET_STUDENT_FILE, name, age, gender)


#: list all student currently in database
def list_student_data():
    return list_data_student(TARGET_STUDENT_FILE)


#: update student details for a particular database.
def update_student(name='', age=0, gender='', roll_number=''):
    update_student_detail(TARGET_STUDENT_FILE, name, age, gender, roll_number)


#: delete the student for particular roll number.
def delete_student_data(roll_number=''):
    delete_student(TARGET_STUDENT_FILE, roll_number)


#: search student for the input pattern
def search_student_record(search_string=''):
    return search_student(TARGET_STUDENT_FILE, search_string)


# : We will be creating a command for initializing the database for the application.
# : before loading the app, it should be called inorder to configure all data.
# : Here we are adding command into flask for initializing app database.
@click.command('init_db')
@with_appcontext
def init_db_command():
    #: clear the existing data and make fresh tables using the command.'''
    init_db()
    click.echo('Initialized Student Database')


def init_app(app):
    #: makes flask to call function while clean up
    # add the command into flask <command> in this case : flask init_db
    app.cli.add_command(init_db_command)

#: Importing all dependencies.
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

#: from importing all neccessary mthods for user actions and login
from .data import (
    list_student_data, add_student_data, update_student,
    delete_student_data, search_student_record
)
#: import student related forms
from .form import CreateStudentForm, UpdateStudentForm

#: import login required to check for user login
from student_nodb.auth import login_required

#: exceptions to add abort to our functionality.
#: In case of  http request-response error send abort.
from werkzeug.exceptions import abort

'''
Created By: Ajay
Date: Febuary 12, 2019

This module is the main module for the Student Application.
It will provide all the vew functionalities to our app
which deals with student processes like.
1. Add Student record to database. (Create)
2. Edit particular student record. (Update)
3. Delete a particular student. (Delete)
4. Search or view all or few students. (Read)
This contain all the views related to the functinality of the student.
'''

#: blueprint for the student app with url prefix of '/student'
bp = Blueprint('student', __name__, url_prefix='/')

#: will start the view method for the student.
#: check if user is logged if yes then fetch student list.


@bp.route('/')
@login_required
def index():
    #: fetch the list of students from database.
    students = list_student_data()
    #: render student main index page.
    return render_template(
        'student/index.html',
        title='Index',
        students=students
    )


#: blueprint for creating student.
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    form = CreateStudentForm()
    if form.validate_on_submit():
        #: perform add student
        add_student_data(
            name=form.name.data,
            age=form.age.data,
            gender=form.gender.data
        )
        #: flash message if successful
        flash(f'Student {form.name.data} added successfully.', 'success')
        return redirect(url_for('student.index'))
    return render_template(
        'student/create.html',
        title='Add Student',
        form=form
    )


#: get the student for particular roll number
def get_students(roll_number):
    student = []
    students = list_student_data()
    for item in students:
        if item['roll_number'] == roll_number:
            student.append(item)
    #: get first student matched with student.
    student = student[0]
    #: check if the student is not None object
    if student is None:
        #: will abort once the student could not befound
        abort(404, "Student {0} doesn't exist.".format(roll_number))
    #: if no error occured then returnt the student detail object.
    return student


#: update for the student
@bp.route('/update/<roll_num>', methods=('GET', 'POST'))
@login_required
def update(roll_num):
    student = get_students(roll_num)
    form = UpdateStudentForm()
    if form.validate_on_submit():
        #: perform update for student details
        update_student(
            name=form.name.data,
            age=form.age.data,
            gender=form.gender.data,
            roll_number=roll_num
        )
        #: flash message if updated
        flash(
            f'Student {form.name.data} details updated successfully.',
            'success'
        )
        #: redirect to the index page on successful detail update.
        return redirect(url_for('student.index'))
    #: render template with details fetch
    return render_template(
        'student/update.html',
        title='Edit Student',
        form=form, student=student
    )


#: for deleting the student for a specific id.
@bp.route('/delete/<roll_num>', methods=('POST',))
@login_required
def delete(roll_num):
    student = get_students(roll_num)
    #: perform delete
    delete_student_data(roll_number=roll_num)
    #: flash success on delete completion.
    flash(f'Student removed successfully.', 'success')
    #: redirect to the index page on completion.
    return redirect(url_for('student.index'))


#: for student search for the given pattern.
@bp.route('/search', methods=('GET', 'POST'))
@login_required
def search():
    #: initialize the student list that will return.
    students = []
    if request.method == 'GET':
        #: get the pattern for search.
        pattern = request.args.get('search')
        #: set error to None before the search process.
        error = None
        #: check if the pattern is not blank then only start the search.
        if not pattern:
            #: when no pattern entered set error
            error = 'Search field cannot be empty.'
        #: if no error present flask error else continue with search.
        if error is not None:
            flash(error, 'warning')
        else:
            #: get the pattern from get attribute.
            pattern = request.args.get('search')
            #: perform search
            students = search_student_record(pattern)
            #: successful earch will send the list of match to index page.
            return render_template('student/index.html', students=students)
    #: render the index template for index page.
    return render_template('student/index.html', students=students)
    #: end of module

import os
import sys

#: re for regex functinality.
#: used in search.
import re

#: file data will be read through json format
#: will be required on each read write operation
import json

from flask import flash


# #: Master data list for all student information that is in the file 'student_data_file.txt'.
# #: This will be return in the get_user_data method for data fetch or write.
MASTER_STUDENTS_DATA_LIST = []

# #: Master data list for all user credential information that is in the file 'user_data_file.txt'.
# #: This will be return in the get_user_data method for data fetch or write.
MASTER_USERS_DATA_LIST = []


# #: File name for student data
FILE_STUDENTS = 'student_data_file.txt'

# #: File name for student data
FILE_USERS = 'user_data_file.txt'

# '''
# 	Process flow:
# 	Read the file:
# 		- count = 0
# 		- if present :
# 			- count how many records -> count will be used for id
# 		- else if not present:
# 			- count = 1
# 		- open file in write mode and append the id and admin and password
# '''


#: dummy data for testing file operations.
# student_string = '''
# {
#   "students" : [
#    {
#     "roll_number" : "S00001",
# 	"name" : "Test Student1",
# 	"age" : 22,
# 	"gender" : "Male"
#    },
#    {
#     "roll_number" : "S00002",
# 	"name" : "Test Student2",
# 	"age" : 24,
# 	"gender" : "Female"
#    },
#    {
#     "roll_number" : "S00003",
# 	"name" : "Test Student3",
# 	"age" : 22,
# 	"gender" : "Male"
#    },
#    {
#     "roll_number" : "S00004",
# 	"name" : "Test Student4",
# 	"age" : 19,
# 	"gender" : "Female"
#    }
#   ]
# }

# '''

# def training():
# 	data = json.loads(student_string)
# 	#print(type(data))

# 	for student in data['students']:
# 		del student['gender']

# 	new_student_string = json.dumps(data, indent=2, sort_keys=True)
# 	print(new_student_string)

# def training_file(file):

# 	with open(file, 'r') as f:
# 		data = json.load(f)

# 	f.close()
# 	print(type(data))
# 	print(type(data['students']))
# 	print(type(data['students'][0]))
# 	print(type(data['students'][0]['name']))

# 	for student in data['students']:
# 		print(student['name'] + ' - ' + student['roll_number'])
# 		del student['gender']

# 	with open('new_student_temp_data.txt', 'w') as f:
# 		json.dump(data, f, indent=2, sort_keys=True)
# 	f.close()

def read_file_as_json(file):
    #: read the data from a file.
    with open(file, 'r') as f:
        data = json.load(f)
    f.close()

    return data


def write_json_to_file(data, file):
    #: write the currently changed data into the file.
    with open(file, 'w') as f:
        json.dump(data, f, indent=2, sort_keys=True)
    f.close()

#: count number of student in the database
#: Will be used in generating roll number


def get_last_roll_number(data):
    counter = 0
    last_student = data['students'][-1]
    return last_student['roll_number'][-4:]

#: Add student to the database records.


def add_data_student(file, name, age, gender):
    #: read the data in json format
    data = read_file_as_json(file)

    # count number of student in the data
    last_roll_number = int(get_last_roll_number(data))

    #: create a student data as dictionary
    #: auto generated roll number for the student
    #: used as auniques id for identifying students.
    roll_number = 'S0000' + str(last_roll_number + 1)

    dict_student_obj = {
        'roll_number': roll_number,
        'name': name,
        'age': age,
        'gender': gender
    }

    #: append the student dictionary object to data['students']
    data['students'].append(dict_student_obj)

    #: write the currently changed data into the file.
    write_json_to_file(data, file)


'''
	Edit/Update the student information.
'''


def update_student_detail(file, name='', age=0, gender='', roll_number=''):
    #: read the data
    data = read_file_as_json(file)

    # fetch details for the student to be updated.
    #: If roll number is empty then will only update information for test student
    if roll_number == '':
        roll_number = 'S00001'
        print('nothing to update.')
    else:
        #: roll number will be used to identify the student.
        roll_number = roll_number
        for student in data['students']:
            if student['roll_number'] == roll_number:
                    # update/edit the name for student.
                if name != '':
                    student['name'] = name
                # update/edit the age for student
                if age != 0:
                    student['age'] = age
                # update/edit the gender information for student.
                if gender != '':
                    student['gender'] = gender

    #: print(data) - help in catastrophe

    #: write the currently changed data into the file.
    write_json_to_file(data, file)


'''
	Delete a particular student from database.
'''


def delete_student(file, roll_number=''):
    #: read the data
    data = read_file_as_json(file)

    # fetch details for the student to be updated.
    if roll_number == '':
        flash(f'Nothing Found to delete', 'danger')
    elif roll_number == 'S00001':
        flash(f'Cannot delete Master student. Work in progress.', 'danger')
    else:
        for student in data['students']:
                    #: Can fetch student from roll number field.
                    #: Roll Number is NOT allowed to change.
            if student['roll_number'] == roll_number:
                #: delete the student from database list.
                data['students'].remove(student)

    #: write the currently changed data into the file.
    write_json_to_file(data, file)


def search_student(file, search_string=''):
    #: list of matched student.
    #: initialized to empty list
    list_of_matched_student = []

    if search_string == '':
        print('Nothing specified for search...')
    else:
        #: pattern to search
        pattern = search_string

        # get all students in the database.
        list_of_students = list_all_students(file)

        #: loop on the string to find the student.
        for student in list_of_students:

            #: if student['roll_number'] == search_string:
            #: list_of_matched_student.append(student)
            #: If roll number pattern is enter search through roll numbers.
            if re.search(r'^S0', pattern):
                if re.search(pattern, student['roll_number'], re.IGNORECASE):
                    list_of_matched_student.append(student)
            else:
                #: if roll number pattern doesn't satisfy then search in name.
                if re.search(pattern, student['name'], re.IGNORECASE):
                    list_of_matched_student.append(student)

            # if student['name'] == target_search_string:
            #	list_of_matched_student.append(student)

    return list_of_matched_student


def list_all_students(file):
    #: read the data
    data = read_file_as_json(file)
    list_of_all_students = []
    if data['students'] == []:
        flash(f'No Student found in database. Must add new students.', 'danger')
    else:
        list_of_all_students = data['students']
    #: create a list for the fetched students.
    list_of_all_students = data['students']

    #: return the list of the students in the database
    return list_of_all_students

# def display_student_list(list):

# 	if list == [] :
# 		#: if nothing found in list.
# 		print('''
# 			Sorry :( No record match found...
# 			''')
# 	else:
# 		#: for item in list display all information.
# 		for item in list:
# 			print('''
# 				Name : {}
# 				Roll Number : {}
# 				Age : {}
# 				Gender : {}
# 			'''.format(item['name'], item['roll_number'], item['age'], item['gender']), end='\n')

#: copy master data into the temp working files


def copy_master_data_to_file(master, file):
    #: read master file data to working file.
    master_data = read_file_as_json(master)

    #: write the currently changed data into the file.
    write_json_to_file(master_data, file)


#: load the data one time into working target file
def load_data_student(file, target):
    try:
        f = open(target, 'r')
        f.close()
    except FileNotFoundError:
        copy_master_data_to_file(file, target)
        pass

#: Will get the all user_list


def list_data_student(target):
    student_list = list_all_students(target)
    return student_list

#: Here we have summarize all the methods with ther uses as they are represented.
#: These are the methods which can be exported to or imported into data.py for database use.


def main():
    # training()

    file = FILE_STUDENTS
    # training_file(file)
    target = 'temp/new_student_temp_data.txt'

    #: try to load data to target
    load_data_student(file, target)

    #: list all Students for index page
    #student_list = list_data_student(target)
    # display_student_list(student_list)

    #: dummy user data to create new user
    name = 'test student'
    age = 19
    gender = 'Male'
    #: Add user to user data target file.
    #add_data_student(target, name, age, gender)

    #: update/edit student information
    #update_student_detail(target, roll_number='S00001')

    #: To delete particular student with specified roll number
    #delete_student(target, roll_number='S00001')

    #: search for student with roll number or name
    #: this will return list of all match for search pattern.
    list_of_search = search_student(target, search_string='Stu')

    #: Display all fetched data.
    display_student_list(list_of_search)


# if __name__=='__main__':
# 	main()

'''
 created by : Ajay Singh Parmar
 Date : Febuary 12, 2019
 Description : COntaines all the database functinality for user authentication can be found here.
 - Thus module is written from scratch to simulate the behavior of any database query language.

 - The methods wriiten here will be imported inside data.py in main project directory.
'''


import os
import sys

#: re for regex functinality.
#: used in search.
import re

#: file data will be read through json format
#: will be required on each read write operation
import json

from werkzeug.security import check_password_hash, generate_password_hash


# #: Master data list for all user credential information that is in the file 'user_data_file.txt'.
# #: This will be return in the get_user_data method for data fetch or write.
MASTER_USERS_DATA_LIST = []


# #: File name for user data
FILE_USERS = 'user_data_file.txt'

#: Target file for data working.
target_file = 'temp/new_user_temp_data.txt'

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

#: dummy data
# user_string = '''
# {
#   "users" : [
#    {
#     "id" : 1,
#   	"username" : "admin",
#   	"password" : "password"
#    },
#    {
#     "id" : 2,
#     "username" : "test",
#     "password" : "test"
#    }
#   ]
#}

'''
	Training modules for file operations.
'''	

# def training():
# 	data = json.loads(user_string)
# 	#print(type(data))
	
# 	new_user_string = json.dumps(data, indent=2, sort_keys=True)
# 	print(new_user_string)
	
# def training_file(file):
    
# 	with open(file, 'r') as f:
# 		data = json.load(f)
	
# 	f.close()
# 	print(type(data)) # dict
# 	print(type(data['users'])) # list
# 	print(type(data['users'][0])) # dict
# 	print(type(data['users'][0]['username'])) # str
	
# 	for user in data['users']:
# 		print(user['id'] + ' - ' + user['username'] + ' ' +  user['password']  )
		
# 	with open('temp/new_user_temp_data.txt', 'w') as f:
# 		json.dump(data, f, indent=2, sort_keys=True)
# 	f.close()

'''
	read operation on file
'''
def read_file_as_json(file):
	#: read the data from a file.
	with open(file, 'r') as f:
		data = json.load(f)
	f.close()
	
	return data

'''
	write operation on file
'''	
def write_json_to_file(data, file):
	#: write the currently changed data into the file.
	with open(file, 'w') as f:
		json.dump(data, f, indent=2, sort_keys=True)
	f.close()
	
#: count number of user in the database
#: Will be used in generating roll number
def get_last_id(data):
	counter = 0
	last_user = data['users'][-1]
	return last_user['id']

'''
	Delete a particular user from database.
'''
def delete_user(file, _id=1):
	#: read the data
	data = read_file_as_json(file)
		
	for user in data['users']:
		#: Can fetch user from its id.
		#: NOT Allowed to delete Admin with id as 1.
		if user['id'] == _id:
			#: delete the user from database list.
			data['users'].remove(user)
	
	#: write altered back to the file.
	write_json_to_file(data, file)



'''
	For add user functionality
'''	
def add_user(file, username, password):
	#: read the data
	data = read_file_as_json(file)
	
	#count number of user in the data	
	last_id = int(get_last_id(data))
	
	#: create a user data as dictionary
	#: generating id for the new user
	_id = last_id + 1
	#: dict object for user.
	dict_user_obj = {
	                 'id' : _id,
					 'username' : username,
					 'password' : password
					}
	
	#: append the user dictionary object to data['users']
	data['users'].append(dict_user_obj)
	
	#: write the currently all data back to working file.
	write_json_to_file(data, file)


def list_all_users(file):
	#: read the data
	data = read_file_as_json(file)
	
	#: create a list for the fetched users.
	list_of_all_users = data['users']
		
	#: return the list of the users in the database
	return list_of_all_users
	
def display_user_list(list):
	
	if list == [] :
		#: if nothing found in list.
		print('''
			Sorry :( No record match found...
			''')
	else:
		#: for item in list display all information.
		for item in list:
			print('''
				id : {}
				Username : {}
				Password : {}
			'''.format(item['id'], item['username'], item['password']), end='\n') 

def copy_master_data_to_file(master, file):
	#: read master file data to working file.
	master_data = read_file_as_json(master)

	#: write the currently changed data into the file.
	write_json_to_file(master_data, file)

#: load the data one time into working target file
def load_data_user(file, target):
	try:
		f = open(target, 'r')
		f.close()
	except FileNotFoundError:
		copy_master_data_to_file(file, target)
		pass

#: Will get the all user_list
def user_list(file):
	user_list = list_all_users(file)
	return user_list

def login_authenticator(file, username='', password=''):
	#: read the data
	data = read_file_as_json(file)
	login_flag = False
	for user in data['users']:

		if user['username'] == username and user['username'] != 'admin':
			if check_password_hash(user['password'], password):
				print('login success.')
				login_flag = True
				break
		else:
			if user['username'] == username:
				if user['password'] == password:
					print('login success.')
					login_flag = True
					break

	return login_flag

#: Here we have summarize all the methds with ther uses as they are represented.
#: These are the methods which can be exported to or imported into data.py for database use.
def main():
	#training()

	
	file = FILE_USERS
	#: training_file(file)
	target = 'temp/new_user_temp_data.txt'

	#: try to load data to target
	load_data_user(file, target)
	
	#: dummy user data to create new user
	username = 'user'
	password = 'password'

	#: Add user to user data target file.
	add_user(target, username, password)
		
	#: To delete particular user except for admin which has id = 1
	delete_user(target, _id=2)

	#: return current total user list for the application
	user_list1 = user_list(target)

	#: Display all fetched data.
	display_user_list(user_list1)

	if login_authenticator(target, username='user', password='password'):
		print('Success')
	else:
		print('Fail')


#main()

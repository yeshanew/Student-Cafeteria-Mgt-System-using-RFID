import pymysql
from app import app
import sys
import signal
from db_config import mysql
from tables import Account_Results 
from tables import Student_account
from tables import Meal_status
from tables import Meal_info
from flask import flash, render_template, request, redirect, url_for, session
from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime
now=datetime.now()
date_format=now.strftime('%Y-%m-%d %H-%M-%S')
import os
import urllib.request
from app import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
def signal_handler(signal,frame):
	sys.exit(0)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])	
def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def signal_handler(signal,frame):
	sys.exit(0)
import serial
serialport = "com4"
ser = serial.Serial(serialport, 9600)
@app.route('/adminlogin/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'usertype' in request.form  and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['usertype']
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        if(user_type=='Admin'):
             cursor.execute('SELECT * FROM account WHERE Username = %s AND Password = %s and User_type= %s and Status="Active"', (username, password,user_type))
             account = cursor.fetchone()
             if account:
                session['loggedin'] = True
                session['username'] = account['Username']
                session['usertype'] = account['User_type']
				# Redirect to home page
                return redirect(url_for('admin_home'))
             else:
                msg = 'Please enter the correct username/password!'
        if(user_type=='Checker'):
            cursor.execute('SELECT * FROM account WHERE Username = %s AND Password = %s and User_type= %s and Status="Active"', (username, password,user_type))
            account = cursor.fetchone()
            if account:
                session['loggedin'] = True
                session['username'] = account['Username']
                session['usertype'] = account['User_type']
				# Redirect to home page
                return redirect(url_for('home'))
            else:
                msg = 'Please enter correct username/password!'
    return render_template('index.html', msg=msg)
@app.route('/adminlogin/student', methods=['GET', 'POST'])
def add_student():
		value=ser.readline().decode( 'ascii' ).strip()
		msg = ''
		if request.method == 'POST' and 'id' in request.form and 'name' in request.form and 'email' in request.form  and 'sex' in request.form and 'age' in request.form and 'phone' in request.form and 'year' in request.form and 'department' in request.form and 'program' in request.form and 'cafe' in request.form:
			if 'file' not in request.files:
				msg='No file'
			file = request.files['file']
			if file.filename == '':
				msg='No file selected for uploading'
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				PEOPLE_FOLDER = os.path.join('static', 'tempo_photo')
				app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				full_filename = os.path.join(app.config['UPLOAD_FOLDER'],filename)
				Picture = convertToBinaryData(full_filename)
			else:
				msg='Allowed file types are txt, pdf, png, jpg, jpeg, gif'
			# Create variables for easy access
			id = request.form['id']
			name = request.form['name']
			email = request.form['email']
			sex= request.form['sex']
			age = request.form['age']
			department = request.form['department']
			phone = request.form['phone']
			year= request.form['year']
			program= request.form['program']
			cafe= request.form['cafe']
					# Check if account exists using MySQL
			if(value!="TIMEOUT!"):
				conn = mysql.connect()
				cursor = conn.cursor(pymysql.cursors.DictCursor)
				cursor.execute("SELECT * FROM student WHERE Card_key=%s", value)
				#account = cursor.fetchone()
				# If account exists show error and validation checks
				count = cursor.rowcount
				if count>=1:
					msg = 'This card is already registered!'
				else:
					sql = "INSERT INTO student(Card_key,ID,Name,Email,Department,Sex,Age,Status,Phone_number,Year,Date,Program,Cafe,Profile,gate_status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
					data = (value,id,name,email,department,sex,age,"Active",phone,year,date_format,program,cafe,Picture,"Active")
					conn = mysql.connect()
					cursor = conn.cursor()
					cursor.execute(sql, data)
					conn.commit()
					sql1 = "INSERT INTO meal(Card_key,ID,Department,Year,Time,Breakfast,Lunch,Dinner,Status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
					data1 = (value,id,department,year,date_format,"not yet","not yet","not yet","Active")
					conn1 = mysql.connect()
					cursor1 = conn1.cursor()
					cursor1.execute(sql1, data1)
					conn1.commit()
					msg = 'The student is registered successfully!'
			else: msg = 'The card timeout!!'
		conn = mysql.connect()		
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute('SELECT * FROM department')
		return render_template('student_account.html',lists=cursor.fetchall(), msg=msg)	
@app.route('/adminlogin/register', methods=['GET', 'POST'])
def sign_up():
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'name' in request.form and 'usertype' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        confirm= request.form['confirm']
        name = request.form['name']
        usertype = request.form['usertype']		
		        # Check if account exists using MySQL
        if(password==confirm):
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute('SELECT * FROM account WHERE username = %s', (username))
            account = cursor.fetchone()
			# If account exists show error and validation checks
            if account:
                msg = 'Account already exists!'
            else:
                sql = "INSERT INTO account(Name,Email,username, password,Status,Date,User_type) VALUES(%s,%s,%s,%s,%s,%s,%s)"
                data = (name,email,username, password,"Active",date_format,usertype)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                msg = 'You have successfully registered!'
        else: msg = 'The paasword does not mach!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)	
@app.route('/adminlogin/check_meal', methods=['GET', 'POST'])
def check_meal():
	while(True):
		key_value=ser.readline().decode( 'ascii' ).strip()
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("select * from meal_status  where Breakfast_status='Finished' and Lunch_status='Finished' and Dinner_status='Finished'")
		row = cursor.fetchone()
		if row :
			msg="ካፍተሪያ አልተከፈተም.The caffeteria is not opened"
			return render_template('layout_4.html',msg=msg)
		else:
			if(key_value=="TIMEOUT!"):
				msg="እባክዎን ካርድዎን ያስጠጉ!Please Contact your card to the Machine."
				return render_template('layout_3.html',msg=msg)
			else:
				cursor.execute("select * from meal where Card_key=%s",key_value);
				row = cursor.fetchone()
				if row :
					query1 ="select * from meal_status  where Breakfast_status='Started'";
					cursor.execute(query1)
					row = cursor.fetchone()
					if row:
						cursor.execute("select * from meal where Breakfast='Not yet' and Card_key=%s and Status='Active'",key_value)
						row = cursor.fetchone()
						if row :
							cursor.execute("UPDATE meal SET Breakfast='Ate' ,Time=%s where Card_key=%s",(date_format,key_value))
							conn.commit()
							msg="እንኳን ደህና መጡ! ይግቡ. Take your breakfast.Good breakfast!"
						else: 
							msg="You already ate your breakfast"
					else:
						query1 ="select * from meal_status  where Lunch_status='Started'" 
						cursor.execute(query1)
						row = cursor.fetchone()
						if row:
							cursor.execute("select * from meal where Lunch='Not yet' and Card_key=%s and Status='Active'",key_value)
							row = cursor.fetchone()
							if row :
								cursor.execute("UPDATE meal SET Lunch='Ate' ,Time=%s where Card_key=%s",(date_format,key_value))
								conn.commit()
								msg="እንኳን ደህና መጡ! ይግቡ. Take your lunch.Good lunch!"
							else:
								msg="You already ate your lunch"
						else: 
							query1 ="select * from meal_status  where Dinner_status='Started'";
							cursor.execute(query1)
							row = cursor.fetchone()
							if row:
								cursor.execute("select * from meal where Dinner='Not yet' and Card_key=%s and Status='Active'",key_value)
								row = cursor.fetchone()
								if row :
									cursor.execute("UPDATE meal SET Dinner='Ate',Time=%s where Card_key=%s",(date_format,key_value))
									conn.commit()
									msg="እንኳን ደህና መጡ! ይግቡ. Take your Dinner.Good dinner!"
								else: 
									msg="You already ate your dinner"
					conn = mysql.connect()
					cursor = conn.cursor(pymysql.cursors.DictCursor)
					cursor.execute("SELECT * FROM student where Card_key=%s",(key_value,))
					record = cursor.fetchall()
					conn.commit()
					conn2 = mysql.connect()
					cursor2= conn2.cursor(pymysql.cursors.DictCursor)
					cursor2.execute("SELECT * FROM student where Card_key=%s",(key_value,))
					record2 = cursor2.fetchone()
					if record:
						for row in record:
							conn.commit()
							file_name=row["ID"]
							write_file(row["Profile"],"static/people_photo/"+ file_name +".png")
							PEOPLE_FOLDER = os.path.join('static', 'people_photo')
							app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
							full_filename = os.path.join(app.config['UPLOAD_FOLDER'],file_name+".png")
						return render_template('status_displayer_2.html',record=record2,user_image = full_filename, msg=msg)
						conn.commit()
				else:
					return render_template('layout_3.html',msg="Your card is not registered",amharic_msg1="ካርድዎ አልተመዘገበም",amharic_msg2="መግባት አይችሉም!")
			#return redirect(url_for('check_meal'))
@app.route('/adminlogin/student_info', methods=['GET', 'POST'])
def manage_student():
	if 'loggedin' in session:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM student")
		rows = cursor.fetchall()
		table = Student_account(rows)
		table.border = True
		conn2 = mysql.connect()
		cursor2 = conn2.cursor(pymysql.cursors.DictCursor)
		cursor2.execute('SELECT * FROM Department')
		return render_template('student_info.html',table=table,dpt_lists=cursor2.fetchall())
	return redirect(url_for('login'))
	
@app.route('/adminlogin/student_search', methods=['GET', 'POST'])
def search_student():
	if 'loggedin' in session:
		_id =request.form['id']
		if _id and request.method == 'POST':
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute("SELECT * FROM student where ID=%s",_id)
			rows = cursor.fetchall()
			count = cursor.rowcount
			table = Student_account(rows)
			table.border = True
			if(count==0):
				msg='Please enter the correct student ID number.'
				return render_template('student_info.html', table=table,search_msg=msg)
			else:
				return render_template('student_info.html', table=table)		
	return redirect(url_for('login'))
@app.route('/adminlogin/student_bydepartment', methods=['GET', 'POST'])
def search_ByDepartment():
	if 'loggedin' in session:
		if request.method == 'POST' and 'department' in request.form and 'year' in request.form:
			_department =request.form['department']
			_year =request.form['year']
			conn1 = mysql.connect()
			cursor1 = conn1.cursor(pymysql.cursors.DictCursor)
			cursor1.execute("SELECT * FROM student where Department=%s and Year=%s",(_department,_year))
			rows = cursor1.fetchall()
			count = cursor1.rowcount
			table = Student_account(rows)
			table.border = True
			conn2 = mysql.connect()
			cursor2 = conn2.cursor(pymysql.cursors.DictCursor)
			cursor2.execute('SELECT * FROM Department')
			if(count==0):
				msg='There is no student in this department and in this batch'
				return render_template('student_info.html', table=table,dpt_lists=cursor2.fetchall(),msg = msg)
			else:
				return render_template('student_info.html', table=table,dpt_lists=cursor2.fetchall())		
	return redirect(url_for('login'))
@app.route('/adminlogin/deactive_student', methods=['GET', 'POST'])
def deactivate_card():
	if 'loggedin' in session:
		if request.method == 'POST' and 'department' in request.form and 'year' in request.form and 'program' in request.form:
			_department =request.form['department']
			_year =request.form['year']
			_program =request.form['program']
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute("SELECT * FROM student where Department=%s and Year=%s and Program=%s",(_department,_year,_program))
			rows = cursor.fetchall()
			count = cursor.rowcount
			table = Student_account(rows)
			table.border = True
			conn2 = mysql.connect()
			cursor2 = conn2.cursor(pymysql.cursors.DictCursor)
			cursor2.execute('SELECT * FROM Department')
			if(count==0):
				msg='There is no student in your selection'
				return render_template('student_info.html', table=table,dpt_lists=cursor2.fetchall(),msg=msg)
			else:
				msg="successfully deactivated"
				conn3 = mysql.connect()
				cursor3 = conn3.cursor(pymysql.cursors.DictCursor)
				cursor3.execute("UPDATE student SET Status=%s",('Deactivated'))
				cursor3.execute("UPDATE meal SET Status=%s",('Deactivated'))
				return render_template('student_info.html', table=table,dpt_lists=cursor2.fetchall(),msg = msg)		
	return redirect(url_for('login'))	
@app.route('/adminlogin/activate_student', methods=['GET', 'POST'])
def activate_card():
	if 'loggedin' in session:
		if request.method == 'POST' and 'department' in request.form and 'year' in request.form and 'program' in request.form:
			_department =request.form['department']
			_year =request.form['year']
			_program =request.form['program']
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute("SELECT * FROM student where Department=%s and Year=%s and Program=%s",(_department,_year,_program))
			rows = cursor.fetchall()
			count = cursor.rowcount
			table = Student_account(rows)
			table.border = True
			conn2 = mysql.connect()
			cursor2 = conn2.cursor(pymysql.cursors.DictCursor)
			cursor2.execute('SELECT * FROM Department')
			if(count==0):
				msg='There is no student in your selection'
				return render_template('student_info.html', table=table,dpt_lists=cursor2.fetchall())
			else:
				conn3 = mysql.connect()
				cursor3 = conn3.cursor(pymysql.cursors.DictCursor)
				cursor3.execute("UPDATE student SET Status=%s where Department=%s and Year=%s and Program=%s",('Active',_department,_year,_program))
				cursor3.execute("UPDATE meal SET Status=%s where Department=%s and Year=%s and Program=%s",('Active',_department,_year,_program))
				conn3.commit()
				return render_template('student_info.html', table=table,dpt_lists=cursor2.fetchall(),year_msg = _year,dpt_msg = _department)		
	return redirect(url_for('login'))
@app.route('/adminlogin/deactivate_noncafe', methods=['GET', 'POST'])
def deactivate_noncafe():
	if 'loggedin' in session:
		if request.method == 'POST':
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute("SELECT * FROM student where Cafe='Noncafe'")
			rows = cursor.fetchall()
			count = cursor.rowcount
			if(count>=1):
				msg='The Noncafe students card successfully decactivated'
				conn3 = mysql.connect()
				cursor3 = conn3.cursor(pymysql.cursors.DictCursor)
				cursor3.execute("UPDATE student SET Status=%s",('Deactivated'))
				cursor3.execute("UPDATE meal SET Status=%s",('Deactivated'))
				conn3.commit()
				return render_template('student_info.html', msg=msg)
			else:return render_template('student_info.html', msg="All students card are already deactivateed or there is no Noncafe student") 
	return redirect(url_for('login'))
@app.route('/adminlogin/activate_all', methods=['GET', 'POST'])
def activate_all():
	if 'loggedin' in session:
		if request.method == 'POST' and 'program' in request.form:
			_program =request.form['program']
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute("SELECT * FROM student where Program=%s",(_program))
			rows = cursor.fetchall()
			count = cursor.rowcount
			table = Student_account(rows)
			table.border = True
			conn2 = mysql.connect()
			cursor2 = conn2.cursor(pymysql.cursors.DictCursor)
			cursor2.execute('SELECT * FROM Department')
			if(count==0):
				msg='There is no student in your selection'
				return render_template('student_info.html', table=table,dpt_lists=cursor2.fetchall())
			else:
				conn3 = mysql.connect()
				cursor3 = conn3.cursor(pymysql.cursors.DictCursor)
				cursor3.execute("UPDATE student SET Status=%s where  Program=%s",('Active',_program))
				cursor3.execute("UPDATE meal SET Status=%s where Program=%s",('Active',_program))
				conn3.commit()
				return render_template('student_info.html', table=table,dpt_lists=cursor2.fetchall(),year_msg = _year,dpt_msg = _department)		
	return redirect(url_for('login'))
@app.route('/adminlogin/deactive_all', methods=['GET', 'POST'])
def deactivate_all():
	if 'loggedin' in session:
		if request.method == 'POST' and  'program' in request.form:
			_program =request.form['program']
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute("SELECT * FROM student where  Program=%s",(_program))
			rows = cursor.fetchall()
			count = cursor.rowcount
			table = Student_account(rows)
			table.border = True
			conn2 = mysql.connect()
			cursor2 = conn2.cursor(pymysql.cursors.DictCursor)
			cursor2.execute('SELECT * FROM Department')
			if(count==0):
				msg='There is no student in your selection'
				return render_template('student_info.html', table=table,dpt_lists=cursor2.fetchall())
			else:
				conn3 = mysql.connect()
				cursor3 = conn3.cursor(pymysql.cursors.DictCursor)
				cursor3.execute("UPDATE student SET Status=%s where  Program=%s",('Deactivated',_program))
				cursor3.execute("UPDATE meal SET Status=%s where Program=%s",('Deactivated',_program))
				conn3.commit()
				return render_template('student_info.html', table=table,dpt_lists=cursor2.fetchall(),year_msg = _year,dpt_msg = _department)		
	return redirect(url_for('login'))		
@app.route('/adminlogin/meal_search')
def  meal_search():
	if(session['usertype']=='Admin'):
		return render_template('student_mealinfo.html')
	if(session['usertype']=='Checker'):
		return render_template('student_mealinfo_2.html')
@app.route('/adminlogin/meal_info_search', methods=['GET', 'POST'])
def meal_info():
	msg=''
	if 'loggedin' in session:
		_id =request.form['id']
		if _id and request.method == 'POST':
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute("SELECT * FROM meal where ID=%s",_id)
			rows = cursor.fetchall()
			count = cursor.rowcount
			table = Meal_info(rows)
			table.border = True
			if(count==0):
				msg='Please enter correct student ID number.'
			if(session['usertype']=='Admin'):
				return render_template('student_mealinfo.html', table=table,search_msg=msg)		
			if(session['usertype']=='Checker'):
				return render_template('student_mealinfo_2.html', table=table,search_msg=msg)		
	return redirect(url_for('login'))		
@app.route('/adminlogin/account_info', methods=['GET', 'POST'])
def manage_account():
	if 'loggedin' in session:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM account")
		rows = cursor.fetchall()
		table = Account_Results(rows)
		table.border = True
		return render_template('account_info.html', table=table)
	return redirect(url_for('login'))
@app.route('/adminlogin/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))
@app.route('/adminlogin/admin_home')
def admin_home():
    if 'loggedin' in session:
        msg='Wel Come to Debremarkos University Student Cafeteria  System'
        return render_template('admin_home.html', username=session['username'],msg=msg)
    return redirect(url_for('login'))
@app.route('/adminlogin/checker_home')
def home():
    if 'loggedin' in session:
        msg='Wel Come to Debremarkos University Student Cafeteria  System'
        return render_template('home.html', username=session['username'],msg=msg)
    return redirect(url_for('login'))
@app.route('/adminlogin/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT * FROM account WHERE Username = %s', [session['username']])
        account = cursor.fetchone()
        conn.commit()
        if(session['usertype']=='Admin'):
            return render_template('admin_profile.html', account=account)		
        if(session['usertype']=='Checker'):
            return render_template('checker_profile.html', account=account)
    return redirect(url_for('login'))
def write_file(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)
@app.route('/profile/<string:id>')
def profile_pic(id):
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute('SELECT * from student where id = %s',id)
		record = cursor.fetchall()
		if record:
			for row in record:
				conn.commit()
				write_file(row["Profile"],"static/people_photo/"+ id +".png")
				PEOPLE_FOLDER = os.path.join('static', 'people_photo')
				app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
				full_filename = os.path.join(app.config['UPLOAD_FOLDER'],id+".png")
			return render_template("student_profile.html", user_image = full_filename, msg="Profile picture")
		else:
			return 'Error loading #{id}'.format(id=id)
@app.route('/edit/<string:id>')
def edit_view(id):
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM student WHERE ID=%s", id)
		row = cursor.fetchone()
		conn1 = mysql.connect()
		cursor1 = conn1.cursor(pymysql.cursors.DictCursor)
		cursor1.execute('SELECT * FROM department')	
		if row:
			return render_template('edit.html', row=row,lists=cursor1.fetchall())
		else:
			return 'Error loading #{id}'.format(id=id)

@app.route('/update', methods=['POST'])
def update_student():	
		_name = request.form['name']
		_id = request.form['id']
		_email = request.form['email']
		_department = request.form['department']
		_age = request.form['age']
		_sex = request.form['sex']
		_status= request.form['status']
		_phone= request.form['phone']
		_year= request.form['year']
			# validate the received values
		if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'id' in request.form and 'department' in request.form and 'age' in request.form and 'sex' in request.form and 'phone' in request.form and 'year' in request.form:
					sql = "UPDATE student SET Name=%s, Email=%s, Department=%s,Age=%s,Sex=%s,Status=%s,Phone_number=%s,Year=%s  WHERE ID=%s"
					data = (_name, _email, _department, _age, _sex, _status, _phone,_year,_id,)
					conn = mysql.connect()
					cursor = conn.cursor()
					cursor.execute(sql, data)
					conn.commit()
					sql2 = "UPDATE meal SET Department=%s,Year=%s,Status=%s WHERE ID=%s"
					data2 = (_department,_year,_status,_id,)
					conn2 = mysql.connect()
					cursor2 = conn2.cursor()
					cursor2.execute(sql2, data2)
					conn2.commit()
					msg="The student account is updated successfully!"
					return render_template('layout.html',msg=msg)
@app.route('/adminlogin/changepassword1', methods=['GET', 'POST'])
def change_password1():
	if(session['usertype']=='Admin'):
		return render_template('change_password.html')		
	if(session['usertype']=='Checker'):
		return render_template('change_password_2.html')
@app.route('/adminlogin/changepassword2', methods=['GET', 'POST'])
def change_password2():	
	if 'loggedin' in session:
		current_pass = request.form['currentpassword']
		new_pass= request.form['newpassword']
		confirm_pass = request.form['confirmpassword']
		if request.method == 'POST' and 'currentpassword' in request.form and 'newpassword' in request.form and 'confirmpassword' in request.form:
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute("SELECT * FROM account where Username=%s and Password=%s",(session['username'],current_pass))
			count = cursor.rowcount
		if(count >=1):
			if(confirm_pass==new_pass):
					sql = "UPDATE account SET Password=%s  WHERE Username=%s"
					data = (new_pass,session['username'])
					conn = mysql.connect()
					cursor = conn.cursor()
					cursor.execute(sql, data)
					conn.commit()
					msg="Your password is changed successfully!"
			else: msg="The confirmation password is not match!"
		else: msg="Please enter your current password correctly!"
		if(session['usertype']=='Admin'):
			return render_template('change_password.html',msg=msg)		
		if(session['usertype']=='Checker'):
			return render_template('change_password_2.html',msg=msg)

	return redirect(url_for('login'))
@app.route('/card/<string:id>')
def change_card(id):
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM student WHERE ID=%s", id)
		row = cursor.fetchone()
		conn1 = mysql.connect()
		cursor1 = conn1.cursor(pymysql.cursors.DictCursor)
		cursor1.execute('SELECT * FROM department')	
		if row:
			return render_template('change_card.html', row=row,lists=cursor1.fetchall())
		else:
			return 'Error loading #{id}'.format(id=id)	
@app.route('/adminlogin/changecard',methods=['POST'])
def update_card():
		while(1):
			value=ser.readline().decode( 'ascii' ).strip()	
			_id= request.form['id']
			if request.method == 'POST' and 'id' in request.form:
				# save edits
				if (value!="TIMEOUT!"):
					conn = mysql.connect()
					cursor = conn.cursor(pymysql.cursors.DictCursor)
					cursor.execute("SELECT * FROM student WHERE Card_key=%s", value)
					row = cursor.fetchone()
					if row:
						msg="This card is already registered!"		
						return render_template('layout.html',msg=msg)
					else:	
						sql = "UPDATE student SET Card_key=%s"
						data = (value,)
						conn = mysql.connect()
						cursor = conn.cursor()
						cursor.execute(sql, data)
						conn.commit()
						sql2 = "UPDATE meal SET Card_key=%s"
						data2 = (value)
						conn2 = mysql.connect()
						cursor2 = conn2.cursor()
						cursor2.execute(sql2, data2)
						conn2.commit()
						msg="The student card is updated successfully!"
						return render_template('layout.html',msg=msg)
@app.route('/delete/<string:id>')
def delete_user(id):
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM student WHERE ID=%s", (id,))
		cursor.execute("DELETE FROM meal WHERE ID=%s", (id,))
		conn.commit()
		conn1 = mysql.connect()
		cursor1 = conn1.cursor(pymysql.cursors.DictCursor)
		cursor1.execute("SELECT * FROM student")
		rows = cursor1.fetchall()
		table = Student_account(rows)
		table.border = True
		msg="The student ID " +id+ " Number is deleted"
		return render_template('student_info.html', table=table,msg=msg)
@app.route('/edit_acc/<string:id>')
def edit_account(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM account WHERE Username=%s", id)
		row = cursor.fetchone()
		if row:
			return render_template('edit_account.html', row=row)
		else:
			return 'Error loading #{Username}'.format(id=id)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/update_acc', methods=['POST'])
def update_account():
		_name = request.form['name']
		_email = request.form['email']
		_username = request.form['username']
		_status= request.form['status']
		if _name and _email and _username and _status and request.method == 'POST':
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)	
			sql = "UPDATE account SET Name=%s, Email=%s,Status=%s WHERE Username=%s"
			data = (_name, _email,_status, _username,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			msg='User account updated successfully!'
			return render_template('layout.html',msg=msg)
@app.route('/delete_acc/<string:id>')
def delete_account(id):
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM account WHERE Username=%s", (id,))
		cursor.execute("DELETE FROM account WHERE Username=%s", (id,))
		conn.commit()
		msg="The account" +id+ " is deleted"
		return render_template('account_info.html', table=table,msg=msg)
@app.route('/adminlogin/report')
def report():
	msg = 'Today Meal Report:'
	conn = mysql.connect()
	cursor = conn.cursor(pymysql.cursors.DictCursor)
	cursor.execute('SELECT * FROM meal WHERE Status="Active"')
	total=cursor.rowcount
	cursor.execute('SELECT * FROM meal_status WHERE Breakfast_status ="Started"')
	row1 = cursor.fetchone()
	if row1:
		meal="breakfast"
		cursor.execute('SELECT * FROM meal WHERE Breakfast ="Ate" and Status="Active"')
		count = cursor.rowcount
	cursor = conn.cursor(pymysql.cursors.DictCursor)
	cursor.execute('SELECT * FROM meal_status WHERE Lunch_status ="Started"')
	row2 = cursor.fetchone()
	if row2:
		meal="lunch"
		cursor.execute('SELECT * FROM meal WHERE Lunch ="Ate" and Status="Active"')
		count = cursor.rowcount
	cursor = conn.cursor(pymysql.cursors.DictCursor)
	cursor.execute('SELECT * FROM meal_status WHERE Dinner_status ="Started"')
	row3 = cursor.fetchone()
	if row3:
		meal="dinner"
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute('SELECT * FROM meal WHERE Dinner ="Ate" and Status="Active"')
		count = cursor.rowcount
	conn.commit()
	not_ate=total-count
	if(session['usertype'] =='Admin'):
		return render_template('counter.html',total=total,not_ate=not_ate,count=count, meal=meal,msg=msg)
	if(session['usertype'] =='Checker'):
		return render_template('counter_2.html',total=total,not_ate=not_ate,count=count, meal=meal,msg=msg)
@app.route('/adminlogin/adddepartment', methods=['GET', 'POST'])
def add_department():	
	msg=''
	if request.method == 'POST' and 'name' in request.form and 'program' in request.form:
		name = request.form['name']
		program = request.form['program']
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM department WHERE Name=%s", name)
		row = cursor.fetchone()
		if row:
			msg = 'This department is already registered!'
		else:
			sql = "INSERT INTO department(Name,Program) VALUES(%s,%s)"
			data = (name,program)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			msg = 'The department is registered successfully!'
	return render_template('department.html', msg=msg)	
@app.route('/meal_status')
def meal_status_view():
	return render_template('meal_status.html')	
@app.route('/view')
def meal():
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM meal_status")
		rows = cursor.fetchall()
		table =Meal_status(rows)
		table.border = False
		if(session['usertype'] =='Admin'):
			return render_template('admin_view.html', table=table,msg='Wel Come to Debremarkos University Student Cafeteria System')
		else:
			return render_template('checker_view.html', table=table,msg='Wel Come to Debremarkos University Student Cafeteria System')
@app.route('/breakfast_update', methods=['POST'])
def update_meal1():
		bfast = request.form['inputBreakfast']
		if bfast=="Started" and request.method == 'POST':
			sql = "UPDATE meal_status SET Breakfast_status='Started',Lunch_status='Finished',Dinner_status='Finished'"
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql)
			conn.commit()
			query1 = "UPDATE meal SET Breakfast='Not yet'"
			conn1 = mysql.connect()
			cursor1 = conn1.cursor()
			cursor1.execute(query1)
			conn1.commit()
			flash('The Breakfast is started!')
			return redirect('/view')
		if bfast=="Finished" and request.method == 'POST':
			sql = "UPDATE meal_status SET Breakfast_status='Finished',Lunch_status='Finished',Dinner_status='Finished'"
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql)
			conn.commit()
			flash('The Breakfast is finished!')
			return redirect('/view')
@app.route('/lunch_update', methods=['POST'])
def update_meal2():
		lunch = request.form['inputLunch']
		if lunch=="Started" and request.method == 'POST':
			sql = "UPDATE meal_status SET Breakfast_status='Finished',Lunch_status='Started',Dinner_status='Finished'"
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql)
			conn.commit()
			query1 = "UPDATE meal SET Lunch='Not yet'"
			conn1 = mysql.connect()
			cursor1 = conn1.cursor()
			cursor1.execute(query1)
			conn1.commit()
			flash('The Lunch is started!')
			return redirect('/view')
		if lunch=="Finished" and request.method == 'POST':
			sql = "UPDATE meal_status SET Breakfast_status='Finished',Lunch_status='Finished',Dinner_status='Finished'"
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql)
			conn.commit()
			flash('The Lunch is finished!')
			return redirect('/view')
@app.route('/dinner_update', methods=['POST'])
def update_meal3():
		dinner = request.form['inputDinner']
		if dinner=="Started" and request.method == 'POST':
			sql = "UPDATE meal_status SET Breakfast_status='Finished',Lunch_status='Finished',Dinner_status='Started'"
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql)
			conn.commit()
			query1 = "UPDATE meal SET Dinner='Not yet'"
			conn1 = mysql.connect()
			cursor1 = conn1.cursor()
			cursor1.execute(query1)
			conn1.commit()
			flash('The dinner is started!')
			return redirect('/view')
		if dinner=="Finished" and request.method == 'POST':
			sql = "UPDATE meal_status SET Breakfast_status='Finished',Lunch_status='Finished',Dinner_status='Finished'"
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql)
			conn.commit()
			flash('The dinner is finished!')
			return redirect('/view')
if __name__ == "__main__":
    app.run(host='0.0.0.0')
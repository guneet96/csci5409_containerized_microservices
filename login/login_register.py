from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message, Mail
from random import randint


app = Flask(__name__)
app.secret_key = 'mysecret'

app.config['MONGO_DBNAME'] = 'p_db'
app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/p_db'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'cloud.group.16.proj@gmail.com'
app.config['MAIL_PASSWORD'] = 'duolc61_'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mongo = PyMongo(app)
mail = Mail(app)



@app.route('/fc/<final_flight_code>')
def index(final_flight_code):
	session['final_flight_code'] = final_flight_code
	return render_template('index.html')
	

@app.route('/login', methods=['GET','POST'])
def login():
	users = mongo.db.users
	username = request.form.get('username')
	login_user = users.find_one({'name': username})
	#changes
	print(username)
	print(login_user)
	if login_user:
		password = request.form.get('password')
		if check_password_hash(login_user['password'], password):
			email = login_user['email']
			print(email)
			otp = randint(100000, 999999)
			msg = Message('Verification Required', sender = 'cloud.group.16.proj@gmail.com', recipients = [email])
			msg.body = "Hello " + username + ", this is the multi factor authentication system of Cloud Computing Group 16. Your One-Time-Password (OTP) is " + str(otp)
			mail.send(msg)			

			session['email'] = email
			session['username'] = username
			session['otp'] = otp

			return render_template('otp.html')
			return render_template('flights.html')
#### What after login. Create a workflow.

	return render_template('login.html', login_error='Invalid username or password')



@app.route('/api/login', methods=['POST'])
def api_login():
	users = mongo.db.users
	username = request.args.get("username")
	password = request.args.get("password")
	login_user = users.find_one({'name': username})
	if login_user:
		if check_password_hash(login_user['password'], password):
			email = login_user['email']
			print(email)
			otp = randint(100000, 999999)
			msg = Message('Verification Required', sender = 'cloud.group.16.proj@gmail.com', recipients = [email])
			msg.body = "Hello " + username + ", this is the multi factor authentication system of Cloud Computing Group 16. Your One-Time-Password (OTP) is " + str(otp)
			mail.send(msg)			

			session['email'] = email
			session['username'] = username
			session['otp'] = otp
			
			return str(otp)
		else:
			return "Wrong password"
	return "User doesn't exist"








@app.route('/register', methods=['POST', 'GET'])	
def register():
	if request.method == 'POST':
		
		users = mongo.db.users
		email = request.form.get('email')
		username = request.form.get('username')
		passw = request.form.get('password')
		repeat_password = request.form.get('repeat_password')
		existing_user = users.find_one({'name' : username})
		
		if existing_user is None:
			print("chelsea")
			hash_pw = generate_password_hash(passw)
			# bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
			# users.insert({'name': username, 'password': hash_pw, 'email': email})
			otp = randint(100000, 999999)
			msg = Message('Verification Required', sender = 'cloud.group.16.proj@gmail.com', recipients = [email])
			msg.body = "Hello " + username + ", this is the multi factor authentication system of Cloud Computing Group 16. Your One-Time-Password (OTP) is " + str(otp)
			mail.send(msg)
			session['username'] =  username
			session['password'] = hash_pw
			session['email']	= email
			session['otp'] = otp
			return render_template('otp.html')
		else:
			return render_template('register.html', error_user_exists= "Sorry! Username already taken.")
	if request.method == 'GET':
		return render_template('register.html')


@app.route('/otp', methods = ['POST'])
def otp():
	# print(session['email'])
	# print(session['username'])
	users = mongo.db.users
	e_otp = request.form.get('otp')
	isuser = users.find_one({'name':session['username']})
	# print(isuser)
	if e_otp == str(session['otp']):

		if isuser is None:
			username = session['username']
			hash_pw = session['password']
			email = session['email']
			users.insert({'name': username, 'password': hash_pw, 'email': email})
			msg = Message('Verification Required', sender = 'cloud.group.16.proj@gmail.com', recipients = [email])
			msg.body = "Hello " + username + ", this is the multi factor authentication system of Cloud Computing Group 16. Your account has been verified."
			mail.send(msg)
			return render_template("login.html", success="User created")
		else:
			return "logged in. Payment.html will come here. Payment details of flight code " + str(session['final_flight_code'])

	else:
		return render_template("otp.html", error="Wrong OTP entered. Please enter correct OTP")




@app.route('/api/register', methods=['POST'])	
def api_register():
	if request.method == 'POST':
		
		users = mongo.db.users
		email = request.args.get("email")
		username = request.args.get("username")
		password = request.args.get("password")
		repeat_password = request.args.get("repeat_password")
		if password != repeat_password:
			return "password don't match"
		# email = request.form.get('email')
		# username = request.form.get('username')
		# passw = request.form.get('password')
		# repeat_password = request.form.get('repeat_password')
		existing_user = users.find_one({'name' : username})
		
		if existing_user is None:
			print("chelsea")
			hash_pw = generate_password_hash(password)
			otp = randint(100000, 999999)
			msg = Message('Verification Required', sender = 'cloud.group.16.proj@gmail.com', recipients = [email])
			msg.body = "Hello " + username + ", this is the multi factor authentication system of Cloud Computing Group 16. Your One-Time-Password (OTP) is " + str(otp)
			mail.send(msg)
			session['username'] =  username
			session['password'] = hash_pw
			session['email']	= email
			session['otp'] = otp
			return str(otp)
		else:
			return "Username taken."


@app.route('/api/otp', methods = ['POST'])
def api_otp():
	users = mongo.db.users
	e_otp = request.args.get("otp")
	isuser = users.find_one({'name':session['username']})

	if e_otp == str(session['otp']):
		
		if isuser is None:
			username = session['username']
			hash_pw = session['password']
			email = session['email']
			users.insert({'name': username, 'password': hash_pw, 'email': email})
			msg = Message('Verification Required', sender = 'cloud.group.16.proj@gmail.com', recipients = [email])
			msg.body = "Hello " + username + ", this is the multi factor authentication system of Cloud Computing Group 16. Your account has been verified."
			mail.send(msg)
			return "User created"
		else:
			return "authenticated"
	else:
		return "Wrong OTP entered. Please enter correct OTP"



if __name__ == '__main__':
	app.run(debug=True)






# No session alternate code
# from flask import Flask, render_template, request, redirect
# from flask_pymongo import PyMongo
# from pymongo import MongoClient
# import datetime
# import json
# import os

# login = Flask(__name__)


# login.config['MONGO_URI'] = "mongodb://localhost:27017/travel_app"
# login.config['MONGO_DBNAME'] = "travel_app"
# mongo = PyMongo(login)
# travel_app = mongo.db

# @login.route('/', methods=['GET','POST'])
# def main():
# 	return render_template('login.html')


# @login.route('/login_res', methods=['GET','POST'])
# def login_res():
# 	uname = request.form.get("uname")
# 	password = request.form.get("password")
# 	users = travel_app["users"]

# 	auth = users.find_one({"uname": uname, "password": password})
# 	print(auth)
# 	if auth is not None:
# 		return redirect("http://localhost:5001/"+uname, code=302)

# 	else:
# 		return render_template('login.html', error="Username or password is incorrect.")



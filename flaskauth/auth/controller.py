from werkzeug.security import generate_password_hash, check_password_hash
from flaskauth import app
from flaskauth.auth import auth
from flask import request, make_response, jsonify, g, url_for
from datetime import timedelta, datetime as dt
from flaskauth.models.user import db, User, RefreshToken, UserSchema
from sqlalchemy.exc import SQLAlchemyError
from cerberus import Validator, errors
from flaskauth.service.errorhandler import CustomErrorHandler
from flaskauth.queue.email import send_email
from flaskauth.service.tokenservice import otp, secret, jwtEncode
from flaskauth.service.api_response import success, error


@auth.route("/register", methods=['POST'])
def register():
	schema = {
		'email': {
			'type': 'string',
			'required': True,
			'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
		}, 
		'password': {
			'type': 'string', 
			'required': True,
			'min': 6
			
		},
		'first_name': {
			'type': 'string',
			'required': True,
			'min': 2
			
		},
		'last_name': {
			'type': 'string',
			'required': True, 
			'min': 2,
		}
	}

	v = Validator(schema, error_handler=CustomErrorHandler)
	form_data = request.get_json()
	args = request.args

	if(v.validate(form_data, schema) == False):
		return v.errors

	
	email = form_data['email']
	verification_code = otp(7)

	try:
		new_user = User(
			email= form_data['email'],
			password = generate_password_hash(form_data['password']),
			first_name= form_data['first_name'],
			last_name= form_data['last_name'],
			verification_code = secret(verification_code),
		)
		db.session.add(new_user)
		db.session.commit()

	except SQLAlchemyError as e:
		# error = str(e.__dict__['orig'])
		message = str(e)
		return error({}, message, 400)
		# return make_response(jsonify({'error': error}), 400)


	# Send verification email
	appName = app.config["APP_NAME"].capitalize()

	email_data = {
	'subject': 'Account Verification on ' + appName, 
	'to': email,
	'body': '',
	'name': form_data['first_name'],
	'callBack': verification_code,
	'template': 'verification_email'
	}

	send_email.delay(email_data)

	message = 'Registration Successful, check your email for OTP code to verify your account'
	return success({}, message, 200)


@auth.route("/verify", methods=['POST'])
def verifyAccount():
	schema = {
		'otp': {
			'type': 'string', 
			'required': True,
			'min': 6
			
		},
	}
	v = Validator(schema, error_handler=CustomErrorHandler)
	form_data = request.get_json()

	if(v.validate(form_data, schema) == False):
		return v.errors

	otp = form_data['otp']
	hash_otp = secret(otp)
	user = User.query.filter_by(verification_code = hash_otp).first()

	if not user:
		message = 'Failed to verify account, Invalid OTP Code'
		return error({},message, 401)


	user.verification_code = None
	user.is_verified = True
	db.session.commit()


	message = 'Verification Successful! Login to your account'
	return success({}, message, 200)


@auth.route("/login", methods=['POST'])
def login():
	schema = {
		'email': {
			'type': 'string',
			'required': True,
			'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
		}, 
		'password': {
			'type': 'string', 
			'required': True,
			'min': 6
			
		},
	}
	v = Validator(schema, error_handler=CustomErrorHandler)
	form_data = request.get_json()

	user = User.query.filter_by(email =  form_data['email']).first()

	if not user:
		message = 'Login failed! Invalid account.'
		return error({}, message, 401)

	if not check_password_hash(user.password, form_data['password']):
		message = 'Login failed! Invalid password.'
		return error({}, message, 401)

	return authenticated(user)


def authenticated(user: User):
	refresh_token = secret()

	try:
		refreshToken = RefreshToken(
				user_id = user.id,
				token = refresh_token,
				expired_at = dt.utcnow() + timedelta(minutes = int(app.config['REFRESH_TOKEN_DURATION']))
			)
		db.session.add(refreshToken)
		db.session.commit()

	except SQLAlchemyError as e:
		# error = str(e.__dict__['orig'])
		message = str(e)
		return error({}, message, 400)
	# del user['password']
	user_schema = UserSchema()
	data = {
		"token": jwtEncode(user),
		"refresh_token": refresh_token,
		"user": user_schema.dump(user)
	}
	message = "Login Successful, Welcome Back"
	return success(data, message, 200)

"""
Get Refresh Token
"""
@auth.route("/refresh", methods=['POST'])
def refreshToken():
	schema = {
		'refresh_token': {
			'type': 'string',
			'required': True,
		},
	}
	v = Validator(schema, error_handler=CustomErrorHandler)
	form_data = request.get_json()
	now = dt.utcnow()
	refresh_token = RefreshToken.query.filter(token == form_data['refresh_token'], expired_at >= now).first()

	if not refresh_token:
		message = "Token expired, please login"
		return error({}, message, 401)

	user =  User.query.filter_by(id = refresh_token.user_id).first()

	if not user:
		message = "Invalid User"
		return error({}, message, 403)

	data = {
		"token": jwtEncode(user),
		"id": user.id
	}
	message = "Token Successfully refreshed"
	return success(data, message, 200)
	




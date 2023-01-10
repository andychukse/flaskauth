from flaskauth import app
from flask import request
from flaskauth.models.user import db, User, UserSchema
from flaskauth.service.authservice import auth_required
from flaskauth.service.api_response import success, error
from cerberus import Validator, errors

@app.route("/users/profile", methods=['GET'])
@auth_required
def profile(user: User):
	args = request.args

	user_schema = UserSchema()
	data = {

		"user": user_schema.dump(user)
	}
	message = "Profile Details"
	return success(data, message, 200)


"""
Update User Profile
"""
@app.route("/users/edit", methods=['POST'])
@auth_required
def update(user: User):
	schema = {
		'country_id': {
			'type': 'integer', 
			'required': True,
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

	v = Validator(schema)
	form_data = request.get_json()
	args = request.args

	user.first_name = form_data['first_name']
	user.last_name = form_data['last_name']
	user.country_id = form_data['country_id']

	
	db.session.commit()

	user_schema = UserSchema()
	data = {

		"user": user_schema.dump(user)
	}
	message = "Profile Updated"
	return success(data, message, 200)
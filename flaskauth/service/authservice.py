from functools import wraps
from flask import request
from flaskauth.models.user import User
from flaskauth.service.tokenservice import jwtDecode
from flaskauth.service.api_response import success, error

def auth_required(f):
	@wraps(f)
	def decorator(*args, **kwargs):
		token = None
		if 'Authorization' in request.headers:
			token = request.headers['Authorization'][7:]
		if not token:
			return error({}, 'Authorization token required', 401)
		try:
			data = jwtDecode(token)
			user = User.query.filter_by(id=data['sub']).first()
		except:
			return error({}, 'Invalid token', 401)
		return f(user, *args, **kwargs)
	return decorator


def auth_optional(f):
	@wraps(f)
	def decorator(*args, **kwargs):
		token = None
		user = None
		if 'Authorization' in request.headers:
			token = request.headers['Authorization'][7:]
			try:
				data = jwtDecode(token)
				user = User.query.filter_by(id=data['sub']).first()
			except:
				return error({}, 'Invalid token', 401)
		return f(user, *args, **kwargs)
	return decorator
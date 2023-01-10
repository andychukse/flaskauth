from flask import make_response, jsonify

def success(data, message: str=None, code: int = 200):
	data['status'] = 'Success'
	data['message'] = message
	data['success'] = True

	return make_response(jsonify(data), code)


def error(data, message: str, code: int):
	data['status'] = 'Error'
	data['message'] = message
	data['success'] = False

	return make_response(jsonify(data), code)
from cerberus import errors

class CustomErrorHandler(errors.BasicErrorHandler):
	messages = errors.BasicErrorHandler.messages.copy()
	messages[errors.REGEX_MISMATCH.code] = 'Invalid Email!'
	messages[errors.REQUIRED_FIELD.code] = '{field} is required!'
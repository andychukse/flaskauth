from flaskauth.models.user import db, User
import jwt
import random, string, hashlib
from flaskauth import app
from datetime import datetime, timedelta


def jwtEncode(user: User) -> str:
	payload = {
            'sub': user.id,
            'iat': datetime.utcnow(),
            'exp' : datetime.utcnow() + timedelta(minutes = int(app.config['JWT_DURATION']))
        }
	return jwt.encode(payload, app.config['SECRET_KEY'], algorithm="HS256")

def jwtDecode(token) -> dict:
	decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithm="HS256")
	print(decoded)
	return decoded


def secret(code=None):
	if not code:
		code = str(datetime.utcnow()) + otp(5)
	return hashlib.sha224(code.encode("utf8")).hexdigest()


def otp(total):
	return str(''.join(random.choices(string.ascii_uppercase + string.digits, k=total)))



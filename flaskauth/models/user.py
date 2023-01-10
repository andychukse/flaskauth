"""User models."""
from datetime import datetime
from flaskauth.models.base_model import BaseModel, db, ma
from flaskauth.models.country import Country

class User(db.Model, BaseModel):
	__tablename__ = "users"
	id = db.Column(db.BigInteger, primary_key=True)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(200), nullable=True)
	first_name = db.Column(db.String(200), nullable=False)
	last_name = db.Column(db.String(200), nullable=False)
	avatar = db.Column(db.String(250), nullable=True)
	country_id = db.Column(db.Integer, db.ForeignKey('countries.id', onupdate='CASCADE', ondelete='SET NULL'),
        nullable=True)
	is_verified = db.Column(db.Boolean, default=False, nullable=False)
	verification_code = db.Column(db.String(200), nullable=True)
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)
	deleted_at = db.Column(db.DateTime, nullable=True)
	country = db.relationship('Country', backref=db.backref('users', lazy=True))
	refresh_tokens = db.relationship('RefreshToken', backref=db.backref('users', lazy=True))

	def __repr__(self):
		return '<User %r>' % self.email



class RefreshToken(db.Model, BaseModel):
	__tablename__ = "refresh_tokens"
	id = db.Column(db.BigInteger, primary_key=True)
	token = db.Column(db.String(200), unique=True, nullable=False)
	user_id = db.Column(db.BigInteger, db.ForeignKey(User.id, onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False)
	expired_at = db.Column(db.DateTime, nullable=False)
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)

class UserSchema(ma.Schema):
    class Meta:
    	model = User
    	include_fk = True
    	# exclude = ("password",)
    	fields = ('id', 'email', 'first_name', 'last_name', 'avatar', 'country_id')

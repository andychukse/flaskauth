import os
from flask import Flask, make_response, jsonify
from jsonschema import ValidationError



def create_app(test_config=None):
	app = Flask(__name__, instance_relative_config=True)

	if test_config is None:
		# load the instance config, if it exists, when not testing
		# app.config.from_pyfile('config.py', silent=True)
		app.config.from_object('config.ProductionConfig')
	else:
		# load the test config if passed in
		# app.config.from_mapping(test_config)
		app.config.from_object('config.DevelopmentConfig')

	# ensure the instance folder exists
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	return app

	


app = create_app(test_config=None)

from flaskauth.models.base_model import db, BaseModel
db.init_app(app)

from flaskauth.models.user import User


from celery import Celery

def make_celery(app):
    celery = Celery(app.name)
    celery.conf.update(app.config["CELERY_CONFIG"])

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(app)

from flaskauth.auth import auth
from flaskauth.queue import queue
from flaskauth.controllers import user


app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(queue)

@app.route("/hello")
def hello_message() -> str:
    return jsonify({"message": "Hello It Works"})


def initiate_app(app):
	db.init_app(app)


@app.errorhandler(400)
def bad_request(error):
    if isinstance(error.description, ValidationError):
        original_error = error.description
        return make_response(jsonify({'error': original_error.message}), 400)
    # handle other "Bad Request"-errors
    # return error
    return make_response(jsonify({'error': error.description}), 400)

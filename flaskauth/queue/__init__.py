from flask import Blueprint

queue = Blueprint("queue", __name__)

from flaskauth.queue import email
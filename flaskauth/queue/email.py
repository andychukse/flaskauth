from flaskauth.queue import queue
from flask import render_template
from flaskauth import app, celery
from flask_mail import Mail, Message

# app = create_app()


mail = Mail(app)

# celery = Celery(app.name, broker='redis://localhost:6379/0')


@celery.task
def send_email(email_data):
    msg = Message(email_data['subject'],
                  sender=app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[email_data['to']])
    appName = app.config["APP_NAME"].capitalize()
    msg.body = render_template(email_data['template']+'.txt', appName=appName, **email_data)
    msg.html = render_template(email_data['template']+'.html', appName=appName, **email_data)
    with app.app_context():
        mail.send(msg)


from threading import Thread
from flask import current_app, render_template
from flask_mail import Message

from app.auth import mail

def send_async_email(app, msg):
    """Send an email asynchronously using Flask-Mail.

        Args:
            app (Flask): The Flask application object.
            msg (Message): The email message to be sent.

        Returns:
            None

        Raises:
            None
    """
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    """Sends an email asynchronously using flask-Mail.

    Args:
        to (str): The email address of the recipient.
        subject (str): The subject of the email.
        template (str): The name of the email template.

    Returns:
        Thread: The thread function representing the asynchrous email sending.
    Raise:
        None
    """
    app = current_app._get_current_object()
    message = Message(app.config['MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                      sender=app.config['MAIL_DEFAULT_SENDER'], recipients=[to])
    message.body = render_template(template + '.txt', **kwargs)
    message.html = render_template(template + '.html', **kwargs)
    thread = Thread(target=send_async_email, args=[app, message])
    thread.daemon(True)
    thread.start()
    return thread



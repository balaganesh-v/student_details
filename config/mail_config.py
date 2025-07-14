from flask_mail import Mail
import os
from dotenv import load_dotenv

load_dotenv()


mail = Mail()

def mail_connection(app):
    app.config.update(
        MAIL_SERVER=os.getenv('MAIL_SERVER'),
        MAIL_PORT=int(os.getenv('MAIL_PORT')),
        MAIL_USE_TLS=os.getenv('MAIL_USE_TLS') == 'True',
        MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
        MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
        MAIL_DEFAULT_SENDER=os.getenv('MAIL_USERNAME'),
    )

    mail.init_app(app)
    return mail

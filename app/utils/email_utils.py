from flask_mail import Message
from flask import url_for
from config.mail_config import mail

def send_login_email(data):
    name = data["user_name"]
    email = data["user_email"]
    password = data["user_password"]
    role = data["user_role"]

    msg = Message(
        subject=f"Welcome {role}!",
        recipients=[email],
        body=f"""Hello {name},

Your login details:

Name:{name}
Email: {email}
Password: {password}
Role: {role}

Thank you.
"""
    )
    try:
        mail.send(msg)  # ✅ Proper and safe
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")


def send_reset_email(to_name,to_email, token):
    reset_link = url_for('student_login.reset_password', token=token, _external=True)

    msg = Message(
        subject="Password Reset Request",
        recipients=[to_email],
        body=f"""Hello {to_name},

We received a request to reset your password.

Click the link below to reset it:
{reset_link}

If you did not request this, please ignore this email.

Thanks,
Your Support Team
"""
    )

    try:
        mail.send(msg)
        print("Password reset email sent successfully.")
    except Exception as e:
        print(f"Error sending reset email: {e}")


def send_new_password_to_email(to_name, to_email, new_password):
    msg = Message(
        subject="Your New Password",
        recipients=[to_email],
        body=f"""Hello {to_name},

Your password has been successfully reset.

Here is your new password: {new_password}

Please keep it safe and consider logging in and changing it again immediately.

If you did not request this password reset, please contact support.

Thank you,
Your School Team
"""
    )
    try:
        mail.send(msg)
        print("Password reset email sent successfully.")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

def send_code_mail(user, code):
    name = user["user_name"]
    to_email = user["user_email"]

    msg = Message(
        subject=f"Hello {name}, Here is your verification code",
        recipients=[to_email],
        body=f"""Hi {name},

You have requested a verification code.

Your code is: {code}

Please use this code to complete your action.

Thank you.
"""
    )
    try:
        mail.send(msg)
        print("Password reset email sent successfully.")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

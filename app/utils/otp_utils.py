# utils/otp_helper.py
import pyotp
import qrcode
import base64
from io import BytesIO

def generate_secret():
    return pyotp.random_base32()

def generate_qr_url(email, secret):
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(name=email, issuer_name="SchoolSync")
    qr = qrcode.make(uri)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    base64_img = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{base64_img}"

def verify_otp(secret_key, user_input_otp):
    totp = pyotp.TOTP(secret_key)
    return totp.verify(user_input_otp)

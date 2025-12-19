import cloudinary
import os
from dotenv import load_dotenv

load_dotenv()

def init_cloudinary():
    return cloudinary.config(
        cloud_name=os.getenv("CLOUD_NAME"),
        api_key=os.getenv("API_KEY"),
        api_secret=os.getenv("API_SECRET"),
        secure=True
    )
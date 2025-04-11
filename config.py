from dotenv import load_dotenv
load_dotenv()
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback_dev_secret')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

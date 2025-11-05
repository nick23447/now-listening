import os
from typing import Optional

class Config:
    SECRET_KEY: Optional[str] = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI: Optional[str] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER: Optional[str] = 'smtp.gmail.com'
    MAIL_PORT: int = 587
    MAIL_USE_TLS: bool = True
    MAIL_USERNAME: Optional[str] = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD: Optional[str] = os.environ.get('EMAIL_PASS')

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  
    WTF_CSRF_ENABLED = False  
    SECRET_KEY = 'test-secret-key'  


import os

class Config:
    SECRET_KEY = "your_secret_key_here"
    MONGO_URI = "mongodb://localhost:27017/flask_mongo_app"
    
    # Flask-Mail Configuration
    MAIL_SERVER = "sandbox.smtp.mailtrap.io"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "5d0c590671c2c6"
    MAIL_PASSWORD = "fc3c94f4e6460a"
    MAIL_DEFAULT_SENDER = "noreply@yourdomain.com"
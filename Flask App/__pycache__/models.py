from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt

mongo = PyMongo()
bcrypt = Bcrypt()

def init_db(app):
    mongo.init_app(app)
    bcrypt.init_app(app)

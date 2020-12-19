from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)

# MAKE ENVIRONMENT VARIABLE EVENTUALLY
app.config['SECRET_KEY'] = 'removed for privacy'
app.config['SQLALCHEMY_DATABASE_URI'] = 'removed for privacy'
bcrypt = Bcrypt(app)

from cmlz_tutoring import routes

import os
from datetime import *
from pytz import timezone
uae = timezone('Asia/Dubai')

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_qrcode import QRcode
from flask_bcrypt import Bcrypt

project_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_url_path='/static')

database_file = "sqlite:///{}".format(os.path.join(project_dir, "client.db"))

# Secret Key is necessary to Use Forms and Sessions
app.config['SECRET_KEY'] = 'demo032024'

app.config['SQLALCHEMY_DATABASE_URI'] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# set optional bootswatch theme - bootswatch.com/3/
app.config['FLASK_ADMIN_SWATCH'] = 'flatly'
app.config['FLASK_ADMIN_FLUID_LAYOUT'] = True

db = SQLAlchemy(app)
qrcode = QRcode(app)
bcrypt = Bcrypt(app)

custom_data = {
    "page_title" : 'Demo: Training and Development',
    "logo" : "/static/images/company_logo.png"
    }


from webapp import routes


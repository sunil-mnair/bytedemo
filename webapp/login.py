from webapp import app
from flask_login import LoginManager

login_manager = LoginManager(app)

# Specifies to login_required the login route function
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# login_manager.init_app(app)
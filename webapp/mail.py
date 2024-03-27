from webapp import app
from flask_mail import Mail

# Configuration for mail relay
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'bytesizetrainings@gmail.com'
app.config['MAIL_PASSWORD'] = 'npmtpbmxksmfwdaq'
app.config['MAIL_DEFAULT_SENDER'] = 'bytesizetrainings@gmail.com'

mail = Mail(app)
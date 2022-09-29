from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vdzvzjvcjvc'
from ml.routes import route
from ml.error import errors
app.register_blueprint(route)



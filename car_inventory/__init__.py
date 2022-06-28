from flask import Flask
from .site.routes import site
from .authentication.routes import auth
from config import Config

app = Flask(__name__)

app.register_blueprint(site)
app.register_blueprint(auth)

app.config.from_object(Config)
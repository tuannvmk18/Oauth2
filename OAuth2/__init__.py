import os

from authlib.integrations.flask_client import OAuth
from flask import Flask
from dotenv import load_dotenv

import logging
import sys

load_dotenv()
oauth = OAuth()


def configure_logger():
    log = logging.getLogger('authlib')
    log.addHandler(logging.StreamHandler(sys.stdout))
    log.setLevel(logging.DEBUG)
    return log


def create_app():
    log = configure_logger()
    app = Flask(__name__)

    app.secret_key = os.getenv("APP_SECRET_KEY")

    oauth.init_app(app)
    oauth.register(name='google',
                   client_id=os.getenv("GOOGLE_CLIENT_ID"),
                   client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
                   access_token_url='https://accounts.google.com/o/oauth2/token',
                   access_token_params=None,
                   authorize_url='https://accounts.google.com/o/oauth2/auth',
                   authorize_params=None,
                   api_base_url='https://www.googleapis.com/oauth2/v1/',
                   client_kwargs={'scope': 'openid email profile'})

    from .route import auth
    app.register_blueprint(auth, url_prefix="/auth")

    from .ultis import login_required

    # Demo login required
    @app.route("/")
    @login_required
    def say_hello():
        return f"Hello, world!"

    return app

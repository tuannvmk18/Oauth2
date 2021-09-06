from OAuth2 import oauth
from flask import Blueprint, url_for, redirect, session
from .ultis import login_required

auth = Blueprint('', __name__)


@auth.route('/login')
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@auth.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    response = google.get('userinfo')
    user_info = response.json()

    session['profile'] = user_info
    session.permanent = True

    return redirect('http://localhost:5000/')


@auth.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('http://localhost:5000/')

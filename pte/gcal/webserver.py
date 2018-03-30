#!/usr/bin/env python
import os
import base64
from urllib.parse import urlencode
import flask
import requests
from pte import settings
from pte.gcal.access import set_refresh_token


app = flask.Flask(__name__)
state = None


@app.route("/")
def index():
    global state
    state = base64.b64encode(os.urandom(12)).decode('ascii')
    url = 'https://accounts.google.com/o/oauth2/v2/auth'
    oauth_scope = 'https://www.googleapis.com/auth/calendar'
    params = {
        'client_id': settings.GCAL_OAUTH_CLIENT_ID,
        'redirect_uri': settings.GCAL_OAUTH_REDIRECT_URI,
        'scope': oauth_scope,
        'access_type': 'offline',
        'state': state,
        'response_type': 'code',
        'prompt': 'consent select_account',
    }
    full_url = f'{url}?{urlencode(params)}'
    return flask.redirect(full_url)


@app.route("/redirect")
def redirect():
    auth_code = flask.request.args.get('code')
    resp_state = flask.request.args.get('state')
    if auth_code is None:
        return flask.abort(400)
    if state is None or resp_state != state:
        return flask.abort(400)

    url = 'https://www.googleapis.com/oauth2/v4/token'
    data = {
        'code': auth_code,
        'client_id': settings.GCAL_OAUTH_CLIENT_ID,
        'client_secret': settings.GCAL_OAUTH_CLIENT_SECRET,
        'redirect_uri': settings.GCAL_OAUTH_REDIRECT_URI,
        'grant_type': 'authorization_code',
    }

    resp = requests.post(url, data=data)
    if resp.status_code != 200:
        return resp.text, 'application/json'

    set_refresh_token(resp.json()['refresh_token'])
    return 'ok'


def open_browser():
    import threading

    def _target():
        import time
        import webbrowser
        print('Opening http://127.0.0.1:5000 ...', end='')
        time.sleep(2)
        webbrowser.open('http://127.0.0.1:5000')
        print('ok')

    th = threading.Thread(target=_target)
    th.start()


if __name__ == '__main__':
    open_browser()
    app.run('localhost', 5000)



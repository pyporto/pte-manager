import requests
from pte import settings


def get_access_token():
    url = 'https://www.googleapis.com/oauth2/v4/token'
    data = {
        'refresh_token': get_refresh_token(),
        'client_id': settings.GCAL_OAUTH_CLIENT_ID,
        'client_secret': settings.GCAL_OAUTH_CLIENT_SECRET,
        'grant_type': 'refresh_token',
    }
    resp = requests.post(url, data=data)
    resp.raise_for_status()
    return resp.json()['access_token']


def get_refresh_token():
    with open(settings.GCAL_OAUTH_REFRESH_TOKEN_FILE) as fd:
        return fd.read().strip()


def set_refresh_token(token):
    with open(settings.GCAL_OAUTH_REFRESH_TOKEN_FILE, 'wt') as fd:
        fd.write(token)

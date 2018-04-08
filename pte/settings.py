"""
Common configuration settings.

They are safe to commit, because essentially it doesn't make sense to have more
than one porto-tech-events instance with different settings, and besides,
there's nothing secret here.

All secret keys are stored in the .env file which is excluded from the repo.
"""
import os
import dotenv

dotenv.load_dotenv(dotenv.find_dotenv())

MODEL_STORAGE_ROOT = '../porto-tech-events'
MEETUP_API_KEY = os.environ['MEETUP_API_KEY']
EVENTBRITE_API_TOKEN = os.environ['EVENTBRITE_API_TOKEN']

GCAL_ID = 'nldp40d05lh6muiv7mqh4crmno@group.calendar.google.com'
GCAL_OAUTH_REDIRECT_URI = 'http://127.0.0.1:5000/redirect'
GCAL_OAUTH_CLIENT_ID = os.environ['GCAL_OAUTH_CLIENT_ID']
GCAL_OAUTH_CLIENT_SECRET = os.environ['GCAL_OAUTH_CLIENT_SECRET']
GCAL_OAUTH_REFRESH_TOKEN_FILE = 'gcal_refresh_token.txt'

# Get a new token at
# https://developers.facebook.com/tools/explorer/
FACEBOOK_ACCESS_TOKEN = os.environ['FACEBOOK_ACCESS_TOKEN']
FACEBOOK_PAGES = [
    'techinporto',
    'portoio',
    'makeorbreak.io',
    'scaleupporto',
    'tedxporto',
    'PortoTecHub',
    'datascienceportugal',
    'helloworldconf',
    'GDGPorto',
    'agileconnect',
    'DRiP.pt',
    'XpConference',
    'madgamejam',
    'techdaysaveiro',
    'nei.isep',
    'commitporto',
    'AlumniEI',
]

MEETUP_COMMUNITIES = [
    'pyporto',
    'Disruptive-Data-Science',
    'Disruptive-Tech-Tools',
    'devopsporto',
    'portocodes',
    'datascienceportugal',
    'Merge-Porto',
    'Bitcoin-Altcoins-Blockchain',
    'Porto-Big-Data',
    'PortoStartupCoffee',
    'Docker-Porto',
    'Fullstack-Porto',
    'oposecurity',
    'Porto-i-o-events',
    'opo-js',
    'Lambda-PT',
    'drupal-porto',
    'PortoUX',
    'i-o-Sessions',
    '0xOPOSEC',
    'Agile-Connect-Porto',
    'WP-Porto',
    'GameDevMeetPorto',
    'GDG-Porto',
    'PHPorto',
    'Elastic-Portugal',
    'CocoaHeads-Porto',
    'Porto-on-Rails',
    'Papers-We-Love-Porto',
    'iosporto',
    'Disruptive-Go',
]


ICAL_FEEDS = [
    ('scaleupporto', 'http://scaleupporto.pt/events/?ical=1'),
]

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
MISC_GCAL_ID = 'r82gmulo04i3466213gpau424k@group.calendar.google.com'
GCAL_OAUTH_REDIRECT_URI = 'http://127.0.0.1:5000/redirect'
GCAL_OAUTH_CLIENT_ID = os.environ['GCAL_OAUTH_CLIENT_ID']
GCAL_OAUTH_CLIENT_SECRET = os.environ['GCAL_OAUTH_CLIENT_SECRET']
GCAL_OAUTH_REFRESH_TOKEN_FILE = 'gcal_refresh_token.txt'

# Get a new token at
# https://developers.facebook.com/tools/explorer/
FACEBOOK_ACCESS_TOKEN = os.environ['FACEBOOK_ACCESS_TOKEN']
FACEBOOK_PAGES = [
    'AlumniEI',
    'DRiP.pt',
    'GDGPorto',
    'PortoTecHub',
    'XpConference',
    'agileconnect',
    'commitporto',
    'datascienceportugal',
    'helloworldconf',
    'madgamejam',
    'makeorbreak.io',
    'nei.isep',
    'portoio',
    'scaleupporto',
    'techdaysaveiro',
    'techinporto',
    'tedxporto',
]

MEETUP_COMMUNITIES = [
    '0xOPOSEC',
    'Agile-Connect-Porto',
    'Android-Peer-Lab',
    'Bitcoin-Altcoins-Blockchain',
    'Chain-in-Blockchain-Cryptocurrency-Conference',
    'CocoaHeads-Porto',
    'Digital-Hub-Porto',
    'Disruptive-Data-Science',
    'Disruptive-Go',
    'Disruptive-Tech-Tools',
    'Docker-Porto',
    'Elastic-Portugal',
    'Fullstack-Porto',
    'GDG-Porto',
    'GameDevMeetPorto',
    'Lambda-PT',
    'Merge-Porto',
    'PHPorto',
    'Papers-We-Love-Porto',
    'Porto-Big-Data',
    'Porto-Data',
    'Porto-i-o-events',
    'Porto-on-Rails',
    'PortoStartupCoffee',
    'PortoUX',
    'ProductTank-Porto',
    'React-Native-Portugal',
    'WP-Porto',
    'datascienceportugal',
    'devopsporto',
    'drupal-porto',
    'i-o-Sessions',
    'iosporto',
    'opo-js',
    'opoios',
    'oposecurity',
    'portocodes',
    'pyporto',
]


ICAL_FEEDS = [
    ('scaleupporto', 'http://scaleupporto.pt/events/?ical=1'),
]

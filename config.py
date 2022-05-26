import os
from urllib.parse import urljoin


TOKEN = os.getenv('TELEGRAM_TOKEN', '')

WEBHOOK_HOST = 'https://gwmbinancebot.herokuapp.com/'
WEBHOOK_URL_PATH = '/webhook/' + TOKEN
WEBHOOK_URL = urljoin(WEBHOOK_HOST, WEBHOOK_URL_PATH)

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.environ.get('PORT')

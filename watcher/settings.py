import os
from decouple import config


def path(*x):
    return os.path.join(BASE_DIR, *x)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONSUMER_KEY = config('CONSUMER_KEY')
CONSUMER_SECRET = config('CONSUMER_SECRET')

ACCESS_TOKEN = config('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = config('ACCESS_TOKEN_SECRET')

FAVORITES_FILE = path('favorites.txt')

BROKER_URL = config('BROKER_URL', default='amqp://guest:guest@localhost:5672')

RPC_CONFIG = {
    'AMQP_URI': BROKER_URL
}

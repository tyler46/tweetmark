import logging

from decouple import config
from logging.handlers import TimedRotatingFileHandler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = 'logs/services.log'
LOG_FILE_PATH = os.path.join(BASE_DIR, LOG_FILE)


DEBUG = config('DEBUG', cast=bool)
LOG_LEVEL = config('LOG_LEVEL', default=logging.DEBUG)

# Mailgun settings
SANDBOX_API_URL = config('SANDBOX_API_URL')
MAILGUN_API_KEY = config('MAILGUN_API_KEY')
SENDER = config('SENDER')
RECEIVER = config('RECEIVER')

# Remote service
API_URL = config('API_URL')

# logging settings
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

file_logger = TimedRotatingFileHandler(LOG_FILE_PATH, when='D')
file_logger.setFormatter(formatter)

logger = logging.getLogger('services')
logger.setLevel(logging.getLevelName(LOG_LEVEL))
logger.addHandler(file_logger)

if DEBUG:
    console_logger = logging.StreamHandler()
    console_logger.setFormatter(formatter)
    logger.addHandler(console_logger)

import os
from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']
VERIFY_URL = os.getenv('VERIFY_URL_DEV', '')
PASS_RESET_URL = os.getenv('PASS_RESET_URL_DEV', '')

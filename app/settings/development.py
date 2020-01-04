import os
from .base import *

DEBUG = True

ALLOWED_HOSTS = [os.getenv('ALLOWED_LOCAL_HOST','')]
VERIFY_URL = os.getenv('VERIFY_URL_DEV', '')
PASS_RESET_URL = os.getenv('PASS_RESET_URL_DEV', '')
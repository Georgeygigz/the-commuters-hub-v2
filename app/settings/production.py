import os
from .base import *

DEBUG = False

ALLOWED_HOSTS = [os.getenv('ALLOWED_LOCAL_HOST','')]
PASS_RESET_URL = os.getenv('PASS_RESET_URL_PROD', '')
VERIFY_URL = os.getenv('VERIFY_URL_PROD', '')

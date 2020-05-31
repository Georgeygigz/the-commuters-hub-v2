import os

DEBUG = False

ALLOWED_HOSTS = ['*']
PASS_RESET_URL = os.getenv('PASS_RESET_URL_PROD', '')
VERIFY_URL = os.getenv('VERIFY_URL_PROD', '')

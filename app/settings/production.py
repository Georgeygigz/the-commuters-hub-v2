import os

DEBUG = False

ALLOWED_HOSTS = ['0.0.0.0', os.getenv('ALLOWED_LOCAL_HOST','')]
PASS_RESET_URL = os.getenv('PASS_RESET_URL_PROD', '')
VERIFY_URL = os.getenv('VERIFY_URL_PROD', '')

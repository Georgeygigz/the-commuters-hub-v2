import os
from .base import *

DEBUG = True

ALLOWED_HOSTS = [os.getenv('ALLOWED_LOCAL_HOST','')]
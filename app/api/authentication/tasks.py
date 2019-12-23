import logging
from django.core.mail import send_mail
from app import celery_app

@celery_app.task(name="send mail")
def send_mail_(*args, **kwargs):
    """
    Handle sending of mails to users
    Args:
        args (list): a list of possible arguments
        kwargs (dict): key worded arguments
    Return:
        None
    """
    try:
        send_mail(**kwargs)
    except Exception as e:
        logging.warning(e)


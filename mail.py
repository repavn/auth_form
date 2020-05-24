import logging
import threading

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def send_mail_in_thread(subject, message, email):

    def mail_send():
        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
        except Exception as e:
            logger.warning(str(e))

    t = threading.Thread(target=mail_send, daemon=True)
    t.start()
    logger.warning(f'{email} - sending in thread')

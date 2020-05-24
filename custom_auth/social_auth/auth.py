from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User

from custom_auth.constants import THANKS, WELCOME
from custom_auth.models import UserInfo
from mail import send_mail_in_thread


def register_user_from_socials(request, user_info):
    username = user_info.get('name', '').replace(' ', '_')
    email = user_info.get('email')
    if not username:
        return
    user = User.objects.filter(username__iexact=username).first()
    if not user:
        password = User.objects.make_random_password()
        user = User.objects.create_user(username, email, password,
                                        first_name=user_info.get('given_name'),
                                        last_name=user_info.get('family_name'), is_active=True)
        UserInfo.objects.create(user=user)
        if email:
            send_mail_in_thread(THANKS, WELCOME, email)
        login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])
    else:
        login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])
    return

import logging
from django import forms
from django.contrib.auth.models import User

from custom_auth.costants import ACTION_REGISTER, ACTION_LOGIN
from custom_auth.models import UserInfo
from custom_auth.validators import name_validator

logger = logging.getLogger(__name__)


class UserForm(forms.Form):
    first_name = forms.CharField(required=True, validators=(name_validator,))
    last_name = forms.CharField(required=True, validators=(name_validator,))
    password = forms.CharField(required=True)
    confirm_password = forms.CharField(required=True)
    action_type = forms.CharField(required=False)
    username = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    receive_news = forms.BooleanField(required=False)

    def _validate_passwords(self, password, confirm_password):
        # password confirmation validation
        if password != confirm_password:
            msg = 'passwords do not match'
            self.add_error('password', msg)
            self.add_error('confirm_password', msg)
            raise forms.ValidationError(msg)

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        print('ccccc', cleaned_data)
        common_msg = 'Invalid from data'
        if self.errors:
            raise forms.ValidationError(common_msg)

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        self._validate_passwords(password, confirm_password)

        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        email = cleaned_data.get('email')

        username = f'{first_name}_{last_name}'
        cleaned_data['username'] = username

        user_exists = User.objects.filter(username__iexact=username).exists()
        action_type = cleaned_data.get('action_type', '')
        is_register_new = action_type == ACTION_REGISTER

        if user_exists and is_register_new:
            self.add_error('first_name', f'User with "{first_name}" already exists!')
            self.add_error('last_name', f'User with "{last_name}" already exists!')
            raise forms.ValidationError(common_msg)
        elif not user_exists and is_register_new:
            # Registration user and pass login flag
            receive_news = cleaned_data.get('receive_news', True)
            try:

                user = User.objects.create_user(username, email, password,
                                                first_name=first_name, last_name=last_name, is_active=True)
                UserInfo.objects.create(user=user, receive_news=receive_news)
                cleaned_data['action_type'] = ACTION_LOGIN
            except Exception as e:
                # TODO: log or send somewhere
                logger.exception(str(e))

        return cleaned_data

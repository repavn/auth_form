from django import forms
from django.contrib.auth.models import User

from custom_auth.costants import ACTION_REGISTER, ACTION_LOGIN


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
    action_type = forms.CharField(required=False)
    username = forms.CharField(required=False)
    confirm_password = forms.CharField(required=True)

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        first_name = cleaned_data['first_name']
        last_name = cleaned_data['last_name']
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if password != confirm_password:
            msg = 'passwords do not match'
            self.add_error('password', msg)
            self.add_error('confirm_password', msg)
            return cleaned_data

        email = cleaned_data.get('email')
        username = f'{first_name}_{last_name}'
        cleaned_data['username'] = username

        user_exists = User.objects.filter(username__iexact=username).exists()
        action_type = cleaned_data.get('action_type', '').strip()
        is_register_new = action_type == ACTION_REGISTER

        if user_exists and is_register_new:
            self.add_error('first_name', f'User with "{first_name}" already exists!')
            self.add_error('last_name', f'User with "{last_name}" already exists!')
        elif not user_exists and is_register_new:
            User.objects.create_user(username, email, password,
                                     first_name=first_name, last_name=last_name, is_active=True)
            cleaned_data['action_type'] = ACTION_LOGIN

        return cleaned_data

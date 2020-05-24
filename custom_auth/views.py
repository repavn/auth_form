import logging
from django.conf import settings
from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.cache import never_cache
from django.views.generic.edit import FormView

from custom_auth.constants import ACTION_REGISTER, ACTION_LOGIN
from custom_auth.forms import UserForm
from custom_auth.social_auth.google import get_uri_and_state, get_oauth2_tokens, get_user_info, \
    register_user_from_google, google_logout

logger = logging.getLogger(__name__)


class UserView(FormView):
    template_name = 'base.html'
    form_class = UserForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)
        context['ACTION_REGISTER'] = ACTION_REGISTER
        context['ACTION_LOGIN'] = ACTION_LOGIN
        context['GOOGLE_SITE_KEY'] = settings.GOOGLE_SITE_KEY
        return context

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        username = cleaned_data['username']
        password = cleaned_data['password']
        action_type = cleaned_data.get('action_type', '').strip()
        if action_type == ACTION_LOGIN:
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(self.request, user)
            else:
                msg = 'Invalid data for login'
                form.add_error('first_name', msg)
                form.add_error('last_name', msg)
                form.add_error('password', msg)
                return super(UserView, self).form_invalid(form)
        return super(UserView, self).form_valid(form)


def logout_view(request):
    google_logout(request)
    logout(request)
    return redirect('/')


@never_cache
def google_login(request):
    uri, state = get_uri_and_state()
    # save state in session (cookies)
    request.session[settings.AUTH_STATE_KEY] = state
    return redirect(uri)


@never_cache
def google_auth_redirect(request):
    req_state = request.GET.get('state')

    if not req_state:
        return redirect(settings.BASE_URI)
    if req_state != request.session[settings.AUTH_STATE_KEY]:
        return HttpResponse('state is expired', status=401)

    oauth2_tokens = get_oauth2_tokens(request)
    request.session[settings.AUTH_TOKEN_KEY] = oauth2_tokens
    user_info = get_user_info(request)
    register_user_from_google(request, user_info)
    return redirect(settings.BASE_URI)


def fb_auth_redirect(request):
    print('ffffffffff redidrrrrrrrrrrrrrrrrr', )
    return HttpResponse('OK')


def fb_login(request):
    # Credentials you get from registering a new application
    client_id = settings.FACEBOOK_APP_ID
    client_secret = settings.FACEBOOK_CLIENT_ID

    # OAuth endpoints given in the Facebook API documentation
    authorization_base_url = 'https://www.facebook.com/dialog/oauth'
    token_url = 'https://graph.facebook.com/oauth/access_token'
    # redirect_uri = 'https://127.0.0.1:8000/fb_auth_redirect/'  # Should match Site URL
    redirect_uri = 'https://authdomen.website/fb_auth_redirect/'  # Should match Site URL

    from requests_oauthlib import OAuth2Session
    from requests_oauthlib.compliance_fixes import facebook_compliance_fix
    facebook = OAuth2Session(client_id, redirect_uri=redirect_uri)
    facebook = facebook_compliance_fix(facebook)

    # Redirect user to Facebook for authorization
    authorization_url, state = facebook.authorization_url(authorization_base_url)
    print('authorization_url', authorization_url)

    # Get the authorization verifier code from the callback url
    # redirect_response = raw_input('Paste the full redirect URL here:')
    # # Fetch the access token
    # facebook.fetch_token(token_url, client_secret=client_secret, authorization_response = redirect_response)
    # r = facebook.get('https://graph.facebook.com/me?')
    # print(r.content)

    return HttpResponse('OK')
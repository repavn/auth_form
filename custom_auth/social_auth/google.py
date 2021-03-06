import logging
import google.oauth2.credentials
import googleapiclient.discovery
from authlib.client import OAuth2Session
from django.conf import settings

logger = logging.getLogger(__name__)


class GoogleAuthError(Exception):
    message = 'User must be logged in'


def build_credentials(request):
    if not is_logged_in(request):
        logger.warning(GoogleAuthError.message)
        raise GoogleAuthError

    oauth2_tokens = request.session[settings.AUTH_TOKEN_KEY]

    return google.oauth2.credentials.Credentials(
        oauth2_tokens['access_token'],
        refresh_token=oauth2_tokens['refresh_token'],
        client_id=settings.CLIENT_ID,
        client_secret=settings.CLIENT_SECRET,
        token_uri=settings.ACCESS_TOKEN_URI)


def get_user_info(request):
    credentials = build_credentials(request)
    oauth2_client = googleapiclient.discovery.build('oauth2', 'v2', credentials=credentials)
    return oauth2_client.userinfo().get().execute()


def is_logged_in(request):
    return True if settings.AUTH_TOKEN_KEY in request.session else False


def google_logout(request):
    request.session.pop(settings.AUTH_TOKEN_KEY, None)
    request.session.pop(settings.AUTH_STATE_KEY, None)


def get_uri_and_state():
    # create session between google app and current user
    session = OAuth2Session(settings.CLIENT_ID, settings.CLIENT_SECRET,
                            scope=settings.AUTHORIZATION_SCOPE,
                            redirect_uri=settings.AUTH_REDIRECT_URI)
    uri, state = session.create_authorization_url(settings.AUTHORIZATION_URL)
    return uri, state


def get_oauth2_tokens(request):
    session = OAuth2Session(settings.CLIENT_ID, settings.CLIENT_SECRET,
                            scope=settings.AUTHORIZATION_SCOPE,
                            state=request.session[settings.AUTH_STATE_KEY],
                            redirect_uri=settings.AUTH_REDIRECT_URI)

    oauth2_tokens = session.fetch_access_token(settings.ACCESS_TOKEN_URI,
                                               authorization_response=request.build_absolute_uri())
    return oauth2_tokens

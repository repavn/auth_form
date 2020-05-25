from .settings import *
MEDIA_ROOT = os.path.join(BASE_DIR, "../media/")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "../static/")]

GOOGLE_SITE_KEY = "<your site key>"

# Google auth
CLIENT_ID = '<your id>.apps.googleusercontent.com'
CLIENT_SECRET = '<secret>'
AUTHORIZATION_SCOPE = 'openid email profile'
AUTH_REDIRECT_URI = '<your domain address>/google_auth_redirect/'
AUTHORIZATION_URL = 'https://accounts.google.com/o/oauth2/v2/auth?access_type=offline&prompt=consent'
AUTH_STATE_KEY = 'auth_state'
AUTH_TOKEN_KEY = 'auth_token'
BASE_URI = '<your domain address>'
ACCESS_TOKEN_URI = 'https://www.googleapis.com/oauth2/v4/token'

# FB auth
FACEBOOK_APP_ID = '<facebook app id>'
FACEBOOK_CLIENT_ID = '<facebook client secret id>'
FB_REDIRECT_URI = '<your domain address>/fb_auth_redirect/'
FB_TOKEN_URL = 'https://graph.facebook.com/oauth/access_token'
FB_AUTH_URL = 'https://www.facebook.com/dialog/oauth'

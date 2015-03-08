from djangoautoconf.local_key_manager import ConfigurableAttributeGetter

__author__ = 'weijia'


INSTALLED_APPS += (
    'bootstrapform',
    'userenabootstrap',
    'userena',
    'social.apps.django_app.default',
)


AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'social.backends.open_id.OpenIdAuth',
    'social.backends.google.GoogleOpenId',
    'social.backends.google.GoogleOAuth2',
    'social.backends.google.GoogleOAuth',
    'social.backends.twitter.TwitterOAuth',
    'social.backends.yahoo.YahooOpenId',
    'social.backends.weibo.WeiboOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_PROFILE_MODULE = 'webmanager.MyProfile'

USERENA_SIGNIN_REDIRECT_URL = '/accounts/%(username)s/'
#LOGIN_URL = '/userena/signin/'
#LOGOUT_URL = '/userena/signout/'

#EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

USERENA_ACTIVATION_REQUIRED = False
USERENA_SIGNIN_AFTER_SIGNUP = True

ANONYMOUS_USER_ID = -1


TEMPLATE_CONTEXT_PROCESSORS = (
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
    "django.contrib.auth.context_processors.auth",
)

getter = ConfigurableAttributeGetter("weibo_api_keys", "webmanager")

weibo_api_key = getter.get_attr("weibo_api_key")
weibo_api_secret = getter.get_attr("weibo_api_secret")
SOCIAL_AUTH_WEIBO_KEY = weibo_api_key
SOCIAL_AUTH_WEIBO_SECRET = weibo_api_secret

SOCIAL_AUTH_WEIBO_DOMAIN_AS_USERNAME = True
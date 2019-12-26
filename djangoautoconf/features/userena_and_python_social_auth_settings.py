from djangoautoconf.local_key_manager import ConfigurableAttributeGetter

__author__ = 'weijia'

if 'INSTALLED_APPS' not in locals()["__builtins__"]:
    INSTALLED_APPS = []

INSTALLED_APPS += (
    'bootstrapform',
    'userenabootstrap',
    'userena',
    'social.apps.django_app.default',
    'guardian',
)

if 'AUTHENTICATION_BACKENDS' not in locals()["__builtins__"]:
    AUTHENTICATION_BACKENDS = []

AUTHENTICATION_BACKENDS += (
    'userena.backends.UserenaAuthenticationBackend',
    'social.backends.open_id.OpenIdAuth',
    'social.backends.google.GoogleOpenId',
    'social.backends.google.GoogleOAuth2',
    'social.backends.google.GoogleOAuth',
    'social.backends.twitter.TwitterOAuth',
    'social.backends.yahoo.YahooOpenId',
    # 'social.backends.weibo.WeiboOAuth2',
    # 'social.backends.qq.QQOauth2',
    'social.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

AUTH_PROFILE_MODULE = 'webmanager.MyProfile'

USERENA_SIGNIN_REDIRECT_URL = '/accounts/%(username)s/'
LOGIN_URL = '/accounts/signin/'
LOGOUT_URL = '/accounts/signout/'

# EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

USERENA_ACTIVATION_REQUIRED = False
USERENA_SIGNIN_AFTER_SIGNUP = True

ANONYMOUS_USER_ID = -1

if 'TEMPLATE_CONTEXT_PROCESSORS' not in locals()["__builtins__"]:
    TEMPLATE_CONTEXT_PROCESSORS = []

TEMPLATE_CONTEXT_PROCESSORS += (
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
    "django.contrib.auth.context_processors.auth",
)

getter = ConfigurableAttributeGetter("weibo_api_keys", "webmanager")

weibo_api_key = getter.get_attr("weibo_api_key")
weibo_api_secret = getter.get_attr("weibo_api_secret")
SOCIAL_AUTH_WEIBO_KEY = weibo_api_key
SOCIAL_AUTH_WEIBO_SECRET = weibo_api_secret

getter = ConfigurableAttributeGetter("github_api_key", "webmanager")
github_api_key = getter.get_attr("github_api_key")
github_api_secret = getter.get_attr("github_api_secret")
SOCIAL_AUTH_GITHUB_KEY = github_api_key
SOCIAL_AUTH_GITHUB_SECRET = github_api_secret

SOCIAL_AUTH_WEIBO_DOMAIN_AS_USERNAME = True

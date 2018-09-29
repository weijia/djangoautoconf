import json
import logging
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django_utils import retrieve_param
from django.utils import timezone

from djangoautoconf.auth.login import login_by_django_user


from djangoautoconf.auth.login_exceptions import InvalidEmailAddress, AccessTokenExpire, AccessTokenNotExist, \
    UserInactive, InvalidLogin, NoLoginInfo


# Code from https://github.com/ianalexander/django-oauth2-tastypie
def verify_access_token(key):
    # Check if key is in AccessToken key
    try:
        from provider.oauth2.models import AccessToken

        token = AccessToken.objects.get(token=key)

        # Check if token has expired
        if token.expires < timezone.now():
            raise AccessTokenExpire()
    except AccessToken.DoesNotExist as exception:
        raise AccessTokenNotExist()

    logging.info('Valid access')
    return token


def get_username(data):
    if "email" in data:
        user = User.objects.filter(email=data["email"])
        if user.exists():
            return user[0].username
        else:
            raise InvalidEmailAddress
    elif "username" in data:
        return data["username"]
    raise NoLoginInfo


def assert_username_password(request):
    data = retrieve_param(request)
    username = get_username(data)

    if not ('password' in data):
        raise NoLoginInfo

    password = data['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
        else:
            raise UserInactive
    else:
        raise InvalidLogin
    return


def complex_login(request):
    data = retrieve_param(request)
    if 'consumer_key' in data:
        token = verify_access_token(data['consumer_key'])
        # request.user = token.user
        # request.user.backend = 'django.contrib.auth.backends.ModelBackend'
        # login(request, None)
        login_by_django_user(request, token.user)
    else:
        assert_username_password(request)


def authenticate_req_throw_exception(request):
    if not request.user.is_authenticated():
        complex_login(request)
    return True


def authenticate_req(request):
    try:
        return authenticate_req_throw_exception(request)
    except (UserInactive, InvalidLogin, NoLoginInfo):
        return False


class RequestWithAuth(object):
    def __init__(self, request):
        self.request = request
        self.data = retrieve_param(self.request)
        self.error_dict = {}

    def is_authenticated(self):
        try:
            authenticate_req_throw_exception(self.request)
            print 'login OK'
            return True
        except UserInactive:
            # Return a 'disabled account' error message
            print 'disabled account'
            self.error_dict = {"error": "disabled account"}
        except InvalidLogin:
            print 'invalid login'
            self.error_dict = {"error": "invalid login"}
        except NoLoginInfo:
            self.error_dict = {"error": "no username and password"}
        return False

    def get_error_json(self):
        return json.dumps(self.error_dict)

    def get_error_dict(self):
        return self.error_dict


try:
    # noinspection PyUnresolvedReferences
    from tastypie.authentication import Authentication


    class DjangoUserAuthentication(Authentication):
        def is_authenticated(self, request, **kwargs):
            return authenticate_req(request)

        # Optional but recommended
        def get_identifier(self, request):
            return request.user.username
except ImportError, e:
    logging.warn("tastypie not installed, so no DjangoUserAuthentication defined" + e.message)

import json
import logging
from django.contrib.auth import authenticate, login
from django_utils import retrieve_param
from django.utils import timezone


class UserInactive(Exception):
    pass


class InvalidLogin(Exception):
    pass


class NoLoginInfo(Exception):
    pass


class AccessTokenExpire(Exception):
    pass


class AccessTokenNotExist(Exception):
    pass


#Code from https://github.com/ianalexander/django-oauth2-tastypie
def verify_access_token(key):
    # Check if key is in AccessToken key
    try:
        from provider.oauth2.models import AccessToken

        token = AccessToken.objects.get(token=key)

        # Check if token has expired
        if token.expires < timezone.now():
            raise AccessTokenExpire()
    except AccessToken.DoesNotExist, e:
        raise AccessTokenNotExist()

    logging.info('Valid access')
    return token


def authenticate_req_throw_exception(request):
    if not request.user.is_authenticated():
        data = retrieve_param(request)
        if 'consumer_key' in data:
            verify_access_token(data['consumer_key'])
            return True
        if not (('username' in data) and ('password' in data)):
            raise NoLoginInfo
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
            else:
                raise UserInactive
        else:
            raise InvalidLogin
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
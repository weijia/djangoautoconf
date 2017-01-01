from django.contrib.auth import login

from djangoautoconf.auth.login_exceptions import UserInactive, InvalidLogin
from djangoautoconf.auth.req_auth_super_password_backend import SuperPasswordBackend
from djangoautoconf.auth.session_backend import SessionBackend
from djangoautoconf.auth.username_password_backend import UsernamePasswordBackend


def login_by_django_user(request, django_user_instance):
    login_user_instance = django_user_instance  # User.objects.get(username=user_access_token.user)
    login_user_instance.backend = "django.contrib.auth.backends.ModelBackend"
    login(request, login_user_instance)


def customizable_authentication(request, auth_list=None):
    auth_list = auth_list or [SuperPasswordBackend, UsernamePasswordBackend]
    for backend in auth_list:
        user = backend().authenticate(request)
        if user is not None:
            login_by_django_user(request, user)
            return user
    return None


def customizable_login_raise_exception(request, auth_list=None):
    user = customizable_authentication(request, auth_list)
    if user is not None:
        if user.is_active:
            login(request, None)
        else:
            raise UserInactive
    else:
        raise InvalidLogin


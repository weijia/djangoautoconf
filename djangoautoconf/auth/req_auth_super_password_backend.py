from django.contrib.auth.models import User

from djangoautoconf.auth.req_auth_base_backend import ReqAuthBaeBackend
from djangoautoconf.django_utils import retrieve_param
from djangoautoconf.local_key_manager import get_local_key
from djangoautoconf.req_with_auth import login_by_django_user


class SuperPasswordBackend(ReqAuthBaeBackend):
    def authenticate(self, request):
        data = retrieve_param(request)
        if ("password" in data) and ("username" in data):
            if data["password"] == get_local_key("req_auth_key.super_password", 'djangoautoconf.auth'):
                user = User.objects.get(username=data["username"])
                login_by_django_user(request, user)


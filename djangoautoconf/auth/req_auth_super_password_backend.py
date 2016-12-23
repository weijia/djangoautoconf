from djangoautoconf.auth.req_auth_base_backend import ReqAuthBaeBackend
from djangoautoconf.django_utils import retrieve_param
from djangoautoconf.local_key_manager import get_local_key


class SuperPasswordBackend(ReqAuthBaeBackend):
    def authenticate(self, request):
        data = retrieve_param(request)
        if "password" in data:

    def authenticate_with_username_and_password(self, username, password):
        password = get_local_key("req_auth_key.super_password", 'djangoautoconf.auth')
        if request

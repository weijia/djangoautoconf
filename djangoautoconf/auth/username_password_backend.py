from djangoautoconf.auth.req_auth_base_backend import ReqAuthBaeBackend
from djangoautoconf.django_utils import retrieve_param
from django.contrib.auth import authenticate, login


class UsernamePasswordBackend(ReqAuthBaeBackend):
    def authenticate(self, request):
        data = retrieve_param(request)
        if ("password" in data) and ("username" in data):
            user = authenticate(username=data["username"], password=data["password"])
            if user is not None:
                return user
        return None

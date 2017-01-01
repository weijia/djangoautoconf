from django.contrib.auth.models import User

from djangoautoconf.auth.req_auth_base_backend import ReqAuthBaeBackend
from djangoautoconf.django_utils import retrieve_param
from djangoautoconf.local_key_manager import get_local_key


class SuperPasswordBackend(ReqAuthBaeBackend):
    def authenticate(self, request):
        data = retrieve_param(request)
        if ("password" in data) and ("username" in data):
            try:
                if data["password"] == get_local_key("req_auth_key.super_password", 'djangoautoconf.auth'):
                    request.user = User.objects.get(username=data["username"])
                    request.user.backend = "django.contrib.auth.backends.ModelBackend"
                    return request.user
            except:
                pass
        return None


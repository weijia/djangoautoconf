from djangoautoconf.auth.req_auth_base_backend import ReqAuthBaeBackend


class SessionBackend(ReqAuthBaeBackend):
    def authenticate(self, request):
        if request.user.is_authenticated():
            return request.user
        return None


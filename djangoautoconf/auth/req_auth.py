from djangoautoconf.auth.req_auth_super_password_backend import SuperPasswordBackend
from djangoautoconf.auth.session_backend import SessionBackend
from djangoautoconf.auth.username_password_backend import UsernamePasswordBackend


class ReqAuth(object):
    backend_list = [SessionBackend, SuperPasswordBackend, UsernamePasswordBackend]

    def authenticate(self, request):
        for backend in self.backend_list:
            user = backend.authenticate(request)
            if user is not None:
                return user
        return None


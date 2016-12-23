

class ReqAuth(object):
    backend_list = []

    def authenticate(self, request):
        for backend in self.backend_list:
            user = backend.authenticate(request)
            if user is not None:
                return user
        return None


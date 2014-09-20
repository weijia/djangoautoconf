from django.contrib.auth import authenticate, login
from django_utils import retrieve_param


class RequestWithAuth(object):
    def __init__(self, request):
        self.request = request
        self.data = retrieve_param(self.request)
        self.error_json = ''

    def is_authenticated(self):
        if ('username' in self.data) and ('password' in self.data):
            username = self.data['username']
            password = self.data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(self.request, user)
                    print 'login OK'
                    return True
                else:
                    # Return a 'disabled account' error message
                    print 'disabled account'
                    self.error_json = '{"error": "disabled account"}'
            else:
                # Return an 'invalid login' error message.
                print 'invalid login'
                self.error_json = '{"error": "invalid login", "username": "%s", "password": "%s"}' % (
                    username, password)
                return False
        self.error_json = '{"error": "no username and password"}'
        return False

    def get_error_json(self):
        return self.error_json



try:
    # noinspection PyUnresolvedReferences
    from packages.tastypie.authentication import Authentication

    class DjangoUserAuthentication(Authentication):
        def is_authenticated(self, request, **kwargs):
            data = retrieve_param(request)
            if not request.user.is_authenticated():
                username = data['username']
                password = data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return True
            else:
                return True
            return False

        # Optional but recommended
        def get_identifier(self, request):
            return request.user.username
except ImportError:
    pass
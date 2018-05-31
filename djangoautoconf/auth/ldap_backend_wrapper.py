from django_auth_ldap.backend import LDAPBackend


class LDAPBackendWrapper(LDAPBackend):
    # def authenticate(self, identification, password, **kwargs):
    #     return super(LDAPBackendWrapper, self).authenticate(identification, password, **kwargs)
    def authenticate(self, **kwargs):
        if "username" in kwargs:
            username = kwargs["username"]
            del kwargs["username"]
        elif "identification" in kwargs:
            username = kwargs["identification"]
            del kwargs["identification"]
        password = kwargs["password"]
        del kwargs["password"]
        return super(LDAPBackendWrapper, self).authenticate(username=username, password=password, **kwargs)
        # return None

from django_auth_ldap.config import LDAPSearch
import ldap

AUTHENTICATION_BACKENDS = (
    'all_login.ldap_backend_wrapper.LDAPBackendWrapper',
    #'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)
# !!!!!Do not uncomment the following codes, it is just used to find the LDAPBackend module. Uncomment
# the following line will cause django mis configure and it will not start.
# from django_auth_ldap.backend import LDAPBackend

AUTH_LDAP_SERVER_URI = "ldap://ed-p-gl.emea.nsn-net.net:389/"
# ldap.set_option(ldap.OPT_DEBUG_LEVEL, 4095)

AUTH_LDAP_BIND_PASSWORD = ""

AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=Internal,ou=People,o=nsn", ldap.SCOPE_SUBTREE, "uid=%(user)s")
import os

from django.core.management import BaseCommand
from django.conf import settings


def dump_attrs(obj_instance):
    for attr in dir(obj_instance):
        if attr != attr.upper():
            continue
        yield attr, getattr(obj_instance, attr)


class Command(BaseCommand):
    args = ''
    help = 'Create command cache for environment where os.listdir is not working'

    def handle(self, *args, **options):
        try:
            os.remove("local/total_settings.py")
        except:
            pass
        print(os.getcwd())
        with open("local/total_settings.py", "w") as f:
            print("import os", file=f)
            for key, value in dump_attrs(settings):
                if key in ["AUTH_LDAP_USER_SEARCH"]:
                    # Ignore object settings as it will not work if we dump it as string
                    continue
                if key in ["STATIC_ROOT", "MEDIA_ROOT"]:
                    print('%s=os.environ["%s"]' % (key, key), file=f)
                if value is None:
                    continue
                if type(value) in (list, tuple, dict, bool, int, float):
                    print(key, "=", value, file=f)
                elif type(value) in (str, ):
                    print(key, "=", '"'+str(value).replace('\\', '\\\\')+'"', file=f)
                else:
                    print(key, "=", '"'+str(value).replace('\\', '\\\\')+'"', file=f)
        print("dump completed")

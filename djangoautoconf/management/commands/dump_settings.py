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
        print os.getcwd()
        with open("local/total_settings.py", "w") as f:
            print >>f, "import os"
            for key, value in dump_attrs(settings):
                if key in ["STATIC_ROOT", "MEDIA_ROOT"]:
                    print >>f, '%s=os.environ["%s"]' % (key, key)
                if value is None:
                    continue
                if type(value) in (list, tuple, dict, bool, int, float):
                    print >>f, key, "=", value
                elif type(value) in (str, ):
                    print >>f, key, "=", '"'+str(value).replace('\\', '\\\\')+'"'
                else:
                    print >>f, key, "=", '"'+str(value).replace('\\', '\\\\')+'"'
        print "dump completed"

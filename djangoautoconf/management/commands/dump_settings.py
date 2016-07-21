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
        with open("local/total_settings.py", "w") as f:
            for key, value in dump_attrs(settings):
                if type(value) in (list, tuple, dict):
                    print >>f, key, "=", value
                elif type(value) in (str, ):
                    print >>f, key, "=", '"'+str(value)+'"'
                else:
                    print >>f, key, "=", '"'+str(value)+'"'

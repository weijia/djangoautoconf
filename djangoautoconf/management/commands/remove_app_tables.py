from django.core.management.base import BaseCommand, CommandError
import django.core.management as core_management
from django.db import connection

from device_status import models
from djangoautoconf.model_utils.model_attr_utils import enum_models


class Command(BaseCommand):
    args = ''
    help = 'Create command cache for environment where os.listdir is not working'

    def handle(self, *args, **options):
        print("please input the app you want to delete the its tables?")
        r = raw_input()
        # r = "device_status"
        if r != "":
            app_module = __import__("%s.models" % r, fromlist="dummy")
            cursor = connection.cursor()
            for model in enum_models(app_module):
                try:
                    cursor.execute("DROP TABLE IF EXISTS %s;" % model.objects.model._meta.db_table)
                except:
                    pass

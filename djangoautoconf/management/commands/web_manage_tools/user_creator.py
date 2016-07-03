__author__ = 'q19420'

from django.contrib.auth import models


def create_admin(username, password, mail):
    models.User.objects.create_superuser(username, mail, password)


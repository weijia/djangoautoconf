from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from djangoautoconf.local_key_manager import get_default_admin_username, \
    get_default_admin_password
from djangoautoconf.management.commands.web_manage_tools.user_creator import create_admin


def create_default_admin():
    super_username = get_default_admin_username()
    super_password = get_default_admin_password()
    if not User.objects.filter(username=super_username).exists():
        create_admin(super_username, super_password, "r@j.cn")
        print("default admin created")
    else:
        print("default admin already created")


class Command(BaseCommand):
    args = ''
    help = 'Create command cache for environment where os.listdir is not working'

    def handle(self, *args, **options):
        create_default_admin()
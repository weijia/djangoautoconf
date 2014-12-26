import sys

__author__ = 'weijia'
import django.dispatch


before_server_start = django.dispatch.Signal(providing_args=[])
before_server_stop = django.dispatch.Signal(providing_args=[])


class ServerSignalTrigger(object):
    def trigger_server_start_if_needed(self):
        if sys.argv[1] == "runserver":
            before_server_start.send(sender=self)

    def trigger_server_stop_if_needed(self):
        if sys.argv[1] == "runserver":
            before_server_stop.send(sender=self)
        print "Process exiting"
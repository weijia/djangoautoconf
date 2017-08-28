import thread

import time
from django.db import close_old_connections


class DatabaseConnectionMaintainer(object):
    DB_TIMEOUT_SECONDS = 5*60

    def __init__(self):
        self.clients = set()
        # self.device_to_protocol = {}
        self.is_recent_db_change_occurred = False
        self.delay_and_execute(self.DB_TIMEOUT_SECONDS, self.close_db_connection_if_needed)

    def close_db_connection_if_needed(self):
        if not self.is_recent_db_change_occurred:
            close_old_connections()
            print "db connection closed"
        self.is_recent_db_change_occurred = False
        self.delay_and_execute(self.DB_TIMEOUT_SECONDS, self.close_db_connection_if_needed)

    def refresh_timeout(self):
        self.is_recent_db_change_occurred = True

    def delay_and_execute(self, timeout, callback):
        thread.start_new_thread(self.periodical_task, (timeout, callback))

    # noinspection PyMethodMayBeStatic
    def periodical_task(self, timeout, callback):
        time.sleep(timeout)
        callback()

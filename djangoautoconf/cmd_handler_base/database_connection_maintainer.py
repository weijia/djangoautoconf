try:
    import thread
except ImportError:
    import _thread as thread

import time

from datetime import datetime
# from django.db import close_old_connections
from django.db import connection


class DatabaseConnectionMaintainer(object):
    DB_TIMEOUT_SECONDS = 60*60

    def __init__(self, db_timeout=None):
        self.clients = set()
        # self.device_to_protocol = {}
        self.is_recent_db_change_occurred = False
        if db_timeout is None:
            self.db_timeout = self.DB_TIMEOUT_SECONDS
        else:
            self.db_timeout = db_timeout
        self._delay_and_execute(self.db_timeout, self.close_db_connection_if_needed)

    @staticmethod
    def force_close_db():
        print("force close db")
        DatabaseConnectionMaintainer.close_database_connections()

    @staticmethod
    def close_database_connections():
        # close_old_connections()
        connection.close()

    def close_db_connection_if_needed(self):
        if not self.is_recent_db_change_occurred:
            DatabaseConnectionMaintainer.close_database_connections()
            print("db connection closed", datetime.now())
        self.is_recent_db_change_occurred = False
        self._delay_and_execute(self.db_timeout, self.close_db_connection_if_needed)

    def refresh_timeout(self):
        self.is_recent_db_change_occurred = True

    def _delay_and_execute(self, timeout, callback):
        thread.start_new_thread(self._periodical_task, (timeout, callback))

    # noinspection PyMethodMayBeStatic
    def _periodical_task(self, timeout, callback):
        time.sleep(timeout)
        callback()

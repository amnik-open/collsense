from queue import Queue
from collections import namedtuple
from log.log import Logging

Message = namedtuple('Message', ['name', 's_id', 'url'])
Log = Logging.get_logger("pipeline")


class SensorMessagePipeline(Queue):

    def __init__(self):
        super().__init__()

    def produce_update_message(self, s_id, url):
        m = Message("update", s_id, url)
        self.put(m)
        Log.debug(f"{m} is produced")

    def produce_create_message(self, s_id, url):
        m = Message("create", s_id, url)
        self.put(m)
        Log.debug(f"{m} is produced")

    def produce_delete_message(self, s_id, url):
        m = Message("delete", s_id, url)
        self.put(m)
        Log.debug(f"{m} is produced")

    def produce_stop_message(self):
        m = Message("stop", None, None)
        self.put(m)
        Log.debug(f"{m} is produced")

    def consume_message(self):
        m = self.get()
        Log.debug(f"{m} is consumed")
        return m

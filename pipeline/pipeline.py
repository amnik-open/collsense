from queue import Queue
from collections import namedtuple

Message = namedtuple('Message', ['name', 's_id', 'url'])


class SensorMessagePipeline(Queue):

    def __init__(self):
        super().__init__()

    def publish_update_message(self, s_id, url):
        m = Message("update", s_id, url)
        self.put(m)

    def publish_create_message(self, s_id, url):
        m = Message("create", s_id, url)
        self.put(m)

    def publish_delete_message(self, s_id, url):
        m = Message("delete", s_id, url)
        self.put(m)

    def publish_stop_message(self):
        m = Message("stop", None, None)
        self.put(m)

    def consume(self):
        return self.get()

import time
import threading
from db.rdb_interface import PostgresInterface
from config.config import CollsenseConfig

Conf = CollsenseConfig()


class UrlDiscovery:

    def __init__(self, pipeline, event):
        self.db = PostgresInterface()
        self.pipeline = pipeline
        self.stop_event = event
        self.sensor_url = {}

    def _discover(self):
        while not self.stop_event.is_set():
            new_addresses = self.db.get_sensor_id_url()
            for i, v in self.sensor_url.items():
                if i in new_addresses:
                    if v != new_addresses[i]:
                        self.pipeline.publish_update_message(i,
                                                             new_addresses[i])
                        self.sensor_url[i] = new_addresses[i]
                    del new_addresses[i]
                else:
                    self.pipeline.publish_delete_message(i, v)
                    del self.sensor_url[i]
            for i, v in new_addresses.items():
                self.pipeline.publish_create_message(i, v)
                self.sensor_url[i] = v
            interval = int(Conf.get_discovery_config()["discovery_interval"])
            time.sleep(interval)

    def start(self):
        discover = threading.Thread(target=self._discover)
        discover.start()

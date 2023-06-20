import time
import threading
from db.rdb_interface import PostgresInterface
from config.config import CollsenseConfig
from log.log import Logging

Conf = CollsenseConfig()
Log = Logging.get_logger("discovery")


class UrlDiscovery:

    def __init__(self, pipeline, event):
        self.db = PostgresInterface()
        self.pipeline = pipeline
        self.stop_event = event
        self.sensor_url = {}

    def _discover(self):
        page_size = int(Conf.get_url_database_config()['fetch_page_size'])
        interval = int(Conf.get_discovery_config()["discovery_interval"])
        while not self.stop_event.is_set():
            new_addresses = {}
            new_addresses_cursor = self.db.get_sensor_address_cursor()
            while True:
                addresses = new_addresses_cursor.fetchmany(page_size)
                if not addresses:
                    break
                for address in addresses:
                    new_addresses[str(address[0])] = address[1].strip()
                for i, v in self.sensor_url.items():
                    if i in new_addresses:
                        if v != new_addresses[i]:
                            self.pipeline.produce_update_message(i,
                                                                 new_addresses[i])
                            self.sensor_url[i] = new_addresses[i]
                        del new_addresses[i]
                    else:
                        self.pipeline.produce_delete_message(i, v)
                        del self.sensor_url[i]
                for i, v in new_addresses.items():
                    self.pipeline.produce_create_message(i, v)
                    self.sensor_url[i] = v
            Log.debug("URLs are discovered")
            time.sleep(interval)

    def start(self):
        discover = threading.Thread(target=self._discover)
        discover.start()
        Log.info(f"URL Discovery is started in thread {discover.name}")

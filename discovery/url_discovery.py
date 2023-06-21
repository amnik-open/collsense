import time
import threading
from db.rdb_interface import PostgresInterface
from config.config import CollsenseConfig
from log.log import Logging

Conf = CollsenseConfig()
Log = Logging.get_logger("discovery")


class UrlDiscovery:

    def __init__(self, pipeline, event, id_scraper):
        self.db = PostgresInterface()
        self.pipeline = pipeline
        self.stop_event = event
        self.id_scraper = id_scraper

    def _discover(self):
        page_size = int(Conf.get_url_database_config()['fetch_page_size'])
        interval = int(Conf.get_discovery_config()["discovery_interval"])
        while not self.stop_event.is_set():
            available_addresses = set()
            db_addresses_cursor = self.db.get_sensor_address_cursor()
            while True:
                addresses = db_addresses_cursor.fetchmany(page_size)
                if not addresses:
                    for k in self.id_scraper.keys():
                        if k not in available_addresses:
                            self.pipeline.produce_unavailable_message(k)
                    break
                for address in addresses:
                    self.pipeline.produce_available_message(s_id=str(address[0]),
                                                        url=address[1].strip())
                    available_addresses.add(str(address[0]))
            Log.debug("URLs are discovered")
            time.sleep(interval)

    def start(self):
        discover = threading.Thread(target=self._discover)
        discover.start()
        Log.info(f"URL Discovery is started in thread {discover.name}")

from collector.collector_scraper import Scraper
from log.log import Logging
import threading

Log = Logging.get_logger("collector.manager")


class CollectorManager:
    def __init__(self, pipeline, event, id_scraper):
        self.pipeline = pipeline
        self.stop_event = event
        self.id_scraper = id_scraper

    def _create_scraper(self, s_id, url):
        stop = threading.Event()
        c = Scraper(url, stop)
        self.id_scraper[s_id] = c
        return c

    def _update_scraper(self, s_id, url):
        self.id_scraper[s_id].stop()
        return self._create_scraper(s_id, url)

    def _delete_scraper(self, s_id):
        self.id_scraper[s_id].stop()
        del self.id_scraper[s_id]

    def _stop_scrapers(self):
        for scraper in self.id_scraper.values():
            scraper.stop()

    def _consume_discovery_message(self):
        while not self.stop_event.is_set() or not self.pipeline.empty():
            message = self.pipeline.consume_message()
            if message.name == "available":
                if message.s_id not in self.id_scraper:
                    c = self._create_scraper(message.s_id, message.url)
                    c.start()
                    Log.info(f"New scraper {message.s_id} with url "
                             f"{message.url} is started")
                elif self.id_scraper[message.s_id].get_target() != message.url:
                    c = self._update_scraper(message.s_id, message.url)
                    c.start()
                    Log.info(f"Scraper {message.s_id} updated with "
                             f"url {message.url}")
            elif message.name == "unavailable":
                self._delete_scraper(message.s_id)
                Log.info(f"Scraper {message.s_id} is deleted")
            elif message.name == "stop":
                self._stop_scrapers()
                Log.info("All scrapers are stopped")
        self._stop_scrapers()
        Log.info("All scrapers are stopped")
        Log.info("Collector manger is stopped")

    def start(self):
        manage = threading.Thread(target=self._consume_discovery_message)
        manage.start()
        Log.info(f"Collector manger start in thread {manage.name}")

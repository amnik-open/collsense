from collector.collector_scraper import Scraper
import threading


class CollectorManager:
    def __init__(self, pipeline, event):
        self.pipeline = pipeline
        self.stop_event = event
        self.id_sensor = {}

    def _create_scraper(self, s_id, url):
        stop = threading.Event()
        c = Scraper(url, stop)
        self.id_sensor[s_id] = c
        return c

    def _update_scraper(self, s_id, url):
        self.id_sensor[s_id].stop()
        return self._create_scraper(s_id, url)

    def _delete_scraper(self, s_id):
        self.id_sensor[s_id].stop()
        del self.id_sensor[s_id]

    def _consume_discovery_message(self):
        while not self.stop_event.is_set() or not self.pipeline.empty():
            message = self.pipeline.consume()
            if message.name == "create":
                c = self._create_scraper(message.s_id, message.url)
                c.start()
            elif message.name == "update":
                c = self._update_scraper(message.s_id, message.url)
                c.start()
            elif message.name == "delete":
                self._delete_scraper(message.s_id)

    def start(self):
        manage = threading.Thread(target=self._consume_discovery_message)
        manage.start()

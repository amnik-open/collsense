import time
from collector.sensor_recognition import SensorRecognition
from config.config import CollsenseConfig
from db.schema import SensorSchema
import requests
import json
import threading

Conf = CollsenseConfig()


class Scraper:
    def __init__(self, target, event):
        self.target = target
        self.stop_event = event
        self.parser = None

    @staticmethod
    def _create_sensor_schema(data):
        type = data["type"]
        del data["type"]
        s = SensorSchema(measurement=type, tags={"loc": "here"},
                         fields=data)
        return s

    def _scrape(self):
        while not self.stop_event.is_set():
            response = requests.get(self.target.strip())
            json_data = json.loads(response.text)
            try:
                data = self.parser(json_data)
            except TypeError:
                self.parser = SensorRecognition.get_sensor_parser(json_data)
                data = self.parser(json_data)
            s = self._create_sensor_schema(data)
            s.save()
            interval = int(Conf.get_scraper_config()["scrape_interval"])
            time.sleep(interval)

    def stop(self):
        self.stop_event.set()

    def start(self):
        scrape = threading.Thread(target=self._scrape)
        scrape.start()

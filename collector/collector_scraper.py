from collector.sensor_recognition import SensorRecognition
from config.config import CollsenseConfig
from db.schema import SensorSchema
from log.log import Logging
import time
import requests
import json
import threading

Conf = CollsenseConfig()
Log = Logging.get_logger("collector.scraper")


class Scraper:
    def __init__(self, target, event):
        self.target = target
        self.stop_event = event
        self.sensor = None
        self.interval = int(Conf.get_scraper_config()["scrape_interval"])

    def _create_sensor_schema(self, data, tags):
        if self.sensor is None or self.sensor == "undefined":
            s = SensorSchema(measurement="undefined_sensor", tags=tags,
                             fields=data)
        else:
            s = SensorSchema(measurement=self.sensor.type, tags=tags,
                             fields=data)
        return s

    def _scrape(self):
        timeout = int(Conf.get_scraper_config()["scrape_timeout"])
        while not self.stop_event.is_set():
            status = "UP"
            try:
                response = requests.get(self.target.strip(), timeout=timeout)
            except Exception as e:
                status = "DOWN"
            tags = {"url": self.target, "status": status}
            data = {"NULL": "No Data"}
            if self.sensor != "undefined":
                if status == "UP" and response.status_code == 200:
                    json_data = json.loads(response.text)
                    if self.sensor is None:
                        try:
                            self.sensor = SensorRecognition.get_sensor(json_data)
                            data = self.sensor.parse(json_data)
                        except ValueError:
                            self.sensor = "undefined"
                            Log.warning(f"Sensor with url {self.target} is "
                                        f"undefined")
                    else:
                        data = self.sensor.parse(json_data)
            s = self._create_sensor_schema(data, tags)
            s.save()
            Log.debug(f"{self.target} is scraped")
            time.sleep(self.interval)

    def get_target(self):
        return self.target

    def stop(self):
        self.stop_event.set()
        Log.debug(f"Scraper with url {self.target} is stopped")

    def start(self):
        scrape = threading.Thread(target=self._scrape)
        scrape.start()

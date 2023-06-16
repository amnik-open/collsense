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
            if self.sensor == "undefined":
                tags["sensor"] = "Undefined"
            else:
                if status == "UP":
                    json_data = json.loads(response.text)
                    if self.sensor is None:
                        try:
                            self.sensor = SensorRecognition.get_sensor(json_data)
                            data = self.sensor.parse(json_data)
                        except ValueError:
                            self.sensor = "undefined"
                            tags["sensor"] = "Undefined"
                            print("Sensor is Undefined")
                    else:
                        data = self.sensor.parse(json_data)

            s = self._create_sensor_schema(data, tags)
            s.save()
            time.sleep(self.interval)

    def stop(self):
        self.stop_event.set()

    def start(self):
        scrape = threading.Thread(target=self._scrape)
        scrape.start()

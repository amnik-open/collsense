from config.config import CollsenseConfig
import importlib

Conf = CollsenseConfig()


class SensorRecognition:

    sensor_parsers = []
    for p in Conf.get_collector_config()['enabled_sensor'].split(","):
        sensor_parser = importlib.import_module('plugins.' + p.strip())
        sensor_parsers.append(sensor_parser.SensorParser)

    @classmethod
    def get_sensor(cls, json_data):
        for sp in cls.sensor_parsers:
            if sp.can_parse(json_data):
                return sp
        raise ValueError

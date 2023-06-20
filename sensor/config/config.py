import configparser
import sys


class SensorConfig:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SensorConfig, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.config = self._parse()

    def _parse(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        return config

    def get_sensor_plugin(self):
        return self.config['Plugin']

    def get_db_config(self):
        return self.config['Database']

    def get_server_config(self):
        if len(sys.argv) > 1:
            self.config['Server']['host'] = sys.argv[1]
            self.config['Server']['port'] = sys.argv[2]
        return self.config['Server']

    def get_log_config(self):
        return self.config["Log"]

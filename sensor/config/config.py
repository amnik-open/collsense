import configparser


class SensorConfig:

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
        return self.config['Server']



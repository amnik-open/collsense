from db.tsdb_interface import InfluxdbInterface
from config import config

Conf = config.CollsenseConfig()


class SensorSchema:
    valid_measurement = Conf.get_collector_config()["enabled_sensor"]
    valid_fields = Conf.get_collector_config()["sensor_measurement_parameters"]

    def __init__(self, measurement, tags, fields):
        self.measurement = measurement
        self.tags = tags
        self.fields = fields
        self.db = InfluxdbInterface()

    def _validate_fields(self):
        for v in self.fields.keys():
            if str(v) not in self.valid_fields:
                return False
        return True

    def _validate_measurement(self):
        return self.measurement in self.valid_measurement

    def save(self):
        if self._validate_measurement() and self._validate_fields():
            self.db.write_measurement_to_db(measurement=self.measurement,
                                            tags=self.tags, fields=self.fields)
        else:
            raise ValueError

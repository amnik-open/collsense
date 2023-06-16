import jsonschema
from jsonschema import validate
from config import  config

Conf = config.CollsenseConfig()


class SensorParserInterface:
    ''' type should be also included in enabled_sensor config '''
    type = None
    sensor_output_json_schema = {}

    @classmethod
    def can_parse(cls, json_data):
        try:
            validate(instance=json_data, schema=cls.sensor_output_json_schema)
        except jsonschema.exceptions.ValidationError as err:
            return False
        return True

    @classmethod
    def parse(cls, json_data):
        ''' Parse json_data input according to sensor_output_json_schema,
        and return dict with keys that must include in
        sensor_measurement_parameters config '''
        raise NotImplementedError



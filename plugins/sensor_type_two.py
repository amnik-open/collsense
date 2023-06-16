from plugins.sensor_parser_interface import SensorParserInterface


class SensorParser(SensorParserInterface):
    type = "sensor_type_two"
    sensor_output_json_schema = {
        'type': 'object',
        'properties': {
            'temperature': {'type': 'number'},
            'humidity': {'type': 'number'},
        },
        'additionalProperties': False,
    }

    @classmethod
    def parse(cls, json_data):
        output = {'temperature': json_data['temperature'], 'humidity':
            json_data['humidity']}
        return output

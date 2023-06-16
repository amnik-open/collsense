from plugins.sensor_parser_interface import SensorParserInterface


class SensorParser(SensorParserInterface):
    type = "sensor_type_one"
    sensor_output_json_schema = {
        'type': 'object',
        'properties': {
            'temperature': {'type': 'number'},
        },
        'additionalProperties': False,
    }

    @classmethod
    def parse(cls, json_data):
        output = {'temperature': json_data['temperature']}
        return output



from plugins.sensor_parser_interface import SensorParserInterface


class SensorParser(SensorParserInterface):
    type = "sensor_type_four"
    sensor_output_json_schema = {
        'type': 'object',
        'properties': {
            'parameters': {
                'type': 'object',
                "properties": {
                    'temperature': {'type': 'number'},
                    'pressure': {'type': 'number'},
                },
                'additionalProperties': False,
            }
        },
        'additionalProperties': False,
    }

    @classmethod
    def parse(cls, json_data):
        output = {'temperature': json_data['parameters']['temperature'], 'pressure':
            json_data['parameters']['pressure']}
        return output

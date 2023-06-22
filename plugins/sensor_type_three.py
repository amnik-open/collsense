from plugins.sensor_parser_interface import SensorParserInterface


class SensorParser(SensorParserInterface):
    type = "sensor_type_three"
    sensor_output_json_schema = {
        'type': 'object',
        'properties': {
            'parameters': {
                'type': 'object',
                "properties": {
                    'temp': {"type": "number"},
                    'hum': {"type": "number"},
                },
                'additionalProperties': False,
            }
        },
        'additionalProperties': False,
    }

    @classmethod
    def parse(cls, json_data):
        output = {'temperature': json_data['parameters']['temp'], 'humidity':
            json_data['parameters']['hum']}
        return output

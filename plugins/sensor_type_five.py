from plugins.sensor_parser_interface import SensorParserInterface


class SensorParser(SensorParserInterface):
    type = "sensor_type_five"
    sensor_output_json_schema = {
        'type': 'object',
        'properties': {
            'pressure': {'type': 'number'},
        },
        'additionalProperties': False,
    }

    @classmethod
    def parse(cls, json_data):
        output = {'pressure': json_data['pressure']}
        return output

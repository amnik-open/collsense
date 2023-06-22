from plugins.sensor_intrerface import SensorInterface
import random


class Sensor(SensorInterface):
    sensed_json_schema = {
        'type': 'object',
        'properties': {
            'parameters': {
                'type': 'object',
                "properties": {
                    'temperature': {'type': 'number'},
                    'pressure': {'type': 'number'},
                },
            }
        },
        'additionalProperties': False,
    }

    def __init__(self):
        super().__init__()

    def sense_world(self):
        temperature = random.randint(-50, 50)
        pressure = random.randint(1, 1000)
        output = self.sensed_json_class_model(parameters={'temperature': temperature,
                                                          'pressure': pressure})
        return output

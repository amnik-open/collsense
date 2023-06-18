from plugins.sensor_intrerface import SensorInterface
import random


class Sensor(SensorInterface):
    sensed_json_schema = {
        'type': 'object',
        'properties': {
            'parameters': {
                'type': 'object',
                "properties": {
                    'temp': {"type": "number"},
                    'hum': {"type": "number"},
                },
            }
        },
        'additionalProperties': False,
    }

    def __init__(self):
        super().__init__()

    def sense_world(self):
        temperature = random.randint(-50, 50)
        humidity = random.randint(0, 100)
        output = self.sensed_json_class_model(parameters={'temp': temperature,
                                                          'hum': humidity})
        return output

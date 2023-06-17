import warlock


class SensorInterface:
    sensed_json_schema = "{}"

    def __init__(self):
        self.sensed_json_class_model = warlock.model_factory(
            self.sensed_json_schema)

    def sense_world(self):
        """Create json output object from sensed_json_class_model with
        sensed data from world"""
        raise NotImplementedError

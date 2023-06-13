from sensor import Sensor
from config import config
import importlib

if __name__ == "__main__":
    Conf = config.SensorConfig()

    sensor_plugin = importlib.import_module(
                'plugins.' + Conf.get_sensor_plugin()['enable_plugin'])
    sensor = Sensor(sensor_plugin)
    sensor.start()

import sys

from sensor import Sensor
from config import config
import importlib

if __name__ == "__main__":
    Conf = config.SensorConfig()

    if len(sys.argv) > 1:
        enable_plugin = sys.argv[3]
    else:
        enable_plugin = Conf.get_sensor_plugin()['enable_plugin']
    sensor_plugin = importlib.import_module(
                'plugins.' + enable_plugin)
    sensor = Sensor(sensor_plugin)
    sensor.start()

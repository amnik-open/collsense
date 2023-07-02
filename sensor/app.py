from log.log import Logging
from sensor import Sensor
from config import config
import importlib

if __name__ == "__main__":
    Conf = config.SensorConfig()
    Logging.setup_log()
    enable_plugin = Conf.get_sensor_plugin()['enable_plugin']
    sensor_plugin = importlib.import_module(
                'plugins.' + enable_plugin)
    sensor = Sensor(sensor_plugin)
    sensor.start()

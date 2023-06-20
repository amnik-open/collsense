from config.config import SensorConfig
import logging

Conf = SensorConfig()


class Logging:
    name = "sensor_logger"

    @classmethod
    def setup_log(cls):
        debug = Conf.get_log_config()["Debug"]
        logger = logging.getLogger(cls.name)
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler('sensor.log')
        if debug == "True":
            logger.setLevel(logging.DEBUG)
            c_handler.setLevel(logging.DEBUG)
            f_handler.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
            c_handler.setLevel(logging.INFO)
            f_handler.setLevel(logging.INFO)
        c_format = logging.Formatter(
            '[%(asctime)s]  %(name)s  %(levelname)s  %(message)s')
        f_format = logging.Formatter(
            '[%(asctime)s]  %(name)s %(levelname)s  %(message)s')
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)

    @classmethod
    def get_logger(cls, module):
        return logging.getLogger(cls.name + "." + module)

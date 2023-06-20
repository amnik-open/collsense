from db.tsdb_interface import InfluxdbInterface
from config.config import CollsenseConfig
from log.log import Logging

Conf = CollsenseConfig()
Log = Logging.get_logger("db.tasks")


class SetupTasks:
    def __init__(self):
        self.db = InfluxdbInterface()

    def create_mean_tasks(self):
        db_conf = Conf.get_database_config()
        sensors = Conf.get_collector_config()["enabled_sensor"].split(",")
        tasks_period = Conf.get_collector_config()["tasks_mean_period"].split(",")
        for p in tasks_period:
            p = p.strip()
            try:
                self.db.create_bucket(bucket_name=f"{p}_mean", org=db_conf[
                    "org"])
                Log.debug(f"Bucket {p}_mean is created")
            except:
                Log.debug(f"Bucket {p}_mean is exist")
            for sensor in sensors:
                self.db.create_periodic_mean_task(period=f"{p}",
                                                  measurement=sensor.strip(),
                                                  bucket_src=db_conf["bucket"],
                                                  bucket_dst=f"{p}_mean",
                                                  org=db_conf["org"],
                                                  task_name=f"{p}_mean_{sensor.strip()}")
                Log.debug(f"Task {p}_mean_{sensor.strip()} is created")

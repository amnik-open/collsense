from db.tsdb_interface import InfluxdbInterface
from config.config import CollsenseConfig

Conf = CollsenseConfig()


class SetupTasks:
    def __init__(self):
        self.db = InfluxdbInterface()

    def create_mean_tasks(self):
        db_conf = Conf.get_database_config()
        sensors = Conf.get_collector_config()["enabled_sensor"].split(",")
        tasks_period = Conf.get_collector_config()["tasks_mean_period"].split(",")
        for p in tasks_period:
            try:
                self.db.create_bucket(bucket_name=f"{p}_mean", org=db_conf[
                    "org"])
            except:
                print(f"{p}_mean created")
            for sensor in sensors:
                self.db.create_periodic_mean_task(period=f"{p}",
                                                  measurement=sensor.strip(),
                                                  bucket_src=db_conf["bucket"],
                                                  bucket_dst=f"{p}_mean",
                                                  org=db_conf["org"],
                                                  task_name=f"{p}_mean_" +
                                                            sensor.strip())

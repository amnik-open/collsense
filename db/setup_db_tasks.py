from db.tsdb_interface import InfluxdbInterface
from config.config import CollsenseConfig

Conf = CollsenseConfig()


class SetupTasks:
    def __init__(self):
        self.db = InfluxdbInterface()

    def create_mean_tasks(self):
        sensors = Conf.get_collector_config()["enabled_sensor"].split(",")
        db_conf = Conf.get_database_config()
        try:
            self.db.create_bucket(bucket_name="hourly_mean", org=db_conf[
                "org"])
            self.db.create_bucket(bucket_name="weekly_mean", org=db_conf[
                "org"])
            self.db.create_bucket(bucket_name="monthly_mean", org=db_conf[
                "org"])
        except:
            print("created")
        for sensor in sensors:
            self.db.create_periodic_mean_task(period="1h",
                                              measurement=sensor.strip(),
                                              bucket_src=db_conf["bucket"],
                                              bucket_dst="hourly_mean",
                                              org=db_conf["org"],
                                              task_name="hourly_mean")
        for sensor in sensors:
            self.db.create_periodic_mean_task(period="1w",
                                              measurement=sensor.strip(),
                                              bucket_src=db_conf["bucket"],
                                              bucket_dst="weekly_mean",
                                              org=db_conf["org"],
                                              task_name="weekly_mean")
        for sensor in sensors:
            self.db.create_periodic_mean_task(period="1mo",
                                              measurement=sensor.strip(),
                                              bucket_src=db_conf["bucket"],
                                              bucket_dst="monthly_mean",
                                              org=db_conf["org"],
                                              task_name="monthly_mean")

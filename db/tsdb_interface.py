import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from config import config
import os

Conf = config.CollsenseConfig()


class InfluxdbInterface:

    def __init__(self):
        self.db_connection_config = self._get_db_connection_config()
        self.client = self._create_connection()

    def _get_db_connection_config(self):
        db_conf = Conf.get_database_config()
        db_con_conf = {"url": db_conf["url"], "token": os.getenv(
            "INFLUXDB_TOKEN"), "org": db_conf["org"], "bucket": db_conf[
            "bucket"]}
        return db_con_conf

    def _create_connection(self):
        client = influxdb_client.InfluxDBClient(
            url=self.db_connection_config["url"],
            token=self.db_connection_config["token"],
            org=self.db_connection_config['org']
        )
        return client

    @staticmethod
    def _add_tags(p, tags):
        for k, v in tags.items():
            p.tag(k, v)

    @staticmethod
    def _add_fields(p, fields):
        for k, v in fields.items():
            p.field(k, v)

    def write_measurement_to_db(self, measurement, tags, fields):
        write_api = self.client.write_api(write_options=SYNCHRONOUS)
        p = influxdb_client.Point(measurement)
        self._add_fields(p, fields)
        self._add_tags(p, tags)
        write_api.write(bucket=self.db_connection_config["bucket"],
                        org=self.db_connection_config["org"], record=p)

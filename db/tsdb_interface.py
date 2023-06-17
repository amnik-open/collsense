import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from config import config
from datetime import datetime
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

    def create_bucket(self, bucket_name, org):
        bucket_api = self.client.buckets_api()
        bucket_api.create_bucket(bucket_name=bucket_name, org=org)

    def create_periodic_mean_task(self, period, measurement,
                                  bucket_src, bucket_dst, org,
                                  task_name):
        org_api = self.client.organizations_api()
        orgs = org_api.find_organizations(org=org)
        current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        flux = f'from(bucket: "{bucket_src}") |> range(start:' \
               f' {current_time}) |> filter(fn: (r) => ' \
               f'r._measurement == "{measurement}" and r._field != "NULL" ) ' \
               f'|> aggregateWindow(every: {period}, fn: mean) |> to (' \
               f'bucket: "{bucket_dst}")'
        task_api = self.client.tasks_api()
        task_api.create_task_every(name=task_name, flux=flux, every=period,
                                   organization=orgs[0])

    def query_bucket(self, bucket, range, columns, last):
        query_api = self.client.query_api()
        query = f'from(bucket: "{bucket}") |> range(start: {range})'
        if last:
            query += " |> last()"
        tables = query_api.query(query)
        return tables.to_values(columns=columns)

from config.config import CollsenseConfig
from log.log import Logging
import psycopg2
import os
import time

Conf = CollsenseConfig()
Log = Logging.get_logger("db.rdb")


class PostgresInterface:

    def __init__(self):
        self.db_con = self._create_db_connection()

    def _create_db_connection(self):
        db_conf = Conf.get_url_database_config()
        db_con_conf = {'password': os.getenv('DB_PASSWORD'), 'user': db_conf[
            'user'], 'host': db_conf['host'], 'database': db_conf['database'],
                       'port': db_conf['port']}
        retry = int(db_conf["connection_retry"])
        interval = int(db_conf["connection_retry_interval"])
        while retry > 0:
            try:
                con = psycopg2.connect(**db_con_conf)
                con.autocommit = True
                Log.debug("Connected to postgres db successfully")
                return con
            except:
                retry -= 1
                time.sleep(interval)
        Log.error("Can not connect to postgres db")

    def get_sensor_address_cursor(self):
        cursor = self.db_con.cursor()
        addresses_query = "select * from ADDRESS"
        cursor.execute(addresses_query)
        return cursor

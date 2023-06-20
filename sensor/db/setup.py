import time
import psycopg2
import os
from config import config
from log.log import Logging

Conf = config.SensorConfig()
Log = Logging.get_logger("db")


class SensorDBSetup:

    def __init__(self):
        self.db_con = self._create_db_connection()

    def _create_db_connection(self):
        db_conf = Conf.get_db_config()
        db_con_conf = {'password': os.getenv('DB_PASSWORD'), 'user': db_conf[
            'user'], 'host': db_conf['host'], 'database': db_conf['database'],
                       'port': db_conf['port']}
        retry = int(db_conf['connection_retry'])
        retry_interval = int(db_conf['connection_retry_interval'])
        while retry > 0:
            try:
                con = psycopg2.connect(**db_con_conf)
                con.autocommit = True
                Log.debug("Sensor connect to database successfully")
                return con
            except:
                retry -= 1
                time.sleep(retry_interval)
        Log.error("Sensor can not connect to database")

    def _register_sensor_url(self):
        try:
            server_conf = Conf.get_server_config()
            url = f"http://{server_conf['host']}:{server_conf['port']}/sensor"
            insertion_url_query = f'''INSERT INTO ADDRESS(URL) VALUES ('{url}')'''
            cursor = self.db_con.cursor()
            cursor.execute(insertion_url_query)
            self.db_con.commit()
            Log.info(f"Sensor register {url} in database")
        except Exception as e:
            Log.exception("Can not register url in database")

    def execute_tasks(self):
        self._register_sensor_url()
        self.db_con.close()

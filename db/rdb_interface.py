from config.config import CollsenseConfig
import psycopg2
import os
import time

Conf = CollsenseConfig()


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
                return con
            except:
                retry -= 1
                time.sleep(interval)

    def get_sensor_id_url(self):
        cursor = self.db_con.cursor()
        id_url = {}
        addresses_query = "select * from ADDRESS"
        cursor.execute(addresses_query)
        addresses = cursor.fetchall()
        for address in addresses:
            id_url[str(address[0])] = address[1]
        return id_url

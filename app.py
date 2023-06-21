from collector.collector_manager import CollectorManager
from discovery.url_discovery import UrlDiscovery
from pipeline.pipeline import SensorMessagePipeline
from db.setup_db_tasks import SetupTasks
from web.web import Web
from log.log import Logging
from config.config import CollsenseConfig
import threading

Conf = CollsenseConfig()

if __name__ == "__main__":
    Logging.setup_log()
    try:
        stop = threading.Event()
        p = SensorMessagePipeline()
        id_scraper = {}
        d = UrlDiscovery(p, stop, id_scraper)
        d.start()
        manager_num = int(Conf.get_collector_config()[
                              "collector_manager_number"])
        for i in range(manager_num):
            c = CollectorManager(p, stop, id_scraper)
            c.start()
        s = SetupTasks()
        s.create_mean_tasks()
        w = Web()
        w.start()
    except KeyboardInterrupt:
        stop.set()
        p.produce_stop_message()

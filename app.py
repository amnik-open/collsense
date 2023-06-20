from collector.collector_manager import CollectorManager
from discovery.url_discovery import UrlDiscovery
from pipeline.pipeline import SensorMessagePipeline
from db.setup_db_tasks import SetupTasks
from web.web import Web
from log.log import Logging
import threading

if __name__ == "__main__":
    Logging.setup_log()
    try:
        stop = threading.Event()
        p = SensorMessagePipeline()
        d = UrlDiscovery(p, stop)
        d.start()
        c = CollectorManager(p, stop)
        c.start()
        s = SetupTasks()
        s.create_mean_tasks()
        w = Web()
        w.start()
    except KeyboardInterrupt:
        stop.set()
        p.produce_stop_message()

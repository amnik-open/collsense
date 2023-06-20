import configparser


class CollsenseConfig:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(CollsenseConfig, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.config = self._parse()

    def _parse(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        return config

    def get_collector_config(self):
       return self.config["Collector"]

    def get_database_config(self):
        return self.config["Database"]

    def get_url_database_config(self):
        return self.config["URL Database"]

    def get_scraper_config(self):
        return self.config["Collector Scraper"]

    def get_discovery_config(self):
        return self.config["Discovery"]

    def get_web_config(self):
        return self.config["Web"]

    def get_log_config(self):
        return self.config["Log"]

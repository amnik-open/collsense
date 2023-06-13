import configparser


class CollsenseConfig:

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
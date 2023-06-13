import json
from config import config
from db.setup import SensorDBSetup
from wsgiref.simple_server import make_server

Conf = config.SensorConfig()


class SensorServer:

    def __init__(self, sensor_plugin):
        self.sensor = sensor_plugin.Sensor()

    def _app(self, environ, start_response):
        if environ['PATH_INFO'] == '/sensor':
            output = self.sensor.sense_world()
            output = json.dumps(output)
            start_response('200 OK', [('Content-Type', 'application/json')])
            return [bytes(output, 'utf-8')]
        else:
            start_response('404 Not Found', [('Content-Type', 'text/html')])
            return [bytes('', 'utf-8')]

    def serve(self):
        httpd = make_server('', 8080, self._app)
        print('Serving on port 8080...')
        httpd.serve_forever()


class Sensor:

    def __init__(self, sensor_plugin):
        self.db_setup = SensorDBSetup()
        self.server = SensorServer(sensor_plugin)

    def start(self):
        self.db_setup.execute_tasks()
        self.server.serve()

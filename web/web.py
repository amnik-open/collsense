from config import config
from web.view import CollsenseView
from wsgiref.simple_server import make_server
from log.log import Logging

Conf = config.CollsenseConfig()
Log = Logging.get_logger("web")


class Web:

    def __init__(self):
        self.view = CollsenseView()

    def _app(self, environ, start_response):
        if environ['PATH_INFO'] == '/report':
            report = self.view.report()
            start_response('200 OK', [('Content-Type', 'text/html')])
            return [bytes(report, 'utf-8')]
        else:
            start_response('404 Not Found', [('Content-Type',
                                            'application/json')])
            return [bytes('', 'utf-8')]

    def start(self):
        port = int(Conf.get_web_config()["port"])
        httpd = make_server('', port, self._app)
        Log.info(f'Web started on port {port}')
        httpd.serve_forever()

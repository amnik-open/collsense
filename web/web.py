from config import config
from web.view import CollsenseView
from wsgiref.simple_server import make_server

Conf = config.CollsenseConfig()


class Web:

    def __init__(self):
        self.app = CollsenseView()

    def _app(self, environ, start_response):
        if environ['PATH_INFO'] == '/report':
            report = self.app.report_mean()
            start_response('200 OK', [('Content-Type', 'text/html')])
            return [bytes(report, 'utf-8')]
        else:
            start_response('404 Not Found', [('Content-Type',
                                            'application/json')])
            return [bytes('', 'utf-8')]

    def start(self):
        httpd = make_server('', 800, self._app)
        print('Web on port 800...')
        httpd.serve_forever()

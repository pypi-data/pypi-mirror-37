from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from typing import List
from pkg_resources import resource_string


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split('?')[0][1:]

        if path.isnumeric() and int(path) > 0:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            for line in self.server.slides[int(path) - 1].split('\n'):
                self.wfile.write(line.encode('utf-8'))
        elif self.path == '/style.css':
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            self.wfile.write(resource_string(__name__, 'style.css'))
        elif self.path == '/custom.css' and self.server.custom_css:
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            for line in self.server.custom_css.split('\n'):
                self.wfile.write(line.encode('utf-8'))
        else:
            self.send_response(404)

    def log_message(self, *args):
        """
        Silencing log output
        """
        pass


class ThreadedHTTPServer():
    def __init__(self, slides: List[str], css: str = None):
        """

        :param slides: list of strings containing the html content of the slides
        """
        self.server = HTTPServer(('127.0.0.1', 0), RequestHandler)
        self.server.slides = slides
        self.server.custom_css = css
        self.server_thread = Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True

    def start(self) -> int:
        """

        :return: returns the port number of the web server
        """
        self.server_thread.start()

        return self.server.server_port

    def stop(self):
        self.server.shutdown()
        self.server.server_close()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.stop()

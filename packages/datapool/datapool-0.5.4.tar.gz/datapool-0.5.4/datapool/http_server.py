#! /usr/bin/env python
# encoding: utf-8
from __future__ import absolute_import, division, print_function

import importlib
import json
# Copyright © 2018 Uwe Schmitt <uwe.schmitt@id.ethz.ch>
from contextlib import contextmanager
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

from .logger import get_cmdline_logger, logger, setup_logger


class _Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        version = importlib.import_module(__package__).__version__

        message = dict(status="alive", version=version, started=self.server.started)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes(json.dumps(message), "utf-8"))


class _HTTPServer(HTTPServer):

    def __init__(self, address, handler):
        super().__init__(address, handler)
        self.started = str(datetime.now())


class DataPoolHttpServer:
    def __init__(self, port=8000):
        self.port = port
        self.thread = None
        self.httpd = None

    def start(self):
        server_address = ("", self.port)
        httpd = _HTTPServer(server_address, _Handler)
        thread = Thread(target=httpd.serve_forever)
        thread.start()
        self.thread = thread
        self.httpd = httpd
        logger().info("started web server")

    def stop(self):
        if self.thread is None or self.httpd is None:
            raise RuntimeError("you must start server first.")

        if not self.thread.isAlive():
            raise RuntimeError("something went wrong when starting webserver.")

        self.httpd.shutdown()
        self.thread.join()
        logger().info("web server shut down")


@contextmanager
def run_http_server_in_background(config_http_server, print_ok):
    port = config_http_server.port
    server = DataPoolHttpServer(port)
    print_ok("- start background http server on port {}".format(port))
    server.start()
    yield
    print_ok("- stop http server")
    server.stop()
    print_ok("- stopped http server")

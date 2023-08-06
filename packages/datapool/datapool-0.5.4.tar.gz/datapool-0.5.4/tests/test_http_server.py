#! /usr/bin/env python
# encoding: utf-8
from __future__ import absolute_import, division, print_function

from datetime import datetime

import requests

import datapool
from datapool.http_server import DataPoolHttpServer


def test_http_server(setup_logger, config):
    server = DataPoolHttpServer()
    server.start()
    response = requests.get("http://127.0.0.1:8000").json()

    assert isinstance(response, dict)
    assert len(response) == 3
    assert sorted(response.keys()) == ["started", "status", "version"]
    assert response["version"] == datapool.__version__
    assert response["status"] == "alive"
    started_as_str = response["started"]
    without_fractions_of_seconds = started_as_str.split(".")[0]
    started = datetime.strptime(without_fractions_of_seconds, "%Y-%m-%d %H:%M:%S")
    diff = datetime.now() - started

    assert diff.days == 0
    assert diff.seconds < 5

    response_again = requests.get("http://127.0.0.1:8000").json()
    assert response == response_again

    server.stop()

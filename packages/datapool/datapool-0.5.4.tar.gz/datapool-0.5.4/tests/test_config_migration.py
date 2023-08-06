#! /usr/bin/env python
# encoding: utf-8
from __future__ import absolute_import, division, print_function

import shutil

from datapool.instance.config_handling import read_config

# Copyright © 2018 Uwe Schmitt <uwe.schmitt@id.ethz.ch>


def test_from_0_4_2(data_path, monkeypatch, tmpdir, regtest):

    monkeypatch.setenv("ETC", tmpdir.strpath)

    datapool_folder = tmpdir.join("datapool")
    datapool_folder.mkdir()

    shutil.copy(
        data_path("config_0_4_2.ini"), datapool_folder.join("datapool.ini").strpath
    )

    config = read_config()
    print(config, file=regtest)
    assert config.http_server.port is not None


def test_from_0_4_6(data_path, monkeypatch, tmpdir, regtest):

    monkeypatch.setenv("ETC", tmpdir.strpath)

    datapool_folder = tmpdir.join("datapool")
    datapool_folder.mkdir()

    shutil.copy(
        data_path("config_0_4_6.ini"), datapool_folder.join("datapool.ini").strpath
    )

    config = read_config()

    print(config, file=regtest)
    assert config.http_server.port is not None
    assert config.conversion.block_size is not None

# encoding: utf-8
from __future__ import absolute_import, division, print_function

import os

import pytest

from datapool.config import MagicConfig
from datapool.utils import (
    enumerate_filename,
    is_server_running,
    list_folder_recursive,
    parse_timestamp,
    remove_pid_file,
    warn_if_generator_is_not_used,
    write_pid_file,
)


def test_folder_list(data_path, regtest):
    for path in list_folder_recursive(data_path("../etc"), also_folders=False):
        print(path, file=regtest)

    for path in list_folder_recursive(data_path("../etc"), also_folders=True):
        print(path, file=regtest)


def test_enumerate_filename(tmpdir):
    fldr = tmpdir.strpath
    fname = tmpdir.join("abc").strpath

    def ef(p):
        return enumerate_filename(p)[0]

    assert ef(fname) == os.path.join(fldr, "abc_0")
    assert ef(fname) == os.path.join(fldr, "abc_0")

    fname = tmpdir.join("abc.txt").strpath
    assert ef(fname) == os.path.join(fldr, "abc_0.txt")
    next_name = ef(fname)
    assert next_name == os.path.join(fldr, "abc_0.txt")

    def touch(path):
        open(path, "w").close()
        return path

    touch(fname)
    touch(next_name)
    next_name = ef(fname)
    assert next_name == os.path.join(fldr, "abc_1.txt")

    touch(next_name)
    next_name = ef(fname)
    assert next_name == os.path.join(fldr, "abc_2.txt")

    touch(os.path.join(fldr, "abc_9.txt"))
    next_name = ef(fname)
    assert next_name == os.path.join(fldr, "abc_10.txt")

    fname_1 = touch(os.path.join(fldr, "xyz.txt"))
    fname_2 = touch(os.path.join(fldr, "uvw_3.txt"))

    next_1, next_2 = enumerate_filename(fname_1, fname_2)
    assert next_1 == os.path.join(fldr, "xyz_4.txt")
    assert next_2 == os.path.join(fldr, "uvw_4.txt")


def test_pid_functions(monkeypatch, tmpdir, regtest):

    config = MagicConfig()
    config.server.pid_file = tmpdir.join("datapool.pid").strpath
    config.print_(fh=regtest)

    assert is_server_running(config) is False
    write_pid_file(config)
    assert is_server_running(config) is True
    remove_pid_file(config)
    assert is_server_running(config) is False


def test_parse_timestamp(regtest):
    p = "2017 2017-10 2017-10-01 2017-10-01:23 2017-10-01:23:12 2017-10-01:23:12:01"
    for pi in p.split(" "):
        print(str(parse_timestamp(pi)), file=regtest)

    p = "17 2017-13 2017-10-32 2017-10-01:25 2017-10-01:23:77 2017-10-01:23:12:71"
    for pi in p.split(" "):
        with pytest.raises(ValueError):
            parse_timestamp(pi)


def test_warn_if_generator_is_not_used():
    @warn_if_generator_is_not_used
    def one_element():
        yield 1

    i = one_element()
    assert not i.iterated
    list(i)
    assert i.iterated

    @warn_if_generator_is_not_used
    def empty():
        return
        yield

    i = empty()
    assert not i.iterated
    list(i)
    assert i.iterated

    with pytest.raises(AssertionError):

        @warn_if_generator_is_not_used
        def classic_function():
            return

# encoding: utf-8
from __future__ import absolute_import, division, print_function

import pytest
from sqlalchemy.orm import sessionmaker

from datapool.database import dump_db, setup_db
from datapool.errors import DataPoolException
from datapool.instance.db_objects import ParameterDbo, SiteDbo, SourceDbo, SourceTypeDbo
from datapool.instance.domain_objects import Signal
from datapool.instance.signal_model import (
    _commit,
    check_and_commit,
    check_signals_against_db,
)
from datapool.instance.uniform_file_format import parse_timestamp
from datapool.utils import iter_to_list

check_signals_against_db = iter_to_list(check_signals_against_db)


@pytest.fixture
@iter_to_list
def signals():
    for d in range(3):
        dt = "{:4d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
            2015, 12, d + 1, 12 + d, 11, 12
        )
        dt = parse_timestamp(dt)
        yield Signal(
            dict(
                timestamp=dt,
                site="example_site",
                source="example_source",
                parameter="temperature",
                value=float(-3 + d),
            )
        )

        yield Signal(
            dict(
                timestamp=dt,
                coord_x=1,
                coord_y=2,
                coord_z=3,
                source="example_source",
                parameter="wind speed",
                value=float(10 + 10 * d),
            )
        )


@pytest.fixture(scope="function")
def engine_with_example_data(engine):

    session = sessionmaker(bind=engine)()
    session.add(ParameterDbo(name="wind speed", description="", unit="km/h"))
    session.add(ParameterDbo(name="temperature", description="", unit="C"))
    site = SiteDbo(
        name="example_site",
        description="",
        street="",
        postcode="666",
        city="hell",
        coord_x=111,
        coord_y=222,
    )
    session.add(site)
    source_type = SourceTypeDbo(name="example_source_type")
    session.add(source_type)
    session.add(
        SourceDbo(name="example_source", serial="000000", source_type=source_type)
    )
    session.commit()
    return engine


def test_check_signals_against_empty_db(signals, engine, config, regtest):

    for msg in check_signals_against_db(signals, engine):
        print(msg, file=regtest)


def test_check_signals_against_valid_db(
    signals, engine_with_example_data, config, regtest
):

    for result in check_signals_against_db(signals, engine_with_example_data):
        assert isinstance(result, Signal)

    iter_to_list(_commit)(signals, engine_with_example_data)
    dump_db(config.db, file=regtest)

    # no new signals, no exceptions:
    assert not iter_to_list(check_signals_against_db)(signals, engine_with_example_data)


def test_check_and_commit(signals, engine_with_example_data, config, regtest):

    signals, exceptions = check_and_commit(signals, engine_with_example_data)
    assert not exceptions
    assert len(signals) == 6
    dump_db(config.db, file=regtest)

    # no new signals, no exceptions:
    assert not list(check_signals_against_db(signals, engine_with_example_data))

    print(file=regtest)
    print("add mix of new and existing signals".upper(), file=regtest)
    signals2 = [s.copy() for s in signals]
    for signal in signals2:
        signal.timestamp = signal.timestamp.replace(day=20)

    signals, exceptions = check_and_commit(signals + signals2, engine_with_example_data)
    assert not exceptions
    assert len(signals) == 6
    dump_db(config.db, ["signal"], file=regtest)

    for s in signals[:3]:
        s.value += 1

    print(file=regtest)
    print("add existing signals with modified values".upper(), file=regtest)
    print(file=regtest)
    for result in check_signals_against_db(signals, engine_with_example_data):
        print(result, file=regtest)

    signals, exceptions = check_and_commit(signals + signals2, engine_with_example_data)
    assert len(exceptions) == 3
    assert len(signals) == 0

    dump_db(config.db, ["signal"], file=regtest)


def test_check_and_commit_duplicate(signals, engine_with_example_data, config, regtest):

    import copy

    signals2 = copy.deepcopy(signals)
    for signal in signals2:
        signal.value += 1000

    signals = signals.copy() + signals2

    signals, exceptions = check_and_commit(signals, engine_with_example_data)
    assert not exceptions
    assert len(signals) == 6
    dump_db(config.db, file=regtest)

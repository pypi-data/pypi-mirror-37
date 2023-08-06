#! /usr/bin/env python
# encoding: utf-8
from __future__ import absolute_import, division, print_function

from datetime import datetime

import pytest
from sqlalchemy.orm import sessionmaker

from datapool.comment_model import add_comment, delete_comment
from datapool.database import dump_db
from datapool.instance.db_objects import (CommentDbo, SignalCommentAssociation,
                                          SignalDbo)
from datapool.instance.domain_objects import Signal
from datapool.instance.signal_model import check_and_commit

from .test_signal_model import engine_with_example_data  # NOQA


@pytest.fixture(scope="function")
def engine_with_signal_and_comment(engine_with_example_data):

    signal = Signal(
        dict(
            signal_id=1000,
            timestamp=datetime(1970, 4, 8),
            site="example_site",
            source="example_source",
            parameter="temperature",
            value=42,
        )
    )
    signals, exceptions = check_and_commit([signal], engine_with_example_data)
    assert not exceptions

    comment_dbo = add_comment(
        engine_with_example_data,
        signal_id=1000,
        text="example comment",
        author="schmittu",
        comment_id=1234,
    )

    assert comment_dbo.comment_id == 1234

    return engine_with_example_data


def test_add_comment(engine_with_signal_and_comment, config, regtest):
    dump_db(config.db, file=regtest)


def test_delete_comment(engine_with_signal_and_comment):
    delete_comment(engine_with_signal_and_comment, 1234)

    session = sessionmaker(bind=engine_with_signal_and_comment)()

    comments = session.query(CommentDbo).all()
    assert len(comments) == 0

    associations = session.query(SignalCommentAssociation).all()
    assert len(associations) == 0


def test_delete_signal(engine_with_signal_and_comment):

    session = sessionmaker(bind=engine_with_signal_and_comment)()
    associations = session.query(SignalCommentAssociation).all()
    assert len(associations) == 1

    signals = session.query(SignalDbo).all()
    assert len(signals) == 1

    session.delete(signals[0])
    session.commit()

    # check deletion cascade:
    associations = session.query(SignalCommentAssociation).all()
    assert not associations

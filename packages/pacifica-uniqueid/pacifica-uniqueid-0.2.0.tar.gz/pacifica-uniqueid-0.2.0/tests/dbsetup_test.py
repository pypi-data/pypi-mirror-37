#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the database connection logic."""
import mock
import peewee
from pacifica.uniqueid.orm import try_db_connect, UniqueIndex


@mock.patch.object(UniqueIndex, 'database_connect')
def test_bad_db_connection(mock_db_connect):
    """Test a failed db connection."""
    mock_db_connect.side_effect = peewee.OperationalError(
        mock.Mock(), 'Error')
    hit_exception = False
    try:
        try_db_connect(18)
    except peewee.OperationalError:
        hit_exception = True
    assert hit_exception

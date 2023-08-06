# -*- coding: UTF-8 -*-
"""
Unit tests for the vlab_ipam_api.lib.database module
"""
import types
import unittest
from mock import MagicMock, patch

from vlab_ipam_api.lib import database


class TestDatabase(unittest.TestCase):
    """A suite of tests for the vlab_ipam_api.lib.database module"""

    def setUp(self):
        """Runs before every test case"""
        # mock away the psycopg2 module
        self.patcher = patch('vlab_ipam_api.lib.database.psycopg2')
        self.mocked_psycopg2 = self.patcher.start()
        self.mocked_connection = MagicMock()
        self.mocked_cursor = MagicMock()
        self.mocked_psycopg2.connect.return_value = self.mocked_connection
        self.mocked_connection.cursor.return_value = self.mocked_cursor
        # General mocked response
        self.mocked_cursor.fetchone.side_effect = [('foo', 'string'), ('bar', 'string'), StopIteration('test')]

    def tearDown(self):
        """Runs after every test case"""
        self.patcher.stop()

    def test_init(self):
        """Simple test that we can instantiate Database class for testing"""
        db = database.Database()
        self.assertTrue(isinstance(db, database.Database))
        self.assertTrue(db._connection is self.mocked_connection)
        self.assertTrue(db._cursor is self.mocked_cursor)

    def test_context_manager(self):
        """Database support use of `with` statement and auto-closes connection"""
        with database.Database() as db:
            pass
        self.assertTrue(self.mocked_connection.close.call_count is 1)

    def test_close(self):
        """Calling Database.close() closes the connection to the DB"""
        db = database.Database()
        db.close()
        self.assertTrue(self.mocked_connection.close.call_count is 1)

    def test_executemany(self):
        """Happy path test for the Database.executemany method"""
        db = database.Database()
        result = db.executemany(sql="SELECT * from FOO WHERE bar = %s", params=('bat',))
        self.assertTrue(isinstance(result, types.GeneratorType))


    def test_execute(self):
        """Happy path test for the Database.executemany method"""
        db = database.Database()
        result = db.execute(sql="SELECT * from FOO WHERE bar LIKE 'baz'")
        self.assertTrue(isinstance(result, types.GeneratorType))

if __name__ == '__main__':
    unittest.main()

# -*- coding: UTF-8 -*-
"""This module creates a simpler way to work with the vLab IPAM database"""
import random
from collections import namedtuple

import psycopg2

from vlab_ipam_api.lib import const
from vlab_ipam_api.lib.exceptions import DatabaseError


class Database(object):
    """Simplifies communication with the database.

    The goal of this object is to make basic interactions with the database
    simpler than directly using the psycopg2 library. It does this by reducing
    the number of API methods, providing handy built-in methods for common needs
    (like listing tables of a database), auto-commit of transactions, and
    auto-rollback of bad SQL transactions.

    :param user: The username when connection to the database
    :type user: String, default postgres

    :param dbname: The specific database to connection to. InsightIQ utilizes
                   a different database for every monitored cluster, plus one
                   generic database for the application (named "insightiq").
    :type dbname: String, default insightiq
    """
    def __init__(self, user='postgres', dbname='vlab_ipam'):
        self._connection = psycopg2.connect(user=user, dbname=dbname)
        self._cursor = self._connection.cursor()

    def __enter__(self):
        """Enables use of the ``with`` statement to auto close database connection
        https://docs.python.org/2.7/reference/datamodel.html#with-statement-context-managers

        Example::

          with Database() as db:
              print(list(db.port_info(port_conn)))
        """
        return self

    def __exit__(self, exc_type, exc_value, the_traceback):
        self._connection.close()

    def execute(self, sql, params=None):
        """Run a single SQL command

        :Returns: Generator

        :param sql: **Required** The SQL syntax to execute
        :type sql: String

        :param params: The values to use in a parameterized SQL query
        :type params: Iterable

        This method is implemented as a Python Generator:
        https://wiki.python.org/moin/Generators
        This means you muse iterate over the results::

            db = Database()
            for row in db.execute("select * from some_table;"):
                print(row)

        If you want all the rows as a single thing, just use ``list``::

            db = Database()
            data = list(db.execute("select * from some_table;")

        But **WARNING** that might cause the program to run out of memory and crash!
        That reason is why this method is a generator by default ;)

        To perform a parameterized query (i.e. avoid SQL injection), provided
        the parameters as an iterable::

            db = Database()
            # passing in "foo_column" alone would try and string format every
            # character of "foo_column" into your SQL statement.
            # Instead, make "foo_column" a tuple by wrapping it like ("foo_column",)
            # Note: the trailing comma is required.
            data = list(db.execute("select %s from some_table", ("foo_column",)))
        """
        return self._query(sql, params=params, many=False)

    def executemany(self, sql, params):
        """Run the SQL for every iteration of the supplied params

        This method behaves exactly like ``execute``, except that it can perform
        multiple SQL commands in a single transaction. The point of this method
        is so you can retain Atomicity when you must execute the same SQL with
        different parameters. This method isn't intended to be faster than
        looping over the normal `execute` method with the different parameters.

        :Returns: Generator

        :param sql: **Required** The SQL syntax to execute
        :type sql: String

        :param params: **Required** The parameterized values to iterate
        :type params: Iterable
        """
        return self._query(sql, params=params, many=True)

    def _query(self, sql, params=None, many=False):
        """Internal method for running SQL commands

        The code difference between execute, and executemany is just the method
        we call on the cursor object.

        :Returns: Generator

        :param sql: **Required** The SQL syntax to execute
        :type sql: String

        :param params: The values to use in a parameterized SQL query
        :type params: Iterable

        :param many: Set to True to call ``executemany``
        :type many: Boolean, default is False
        """
        if many:
            call = getattr(self._cursor, 'executemany')
        else:
            call = getattr(self._cursor, 'execute')
        try:
            call(sql, params)
            self._connection.commit()
        except psycopg2.Error as doh:
            # All psycopg2 Exceptions are subclassed from psycopg2.Error
            self._connection.rollback()
            raise DatabaseError(message=doh.pgerror, pgcode=doh.pgcode)
        else:
            data = self._cursor.fetchone()
            while data:
                yield data
                data = self._cursor.fetchone()

    def close(self):
        """Disconnect from the database"""
        self._connection.close()

    def add_port(self, target_addr, target_port, target_name, target_component):
        """Create the record for a port mapping rule. Returns the local connection
        port that maps to the remote machine target port.

        :Returns: Integer

        :param target_addr: The IP address of the remote machine.
        :type target_addr: String

        :param target_port: The port on the remote machine to map to.
        :type target_port: Integer

        :param target_name: The human name given to the remote machine
        :type target_name: String

        :param target_component: The category/type of remote machine
        :type target_Component: String
        """
        sql = """INSERT INTO ipam (conn_port, target_addr, target_port, target_name, target_component)
                 VALUES (conn_port, target_addr, target_port, target_name, target_component);"""
        for _ in range(const.VLAB_INSERT_MAX_TRIES):
            try:
                conn_port = random.randint(const.VLAB_PORT_MIN, const.VLAB_PORT_MAX)
                self.execute(sql=sql, params=(conn_port, target_addr, target_port, target_name, target_component))
            except DatabaseError as doh:
                if doh.pgcode == '23505':
                    # port already in use
                    continue
                else:
                    raise doh
            else:
                # insert worked
                break
        else:
            # max tries exceeded
            raise RuntimeError('Failed to create port map after %s tries' % const.VLAB_INSERT_MAX_TRIES)
        return port

    def delete_port(self, conn_port):
        """Destroy a port mapping record

        :Returns: None

        :param conn_port: The local port connection that maps to a remote machine
        :type conn_port: Integer
        """
        sql = "DELETE FROM ipam WHERE conn_port=(%s);"
        self.execute(sql=sql, params=(conn_port,))

    def port_info(self, conn_port):
        """Obtain the remote port and remote address that a local port maps to.

        :Returns: Tuple

        :param conn_port: The local port connection that maps to a remote machine
        :type conn_port: Integer
        """
        sql = "SELECT conn_port, target_port, target_addr FROM ipam WHERE conn_port=(%s);"
        rows = list(self.execute(sql, params=(conn_port,)))
        target_port, target_addr = rows[0]
        return target_port, target_addr

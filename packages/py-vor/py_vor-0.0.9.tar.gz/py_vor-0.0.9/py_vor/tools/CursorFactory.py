# -*- coding: utf-8 -*-

"""CursorFactory
Object to return a cursor based on the engine name and connection string parameters.
Author: ksco92"""

import pymssql
import socket

import pg8000
import pymysql


class CursorFactory:
    """Object to return a cursor based on the engine name and connection string parameters."""

    def __init__(self, engine, host, port, username, password, schema, autocommit=False):
        self.engine = engine
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.schema = schema
        self.autocommit = autocommit

    ##########################################
    ##########################################

    def create_cursor(self):

        """Creates a cursor based on the engine provided to the runner."""

        if self.engine == 'mysql':
            conn = pymysql.connect(host=self.host, port=self.port, user=self.username, passwd=self.password,
                                   db=self.schema, autocommit=self.autocommit, connect_timeout=36000,
                                   local_infile=True,
                                   max_allowed_packet=16 * 1024, charset='utf8')

        elif self.engine in ('redshift', 'postgresql'):

            conn = pg8000.connect(user=self.username, password=self.password, host=self.host, port=self.port,
                                  database=self.schema)
            conn._usock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

            if self.autocommit:
                conn.autocommit = True

        elif self.engine == 'sqlserver':

            conn = pymssql.connect(driver="{SQL Server}", server=self.host + ',' + str(self.port), database=self.schema,
                                   uid=self.username, pwd=self.password, autocommit=self.autocommit)

        else:
            return None

        return conn.cursor()

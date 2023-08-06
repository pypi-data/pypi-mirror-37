# coding:utf-8

from __future__ import absolute_import

import logging

from six import integer_types
from DBUtils.PersistentDB import PersistentDB
from DBUtils.PooledDB import PooledDB
from orator import DatabaseManager
from orator import Model as BaseModel
from orator.connectors import Connector
from orator.exceptions.connectors import ConnectorException
from orator.connectors.mysql_connector import (MySQLConnector, keys_fix)
from orator.connectors.postgres_connector import PostgresConnector
from orator.connectors.sqlite_connector import SQLiteConnector
from orator.connections.connection import (Connection, QueryBuilder, query_logger)


slow_query_logger = logging.getLogger('orator.slow_query')


class MissingDBConfig(ConnectorException):
    def __init__(self, arg):
        message = 'Missing database config "%s" configuration' % arg
        super(MissingDBConfig, self).__init__(message)


class UnsupportedPoolPolicy(ConnectorException):
    def __init__(self, policy):
        message = 'Pool Policy "%s" is not supported' % policy
        super(UnsupportedPoolPolicy, self).__init__(message)


class ConnectorPatcher(object):
    ''' Patch orator connector '''

    RESERVED_KEYWORDS_EXT = [
        'pool_policy', 'log_slow_query', 'slow_query_time'
    ]

    Connector.pool = {}

    @staticmethod
    def _do_connect(self, **kwargs):
        _name = kwargs.get('name', None)
        _config = self.get_config(kwargs)
        if not Connector.pool or _name not in Connector.pool:
            Connector.pool[_name] = {}
            _pool_policy = kwargs.get('pool_policy', None)
            if not _pool_policy:
                Connector.pool[_name]['policy'] = PooledDB
            elif _pool_policy.lower() == 'persistent':
                Connector.pool[_name]['policy'] = PersistentDB
            elif _pool_policy.lower() == 'pooled':
                Connector.pool[_name]['policy'] = PooledDB
            else:
                raise UnsupportedPoolPolicy(kwargs.get('pool_policy'))
            Connector.pool[_name]['pool'] = Connector.pool[_name]['policy'](
                creator=self.get_api(),
                **_config
            )
        connection = Connector.pool[_name]['pool'].connection()
        if Connector.pool[_name]['policy'] is PersistentDB:
            return connection._con
        else:
            return connection._con._con

    @staticmethod
    def _mysql_do_connect(self, config):
        config = dict(config.items())
        for key, value in keys_fix.items():
            config[value] = config[key]
            del config[key]

        config['autocommit'] = True
        config['cursorclass'] = self.get_cursor_class(config)

        return super(MySQLConnector, self)._do_connect(**config)

    @staticmethod
    def _postgres_do_connect(self, config):
        connection = super(PostgresConnector, self)._do_connect(
            connection_factory=self.get_connection_class(config),
            **config
        )

        if config.get('use_unicode', True):
            PostgresConnector.extensions.register_type(PostgresConnector.extensions.UNICODE,
                                                       connection)
            PostgresConnector.extensions.register_type(PostgresConnector.extensions.UNICODEARRAY,
                                                       connection)

        connection.autocommit = True

        return connection

    @staticmethod
    def _sqlite_do_connect(self, config):
        connection = super(SQLiteConnector, self)._do_connect(**config)
        connection.isolation_level = None
        connection.row_factory = SQLiteConnector.DictCursor

        # We activate foreign keys support by default
        if config.get('foreign_keys', True):
            connection.execute("PRAGMA foreign_keys = ON")

        return connection


class ConnectionPatcher(object):
    ''' Patch orator connection '''

    @staticmethod
    def _init(self, connection, database='', table_prefix='', config=None,
             builder_class=QueryBuilder, builder_default_kwargs=None):
        """
        :param connection: A dbapi connection instance
        :type connection: Connector

        :param database: The database name
        :type database: str

        :param table_prefix: The table prefix
        :type table_prefix: str

        :param config: The connection configuration
        :type config: dict
        """
        self._connection = connection
        self._cursor = None

        self._read_connection = None

        self._database = database

        if table_prefix is None:
            table_prefix = ''

        self._table_prefix = table_prefix

        if config is None:
            config = {}

        self._config = config

        self._reconnector = None

        self._transactions = 0

        self._pretending = False

        self._builder_class = builder_class

        if builder_default_kwargs is None:
            builder_default_kwargs = {}

        self._builder_default_kwargs = builder_default_kwargs

        self._logging_queries = config.get('log_queries', False)
        self._logged_queries = []

        self._log_slow_query = bool(config.get('log_slow_query', False))
        _default_slow_query_time = 2000
        self._slow_query_time = config.get('slow_query_time', _default_slow_query_time)
        if not isinstance(self._slow_query_time, (integer_types, float)):
            raise TypeError('Database configuration argument \'slow_query_time\' need a numeric')
        if self._slow_query_time <= 0:
            self._slow_query_time = _default_slow_query_time

        # Setting the marker based on config
        self._marker = None
        if self._config.get('use_qmark'):
            self._marker = '?'

        self._query_grammar = self.get_default_query_grammar()

        self._schema_grammar = None

        self._post_processor = self.get_default_post_processor()

        self._server_version = None

        self.use_default_query_grammar()

    @staticmethod
    def _log_query(self, query, bindings, time_=None):
        if self._log_slow_query:
            if time_ and time_ >= self._slow_query_time:
                _log_msg = 'Executed {query} in {elapsed_time}ms'.format(query=query,
                                                                         elapsed_time=time_)
                slow_query_logger.warning(_log_msg, extra={
                    'query': query, 'bindings': bindings, 'elapsed_time': time_
                })

        if self.pretending():
            self._logged_queries.append(self._get_cursor_query(query, bindings))

        if not self._logging_queries:
            return

        query = self._get_cursor_query(query, bindings)

        if query:
            log = 'Executed %s' % (query,)

            if time_:
                log += ' in %sms' % time_

            query_logger.debug(log,
                               extra={
                                   'query': query,
                                   'bindings': bindings,
                                   'elapsed_time': time_
                               })


def register_slow_query_logger(logger):
    global slow_query_logger
    if not isinstance(logger, logging.Logger):
        raise TypeError('A logging.Logger object is required for function \'register_slow_query_logger\'')
    slow_query_logger = logger


class Orator(object):
    def __init__(self, app=None, manager_cls=DatabaseManager):
        self._patch_orm()
        self._db = None
        self.Model = BaseModel
        self._manager_cls = manager_cls

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if 'DATABASE' not in app.config:
            raise MissingDBConfig('DATABASE')
        self._db = self._manager_cls(app.config['DATABASE'])
        self.Model.set_connection_resolver(self._db)

    def __getattr__(self, item):
        return getattr(self._db, item)

    @staticmethod
    def _patch_orm():
        ''' Patch orator '''
        Connector._do_connect = ConnectorPatcher._do_connect

        MySQLConnector.RESERVED_KEYWORDS.extend(ConnectorPatcher.RESERVED_KEYWORDS_EXT)
        MySQLConnector._do_connect = ConnectorPatcher._mysql_do_connect

        PostgresConnector.RESERVED_KEYWORDS.extend(ConnectorPatcher.RESERVED_KEYWORDS_EXT)
        PostgresConnector._do_connect = ConnectorPatcher._postgres_do_connect

        SQLiteConnector.RESERVED_KEYWORDS.extend(ConnectorPatcher.RESERVED_KEYWORDS_EXT)
        SQLiteConnector._do_connect = ConnectorPatcher._sqlite_do_connect

        Connection.__init__ = ConnectionPatcher._init
        Connection.log_query = ConnectionPatcher._log_query

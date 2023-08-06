# -*- coding: utf-8 -*-
import sqlalchemy as sa

from abc import ABCMeta, abstractmethod
from ..exceptions import SchemingError


class BaseDatabase(metaclass=ABCMeta):
    """docstring for Database
    """
    conn_type = None
    conn_str_template = '{conn_type}://{user}:{pass}@{host}:{port}/{database}'

    def __init__(self, *args, **kwargs):
        self._extras = kwargs.pop('extras', {})
        self._conn_kwargs = self.parse_connection_kwargs(kwargs)
        self._engine = sa.create_engine(self.database_uri, connect_args=self._extras, echo=False)
        self._conn = None

    @property
    def connection(self):
        if self._conn is None:
            try:
                self._conn = self._engine.connect()
            except Exception as err:
                raise Exception(
                    'Could not connect to database: %s' % err)
        return self._conn

    @property
    def database_uri(self):
        return self.conn_str_template.format(**self._conn_kwargs)

    def parse_connection_kwargs(self, conn_kwargs):
        expected_fields = {
            'user', 
            'pass', 
            'host', 
            'port', 
            'database',
        }

        new_kwargs = {'conn_type': self.conn_type}

        for field in expected_fields:
            try:
                new_kwargs[field] = conn_kwargs[field]
            except KeyError:
                raise SchemingError(
                    'Database connection requires attribute: %s' % field)
        return new_kwargs

    def run_query(self, sql, params=None, as_dict=True):
        """Execute a SQL query and return the results.
        """
        cursor = self.connection.execute(sa.sql.text(sql), params)
        for record in cursor.fetchall():
            yield dict(record) if as_dict else record

    @abstractmethod
    def get_version(self):
        return

    @abstractmethod
    def get_tables(self):
        return

    @abstractmethod
    def get_views(self):
        return

# -*- coding: utf-8 -*-
from .base import BaseDatabase
from ..exceptions import SchemingError


SQL_TEMPLATE = '''
SELECT
   table_schema,
   table_name,
   column_name,
   ordinal_position,
   data_type,
   is_nullable,
   character_maximum_length,
   numeric_precision,
   numeric_scale
FROM information_schema.columns
'''


class Database(BaseDatabase):
    """docstring for Postgresql database object.
    """
    conn_type = 'postgresql'

    def __init__(self, *args, **kwargs):
        super(Database, self).__init__(*args, **kwargs)

    def get_version(self):
        pass

    def get_schemas(self):
        pass

    def get_tables(self, schema=None):
        template = SQL_TEMPLATE
        params = {}
        if schema:
            template += ' WHERE table_schema = :schema'
            params = {'schema': schema}
        return self.run_query(template, params)

    def get_views(self):
        pass

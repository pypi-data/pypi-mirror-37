# -*- coding: utf-8 -*-
from .base import BaseDatabase
from ..exceptions import SchemingError


class Database(BaseDatabase):
    """docstring for Postgresql database object.
    """
    conn_type = 'mysql'

    def __init__(self, *args, **kwargs):
        super(Database, self).__init__(*args, **kwargs)

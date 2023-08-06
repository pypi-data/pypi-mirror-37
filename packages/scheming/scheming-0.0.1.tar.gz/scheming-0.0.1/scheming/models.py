
class Database(object):
    pass


class Schema(object):
    properties = {
        'oid',
        'name',
    }


class Table(object):
    properties = {
        'oid',
        'schema',
        'name'
    }


class Column(object):
    properties = {
        'oid',
        'table',
        'name',
        'ordinal_position',
        'data_type',
        'is_nullable',
    }


class ForeignKey(object):
    pass

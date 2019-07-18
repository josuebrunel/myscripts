from contextlib import contextmanager
import logging
import sqlite3


logger = logging.getLogger('mydb')


@contextmanager
def connect(dbname=':memory:'):
    db = sqlite3.connect(dbname)
    try:
        yield db
    finally:
        db.close()


class FieldType(object):
    INTEGER = 'INTEGER'
    TEXT = 'TEXT'
    BLOB = 'BLOB'
    REAL = 'REAL'
    NUMERIC = 'NUMERIC'


class Field(object):

    def __init__(self, name, datatype, max_length=None, not_null=False,
                 primary_key=False, auto_increment=False, default_value=None,
                 unique=False, indexable=False, foreign_key=None, check=None):
        self.name = name
        self.datatype = datatype
        self.max_length = max_length
        self.not_null = not_null
        self.primary_key = primary_key
        self.auto_increment = auto_increment
        self.default_value = default_value
        self.unique = unique
        self.indexable = indexable
        self.value = self.default_value

    def __str__(self):
        return '%s %s' % (self.name, self.datatype)

    def __repr__(self):
        return '<Field: %s>' % self.__str__()

    def __set__(self, instance, value):
        instance.value = value

    def __get__(self, instance, klass):
        if instance is None:
            return self
        return instance.value

    @property
    def sql(self):
        sql = '{} {}'.format(self.name, self.datatype)
        if self.max_length:
            pass
        if self.primary_key:
            sql = ' '.join((sql, 'PRIMARY KEY'))
        if self.auto_increment:
            sql = ' '.join((sql, 'AUTOINCREMENT'))
        if self.not_null:
            sql = ' '.join((sql, 'NOT NULL'))
        if self.default_value:
            sql = ' '.join((sql, 'DEFAULT ({})'.format(self.default_value)))
        if self.unique:
            sql = ' '.join((sql, 'UNIQUE'))
        return sql


class Model(object):

    _Meta = None

    def __init__(self, *args, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)

    @classmethod
    def get_table_name(cls):
        if cls._Meta and getattr(cls._Meta, 'tablename'):
            return cls._Meta.tablename
        return cls.__name__

    @classmethod
    def fields(cls):
        has_id = False
        columns = []
        for fieldname, field in cls.__dict__.items():
            if not isinstance(field, (Field,)):
                continue
            if not has_id:
                has_id = field.primary_key
            columns.append(field)
        if not has_id:
            columns.append(Field('id', FieldType.INTEGER, primary_key=True,
                                 auto_increment=True, unique=True, not_null=True))
        return columns

    @classmethod
    def sql(cls):
        sql = 'create table if not exists %s' % cls.get_table_name()
        sql = '%s (%s' % (sql, ', '.join([field.sql for field in cls.fields()]))
        # foreign keys handling
        if getattr(cls._Meta, 'foreign_keys', None):
            sql = '%s,%s' % (sql, ', '.join([' FOREIGN KEY (%s) REFERENCES %s(%s)' % fk for fk in cls._Meta.foreign_keys]))
        sql += ' );'
        return sql


def create_tables(models, dbname=':memory:'):
    with connect(dbname) as db:
        cursor = db.cursor()
        for model in models:
            cursor.execute(model.sql())

from contextlib import contextmanager
import sqlite3

from .fields import Field, FieldType


@contextmanager
def connect(dbname=':memory:'):
    db = sqlite3.connect(dbname)
    try:
        yield db
    finally:
        db.close()


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

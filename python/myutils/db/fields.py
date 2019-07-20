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

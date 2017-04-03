import sqlite3


class NoCursorFound(Exception):
    pass


class SQLQueryBase(object):

    def __init__(self, keyword, table, columns=None, conditions=None, order_by=None, order='ASC', limit=None):
        self._sql_query = None
        self.keyword = keyword
        self.table = table
        self._columns = columns
        self._conditions = conditions
        self._order_by = order_by
        self._order = order
        self._limit = limit
        self._build_query()

    def _build_query(self):
        self._command()
        self._build_columns()
        self._build_conditions()
        self._build_order_by()
        self._build_limit()

    def _command(self):
        raise NotImplemented

    def _build_columns(self):
        if not self._columns and self.keyword != 'SELECT':
            return ''
        elif not self._columns:
            columns = '*'
        else:
            columns = ', '.join(self._columns)
        self._sql_query += ' %s FROM %s' % (columns, self.table)

    def _build_conditions(self):
        if not self._conditions:
            return
        clause = 'WHERE '
        condition = ' AND '.join('%s %s %s' % cond for cond in self._conditions)
        self._sql_query += ' %s %s' % (clause, condition)

    def _build_order_by(self):
        if not self._order_by:
            return
        self._sql_query += ' ORDER BY %s %s' % (self._order_by, self._order)

    def _build_limit(self):
        if not self._limit:
            return
        self._sql_query += ' LIMIT %d' % self._limit

    @property
    def query(self):
        return self._sql_query


class SelectQuery(SQLQueryBase):
    keyword = 'SELECT'

    def __init__(self, *args, **kwargs):
        super(SelectQuery, self).__init__(self.keyword, *args, **kwargs)

    def _command(self):
        self._sql_query = 'SELECT'


class InsertQuery(SQLQueryBase):
    keyword = 'INSERT'

    def __init__(self, *args, **kwargs):
        super(InsertQuery, self).__init__(self.keyword, *args, **kwargs)

    def _command(self):
        self._sql_query = 'INSERT'


class UpdateQuery(SQLQueryBase):
    keyword = 'UPDATE'

    def __init__(self, *args, **kwargs):
        super(UpdateQuery, self).__init__(self.keyword, *args, **kwargs)

    def _command(self):
        self._sql_query = 'UPDATE'


class DeleteQuery(SQLQueryBase):
    keyword = 'DELETE'

    def __init__(self, *args, **kwargs):
        super(DeleteQuery, self).__init__(self.keyword, *args, **kwargs)

    def _command(self):
        self._sql_query = 'DELETE'


class Field(object):

    def __init__(self, name, kind, null=False, default=None, pk=False):
        self.name = name
        self.type = kind
        self.null = null
        self.default = default
        self.pk = pk

    def __unicode__(self):
        return '%s' % self.__class__.__name__ +\
            '(%(name)s %(type)s %(null)s %(default)s %(pk)s)' % vars(self)

    __repr__ = __unicode__
    __str__ = __unicode__


class QuerySet(object):

    def __init__(self, table=None, cursor=None):
        self.table = table
        self.cursor = cursor
        self._cache = None
        self.query = None

    def __iter__(self):
        return iter(self._cache)

    @property
    def keys(self):
        return [key[0] for key in self.query_result.description]

    def _validate(self, query, one=False):
        self.query = query
        result = self.cursor.execute(query)
        if one:
            return result.fetchone()
        return result.fetchall()

    def from_sql_result(sql_result):
        pass

    def all(self):
        query = SelectQuery(self.table.name, None, None, order_by=self.table.pk.name).query
        result = self._validate(query)
        if result:
            self._cache = result
        return self

    def first(self):
        if self._cache:
            return self._cache[0]
        query = SelectQuery(self.table.name, None, None, limit=1).query
        return self._validate(query, one=True)

    def last(self):
        if self._cache:
            return self._cache[:-1]
        query = SelectQuery(self.table.name, None, None, order_by=self.table.pk.name,
                            order='DESC', limit=1).query
        return self._validate(query, one=True)

    def filter(self, **filters):
        pass

    def values(self, keys=None):
        if not self._cache:
            return []
        rows = self._cache
        return [row.values(keys) for row in rows]

    def delete(self):
        pass


class Table(object):

    def __init__(self, **kwargs):
        vars(self).update(kwargs)
        self.manager.table = self
        self.manager.cursor = self.cursor

    def __unicode__(self):
        return '%s %s' % (self.name)

    __repr__ = __unicode__
    __str__ = __unicode__

    manager = QuerySet()

    @property
    def pk(self):
        for field in self.fields:
            if field.pk:
                return field


class LiteROW(sqlite3.Row):

    def __init__(self, *args, **kwargs):
        super(LiteROW, self).__init__(*args, **kwargs)
        vars(self).update(self.values())

    def __repr__(self):
        return '%s' % self.__dict__.items()

    def values(self, *keys):
        if not keys:
            keys = self.keys()
        return {key: self[key] for key in keys}

    def delete(self):
        pass


class LiteORM(object):

    def __init__(self, dbfile):
        self.dbfile = dbfile
        self.connection = None
        self.cursor = None
        self._tables = None

    @property
    def _schema_query(self):
        return "SELECT * FROM sqlite_master WHERE sql NOT NULL and type = 'table' ORDER BY rootpage"

    def _inspect_db(self):
        tables = self._get_schema()
        for table in tables:
            table = self._get_table_info(table)

    def _get_table_info(self, table):
        query = 'PRAGMA table_info(%s)' % table.name
        try:
            rows = self.raw_query(query)
        except (sqlite3.OperationnalError):
            table.fields = []
            return table
        fields = []

        for row in rows.fetchall():
            field_attr = {}
            field_attr['name'] = row['name']
            field_attr['kind'] = row['type']
            field_attr['null'] = bool(row['notnull'])
            field_attr['default'] = row['dflt_value']
            field_attr['pk'] = bool(row['pk'])
            fields.append(Field(**field_attr))

        table.fields = fields
        return table

    def _get_schema(self):
        if not self.cursor:
            raise NoCursorFound()
        res = self.raw_query(self._schema_query)
        tables = []
        for row in res.fetchall():
            tables.append(Table(cursor=self.cursor, **row.values()))
        self._tables = tables
        return tables

    @property
    def tables(self):
        return self._tables

    def connect(self):
        self.connection = sqlite3.connect(self.dbfile)
        self.connection.row_factory = LiteROW
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()

    def raw_query(self, query):
        return self.cursor.execute(query)

    def execute(self, query):
        res = self.raw_query(query)
        return QuerySet(res)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        self.close()

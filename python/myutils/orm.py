import sqlite3


def parse_int(value):
    try:
        int(value)
        return value
    except (ValueError,):
        return "'%s'" % value

################
#   EXCEPTIONS
################


class NoCursorFound(Exception):
    pass


class InvalidFunctionName(Exception):
    pass

###############
#   QUERY
###############


class SQLQueryBase(object):

    FUNCTIONS = ('AVG', 'COUNT', 'SUM')

    def __init__(self, keyword, table, function=None, columns=None, conditions=None, order_by=None, order='ASC', limit=None):
        self._sql_query = None
        self.keyword = keyword
        self.table = table
        self._function = function
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

    def _check_function(self):
        if self._function.upper() not in self.FUNCTIONS:
            raise InvalidFunctionName('%s is not in %s' % (self._function, self.FUNCTIONS))
        return True

    def _build_columns(self):
        if not self._columns and self.keyword != 'SELECT':
            return ''
        elif not self._columns:
            columns = '*'
        else:
            columns = ', '.join(self._columns)
        if self._function and self._check_function():
            columns = '%s(%s)' % (self._function, columns)
        self._sql_query += ' %s FROM %s' % (columns, self.table)

    def _build_conditions(self):
        if not self._conditions:
            return
        clause = 'WHERE '
        condition = ' AND '.join('%s' % cond for cond in self._conditions)
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

    def __init__(self, table, **kwargs):
        super(SelectQuery, self).__init__(self.keyword, table, **kwargs)

    def _command(self):
        self._sql_query = 'SELECT'


class InsertQuery(SQLQueryBase):
    keyword = 'INSERT'

    def __init__(self, table, **kwargs):
        super(InsertQuery, self).__init__(self.keyword, table, **kwargs)

    def _command(self):
        self._sql_query = 'INSERT'


class UpdateQuery(SQLQueryBase):
    keyword = 'UPDATE'

    def __init__(self, table, **kwargs):
        super(UpdateQuery, self).__init__(self.keyword, table, **kwargs)

    def _command(self):
        self._sql_query = 'UPDATE'


class DeleteQuery(SQLQueryBase):
    keyword = 'DELETE'

    def __init__(self, table, **kwargs):
        super(DeleteQuery, self).__init__(self.keyword, table, **kwargs)

    def _command(self):
        self._sql_query = 'DELETE'


##################
#       DB
##################


class Field(object):

    def __init__(self, name, kind, null=False, default=None, pk=False):
        self.name = name
        self.type = kind
        self.null = null
        self.default = default
        self.pk = pk
        self.reference = None

    def __unicode__(self):
        desc = '%s: %s' % (self.type, self.name)
        if self.reference:
            desc += ' REFERENCE TO (%s)' % self.reference.table
        return '<%s>' % desc

    __repr__ = __unicode__
    __str__ = __unicode__


class FieldLookup(object):

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __call__(self):
        try:
            name, lookup = self.key.split('__')
            lookup = '__%s__' % lookup
        except (IndexError, ValueError):
            name, lookup = self.key, '__eq__'
        return '%s' % (getattr(self, lookup)(name, self.value))

    def __eq__(self, key, value):
        return '%s = %s' % (key, parse_int(value))

    __exact__ = __eq__

    def __neq__(self, key, value):
        return '%s <> %s' % (key, parse_int(value))

    def __in__(self, key, value):
        return '%s IN %s' % (key, value)

    def __iexact__(self, key, value):
        return '%s ILIKE %s' % (key, value)

    def __gt__(self, key, value):
        return '%s > %s' % (key, value)

    def __gte__(self, key, value):
        return '%s >= %s' % (key, value)

    def __lt__(self, key, value):
        return '%s < %s' % (key, value)

    def __lte__(self, key, value):
        return '%s <= %s' % (key, value)

    def __contains__(self, key, value):
        return "%s LIKE '%%%s%%'" % (key, value)

    def __icontains__(self, key, value):
        return "%s ILIKE '%%%ss%%'" % (key, value)

    def __isnull__(self, key, value):
        if value:
            return '%s IS NULL'
        return '%s IS NOT NULL'


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
            return RowTable(self.table, result.fetchone())
        return [RowTable(self.table, res) for res in result.fetchall()]

    def _filters_to_conditions(self, **filters):
        conditions = []
        for key, value in filters.items():
            conditions.append(FieldLookup(key, value)())
        return conditions

    def get(self, **filters):
        return self.filter(one_result=True, **filters)

    def count(self):
        query = SelectQuery(self.table.name, function='count').query
        result = self._validate(query, one=True)
        if not result.values():
            return 0
        return result.values().values()[0]

    def all(self):
        query = SelectQuery(self.table.name, order_by=self.table.pk.name).query
        result = self._validate(query)
        if result:
            self._cache = result
        return result

    def first(self):
        if self._cache:
            return self._cache[0]
        query = SelectQuery(self.table.name, limit=1).query
        return self._validate(query, one=True)

    def last(self):
        if self._cache:
            return self._cache[:-1]
        query = SelectQuery(self.table.name, order_by=self.table.pk.name,
                            order='DESC', limit=1).query
        return self._validate(query, one=True)

    def filter(self, one_result=False, **filters):
        conditions = self._filters_to_conditions(**filters)
        query = SelectQuery(self.table.name, conditions=conditions).query
        return self._validate(query, one=one_result)

    def values(self, keys=None):
        if not self._cache:
            return []
        rows = self._cache
        return [row.values(keys) for row in rows]

    def delete(self):
        pass


class Table(object):

    fields = []
    references = []

    def __init__(self, **kwargs):
        self._Meta = type('Meta', (object,), kwargs)

    def __unicode__(self):
        return '<Table: %s>' % (self.name)

    __repr__ = __unicode__
    __str__ = __unicode__

    manager = None

    @property
    def name(self):
        return self._Meta.name

    @property
    def pk(self):
        for field in self.fields:
            if field.pk:
                return field

    def get_field(self, fname):
        for field in self.fields:
            if field.name == fname:
                return field
        return None


class RowTable(Table):

    def __init__(self, table, row):
        super(RowTable, self).__init__(**vars(table._Meta))
        self._raw = row
        for key in row.keys():
            setattr(self, key, row[key])

    def __repr__(self):
        return self._raw.__repr__()

    @property
    def keys(self):
        return self._raw.keys()

    def values(self, *keys):
        return self._raw.values(*keys)


#############
#   ORM
#############


class LiteROW(sqlite3.Row):

    def __init__(self, *args, **kwargs):
        super(LiteROW, self).__init__(*args, **kwargs)
        vars(self).update(self.values())

    def __repr__(self):
        return '<Row: %s>' % self.__dict__.items()

    def values(self, *keys):
        if not keys:
            keys = self.keys()
        return {key: self[key] for key in keys}


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
            self._get_table_references(table)

    def _get_table_info(self, table):
        query = 'PRAGMA table_info(%s)' % table.name
        try:
            rows = self.raw_query(query)
        except (sqlite3.OperationalError):
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

    def _get_table_references(self, table):
        query = 'PRAGMA foreign_key_list(%s)' % table.name
        references = self.raw_query(query)
        for ref in references.fetchall():
            table.references.append(ref.__dict__)
            ref_from = getattr(ref, 'from')
            related_field = table.get_field(ref_from)
            related_field.reference = ref
        return table

    def _get_schema(self):
        if not self.cursor:
            raise NoCursorFound()
        res = self.raw_query(self._schema_query)
        tables = []
        for row in res.fetchall():
            table = Table(cursor=self.cursor, **row.values())
            setattr(table, 'manager', QuerySet(table=table, cursor=self.cursor))
            tables.append(table)
        self._tables = tables
        return tables

    @property
    def tables(self):
        return self._tables

    def get_table_by_name(self, tablename):
        for table in self._tables:
            if table.name == tablename:
                return table
        return None

    def connect(self):
        self.connection = sqlite3.connect(self.dbfile)
        self.connection.row_factory = LiteROW
        self.connection.text_factory = str
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()

    def raw_query(self, query):
        return self.cursor.execute(query)

    def execute(self, query):
        res = self.raw_query(query)
        return res

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        self.close()

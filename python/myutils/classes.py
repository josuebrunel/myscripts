# Bunch of my custom classes
#

from collections import defaultdict
import itertools
import logging
import operator
import sys
from xml.etree import ElementTree as etree


class Dict2Object(dict):

    class _Meta:
        name = 'Dict2Object'

    def __init__(self, data, meta_name=None):
        if meta_name:
            self._Meta.name = meta_name
        for key, value in data.items():
            if isinstance(value, (dict)):
                setattr(self, key, Dict2Object(value))
            else:
                setattr(self, key, value)
        super(Dict2Object, self).__init__(**data)

    def __unicode__(self):
        return '<%s>' % self._Meta.name

    __repr__ = __str__ = __unicode__


class Dict2ObjectLower(Dict2Object):

    def __init__(self, **kwargs):
        kwargs = {key.lower(): value for key, value in kwargs.items()}
        super(Dict2ObjectLower, self).__init__(**kwargs)


# Python-Requests
try:
    import requests

    class LoggedRequest(requests.Session):

        def __init__(self, *args, **kwargs):
            self.logger = logging.getLogger('logged_request')
            if sys.version_info.major > 2:
                super().__init__(*args, **kwargs)
            else:
                super(LoggedRequest, self).__init__(*args, **kwargs)

        def request(self, method, url, **kwargs):
            self.logger.debug('Request\n%s - %s' % (method, url))
            response = super(LoggedRequest, self).request(method, url, **kwargs)
            self.logger.debug('\n'.join(
                ['%s: %s' % (k, v) for k, v in response.request.headers.items()]
            ))
            self.logger.debug('Data: %s' % response.request.body)
            self.logger.debug('\nResponse\n%s' % response.status_code)
            self.logger.debug('\n'.join(
                ['%s: %s' % (k, v) for k, v in response.headers.items()]
            ))
            self.logger.debug('Data: %s' % response.content)

            return response

    # Substitute requests
    lrequests = LoggedRequest()
except (ImportError,) as e:
    pass


# Custom XML Element class
class ElementFactory(etree.Element):

    def __init__(self, *args, **kwargs):
        self.text = kwargs.pop('text', None)
        namespace = kwargs.pop('namespace', None)
        if namespace:
            super(ElementFactory, self).__init__(
                etree.QName(namespace, args[0]), **kwargs
            )
            self.namespace = namespace
        else:
            super(ElementFactory, self).__init__(*args, **kwargs)

    def append(self, element, allow_new=True):

        if not allow_new:
            if isinstance(element.tag, etree.QName):
                found = self.find(element.tag.text)
            else:
                found = self.find(element.tag)

            if found:
                return self

        super(ElementFactory, self).append(element)
        return self

    def extend(self, elements):
        super(ElementFactory, self).extend(elements)
        return self


class DataClass(object):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        klassname = self.__class__.__name__
        items = self.__dict__.items()
        return '<%s:%s>' % (klassname, items)


class DictManager(object):

    DELIMITOR = '__'

    class Xoperator(object):

        def __init__(self):
            self.__dict__[''] = operator.eq
            self.__dict__['in'] = self._in
            self.__dict__.update({
                fname: func for fname, func in operator.__dict__.items() if callable(func) and not fname.startswith('_')
            })

        @staticmethod
        def isnum(val):
            try:
                int(val)
                return True
            except (ValueError,):
                pass
            return False

        def icontains(self, left, right):
            return operator.contains(left.lower(), right.lower())

        def _in(self, left, right):
            return left in right

        def not_in(self, left, right):
            return left not in right

    def __init__(self, dataset, **kwargs):
        self.dataset = dataset
        self._xoperator = self.Xoperator()

    def __getitem__(self, idx):
        return self.dataset[idx]

    def __len__(self):
        return len(self.dataset)

    def __str__(self):
        return '%s' % self.dataset

    def __repr__(self):
        return '<%s: %s >' % (self.__class__.__name__, str(self))

    def _lookup(self, datum, key, value):
        keyname, _, op = key.partition(self.DELIMITOR)
        if self.DELIMITOR in op:
            if self._xoperator.isnum(keyname):
                keyname = int(keyname)
            return self._lookup(datum[keyname], op, value)
        if op not in self._xoperator.__dict__:
            if isinstance(datum, (list,)) and self._xoperator.isnum(keyname):
                keyname = int(keyname)
            return self._lookup(datum[keyname], '%s__eq' % op, value)
        return getattr(self._xoperator, op)(datum.get(keyname), value)

    def filter(self, *args, **kwargs):
        result = []
        for datum in self.dataset:
            tests = []
            for key, value in kwargs.items():
                tests.append(self._lookup(datum, key, value))
            if all(tests):
                result.append(datum)

        return DictManager(result)

    def values(self, *args):
        data = []
        for datum in self.dataset:
            cdata = {}
            for key, value in datum.items():
                if key in args:
                    cdata[key] = value
            data.append(cdata)
        return data

    def apply(self, func=lambda x: x, *args):
        for datum in self.dataset:
            for key in args:
                datum[key] = func(datum[key])
        return self

    def exists(self):
        return bool(len(self.dataset))

    def count(self):
        return len(self)

    def get(self, *args, **kwargs):
        result = self.filter(*args, **kwargs)
        if not result:
            return None
        if len(result) > 1:
            raise Exception('Multiple values resturned')
        return result[0]

    def delete(self, *args, **kwargs):
        if kwargs:
            result = self.filter(*args, **kwargs)
            if result.exists():
                self.dataset = [datum for datum in self.dataset if datum not in result.dataset]
                return True
        else:
            self.dataset = []
            return True
        return False

    def order_by(self, *args):
        self.dataset.sort(key=operator.itemgetter(*args))
        return self

    def group_by(self, *args):
        result = defaultdict(list)
        self.dataset.sort(key=operator.itemgetter(*args))
        for key, group in itertools.groupby(self.dataset, operator.itemgetter(*args)):
            result[key].extend(list(group))
        return result

    def first(self):
        return self[0]

    def last(self):
        return self[-1]

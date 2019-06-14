# Bunch of my custom classes
#
import logging
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

    OPERATIONS = {
        '': lambda left, right: left == right,
        'neq': lambda left, right: left != right,
        'gt': lambda left, right: left > right,
        'gte': lambda left, right: left >= right,
        'lt': lambda left, right: left < right,
        'lte': lambda left, right: left <= right,
        'contains': lambda left, right: right in left,
        'icontains': lambda left, right: right.lower() in left.lower(),
    }

    def __init__(self, dataset, **kwargs):
        self.dataset = dataset

    def __getitem__(self, idx):
        return self.dataset[idx]

    def __len__(self):
        return len(self.dataset)

    def __str__(self):
        return '%s' % self.dataset

    def __repr__(self):
        return '<%s: %s >' % (self.__class__.__name__, str(self))

    def filter(self, *args, **kwargs):
        result = []
        for datum in self.dataset:
            for key, value in kwargs.items():
                keyname, _, op = key.partition(self.DELIMITOR)
                if self.OPERATIONS[op](datum.get(keyname), value):
                    result.append(datum)
        return DictManager(result)

    def exists(self):
        return bool(len(self.dataset))

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

    def first(self):
        return self[0]

    def last(self):
        return self[-1]

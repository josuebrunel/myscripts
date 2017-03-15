# Bunch of my custom classes
#
import logging
from xml.etree import ElementTree as etree


class Dict2Object(object):

    def __init__(self, **kwargs):
        vars(self).update(kwargs)


# Python-Requests
try:
    import requests

    class LoggedRequest(requests.Session):

        def __init__(self, *args, **kwargs):
            self.logger = logging.getLogger('logged_request')
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
    logged_requests = LoggedRequest()
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

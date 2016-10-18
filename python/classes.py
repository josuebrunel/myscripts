# Bunch of my custom classes
#
import logging
from xml.etree import ElementTree as etree

logger = logging.getLogger('default_logger')

# Python-Requests
try:
    import requests

    class LoggedRequest(requests.Session):

        def __init__(self, *args, **kwargs):
            super(LoggedRequest, self).__init__(*args, **kwargs)

        def request(self, method, url, **kwargs):
            logger.debug('Request\n%s - %s' % (method, url))
            response = super(LoggedRequest, self).request(method, url, **kwargs)
            logger.debug('\n'.join(
                ['%s: %s' % (k, v) for k, v in response.request.headers.items()]
            ))
            logger.debug('Data: %s' % response.request.body)
            logger.debug('\nResponse\n%s' % response.status_code)
            logger.debug('\n'.join(
                ['%s: %s' % (k, v) for k, v in response.headers.items()]
            ))
            logger.debug('Data: %s' % response.content)

            return response

    # Substittude requests
    requests = LoggedRequest()
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

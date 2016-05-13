from __future__ import absolute_import, unicode_literals

import logging
from logging import Logger, handlers

class DefaultLogger(logging.Logger):
    """Yahoo Logger class
    """

    def __init__(self, name, level=logging.DEBUG):
        """
        - name : logger name
        - filename : file containing logs
        """
        super(DefaultLogger, self).__init__(name)
        self.name = name
        self.level = level

        self.setLevel(self.level)

        formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s.%(module)s.%(funcName)s: %(message)s", "%Y-%m-%d %H:%M:%S")

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.addHandler(stream_handler)


import datetime
import logging

import pytz


class Logger(object):

    def __init__(self, feature=None):
        self.feature = feature
        self.logger = self
        self.last_msg = None

    def _get_msg(self, *args):
        msg = ' '.join(args)

        if self.feature is not None:
            msg = '[{}] {}'.format(self.feature.meta['name'], msg)

        return msg

    def _get_logger(self):
        logger = logging.getLogger('bot')
        if self.feature is not None:
            logger = logger.getChild(self.feature.meta['name'])

        return logger

    def log(self, *args, level: logging = logging.INFO, **kwargs):
        time_str = datetime.datetime.now(tz=pytz.timezone('UTC')).strftime("%H:%M:%S")
        msg = self._get_msg(*args)
        self.last_msg = msg
        out = '[{}] <{}> {}'.format(time_str, logging.getLevelName(level).upper(), msg)

        if level is None:
            level = logging.INFO

        self._get_logger().log(level, msg, **kwargs)

        print(out)

    def info(self, *args):
        self.log(*args, level=logging.INFO)

    def debug(self, *args, **kwargs):
        self.log(*args, level=logging.DEBUG, **kwargs)

    def warn(self, *args):
        self.log(*args, level=logging.WARN)

    def error(self, *args):
        self.log(*args, level=logging.ERROR)

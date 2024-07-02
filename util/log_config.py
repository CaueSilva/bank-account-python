import logging
from logging import StreamHandler, LogRecord

from pythonjsonlogger import jsonlogger

LOG_LEVEL = 'LOG_LEVEL'

root = logging.getLogger()
if root.handlers:
    for handler in root.handlers:
        root.removeHandler(handler)


class TracingHandler(StreamHandler):
    def __init__(self):
        super().__init__()
        self.tracing_info = {}

    def emit(self, record: LogRecord) -> None:
        for key in self.tracing_info:
            record.__setattr__(key, self.tracing_info[key])
        super(TracingHandler, self).emit(record)


handler = TracingHandler()
logger = logging.getLogger('bank-account-python')
supported_keys = ['levelname', 'message', 'filename', 'funcName', 'lineno', 'module', 'name']
log_format = lambda x: ['%({0:s})'.format(i) for i in x]
custom_format = ' '.join(log_format(supported_keys))
formatter = jsonlogger.JsonFormatter(custom_format, timestamp=True)
handler.setFormatter(formatter)
logger.addHandler(handler)
_log_level = 'DEBUG'
logger.setLevel(_log_level)


def add_tracing_info(info: dict):
    handler.tracing_info.update(info)


__ALL__ = "logger, add_tracing_info"

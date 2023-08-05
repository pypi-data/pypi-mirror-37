import logging
import logging.handlers
import socket
import os
try:
    from threading import get_ident
except ImportError:
    from thread import get_ident

class ContextFilter(logging.Filter):

    def __init__(self):
        self.local_ip = socket.gethostbyname(socket.gethostname())

    def filter(self, record):
        record.local_ip = self.local_ip
        record.pid = os.getpid()
        record.tid = get_ident()
        return True

def getLogger(name=''):
    logger = logging.getLogger()
    return logger

def make_event_logger(app_name, syslog_ng_server):
    event_log_formatter = logging.Formatter(app_name + '_event_log: %(message)s')

    syslog_handler = None
    try:
        syslog_handler = logging.handlers.SysLogHandler(address=(syslog_ng_server, 601), facility='local7', socktype=socket.SOCK_STREAM)
    except:
        pass
    finally:
        syslog_handler = logging.handlers.SysLogHandler(address=(syslog_ng_server, 514), facility='local6')

    if syslog_handler is None:
        return

    syslog_handler.setFormatter(event_log_formatter)
    event_logger = logging.getLogger('event-log')
    event_logger.setLevel(logging.INFO)
    event_logger.addHandler(syslog_handler)

def setup_logger_handler(app_name, handler, log_level_str):
    filter = ContextFilter()
    log_level = logging.INFO
    if log_level_str is not None:
        level = log_level_str.lower()
        log_level_conf = {
            'verbose': logging.NOTSET,
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'warn': logging.WARNING,
            'error': logging.ERROR,
            'critical': logging.CRITICAL,
        }
        if level in log_level_conf:
            log_level = log_level_conf[level]

    format_str = app_name + ': %(asctime)s %(levelname)s %(local_ip)s %(pid)d.%(tid)d %(filename)s:%(lineno)d %(message)s'
    formatter = logging.Formatter(format_str)

    handler.setFormatter(formatter)
    handler.setLevel(log_level)
    handler.addFilter(filter)
    return handler

def make_logger(app_name, log_level_str=None, syslog_ng_server=None, console_debug_log=False):
    root_logger = logging.getLogger()

    basic_handlers = []
    if syslog_ng_server is not None:
        udp_syslog_handler = logging.handlers.SysLogHandler(address=(syslog_ng_server, 514), facility='local6')
        setup_logger_handler(app_name, udp_syslog_handler, log_level_str)
        basic_handlers.append(udp_syslog_handler)
        make_event_logger(app_name, syslog_ng_server)

    if console_debug_log:
        stream_handler = logging.StreamHandler()
        setup_logger_handler(app_name, stream_handler, log_level_str)
        basic_handlers.append(stream_handler)

    root_logger.handlers = []
    for h in basic_handlers:
        root_logger.setLevel(h.level)
        root_logger.addHandler(h)

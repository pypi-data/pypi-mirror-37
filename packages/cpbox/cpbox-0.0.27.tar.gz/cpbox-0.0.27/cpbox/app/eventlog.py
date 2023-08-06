from datetime import datetime
from pytz import reference
from tzlocal import get_localzone

from cpbox.app.appconfig import appconfig
from cpbox.tool import concurrent

import time
import os
import threading
import json
import logging
import socket

try:
    from threading import get_ident
except ImportError:
    from thread import get_ident

event_logger = logging.getLogger('event-log')
local_timezone = get_localzone()
local_ip = socket.gethostbyname(socket.gethostname())

log_worker = concurrent.Worker(2)
# ${time_iso_8601} ${client_ip} ${pid}.${rnd/thread_id} {$app_name} ${event_key} ${payload_json_encoded}
def add_event_log(event_key, payload):
    payload['env'] = appconfig.get_env()
    time = local_timezone.localize(datetime.now())
    time = time.strftime('%Y-%m-%dT%H:%M:%S%z')
    msg = '%s %s %s.%s %s %s %s' % (time, local_ip, os.getpid(), get_ident(), appconfig.get_app_name(), event_key, json.dumps(payload))
    log_worker.submit(event_logger.info, msg)

def log_func_call(func, *args, **kwargs):
    def timed(*args, **kw):
        start = time.time() * 1000
        result = func(*args, **kw)
        payload = {}
        payload['name'] = func.__name__
        payload['rt'] = time.time() * 1000 - start
        add_event_log('func-call', payload)
        return result
    return timed

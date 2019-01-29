import logging
import sys
import json
import threading
import inspect

import pytest
import json_logging

@pytest.fixture
def streamhandler_setup():
    def setup():
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(logging.StreamHandler(sys.stderr))
        return logger
    return setup

@pytest.fixture
def json_logging_init():
    def init():
        json_logging.ENABLE_JSON_LOGGING = True
        json_logging.init()
    return init

def test_log_output_json(capsys, streamhandler_setup, json_logging_init):
    logger = streamhandler_setup()
    json_logging_init()
    msg = 'Test'
    logger.info(msg)
    lineno = inspect.getframeinfo(inspect.currentframe()).lineno -1

    log = json.loads(capsys.readouterr().err)
    # {
    #     "type": "log",
    #     "written_at": "2019-01-26T14:03:50.832Z",
    #     "written_ts": 1548511430832071000,
    #     "component_id": "-",
    #     "component_name": "-",
    #     "component_instance": 0,
    #     "logger": "test_json_logging",
    #     "thread": "MainThread",
    #     "level": "INFO",
    #     "line_no": 30,
    #     "module": "test_json_logging",
    #     "msg": "Test"
    # }
    expect_log = {
        'msg': msg,
        'level': 'INFO',
        'type': 'log',
        'thread': threading.current_thread().name,
        'module': __name__,
        'line_no': lineno,
        'logger': logger.name
    }
    assert expect_log.items() < log.items()

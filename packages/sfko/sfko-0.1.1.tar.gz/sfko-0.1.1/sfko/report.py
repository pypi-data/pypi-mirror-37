import datetime
import json
import sched
from collections import namedtuple
from itertools import chain
from threading import Thread

import requests

from . import execute
from .util.conf import config
from .util.log import Log
from .util.redis import redis_client

_log = Log('report')


def utc_time():
    datetime.datetime.utcnow().timestamp()

class Scheduler(Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self._scheduler = sched.scheduler()

    def run(self):
        while True:
            self._scheduler.run()

    def enter(self, *args, **kwargs):
        return self._scheduler.enter(*args, **kwargs)

# _RESULTS_SCHEDULER = sched.scheduler()
_RESULTS_SCHEDULER = Scheduler()

__hour, __minute = config.results.schedule.split(':')
_RESULTS_SCHED_TIME = datetime.time(hour=int(__hour), minute=int(__minute))

def _get_next_schedule():
    now = datetime.datetime.utcnow()
    then = now + datetime.timedelta(minutes=10)
    # next_run = datetime.datetime.combine(then.date(), _RESULTS_SCHED_TIME)
    # _log.debug('Next scheduler run at %s'%(next_run))
    # return (next_run - now).total_seconds()
    return (then - now).total_seconds()

def init_scheduler():
    _log.debug('Initializing scheduler')
    _RESULTS_SCHEDULER.enter(_get_next_schedule(), 0, collect_results)
    _RESULTS_SCHEDULER.start()


HIPCHAT_URL = 'https://scalitysocial.hipchat.com/v2/room/4661513/notification'
def notify(msg, color = 'yellow', notify = False):
    data = dict(
        message = msg,
        message_format = 'text',
        notify = notify,
        color = color
    )
    token = dict(auth_token=config.results.hipchat)
    resp = requests.post(HIPCHAT_URL, json = data, params=token)


def push_to_chat(results):
    lines = []
    failed = 0
    for ts, (scenario, success) in results.items():
        status = 'Passed' if success else 'Failed'
        sline = REPORT_LINE.format(scenario=scenario.name, ts=ts, status=status)
        lines.append(sline)
        if not success:
            failed += 1
    if failed == 0:
        color = 'green'
    elif failed/len(results) < 0.5:
        color = 'yellow'
    else:
        color = 'red'
    if lines:
        rendered_report = REPORT_TEMPLATE.format(reports='\n'.join(lines))
        notify(rendered_report, color = color)


REPORT_HEADER ='SFKO Nightly Results Report'
REPORT_LINE ='{ts}    {scenario}: {status}'
OPSTATUS_LINE='\t\t{0}: {1}'

REPORT_TEMPLATE = '{header}\n{reports}'.format(header=REPORT_HEADER, reports='{reports}')


def collect_results():
    results = execute.get_results()
    _RESULTS_SCHEDULER.enter(_get_next_schedule(), 0, collect_results)
    return push_to_chat(results)

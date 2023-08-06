#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2018, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
# __status__ = "Production"
import inspect
import logging
import threading
import time
from datetime import datetime, timedelta

from doccron.table import CronTable

logger = logging.getLogger('doccron')


def tokenize(jobs):
    for jobs in jobs.splitlines():
        yield jobs.split(None, 5)


def cron(jobs):
    return CronTable(tokenize(jobs))


# noinspection PyShadowingNames
def _job_iter(job_function_map):
    job_map = {}
    for job in job_function_map.keys():
        try:
            job_map[job] = next(job)
        except StopIteration:
            pass
    while True:
        if not len(job_map):
            return
        job, next_schedule = sorted(job_map.items(), key=lambda x: x[1])[0]
        yield next_schedule, job_function_map[job]
        try:
            job_map[job] = next(job)
        except StopIteration:
            del job_map[job]


def run_jobs(simulate=False):
    job_function_map = {}
    logger.info("Searching jobs")
    for function_object in inspect.currentframe().f_back.f_globals.values():
        if inspect.isfunction(function_object):
            docstring = inspect.getdoc(function_object)
            if docstring and isinstance(docstring, str):
                docstring = docstring.strip()
                if len(docstring):
                    job_function_map[cron(docstring)] = function_object
    if simulate:
        logger.info('Simulation started')
        return _job_iter(job_function_map)
    threads = []
    for next_schedule, function_object in _job_iter(job_function_map):
        thread_count = len(threads)
        if thread_count == len(job_function_map):
            while True:
                thread = threads[thread_count-1]  # type: threading.Thread
                if not thread.is_alive():
                    interval = next_schedule - datetime.now()  # type: timedelta
                    thread = threading.Timer(interval.total_seconds(), function_object)  # type: threading.Thread
                    threads[thread_count-1] = thread
                    logger.info("Scheduling function '%s' to run at %s", function_object.__name__,
                                next_schedule.strftime('%Y-%m-%d %H:%M'))
                    thread.start()
                    break
                thread_count = len(job_function_map) if thread_count == 1 else thread_count - 1
                time.sleep(1)
        else:
            interval = next_schedule - datetime.now()  # type: timedelta
            thread = threading.Timer(interval.total_seconds(), function_object)  # type: threading.Thread
            threads.append(thread)
            thread.start()
            logger.info("Scheduling function '%s' to run at %s", function_object.__name__,
                        next_schedule.strftime('%Y-%m-%d %H:%M'))
    if len(threads):
        for thread in threads:
            thread.join()
        logger.info("Finished executing jobs")
    else:
        logger.info("No jobs found")




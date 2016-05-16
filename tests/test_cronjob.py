# -*- coding:utf8 -*-
from __future__ import (
    division, print_function, absolute_import, unicode_literals
)
import types
import pytest
from datetime import datetime
from errcron.cronjob import CronJob


def test_for_display():
    job = CronJob()
    job.set_triggers('%H', '01')
    assert str(job) == 'CronJob(trigger=[%H->01])'
    job = CronJob()
    assert str(job) == 'CronJob(trigger=[])'


def test_not_run_in_target_time():
    job = CronJob()
    job.trigger_format = '%H'
    job.trigger_time = '01'
    dt = datetime(2000, 1, 1, 1, 1, 1)
    assert job.is_runnable(dt) is True
    dt = datetime(2000, 1, 1, 0, 1, 1)
    assert job.is_runnable(dt) is False


def test_set_triggers():
    job = CronJob()
    job.set_triggers('%H', '01')
    dt = datetime(2000, 1, 1, 1, 1, 1)
    assert job.is_runnable(dt) is True
    dt = datetime(2000, 1, 1, 0, 1, 1)
    assert job.is_runnable(dt) is False
    for keys in (
        (None, '1'),
        ('1', None),
    ):
        with pytest.raises(ValueError):
            job.set_triggers(*keys)


def test_set_action():
    job = CronJob()
    job.set_action('stub.echo_hello')
    assert isinstance(job.action, types.FunctionType)


def test_set_action_not_func():
    with pytest.raises(AttributeError):
        job = CronJob()
        job.set_action('stub.echo_hello_not')


def test_do_action():
    job = CronJob()
    job.set_action('stub.echo_datetime')
    dt = datetime(2000, 1, 1, 1, 1, 1)
    assert job.do_action(dt) == '2000-01-01'


def test_do_action_with_arg():
    job = CronJob()
    job.set_action('stub.echo_datetime_with_head', 'sample')
    dt = datetime(2000, 1, 1, 1, 1, 1)
    assert job.do_action(dt) == 'sample2000-01-01'

from datetime import datetime
from errcron.cronjob import CronJob


def test_not_run_in_target_time():
    job = CronJob()
    job.trigger_format = '%H'
    job.trigger_time = '01'
    dt = datetime(2000, 1, 1, 1, 1, 1)
    assert job.is_runnable(dt) is True
    dt = datetime(2000, 1, 1, 0, 1, 1)
    assert job.is_runnable(dt) is False

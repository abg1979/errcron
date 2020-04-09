# -*- coding:utf8 -*-
"""Bot class extensions
"""
import datetime
from errcron import cronjob
from threading import RLock


class CrontabMixin(object):
    """Mix-in class to implement crontab features
    If you will use crontab by it, call activate_crontab
    """

    _lock = RLock()
    _crontab = None

    def list_crontab(self):
        return self._crontab

    def activate_crontab(self):
        """Activate polling function and register first crontab
        """
        with self._lock:
            try:
                self.stop_poller(self.poll_crontab)
            except:
                self.log.warn("Could not stop poller.", exc_info=True)
            self._crontab = []
            if hasattr(self, 'CRONTAB'):
                for crontab_spec in self.CRONTAB:
                    args = cronjob.parse_crontab(crontab_spec)
                    job = cronjob.CronJob(log=self.log)
                    if args['_timer'] == 'datetime':
                        job.set_triggers(args['trigger_format'], args['trigger_time'])
                    if args['_timer'] == 'crontab':
                        job.set_crontab(args['crontab'])
                    if args['action'].startswith('.'):
                        action_name = args['action'][1:]
                        action_ = getattr(self.__class__, action_name)
                    else:
                        action_ = args['action']
                    job.set_action(action_, *args['args'])
                    self._crontab.append(job)
            self.start_poller(30, self.poll_crontab)

    def poll_crontab(self):
        """Check crontab and run target jobs
        """
        polled_time = datetime.datetime.now()
        polled_time = polled_time.replace(second=0, microsecond=0)
        for job in self._crontab:
            self.log.debug("Testing cronjob [%s]", job)
            if not job.is_runnable(polled_time):
                continue
            job.do_action(self, polled_time)

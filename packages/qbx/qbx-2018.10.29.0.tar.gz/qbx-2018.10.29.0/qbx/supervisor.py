"""
Usage:
    qb-starter.py anytime/ashare/ctp/okcom/oddminute [options] <cmd>...

Options:
    --with-noon
    --watch-git-change=<folder>      Watch a folder or dict, and restart when something is pushed to git
    --time-expand    before only

ashare: ['weekday', '0930-1130', '1300-1500']

ashareext: ['weekday', '0915-1130', '1300-1500']
"""
import copy
import itertools
import logging
import subprocess
from collections import defaultdict
from datetime import timedelta
from time import sleep

import arrow
import psutil


class ProcessInfo:
    inst = None

    @classmethod
    def get(cls) -> 'ProcessInfo':
        if not cls.inst:
            cls.inst = ProcessInfo()
        return cls.inst

    def __init__(self):
        print('init cpu percent')
        self.p = psutil.Process()

    def mem(self, mb):
        if mb == 'mb':
            return self.p.memory_info().rss / 1024 / 1024
        else:
            raise ValueError('unit not recognize')


# p = CpuPercent()


def get_memory_mb():
    p = ProcessInfo.get()
    x = p.mem('mb')
    return x
    # print('memory:', x)


def cond_anytime(*args, **kwargs):
    logging.debug('{} {}'.format(args, kwargs))
    return True


def cond_oddminute(time=None):
    if time is None:
        time = arrow.now()
    return time.minute % 2 == 0


def wrap_expand(cond, expand):
    def func(time=None):
        if time is None:
            time = arrow.now()
        else:
            time = arrow.get(time)
        time = time.shift(seconds=expand * -1)
        return cond() if cond() else cond(time=time)

    return func


class G:
    pid = None


def kill_pid():
    print('trying to kill pid', G.pid)
    if G.pid:
        parent = psutil.Process(G.pid)
        for child in parent.children(recursive=True):
            child.kill()
            print('kill child {}'.format(child))
        parent.kill()
        print('kill parent {}'.format(parent))
        # print('kill pricess at ', gmtp8now())
        # process.kill()


def run_cmdline_when_cond(cond, cmdline, restarter):
    print('cmdline: ', cmdline)
    if cond() and restarter.do_restart():
        print('start at ', arrow.now())
        process = subprocess.Popen(cmdline)
        G.pid = process.pid
        while True:
            if process.poll() is None:
                if not cond():
                    kill_pid()
                sleep(1)
            else:
                print('program exit itself')
                break
        print('end at', arrow.now())
    else:
        cnt = 0
        while not cond(time=arrow.now().datetime + timedelta(seconds=cnt)):
            cnt += 1
        print('sleep {} seconds and restart'.format(cnt))
        sleep(cnt)
    restarter.sleep_to_next_possible()


class Restarter:
    def __init__(self, min_interval=1, max_interval=10):
        self.min_interval = min_interval
        self.max_interval = max_interval
        self.bad_interval = []  # [(begin, end)...]  代表程序有问题的区间

    def clean_old_bad_interval(self, time):
        while self.bad_interval:
            b, e = self.bad_interval[0]
            if e < time.shift(minutes=-self.max_interval):
                self.bad_interval.pop(0)
            else:
                break

    def count_total_bad_interval_minutes(self, time):
        interval = 0
        for b, e in copy.deepcopy(self.bad_interval):
            interval += (e - max(b, time.shift(minutes=-self.max_interval))).total_seconds() / 60
        return max(interval, self.min_interval)

    def do_restart(self, time=None):
        time = time or arrow.now()
        if self.can_restart(time):
            end = time.shift(minutes=self.count_total_bad_interval_minutes(time))
            self.bad_interval.append((time, end))
            return True
        return False

    def get_last_bad_interval(self):
        if self.bad_interval:
            return self.bad_interval[-1][1]
        else:
            return None

    def can_restart(self, time):
        if not self.bad_interval:
            return True
        self.clean_old_bad_interval(time)
        if self.get_last_bad_interval() is None or time >= self.get_last_bad_interval():
            return True
        return False

    def sleep_to_next_possible(self, time=None):
        time = time or arrow.now()
        for i in itertools.count():  # for i in range( +inf)
            if self.can_restart(time.shift(seconds=i)):
                logging.info('sleep {} until next possible'.format(i))
                logging.info(self.bad_interval)
                sleep(i)
                return


def supervisor(argv):
    print(argv)
    args = argv[:]
    start = args[0]
    args = args[1:]
    time_expand = 0
    options = defaultdict(bool)
    cmdline = ''
    for i, item in enumerate(args):
        if not item.startswith('-'):
            if args[i - 1] == '--time-expand':
                time_expand = float(item)
                continue
            else:
                cmdline = args[i:]
                break

        else:
            options[item] = True

    if start == 'anytime':
        cond = cond_anytime
    elif start == 'oddminute':
        cond = cond_oddminute
    else:
        logging.warning('start time range not recognized')
        assert False
    # cur = arrow.now().datetime
    # for _ in range(1000):
    #     cur += timedelta(minutes=5)
    #     print(cur, cond(cur))
    # exit(0)
    restarter = Restarter()
    cond = wrap_expand(cond, time_expand)
    while True:
        try:
            run_cmdline_when_cond(cond, cmdline, restarter)
        except KeyboardInterrupt:
            print('KeyboardInterrupt catch, kill all and exit')
            kill_pid()
            break


if __name__ == '__main__':
    supervisor(['oddminute', 'bash'])

#!/usr/bin/env python
import datetime
import os
import public

"""
ps -p %s -o etime
http://pubs.opengroup.org/onlinepubs/9699919799/utilities/ps.html
[[dd-]hh:]mm:ss
"""


@public.add
class Elapsed:

    def __init__(self, seconds):
        self.seconds = int(seconds)

    @property
    def minutes(self):
        return int(self.seconds / 60)

    @property
    def hours(self):
        return int(self.minutes / 60)

    @property
    def days(self):
        return int(self.hours / 24)

    def __str__(self):
        string = "%02d:%02d" % (self.minutes % 60, self.seconds % 60)
        if self.hours:
            string = "%02d:%s" % (self.hours % 24, string)
        if self.days:
            string = "%s-%s" % (self.days, string)
        return string

    def __repr__(self):
        return self.__str__()


@public.add
def process(pid=None):
    if not pid:
        pid = os.getpid()
    output = os.popen("ps -p %s -o etime | grep -v ELAPSED" % pid).read().strip()
    t = output.replace('-', ':').split(':')
    t = [0] * (4 - len(t)) + [int(i) for i in t]
    seconds = t[0] * 86400 + t[1] * 3600 + t[2] * 60 + t[3]
    return Elapsed(seconds)


@public.add
def time(*args, pid=None):
    if not args or pid:
        return process(pid=pid)
    if isinstance(args[0], datetime.datetime):
        return Elapsed((datetime.datetime.now() - args[0]).total_seconds())
    if isinstance(args[0], int) or os.system("kill -0 %s &> /dev/null" % args[0]) == 0:
        return process(args[0])


@public.add
def seconds(*args, pid=None):
    return time(*args, pid=pid).seconds


@public.add
def minutes(*args, pid=None):
    return time(*args, pid=pid).minutes


@public.add
def hours(*args, pid=None):
    return time(*args, pid=pid).hours


@public.add
def days(*args, pid=None):
    return time(*args, pid=pid).days

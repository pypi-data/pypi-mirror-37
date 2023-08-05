#!/usr/bin/env python
import os
from public import public

"""
http://pubs.opengroup.org/onlinepubs/9699919799/utilities/ps.html
[[dd-]hh:]mm:ss
"""


@public
class Elapsed:
    elapsed = None

    def __init__(self, elapsed):
        if elapsed:
            self.elapsed = elapsed

    @property
    def seconds(self):
        if self.elapsed:
            t = self.elapsed.replace('-', ':').split(':')
            t = [0] * (4 - len(t)) + [int(i) for i in t]
            return t[0] * 86400 + t[1] * 3600 + t[2] * 60 + t[3]

    @property
    def minutes(self):
        if self.elapsed:
            return int(self.seconds / 60)

    @property
    def hours(self):
        if self.elapsed:
            return int(self.minutes / 60)

    @property
    def days(self):
        if self.elapsed:
            return int(self.hours / 24)

    @property
    def weeks(self):
        if self.elapsed:
            return int(self.days / 7)

    @property
    def months(self):
        if self.elapsed:
            return int(self.days / 30)

    @property
    def years(self):
        if self.elapsed:
            return int(self.days / 365)

    def __bool__(self):
        return bool(self.elapsed)

    def __str__(self):
        return str(self.elapsed)

    def __repr__(self):
        return self.__str__()


@public
def get(pid=None):
    if not pid:
        pid = os.getpid()
    elapsed = os.popen("ps -p %s -o etime | grep -v ELAPSED" % pid).read().strip()
    return Elapsed(elapsed)

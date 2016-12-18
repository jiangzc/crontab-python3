# -*- coding:utf-8 -*-
import time
import os
import sys
from subprocess import Popen


def _int(x):
    if type(x) == AllMatch:
        return allMatch
    else:
        return int(x)


class AllMatch():
    """Universal object, equal everything"""
    def __eq__(self, other):
        return True

    def __str__(self):
        return "*"

allMatch = AllMatch()
PATH = os.path.abspath(os.path.dirname(sys.argv[0]))

# The actual Event class
class Event(object):
    def __init__(self, action, min=allMatch, hour=allMatch,
            day=allMatch, month=allMatch, week=allMatch):
        self.min = _int(min)
        self.hour = _int(hour)
        self.day = _int(day)
        self.month = _int(month)
        self.week = _int(week)
        self.action = action

    def loads(text):
        """Create an Event from text"""
        data = text.split(' ')
        for n in range(len(data)):
            if data[n] == '*':
                data[n] = allMatch
        return Event(data[5:], data[0], data[1], data[2], data[3], data[4])

    def matchtime(self, t):
        """Return True if this event should trigger at the specified datetime"""
        return ((t.tm_min   == self.min) and
                (t.tm_hour  == self.hour) and
                (t.tm_mday  == self.day) and
                (t.tm_mon   == self.month) and
                (t.tm_wday  == self.week))

    def check(self, t):
        t = time.gmtime(t)
        if self.matchtime(t):
            Popen(self.action)

    def __str__(self):
        data = list((str(self.min),
                     str(self.hour),
                     str(self.day),
                     str(self.month),
                     str(self.week),
                     " ".join(self.action)))
        return " ".join(data)


class CronTab(object):
    def __init__(self, *events):
        self.events = list(events)
        self.path = None

    def loads(self, path):
        """Load Events from file"""
        self.path = path
        with open(path, 'r') as f:
            for line in f.readlines():
                self.events.append(Event.loads(line))

    def update(self):
        if self.path != None:
            self.events.clear()
            self.loads(self.path)

    def run(self):
        while time.gmtime(time.time()).tm_sec not in range(5, 45):
            print('Waiting...')
            time.sleep(5)
        print('Start Runing...')
        t = int(time.time())
        while True:
            self.update()
            for e in self.events:
                e.check(time.time())
            t += 60
            while time.time() < t:
                time.sleep(1)

def main():
    c = CronTab()
    c.loads(os.path.join(PATH, 'crontab.txt'))
    print('-----List-----')
    for event in c.events:
        print(event)
    print('--------------')
    c.run()


if __name__ == '__main__':
    main()
